// ---------------------------------------------------------------------------
// Mari 中文汉化 - 纯显示层翻译引擎
// 只 hook QPainter::drawText（8 个重载），在绘制层把控件文本翻译成中文。
// 英文原文始终留在控件 text() / model 的 DisplayRole 里，开关只是翻转
// 状态 + 重绘，不改动任何数据。Mari 7.5 用 Qt 5.15.2，drawText 的 MSVC
// mangled 名与 Qt 5.12.5 一致，因此用 Qt 5.12.5 SDK 编译、链接到 Mari 的
// Qt5Gui.dll 即可精确拦截。
// ---------------------------------------------------------------------------
#include <QtCore/QCoreApplication>
#include <QtCore/QIdentityProxyModel>
#include <QtCore/QMetaObject>
#include <QtCore/QTimer>
#include <QtCore/QDir>
#include <QtCore/QFile>
#include <QtCore/QHash>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QPointer>
#include <QtCore/QString>
#include <QtCore/QSet>
#include <QtGui/QPainter>
#include <QtGui/QPaintDevice>
#include <QtGui/QFontMetrics>
#include <QtGui/QPalette>
#include <QtGui/QTextOption>
#include <QtWidgets/QAbstractItemDelegate>
#include <QtWidgets/QAbstractItemView>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QProxyStyle>
#include <QtWidgets/QStyle>
#include <QtWidgets/QStyleOptionViewItem>
#include <QtWidgets/QWidget>

#include <windows.h>
#include <psapi.h>

#include <set>
#include <vector>

namespace {

QHash<QString, QString> g_translations;   // 英文原文 -> 中文
bool g_enabled = true;
bool g_hooksInstalled = false;
// 覆盖率预览模式：开启时对每个英文 UI 文本返回 "汉 " + 原文，
// 用于肉眼验证 drawText 钩子覆盖了多少控件。正式翻译时关闭（走词库）。
bool g_previewPrefix = true;
// 4K / DPI 适配：QOpenGLWidget 的 framebuffer = size() * devicePixelRatio()，
// 而 devicePixelRatio() 走 QWidget::metric(PdmDevicePixelRatio)（虚函数）。
// 强制让视口类返回与 UI 缩放一致的 DPR，视口的渲染分辨率才跟 UI 匹配。
bool g_dpiAdaptEnabled = false;
qreal g_dpiScale = 1.0;
using QWidgetMetricFn = int (__cdecl *)(const QWidget *, int);
QWidgetMetricFn g_metricOriginal = nullptr;
bool g_dpiHooksInstalled = false;

struct DpiVtableHook {
    void **slot = nullptr;
    void *original = nullptr;
};

std::vector<DpiVtableHook> g_dpiVtableHooks;

bool containsCjk(const QString &text) {
    for (QChar ch : text) {
        const ushort uc = ch.unicode();
        if ((uc >= 0x4E00 && uc <= 0x9FFF) ||   // CJK 统一表意文字
            (uc >= 0x3400 && uc <= 0x4DBF) ||   // CJK 扩展 A
            (uc >= 0x3000 && uc <= 0x303F) ||   // CJK 标点
            (uc >= 0xFF00 && uc <= 0xFFEF))     // 全角
            return true;
    }
    return false;
}

QString translated(const QString &source) {
    const QString key = source.trimmed();
    if (key.isEmpty())
        return {};
    return g_translations.value(key);
}

// 纯显示层绘制翻译：painter->drawText 传入的是控件的完整文本（QMenu /
// QStyle 路径），这里直接查词库翻译。
QString generalPainterTranslation(QPainter *painter, const QString &text) {
    Q_UNUSED(painter);
    if (!g_enabled)
        return {};
    if (text.isEmpty())
        return {};
    const QString trimmed = text.trimmed();
    if (trimmed.size() <= 1)
        return {};
    if (containsCjk(trimmed))
        return {};

    // 廉价过滤：纯数值/单位几乎不可能是 UI 标签。
    {
        bool allValue = true;
        for (QChar ch : trimmed) {
            if (ch.isDigit() || ch == QLatin1Char('.') || ch == QLatin1Char(',') ||
                ch == QLatin1Char('%') || ch == QLatin1Char('-') ||
                ch == QLatin1Char('+') || ch == QLatin1Char('e') ||
                ch == QLatin1Char('E') || ch == QLatin1Char(' '))
                continue;
            allValue = false;
            break;
        }
        if (allValue)
            return {};
    }

    // 当前阶段统一在英文原文前加"汉"，用于验证 drawText 钩子的覆盖率。
    // 菜单栏文本带 & 助记符（如 "&File"），跳过前导 & 后再判断首字母。
    QString head = trimmed;
    while (head.startsWith(QLatin1Char('&')))
        head.remove(0, 1);
    if (trimmed.size() >= 2 && !head.isEmpty() && head.at(0).isLetter())
        return QStringLiteral("汉 ") + trimmed;
    return {};
}

// ---------------------------------------------------------------------------
// QFontMetrics 测量钩子的类型与全局（提前声明，供 hooked 函数使用）
// ---------------------------------------------------------------------------
typedef int (__cdecl *FmHAdv)(const QFontMetrics *, const QString &, int);
typedef void *(__cdecl *FmBRectRaw)(const QFontMetrics *self, QRect *result,
                                    const QString &text);
typedef void *(__cdecl *FmBRectRectRaw)(const QFontMetrics *self, QRect *result,
                                        const QRect &rect, int flags,
                                        const QString &text, int tabstops,
                                        int *tabarray);
typedef void *(__cdecl *FmBRectXYWHRaw)(const QFontMetrics *self, QRect *result,
                                        int x, int y, int w, int h, int flags,
                                        const QString &text, int tabstops,
                                        int *tabarray);
typedef void *(__cdecl *FmSizeRaw)(const QFontMetrics *self, QSize *result,
                                   int flags, const QString &text, int tabstops,
                                   int *tabarray);
typedef void *(__cdecl *FmTBRectRaw)(const QFontMetrics *self, QRect *result,
                                     const QString &text);
typedef void *(__cdecl *FmElideRaw)(const QFontMetrics *self, QString *result,
                                    const QString &text, Qt::TextElideMode mode,
                                    int width, int flags);

typedef qreal (__cdecl *FmFHAdv)(const QFontMetricsF *, const QString &, int);
typedef void *(__cdecl *FmFBRectRaw)(const QFontMetricsF *self, QRectF *result,
                                     const QString &text);
typedef void *(__cdecl *FmFBRectRectRaw)(const QFontMetricsF *self, QRectF *result,
                                         const QRectF &rect, int flags,
                                         const QString &text, int tabstops,
                                         int *tabarray);
typedef void *(__cdecl *FmFSizeRaw)(const QFontMetricsF *self, QSizeF *result,
                                    int flags, const QString &text, int tabstops,
                                    int *tabarray);
typedef void *(__cdecl *FmFTBRectRaw)(const QFontMetricsF *self, QRectF *result,
                                      const QString &text);
typedef void *(__cdecl *FmFElideRaw)(const QFontMetricsF *self, QString *result,
                                     const QString &text, Qt::TextElideMode mode,
                                     qreal width, int flags);

FmHAdv g_fmHAdv = nullptr;
FmBRectRaw g_fmBRect = nullptr;
FmBRectRectRaw g_fmBRectRect = nullptr;
FmBRectXYWHRaw g_fmBRectXYWH = nullptr;
FmSizeRaw g_fmSize = nullptr;
FmTBRectRaw g_fmTBRect = nullptr;
FmElideRaw g_fmElide = nullptr;
FmFHAdv g_fmfHAdv = nullptr;
FmFBRectRaw g_fmfBRect = nullptr;
FmFBRectRectRaw g_fmfBRectRect = nullptr;
FmFSizeRaw g_fmfSize = nullptr;
FmFTBRectRaw g_fmfTBRect = nullptr;
FmFElideRaw g_fmfElide = nullptr;
bool g_fontHooksInstalled = false;
bool g_fontMeasureReady = false;

// ---------------------------------------------------------------------------
// 显示层包装 delegate：用 QIdentityProxyModel 只翻译 DisplayRole，其余角色
// （字体/前景色/分组标记等）原样透传。原 delegate 照常绘制，因此 Mari 的
// 分组/缩进/选中样式完全保留，且不改动 model 本身的文本。
// ---------------------------------------------------------------------------
class ComboPaintProxyModel final : public QIdentityProxyModel {
public:
    explicit ComboPaintProxyModel(QObject *parent = nullptr)
        : QIdentityProxyModel(parent) {}

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override {
        const QVariant sourceValue = QIdentityProxyModel::data(index, role);
        if (role != Qt::DisplayRole || !g_enabled)
            return sourceValue;
        const QString source = sourceValue.toString();
        const QString result = g_translations.value(source.trimmed());
        return result.isNull() ? sourceValue : QVariant(result);
    }
};

class ComboPaintDelegate final : public QAbstractItemDelegate {
public:
    ComboPaintDelegate(QAbstractItemView *view, QAbstractItemDelegate *original)
        : QAbstractItemDelegate(view), original_(original), proxy_(this) {}

    void paint(QPainter *painter, const QStyleOptionViewItem &option,
               const QModelIndex &index) const override {
        if (!original_ || !index.isValid())
            return;
        const QAbstractItemModel *model = index.model();
        if (proxy_.sourceModel() != model)
            proxy_.setSourceModel(const_cast<QAbstractItemModel *>(model));
        original_->paint(painter, option, proxy_.mapFromSource(index));
    }

    QSize sizeHint(const QStyleOptionViewItem &option,
                   const QModelIndex &index) const override {
        return original_ ? original_->sizeHint(option, index) : QSize();
    }

private:
    QPointer<QAbstractItemDelegate> original_;
    mutable ComboPaintProxyModel proxy_;
};

struct ComboPaintBinding {
    QPointer<QAbstractItemView> view;
    QPointer<QAbstractItemDelegate> original;
    QPointer<ComboPaintDelegate> installed;
};

std::vector<ComboPaintBinding> g_comboPaintBindings;
int installComboDisplayDelegate(QAbstractItemView *view) {
    if (!view)
        return 0;
    if (dynamic_cast<ComboPaintDelegate *>(view->itemDelegate())) {
        view->viewport()->update();
        return 2;
    }
    QAbstractItemDelegate *original = view->itemDelegate();
    if (!original)
        return 0;
    auto *installed = new ComboPaintDelegate(view, original);
    ComboPaintBinding binding;
    binding.view = view;
    binding.original = original;
    binding.installed = installed;
    g_comboPaintBindings.push_back(binding);
    view->setItemDelegate(installed);
    view->viewport()->update();
    return 1;
}

// ---------------------------------------------------------------------------
// DisplayLayer：QProxyStyle。覆盖所有经 QStyle::drawItemText 绘制的控件文本
// （按钮/复选框/菜单项/分组框标题/选项卡/combo 按钮/表头/工具按钮）以及
// itemTextRect 测量。只用 Qt 公开虚函数，不依赖 mangled 符号，Qt 5/6 安全。
// ---------------------------------------------------------------------------
class ChineseProxyStyle final : public QProxyStyle {
public:
    using QProxyStyle::QProxyStyle;

    ~ChineseProxyStyle() override {
        // QProxyStyle normally owns an unparented base style. Here the base is
        // Mari's live application style, so never let proxy destruction delete it.
        if (QStyle *base = baseStyle(); base && base->parent() == this)
            base->setParent(nullptr);
    }

    void drawItemText(QPainter *painter, const QRect &rect, int flags,
                      const QPalette &pal, bool enabled, const QString &text,
                      QPalette::ColorRole textRole = QPalette::NoRole) const override {
        QString draw = text;
        if (g_enabled && !containsCjk(text) && text.size() >= 2) {
            QString head = text;
            while (head.startsWith(QLatin1Char('&')))
                head.remove(0, 1);
            if (!head.isEmpty() && head.at(0).isLetter())
                draw = QStringLiteral("汉 ") + text;
        }
        QProxyStyle::drawItemText(painter, rect, flags, pal, enabled, draw, textRole);
    }

    QRect itemTextRect(const QFontMetrics &fm, const QRect &r, int flags,
                       bool enabled, const QString &text) const override {
        QString draw = text;
        if (g_enabled && !containsCjk(text) && text.size() >= 2) {
            QString head = text;
            while (head.startsWith(QLatin1Char('&')))
                head.remove(0, 1);
            if (!head.isEmpty() && head.at(0).isLetter())
                draw = QStringLiteral("汉 ") + text;
        }
        return QProxyStyle::itemTextRect(fm, r, flags, enabled, draw);
    }
};

QPointer<QStyle> g_originalStyle;
QPointer<ChineseProxyStyle> g_proxyStyle;
bool g_proxyStyleInstalled = false;

void installProxyStyle() {
    if (g_proxyStyleInstalled || !QApplication::instance())
        return;
    QStyle *current = QApplication::style();
    if (!current)
        return;

    // Wrap Mari's exact live style. Do not recreate it by objectName and never
    // fall back to Fusion: both would discard application-specific styling.
    auto *proxy = new ChineseProxyStyle(current);
    current->setParent(proxy);
    g_originalStyle = current;
    g_proxyStyle = proxy;
    QApplication::setStyle(proxy);
    g_proxyStyleInstalled = QApplication::style() == proxy;
}

void restoreProxyStyle() {
    if (!g_proxyStyleInstalled)
        return;

    QStyle *proxy = g_proxyStyle.data();
    QStyle *original = g_originalStyle.data();
    if (QApplication::instance() && proxy && original &&
        QApplication::style() == proxy) {
        // Detach before setStyle(): replacing the proxy may destroy it.
        original->setParent(nullptr);
        QApplication::setStyle(original);
    }
    g_proxyStyle.clear();
    g_originalStyle.clear();
    g_proxyStyleInstalled = false;
}

void restoreComboDisplayDelegates() {
    for (auto it = g_comboPaintBindings.rbegin();
         it != g_comboPaintBindings.rend(); ++it) {
        if (it->view && it->view->itemDelegate() == it->installed)
            it->view->setItemDelegate(it->original);
        delete it->installed.data();
    }
    g_comboPaintBindings.clear();
}

void installAllComboDisplayDelegates() {
    if (!g_enabled)
        return;
    // Mari 的 QComboBox 下拉列表（QComboBoxListView）经 QItemDelegate /
    // QStyledItemDelegate 用 QTextLayout 绘制文本，drawText 钩子覆盖不到。
    // 给每个 QComboBox 的下拉 view 装显示层包装 delegate。
    for (QWidget *widget : QApplication::allWidgets()) {
        if (auto *combo = qobject_cast<QComboBox *>(widget)) {
            if (QAbstractItemView *view = combo->view())
                installComboDisplayDelegate(view);
        }
    }
}

// ---------------------------------------------------------------------------
// 4K / DPI 适配：QOpenGLWidget 的 framebuffer = size() * devicePixelRatio()，
// devicePixelRatio() 走 QWidget::metric(PdmDevicePixelRatio)。Mari 的 3D/UV
// 视口是 QOpenGLWidget 子类，但其 metric 返回屏幕 DPR（=1），不跟 QT_SCALE_FACTOR
// 走，所以视口不随 UI 缩放。这里改 QOpenGLWidget 实例 vtable 里的 metric 槽，
// 让它返回与 UI 缩放一致的 DPR，从而视口的渲染分辨率跟 UI 匹配。
// ---------------------------------------------------------------------------
int hookedQWidgetMetric(const QWidget *self, int metric) {
    if (g_dpiAdaptEnabled &&
        static_cast<QPaintDevice::PaintDeviceMetric>(metric) ==
            QPaintDevice::PdmDevicePixelRatio) {
        return static_cast<int>(g_dpiScale);
    }
    if (g_metricOriginal)
        return g_metricOriginal(self, metric);
    // 没有原函数时，对 DPR 返回默认 1，避免灾难。
    return 1;
}

void installDpiHooks() {
    if (!g_dpiAdaptEnabled || !QApplication::instance())
        return;
    HMODULE qtWidgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!qtWidgets)
        return;
    void *metricAddr = reinterpret_cast<void *>(GetProcAddress(
        qtWidgets,
        "?metric@QWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z"));
    if (!metricAddr)
        return;
    g_metricOriginal = reinterpret_cast<QWidgetMetricFn>(metricAddr);

    // Mari 有多个 QOpenGLWidget 子类（MriColorSlider / MriDragableTextureViewer /
    // MriTexturePropertyView ...），各自 vtable 不同。必须遍历所有 QOpenGLWidget
    // 实例，对每个不同的 vtable 都替换 metric 槽，否则只有第一个被改到，其余
    // GL 视口仍按 DPR=1 渲染，导致"界面缩放有的不一样"。
    std::set<void **> visitedVtables;
    for (QWidget *w : QApplication::allWidgets()) {
        if (!w || !qobject_cast<QOpenGLWidget *>(w))
            continue;
        void **vtable = *reinterpret_cast<void ***>(w);
        if (!visitedVtables.insert(vtable).second)
            continue;   // 已处理过这个 vtable
        for (int i = 0; i < 128; ++i) {
            void **slot = &vtable[i];
            if (*slot == reinterpret_cast<void *>(&hookedQWidgetMetric))
                break;
            if (*slot != metricAddr)
                continue;
            DWORD oldProtect = 0;
            if (VirtualProtect(slot, sizeof(void *), PAGE_READWRITE,
                               &oldProtect)) {
                const void *original = *slot;
                *slot = reinterpret_cast<void *>(&hookedQWidgetMetric);
                DWORD ignored = 0;
                VirtualProtect(slot, sizeof(void *), oldProtect, &ignored);
                FlushInstructionCache(GetCurrentProcess(), slot, sizeof(void *));
                g_dpiVtableHooks.push_back(
                    {slot, const_cast<void *>(original)});
            }
            break;
        }
    }
    g_dpiHooksInstalled = !g_dpiVtableHooks.empty();
}

bool uninstallDpiHooks() {
    for (std::size_t i = g_dpiVtableHooks.size(); i > 0; --i) {
        const std::size_t current = i - 1;
        const DpiVtableHook hook = g_dpiVtableHooks[current];
        if (!hook.slot || *hook.slot != reinterpret_cast<void *>(&hookedQWidgetMetric)) {
            g_dpiVtableHooks.erase(g_dpiVtableHooks.begin() + current);
            continue;
        }
        DWORD oldProtect = 0;
        if (!VirtualProtect(hook.slot, sizeof(void *), PAGE_READWRITE, &oldProtect))
            continue;
        *hook.slot = hook.original;
        DWORD ignored = 0;
        VirtualProtect(hook.slot, sizeof(void *), oldProtect, &ignored);
        FlushInstructionCache(GetCurrentProcess(), hook.slot, sizeof(void *));
        g_dpiVtableHooks.erase(g_dpiVtableHooks.begin() + current);
    }
    g_dpiHooksInstalled = !g_dpiVtableHooks.empty();
    return !g_dpiHooksInstalled;
}

// ---------------------------------------------------------------------------
// QFontMetrics 测量钩子：布局用英文原文算 sizeHint，纯绘制层翻译后中文比
// 英文更宽，会截断/错位。这里在"测量"边界把文本翻译成中文，让 layout /
// elide 看到的是中文宽度，界面布局才正确。翻译命中时额外加一个中文字符
// 的宽度余量，避免中文顶到边缘。
// ---------------------------------------------------------------------------
QString measureText(const QString &text) {
    if (text.isEmpty() || containsCjk(text))
        return {};
    const QString trimmed = text.trimmed();
    QString head = trimmed;
    while (head.startsWith(QLatin1Char('&')))
        head.remove(0, 1);
    if (trimmed.size() >= 2 && !head.isEmpty() && head.at(0).isLetter())
        return QStringLiteral("汉 ") + trimmed;
    return {};
}

int cjkPad(const QFontMetrics *fm) {
    if (g_fmHAdv) {
        int w = g_fmHAdv(fm, QStringLiteral("中"), -1);
        if (w > 0) return w;
    }
    return fm->height();
}
int cjkPadF(const QFontMetricsF *fm) {
    if (g_fmfHAdv) {
        qreal w = g_fmfHAdv(fm, QStringLiteral("中"), -1);
        if (w > 0) return (int)w;
    }
    return (int)fm->height();
}

int hookedFontHAdv(const QFontMetrics *fm, const QString &text, int len) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (len >= 0 && len > t.size()) len = static_cast<int>(t.size());
    if (g_fmHAdv) return g_fmHAdv(fm, t, len) + (tr.isEmpty() ? 0 : cjkPad(fm));
    return 0;
}
int hookedFontHAdvOpt(const QFontMetrics *fm, const QString &text,
                      const QTextOption &opt) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    (void)opt;
    if (g_fmHAdv) return g_fmHAdv(fm, t, -1) + (tr.isEmpty() ? 0 : cjkPad(fm));
    return 0;
}
void *hookedFontBRect(const QFontMetrics *fm, QRect *result, const QString &text) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmBRect) g_fmBRect(fm, result, t);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPad(fm));
    return result;
}
void *hookedFontBRectRect(const QFontMetrics *fm, QRect *result, const QRect &r,
                          int flags, const QString &text, int tabstops,
                          int *tabarray) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmBRectRect) g_fmBRectRect(fm, result, r, flags, t, tabstops, tabarray);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPad(fm));
    return result;
}
void *hookedFontBRectXYWH(const QFontMetrics *fm, QRect *result, int x, int y,
                          int w, int h, int flags, const QString &text,
                          int tabstops, int *tabarray) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmBRectXYWH) g_fmBRectXYWH(fm, result, x, y, w, h, flags, t, tabstops,
                                     tabarray);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPad(fm));
    return result;
}
void *hookedFontSize(const QFontMetrics *fm, QSize *result, int flags,
                     const QString &text, int tabstops, int *tabarray) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmSize) g_fmSize(fm, result, flags, t, tabstops, tabarray);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPad(fm));
    return result;
}
void *hookedFontTBRect(const QFontMetrics *fm, QRect *result, const QString &text) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmTBRect) g_fmTBRect(fm, result, t);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPad(fm));
    return result;
}
void *hookedFontElide(const QFontMetrics *fm, QString *result, const QString &text,
                      Qt::TextElideMode mode, int width, int flags) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmElide) g_fmElide(fm, result, t, mode, width, flags);
    else *result = t;
    return result;
}

qreal hookedFontFHAdv(const QFontMetricsF *fm, const QString &text, int len) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (len >= 0 && len > t.size()) len = static_cast<int>(t.size());
    if (g_fmfHAdv) return g_fmfHAdv(fm, t, len) + (tr.isEmpty() ? 0 : cjkPadF(fm));
    return 0;
}
void *hookedFontFBRect(const QFontMetricsF *fm, QRectF *result, const QString &text) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmfBRect) g_fmfBRect(fm, result, t);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPadF(fm));
    return result;
}
void *hookedFontFBRectRect(const QFontMetricsF *fm, QRectF *result, const QRectF &r,
                           int flags, const QString &text, int tabstops,
                           int *tabarray) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmfBRectRect) g_fmfBRectRect(fm, result, r, flags, t, tabstops, tabarray);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPadF(fm));
    return result;
}
void *hookedFontFSize(const QFontMetricsF *fm, QSizeF *result, int flags,
                      const QString &text, int tabstops, int *tabarray) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmfSize) g_fmfSize(fm, result, flags, t, tabstops, tabarray);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPadF(fm));
    return result;
}
void *hookedFontFTBRect(const QFontMetricsF *fm, QRectF *result, const QString &text) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmfTBRect) g_fmfTBRect(fm, result, t);
    if (!tr.isEmpty()) result->setWidth(result->width() + cjkPadF(fm));
    return result;
}
void *hookedFontFElide(const QFontMetricsF *fm, QString *result, const QString &text,
                       Qt::TextElideMode mode, qreal width, int flags) {
    QString t = text;
    QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (g_fmfElide) g_fmfElide(fm, result, t, mode, width, flags);
    else *result = t;
    return result;
}

// ---------------------------------------------------------------------------
// QPainter::drawText 的 8 个重载签名（与 Mari Qt5Gui.dll 导出的 mangled 名一致）
// ---------------------------------------------------------------------------
using DrawPoint = void (*)(QPainter *, const QPoint &, const QString &);
using DrawPointF = void (*)(QPainter *, const QPointF &, const QString &);
using DrawPointF2 = void (*)(QPainter *, const QPointF &, const QString &, int, int);
using DrawRect = void (*)(QPainter *, const QRect &, int, const QString &, QRect *);
using DrawRectFOption = void (*)(QPainter *, const QRectF &, const QString &, const QTextOption &);
using DrawRectFAlign = void (*)(QPainter *, const QRectF &, int, const QString &, QRectF *);
using DrawXY = void (*)(QPainter *, int, int, const QString &);
using DrawXYWH = void (*)(QPainter *, int, int, int, int, int, const QString &, QRect *);

DrawPoint g_drawPoint = nullptr;
DrawPointF g_drawPointF = nullptr;
DrawPointF2 g_drawPointF2 = nullptr;
DrawRect g_drawRect = nullptr;
DrawRectFOption g_drawRectFOption = nullptr;
DrawRectFAlign g_drawRectFAlign = nullptr;
DrawXY g_drawXY = nullptr;
DrawXYWH g_drawXYWH = nullptr;

void hookedDrawPoint(QPainter *p, const QPoint &pt, const QString &text) {
    QString t = generalPainterTranslation(p, text);
    g_drawPoint(p, pt, t.isEmpty() ? text : t);
}
void hookedDrawPointF(QPainter *p, const QPointF &pt, const QString &text) {
    QString t = generalPainterTranslation(p, text);
    g_drawPointF(p, pt, t.isEmpty() ? text : t);
}
void hookedDrawPointF2(QPainter *p, const QPointF &pt, const QString &text,
                       int flags, int just) {
    QString t = generalPainterTranslation(p, text);
    g_drawPointF2(p, pt, t.isEmpty() ? text : t, flags, just);
}
void hookedDrawRect(QPainter *p, const QRect &r, int flags, const QString &text,
                    QRect *br) {
    QString t = generalPainterTranslation(p, text);
    g_drawRect(p, r, flags, t.isEmpty() ? text : t, br);
}
void hookedDrawRectFOption(QPainter *p, const QRectF &r, const QString &text,
                           const QTextOption &opt) {
    QString t = generalPainterTranslation(p, text);
    g_drawRectFOption(p, r, t.isEmpty() ? text : t, opt);
}
void hookedDrawRectFAlign(QPainter *p, const QRectF &r, int flags,
                          const QString &text, QRectF *br) {
    QString t = generalPainterTranslation(p, text);
    g_drawRectFAlign(p, r, flags, t.isEmpty() ? text : t, br);
}
void hookedDrawXY(QPainter *p, int x, int y, const QString &text) {
    QString t = generalPainterTranslation(p, text);
    g_drawXY(p, x, y, t.isEmpty() ? text : t);
}
void hookedDrawXYWH(QPainter *p, int x, int y, int w, int h, int flags,
                    const QString &text, QRect *br) {
    QString t = generalPainterTranslation(p, text);
    g_drawXYWH(p, x, y, w, h, flags, t.isEmpty() ? text : t, br);
}

// ---------------------------------------------------------------------------
// IAT hook：替换所有已加载模块导入表里指向 drawText 的槽
// ---------------------------------------------------------------------------
struct ImportHookSlot {
    void **slot = nullptr;
    void *original = nullptr;
    void *replacement = nullptr;
};

std::vector<ImportHookSlot> g_hookSlots;
std::vector<ImportHookSlot> g_fontHookSlots;

bool replaceImportInModule(HMODULE module, std::vector<ImportHookSlot> &list,
                           void *original, void *replacement) {
    if (!module || !original || !replacement)
        return false;
    auto *base = reinterpret_cast<unsigned char *>(module);
    auto *dos = reinterpret_cast<IMAGE_DOS_HEADER *>(base);
    if (dos->e_magic != IMAGE_DOS_SIGNATURE)
        return false;
    auto *nt = reinterpret_cast<IMAGE_NT_HEADERS *>(base + dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE)
        return false;
    const DWORD importRva = nt->OptionalHeader
        .DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress;
    if (!importRva)
        return false;
    bool replaced = false;
    auto *descriptor = reinterpret_cast<IMAGE_IMPORT_DESCRIPTOR *>(base + importRva);
    for (; descriptor->Name; ++descriptor) {
        if (!descriptor->FirstThunk)
            continue;
        auto *thunk = reinterpret_cast<IMAGE_THUNK_DATA *>(base + descriptor->FirstThunk);
        for (; thunk->u1.Function; ++thunk) {
            auto **slot = reinterpret_cast<void **>(&thunk->u1.Function);
            if (*slot != original)
                continue;
            ImportHookSlot hook{slot, original, replacement};
            list.push_back(hook);
            DWORD oldProtection = 0;
            if (!VirtualProtect(slot, sizeof(void *), PAGE_READWRITE, &oldProtection)) {
                list.pop_back();
                continue;
            }
            *slot = replacement;
            DWORD ignored = 0;
            VirtualProtect(slot, sizeof(void *), oldProtection, &ignored);
            FlushInstructionCache(GetCurrentProcess(), slot, sizeof(void *));
            replaced = true;
        }
    }
    return replaced;
}

bool replaceImportAllModules(std::vector<ImportHookSlot> &list,
                             void *original, void *replacement) {
    bool any = false;
    HMODULE modules[2048];
    DWORD needed = 0;
    if (!EnumProcessModules(GetCurrentProcess(), modules, sizeof(modules), &needed))
        return false;
    const DWORD count = needed / sizeof(HMODULE);
    for (DWORD i = 0; i < count; ++i) {
        if (replaceImportInModule(modules[i], list, original, replacement))
            any = true;
    }
    return any;
}

bool restoreImportHooks(std::vector<ImportHookSlot> &list) {
    for (std::size_t i = list.size(); i > 0; --i) {
        const std::size_t cur = i - 1;
        const ImportHookSlot hook = list[cur];
        if (!hook.slot || *hook.slot != hook.replacement) {
            list.erase(list.begin() + cur);
            continue;
        }
        DWORD oldProtection = 0;
        if (!VirtualProtect(hook.slot, sizeof(void *), PAGE_READWRITE, &oldProtection))
            continue;
        *hook.slot = hook.original;
        DWORD ignored = 0;
        VirtualProtect(hook.slot, sizeof(void *), oldProtection, &ignored);
        FlushInstructionCache(GetCurrentProcess(), hook.slot, sizeof(void *));
        list.erase(list.begin() + cur);
    }
    return list.empty();
}

// ---------------------------------------------------------------------------
// 安装 / 卸载 drawText 钩子
// ---------------------------------------------------------------------------
bool uninstallHooks();

bool installHooks() {
    if (g_hooksInstalled)
        return true;
    HMODULE qtGui = GetModuleHandleW(L"Qt5Gui.dll");
    if (!qtGui)
        return false;
    bool installed = false;
    auto hookOne = [&](const char *sym, void *hookFn, void *&ortSlot) -> bool {
        void *orig = reinterpret_cast<void *>(GetProcAddress(qtGui, sym));
        if (!orig)
            return false;
        ortSlot = orig;
        return replaceImportAllModules(g_hookSlots, orig, hookFn);
    };
    installed |= hookOne("?drawText@QPainter@@QEAAXAEBVQPoint@@AEBVQString@@@Z",
                         (void *)&hookedDrawPoint, (void *&)g_drawPoint);
    installed |= hookOne("?drawText@QPainter@@QEAAXAEBVQPointF@@AEBVQString@@@Z",
                         (void *)&hookedDrawPointF, (void *&)g_drawPointF);
    installed |= hookOne("?drawText@QPainter@@QEAAXAEBVQPointF@@AEBVQString@@HH@Z",
                         (void *)&hookedDrawPointF2, (void *&)g_drawPointF2);
    installed |= hookOne("?drawText@QPainter@@QEAAXAEBVQRect@@HAEBVQString@@PEAV2@@Z",
                         (void *)&hookedDrawRect, (void *&)g_drawRect);
    installed |= hookOne("?drawText@QPainter@@QEAAXAEBVQRectF@@AEBVQString@@AEBVQTextOption@@@Z",
                         (void *)&hookedDrawRectFOption, (void *&)g_drawRectFOption);
    installed |= hookOne("?drawText@QPainter@@QEAAXAEBVQRectF@@HAEBVQString@@PEAV2@@Z",
                         (void *)&hookedDrawRectFAlign, (void *&)g_drawRectFAlign);
    installed |= hookOne("?drawText@QPainter@@QEAAXHHAEBVQString@@@Z",
                         (void *)&hookedDrawXY, (void *&)g_drawXY);
    installed |= hookOne("?drawText@QPainter@@QEAAXHHHHHAEBVQString@@PEAVQRect@@@Z",
                         (void *)&hookedDrawXYWH, (void *&)g_drawXYWH);
    if (!installed || g_hookSlots.empty()) {
        uninstallHooks();
        return false;
    }
    g_hooksInstalled = true;
    return true;
}

bool rescanDrawTextModules() {
    // 晚加载 DLL 不会经过启动时的 IAT 扫描。这里用各重载保存的 original
    // 地址再次 patch 所有模块——已经替换过的槽指向 replacement，不会再匹配
    // original，因此幂等；新加载的模块会补上。
    bool any = false;
    if (g_drawPoint)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawPoint, (void *)&hookedDrawPoint);
    if (g_drawPointF)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawPointF, (void *)&hookedDrawPointF);
    if (g_drawPointF2)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawPointF2, (void *)&hookedDrawPointF2);
    if (g_drawRect)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawRect, (void *)&hookedDrawRect);
    if (g_drawRectFOption)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawRectFOption, (void *)&hookedDrawRectFOption);
    if (g_drawRectFAlign)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawRectFAlign, (void *)&hookedDrawRectFAlign);
    if (g_drawXY)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawXY, (void *)&hookedDrawXY);
    if (g_drawXYWH)
        any |= replaceImportAllModules(g_hookSlots, (void *)g_drawXYWH, (void *)&hookedDrawXYWH);
    return any;
}

bool uninstallHooks() {
    restoreImportHooks(g_hookSlots);
    g_hooksInstalled = !g_hookSlots.empty();
    return !g_hooksInstalled;
}

// 扫描所有模块，把已解析的 QFontMetrics 符号的导入槽替换为钩子。幂等：
// 已替换的槽指向 replacement，不会再匹配 original；晚加载模块会补上。
void patchFontModules() {
    if (!g_fontMeasureReady)
        return;
    struct Sym { void *orig; void *hook; };
    Sym syms[] = {
        {(void *)g_fmHAdv, (void *)&hookedFontHAdv},
        {(void *)g_fmBRect, (void *)&hookedFontBRect},
        {(void *)g_fmBRectRect, (void *)&hookedFontBRectRect},
        {(void *)g_fmBRectXYWH, (void *)&hookedFontBRectXYWH},
        {(void *)g_fmSize, (void *)&hookedFontSize},
        {(void *)g_fmTBRect, (void *)&hookedFontTBRect},
        {(void *)g_fmElide, (void *)&hookedFontElide},
        {(void *)g_fmfHAdv, (void *)&hookedFontFHAdv},
        {(void *)g_fmfBRect, (void *)&hookedFontFBRect},
        {(void *)g_fmfBRectRect, (void *)&hookedFontFBRectRect},
        {(void *)g_fmfSize, (void *)&hookedFontFSize},
        {(void *)g_fmfTBRect, (void *)&hookedFontFTBRect},
        {(void *)g_fmfElide, (void *)&hookedFontFElide},
    };
    for (const Sym &s : syms) {
        if (s.orig)
            replaceImportAllModules(g_fontHookSlots, s.orig, s.hook);
    }
}

bool isExecutableCodeAddr(const void *p) {
    if (!p) return false;
    MEMORY_BASIC_INFORMATION mbi{};
    if (!VirtualQuery(p, &mbi, sizeof(mbi))) return false;
    if (mbi.State != MEM_COMMIT || mbi.Protect == PAGE_NOACCESS) return false;
    const DWORD exec = PAGE_EXECUTE | PAGE_EXECUTE_READ |
                       PAGE_EXECUTE_READWRITE | PAGE_EXECUTE_WRITECOPY;
    return (mbi.Protect & exec) != 0;
}

bool fontSymbolsAreValid() {
    const void *ptrs[] = {
        (void *)g_fmHAdv, (void *)g_fmBRect, (void *)g_fmBRectRect,
        (void *)g_fmBRectXYWH, (void *)g_fmSize, (void *)g_fmTBRect,
        (void *)g_fmElide, (void *)g_fmfHAdv, (void *)g_fmfBRect,
        (void *)g_fmfBRectRect, (void *)g_fmfSize, (void *)g_fmfTBRect,
        (void *)g_fmfElide,
    };
    for (const void *p : ptrs)
        if (p && !isExecutableCodeAddr(p)) return false;
    return true;
}

void installFontMeasurementHooks() {
    if (g_fontHooksInstalled)
        return;
    HMODULE qtGui = GetModuleHandleW(L"Qt5Gui.dll");
    if (!qtGui)
        return;
    g_fmHAdv = (FmHAdv)GetProcAddress(qtGui,
        "?horizontalAdvance@QFontMetrics@@QEBAHAEBVQString@@H@Z");
    g_fmBRect = (FmBRectRaw)GetProcAddress(qtGui,
        "?boundingRect@QFontMetrics@@QEBA?AVQRect@@AEBVQString@@@Z");
    g_fmBRectRect = (FmBRectRectRaw)GetProcAddress(qtGui,
        "?boundingRect@QFontMetrics@@QEBA?AVQRect@@AEBV2@HAEBVQString@@HPEAH@Z");
    g_fmBRectXYWH = (FmBRectXYWHRaw)GetProcAddress(qtGui,
        "?boundingRect@QFontMetrics@@QEBA?AVQRect@@HHHHHAEBVQString@@HPEAH@Z");
    g_fmSize = (FmSizeRaw)GetProcAddress(qtGui,
        "?size@QFontMetrics@@QEBA?AVQSize@@HAEBVQString@@HPEAH@Z");
    g_fmTBRect = (FmTBRectRaw)GetProcAddress(qtGui,
        "?tightBoundingRect@QFontMetrics@@QEBA?AVQRect@@AEBVQString@@@Z");
    g_fmElide = (FmElideRaw)GetProcAddress(qtGui,
        "?elidedText@QFontMetrics@@QEBA?AVQString@@AEBV2@W4TextElideMode@Qt@@HH@Z");

    g_fmfHAdv = (FmFHAdv)GetProcAddress(qtGui,
        "?horizontalAdvance@QFontMetricsF@@QEBANAEBVQString@@H@Z");
    g_fmfBRect = (FmFBRectRaw)GetProcAddress(qtGui,
        "?boundingRect@QFontMetricsF@@QEBA?AVQRectF@@AEBVQString@@@Z");
    g_fmfBRectRect = (FmFBRectRectRaw)GetProcAddress(qtGui,
        "?boundingRect@QFontMetricsF@@QEBA?AVQRectF@@AEBV2@HAEBVQString@@HPEAH@Z");
    g_fmfSize = (FmFSizeRaw)GetProcAddress(qtGui,
        "?size@QFontMetricsF@@QEBA?AVQSizeF@@HAEBVQString@@HPEAH@Z");
    g_fmfTBRect = (FmFTBRectRaw)GetProcAddress(qtGui,
        "?tightBoundingRect@QFontMetricsF@@QEBA?AVQRectF@@AEBVQString@@@Z");
    g_fmfElide = (FmFElideRaw)GetProcAddress(qtGui,
        "?elidedText@QFontMetricsF@@QEBA?AVQString@@AEBV2@W4TextElideMode@Qt@@NH@Z");

    g_fontHooksInstalled = true;
    g_fontMeasureReady = fontSymbolsAreValid();
    if (g_fontMeasureReady)
        patchFontModules();
}

void uninstallFontHooks() {
    restoreImportHooks(g_fontHookSlots);
    g_fontMeasureReady = false;
    g_fontHooksInstalled = false;
}

bool loadTranslationsFromJson(const QString &path) {
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return false;
    const QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    if (!doc.isObject())
        return false;
    const QJsonObject root = doc.object();
    const QJsonValue trans = root.value(QStringLiteral("translations"));
    if (!trans.isObject())
        return false;
    const QJsonObject entries = trans.toObject();
    for (auto it = entries.begin(); it != entries.end(); ++it) {
        if (it.value().isString())
            g_translations.insert(it.key(), it.value().toString());
    }
    return true;
}

std::wstring selfDirW() {
    std::vector<wchar_t> buf(1024);
    while (buf.size() <= 32768) {
        DWORD n = GetModuleFileNameW(nullptr, buf.data(), (DWORD)buf.size());
        if (!n) return L"";
        if (n < buf.size() - 1)
            return std::wstring(buf.data(), n);
        buf.resize(buf.size() * 2);
    }
    return L"";
}

void loadDictionariesFromDir(const std::wstring &dir) {
    // 读取 DLL 同目录 translations/*.json（含 dictionary_zh.json），合并词库。
    QDir trans(QString::fromStdWString(dir) + QStringLiteral("/translations"));
    const QStringList files = trans.entryList(QStringList() << QStringLiteral("*_zh.json"),
                                             QDir::Files, QDir::Name);
    for (const QString &name : files)
        loadTranslationsFromJson(trans.filePath(name));
}

// 在 GUI 线程执行：加载词库、安装 drawText 钩子、注册刷新定时器。
bool rescanDrawTextModules();

void runOnGuiThread(QApplication *app) {
    const std::wstring dir = selfDirW();
    const std::wstring folder = dir.find_last_of(L"\\/") == std::wstring::npos
        ? dir : dir.substr(0, dir.find_last_of(L"\\/"));
    loadDictionariesFromDir(folder);
    installProxyStyle();
    installHooks();
    installFontMeasurementHooks();
    installAllComboDisplayDelegates();
    // 4K / DPI 适配：从 QT_SCALE_FACTOR 读缩放因子，让 3D/UV 视口（QOpenGLWidget）
    // 的 framebuffer 按同一缩放渲染，跟 UI 匹配。占位 GL widget 已存在，
    // 延迟装 DPI hook 即可让之后创建的视口也生效。
    {
        const QByteArray sf = qgetenv("QT_SCALE_FACTOR");
        bool ok = false;
        const qreal scale = sf.toDouble(&ok);
        if (ok && scale >= 0.1 && scale <= 8.0)
            g_dpiScale = scale;
        else
            g_dpiScale = 1.0;
        g_dpiAdaptEnabled = g_dpiScale > 1.01;
    }
    if (g_dpiAdaptEnabled)
        QTimer::singleShot(1000, app, [] { installDpiHooks(); });
    // 晚加载 DLL（如按需加载的插件）会绕过启动时的 IAT 扫描，定期重扫。
    auto *rescanTimer = new QTimer(app);
    rescanTimer->setInterval(2000);
    QObject::connect(rescanTimer, &QTimer::timeout, [] {
        if (g_hooksInstalled)
            rescanDrawTextModules();
        patchFontModules();
        installAllComboDisplayDelegates();
        if (g_dpiAdaptEnabled)
            installDpiHooks();
    });
    rescanTimer->start();
    QTimer::singleShot(60000, app, [rescanTimer] { rescanTimer->stop(); });
}

// 后台线程：注入发生在 CREATE_SUSPENDED 时，Qt 还没初始化。等 QApplication
// 出现后，切到 GUI 线程安装钩子。
DWORD WINAPI worker(LPVOID) {
    QApplication *app = nullptr;
    for (int i = 0; i < 3000; ++i) {
        if (QCoreApplication::instance()) {
            app = qobject_cast<QApplication *>(QCoreApplication::instance());
            if (app)
                break;
        }
        Sleep(100);
    }
    if (!app)
        return 1;
    QMetaObject::invokeMethod(app, [app] { runOnGuiThread(app); },
                              Qt::QueuedConnection);
    return 0;
}

} // namespace

BOOL WINAPI DllMain(HINSTANCE hinst, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(hinst);
        HANDLE h = CreateThread(nullptr, 0, worker, nullptr, 0, nullptr);
        if (h)
            CloseHandle(h);
    }
    return TRUE;
}

// ---------------------------------------------------------------------------
// C API：供 Mari 的 Python(PySide2) 层通过 ctypes 调用
// ---------------------------------------------------------------------------
extern "C" {

__declspec(dllexport) int __cdecl mari_install() {
    if (!installHooks())
        return 0;
    installFontMeasurementHooks();
    return 1;
}

__declspec(dllexport) int __cdecl mari_uninstall() {
    restoreComboDisplayDelegates();
    uninstallFontHooks();
    const bool hooksRestored = uninstallHooks();
    const bool dpiRestored = uninstallDpiHooks();
    restoreProxyStyle();
    return hooksRestored && dpiRestored ? 1 : 0;
}

__declspec(dllexport) int __cdecl mari_is_installed() {
    return g_hooksInstalled ? 1 : 0;
}

__declspec(dllexport) void __cdecl mari_set_enabled(int enabled) {
    g_enabled = enabled != 0;
}

__declspec(dllexport) int __cdecl mari_is_enabled() {
    return g_enabled ? 1 : 0;
}

__declspec(dllexport) void __cdecl mari_set_preview_prefix(int enabled) {
    g_previewPrefix = enabled != 0;
}

__declspec(dllexport) void __cdecl mari_dpi_set_enabled(
    int enabled, double scale) {
    g_dpiAdaptEnabled = enabled != 0;
    if (scale > 0.1 && scale <= 8.0)
        g_dpiScale = scale;
    if (g_dpiAdaptEnabled)
        installDpiHooks();
    else
        uninstallDpiHooks();
}

__declspec(dllexport) void __cdecl mari_add_translation(
    const wchar_t *source, const wchar_t *target) {
    if (source && target)
        g_translations.insert(QString::fromWCharArray(source),
                              QString::fromWCharArray(target));
}

__declspec(dllexport) void __cdecl mari_clear_translations() {
    g_translations.clear();
}

__declspec(dllexport) int __cdecl mari_load_translations(const wchar_t *path) {
    if (!path)
        return 0;
    return loadTranslationsFromJson(QString::fromWCharArray(path)) ? 1 : 0;
}

__declspec(dllexport) int __cdecl mari_translation_count() {
    return static_cast<int>(g_translations.size());
}

} // extern "C"
