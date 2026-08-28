// ---------------------------------------------------------------------------
// Mari 中文汉化 - 纯显示层翻译引擎
// 只 hook QPainter::drawText（8 个重载），在绘制层把控件文本翻译成中文。
// 英文原文始终留在控件 text() / model 的 DisplayRole 里，开关只是翻转
// 状态 + 重绘，不改动任何数据。运行时从宿主 Qt5 DLL 解析可用能力；找不到
// 的可选入口独立降级，不依赖 Mari 版本名、固定 RVA 或固定虚表槽位。
// ---------------------------------------------------------------------------
#include <QtCore/QCoreApplication>
#include <QtCore/QAbstractEventDispatcher>
#include <QtCore/QAbstractNativeEventFilter>
#include <QtCore/QAbstractItemModel>
#include <QtCore/QModelIndex>
#include <QtCore/QVariant>
#include <QtCore/QIdentityProxyModel>
#include <QtCore/QTimer>
#include <QtCore/QUrl>
#include <QtCore/QDir>
#include <QtCore/QFile>
#include <QtCore/QHash>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QJsonParseError>
#include <QtCore/QPair>
#include <QtCore/QPointer>
#include <QtCore/QString>
#include <QtGui/QPainter>
#include <QtGui/QDesktopServices>
#include <QtGui/QKeyEvent>
#include <QtGui/QKeySequence>
#include <QtGui/QMouseEvent>
#include <QtGui/QFontMetrics>
#include <QtGui/QTextOption>
#include <QtWidgets/QAbstractItemDelegate>
#include <QtWidgets/QAbstractItemView>
#include <QtWidgets/QAbstractButton>
#include <QtWidgets/QApplication>
#include <QtWidgets/QAction>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGraphicsSimpleTextItem>
#include <QtWidgets/QLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMessageBox>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QProxyStyle>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QMenu>
#include <QtWidgets/QStyle>
#include <QtWidgets/QStyleFactory>
#include <QtWidgets/QStyleOptionViewItem>
#include <QtWidgets/QTabBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

#include <windows.h>
#include <shlobj.h>
#include <psapi.h>

#include <vector>
#include <map>
#include <set>
#include <functional>
#include <algorithm>
#include <atomic>
#include <cstddef>
#include <utility>
#include <typeinfo>


namespace {

QHash<QString, QString> g_translations;   // 英文原文 -> 中文
// SpeedTree 同款：归一化英文键 -> 中文 的模糊索引，以及按小写原文排序的键表（用于省略号前缀查找）。
QHash<QString, QString> g_foldedTranslations;
std::vector<QPair<QString, QString>> g_sortedKeys;   // (小写原文, 原文)
std::set<std::string> g_paintSeen;                   // Shift+` 嗅探：未翻译字符串集合
static constexpr size_t kMaxPaintSeen = 100000;
SRWLOCK g_paintSeenLock = SRWLOCK_INIT;
std::atomic_bool g_enabled{true};
bool g_hooksInstalled = false;
bool g_nodeTextHookInstalled = false;
int g_toggleKey = Qt::Key_F3;
bool g_hotkeyDialogOpen = false;
HMODULE g_moduleHandle = nullptr;

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

// 判断一段文本是否可能是可翻译的界面文案（供 Shift+` 嗅探记录用）。
bool isTranslatableString(const QString &s) {
    const QString t = s.trimmed();
    if (t.isEmpty() || containsCjk(t)) return false;
    if (t.size() < 2) return false;
    if (t.at(0) == QLatin1Char('<')) return false;           // HTML
    if (t.contains(QLatin1Char('?'))) return false;          // URL 等
    bool numeric = true;
    for (QChar c : t) {
        if (!(c.isDigit() || c == QLatin1Char('.') || c == QLatin1Char(',') ||
              c == QLatin1Char('%') || c == QLatin1Char('-') ||
              c == QLatin1Char('+') || c == QLatin1Char('e') ||
              c == QLatin1Char('E') || c == QLatin1Char(' '))) {
            numeric = false;
            break;
        }
    }
    return !numeric;
}

// 归一化英文原文，用于模糊匹配（镜像 SpeedTree 的实现）：
// 统一空白/下划线、全角转半角、去组合字符、大小写折叠。
QString normalizeForMatch(QString text) {
    const QString original = text;
    // drawText may run outside the GUI thread. A per-thread bounded cache keeps
    // the hot path lock-free and avoids mutating a shared QHash while painting.
    thread_local QHash<QString, QString> cache;
    static constexpr int kThreadCacheLimit = 4096;
    auto cached = cache.constFind(original);
    if (cached != cache.constEnd())
        return cached.value();

    text.replace(QChar(0x00A0), QLatin1Char(' '));
    text.replace(QChar(0x3000), QLatin1Char(' '));
    text.replace(QLatin1Char('\r'), QLatin1Char('\n'));
    text = text.simplified();
    text.remove(QChar(0x200B)); text.remove(QChar(0x200D)); text.remove(QChar(0xFEFF));
    while (text.endsWith(QChar(0x2026))) text.chop(1);
    while (text.endsWith(QLatin1String("..."))) text.chop(3);
    if (text.endsWith(QLatin1String(" *"))) text.chop(2);
    text.replace(QLatin1Char('_'), QLatin1Char(' '));
    text = text.normalized(QString::NormalizationForm_C);
    for (int i = 0; i < text.size(); ++i) {
        const uint code = text.at(i).unicode();
        if (code >= 0xFF01 && code <= 0xFF5E)
            text[i] = QChar(code - 0xFEE0);
    }
    text = text.toCaseFolded();
    text = text.normalized(QString::NormalizationForm_D);
    QString stripped;
    stripped.reserve(text.size());
    for (const QChar ch : text) {
        const QChar::Category cat = ch.category();
        if (cat == QChar::Mark_NonSpacing || cat == QChar::Mark_SpacingCombining ||
            cat == QChar::Mark_Enclosing)
            continue;
        stripped.append(ch);
    }
    stripped.remove(QLatin1Char(' '));
    QString result = stripped.normalized(QString::NormalizationForm_C);
    if (cache.size() < kThreadCacheLimit)
        cache.insert(original, result);
    return result;
}

// 在词库变更后重建归一化模糊索引与排序键表（SpeedTree 同款，供 O(log N) 查找）。
void rebuildLookupIndex() {
    g_foldedTranslations.clear();
    g_sortedKeys.clear();
    for (auto it = g_translations.cbegin(); it != g_translations.cend(); ++it)
        g_foldedTranslations.insert(normalizeForMatch(it.key()), it.value());
    g_sortedKeys.reserve(g_translations.size());
    for (auto it = g_translations.cbegin(); it != g_translations.cend(); ++it)
        g_sortedKeys.push_back(qMakePair(it.key().toCaseFolded(), it.key()));
    std::sort(g_sortedKeys.begin(), g_sortedKeys.end(),
              [](const QPair<QString, QString> &a, const QPair<QString, QString> &b) {
                  return a.first < b.first;
              });
}

// 省略号截断文本（"Mater…"）——按省略前内容在排序键表里二分找前缀，取最短原文再取中文。
QString findElidedTranslation(const QString &text) {
    QString base = text;
    base.chop(text.endsWith(QChar(0x2026)) ? 1 : 3);
    base = base.trimmed();
    if (base.size() < 2)
        return {};
    const QString low = base.toCaseFolded();
    auto it = std::lower_bound(
        g_sortedKeys.begin(), g_sortedKeys.end(), low,
        [](const QPair<QString, QString> &e, const QString &v) { return e.first < v; });
    QString best;
    for (; it != g_sortedKeys.end(); ++it) {
        const QString &k = it->first;
        if (!k.startsWith(low))
            break;
        if (best.isEmpty() || it->second.size() < best.size())
            best = it->second;
    }
    if (best.isEmpty())
        return {};
    return g_translations.value(best);
}

// 统一翻译查询：精确 -> 助记符/状态后缀还原 -> 归一化模糊 -> 省略号前缀。
// 供绘制层（displayTranslation）与列表/下拉 DisplayRole（ComboPaintProxyModel）共用。
QString lookupTranslation(const QString &text) {
    const QString trimmed = text.trimmed();
    if (trimmed.isEmpty() || containsCjk(trimmed))
        return {};

    // 1) 精确匹配。
    auto exact = g_translations.constFind(trimmed);
    if (exact != g_translations.constEnd())
        return exact.value();

    // 2) 助记符(&) / 状态后缀(*) 还原后再次精确匹配。
    QString key = trimmed;
    QString stateSuffix;
    if (key.endsWith(QLatin1Char('*'))) {
        key.chop(1);
        key = key.trimmed();
        stateSuffix = QStringLiteral("*");
    }
    if (key.contains(QLatin1Char('&')))
        key.remove(QLatin1Char('&'));
    auto found = g_translations.constFind(key);
    if (found != g_translations.constEnd())
        return found.value() + stateSuffix;

    // 3) 归一化模糊匹配（空白/全角/大小写/组合字符统一后）。
    const QString norm = normalizeForMatch(key);
    auto fuzzy = g_foldedTranslations.constFind(norm);
    if (fuzzy != g_foldedTranslations.constEnd())
        return fuzzy.value() + stateSuffix;

    // 4) 省略号截断文本：用排序键表二分找前缀，命中即返回中文。
    if (text.endsWith(QChar(0x2026)) || text.endsWith(QLatin1String("..."))) {
        const QString elided = findElidedTranslation(text);
        if (!elided.isEmpty())
            return elided + stateSuffix;
    }
    // Shift+` 嗅探：记录未翻译且看似可翻译的界面文案（有上限）。
    if (isTranslatableString(trimmed)) {
        const QByteArray utf8 = trimmed.toUtf8();
        // 嗅探只是诊断功能，绝不能让高频绘制路径等待文件导出线程。
        // 锁繁忙时丢弃本次样本；相同文字后续绘制还会再次采集。
        if (TryAcquireSRWLockExclusive(&g_paintSeenLock)) {
            if (g_paintSeen.size() < kMaxPaintSeen)
                g_paintSeen.insert(utf8.constData());
            ReleaseSRWLockExclusive(&g_paintSeenLock);
        }
    }
    return {};
}

std::vector<std::string> paintSeenSnapshot() {
    AcquireSRWLockShared(&g_paintSeenLock);
    std::vector<std::string> result(g_paintSeen.begin(), g_paintSeen.end());
    ReleaseSRWLockShared(&g_paintSeenLock);
    return result;
}

// JSON 字符串转义（键/值）。
static std::string jsonEscape(const std::string &s) {
    std::string out;
    out.reserve(s.size() + 8);
    for (unsigned char c : s) {
        switch (c) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\b': out += "\\b";  break;
            case '\f': out += "\\f";  break;
            case '\n': out += "\\n";  break;
            case '\r': out += "\\r";  break;
            case '\t': out += "\\t";  break;
            default:
                if (c < 0x20) {
                    static const char hex[] = "0123456789abcdef";
                    out += "\\u00";
                    out.push_back(hex[(c >> 4) & 0xF]);
                    out.push_back(hex[c & 0xF]);
                } else {
                    out.push_back(static_cast<char>(c));
                }
        }
    }
    return out;
}

// 省略显示的控件：可见文本被 Qt 截断成 "Mater…"，完整原文往往在 toolTip。
static bool isElidingLabel(const QLabel *lbl) {
    if (!lbl) return false;
    const QString t = lbl->text();
    if (!t.isEmpty() && (t.endsWith(QChar(0x2026)) || t.endsWith(QLatin1String("...")))) {
        const QString tip = lbl->toolTip();
        return !tip.isEmpty() && tip != t;
    }
    return false;
}

static QString labelSource(QLabel *lbl) {
    if (!lbl) return {};
    if (isElidingLabel(lbl)) {
        const QString tip = lbl->toolTip();
        if (!tip.isEmpty()) return tip;
    }
    return lbl->text();
}

static void collectMenuActions(QMenu *menu, const std::function<void(const QString &)> &add) {
    if (!menu) return;
    for (QAction *a : menu->actions()) {
        if (!a->text().isEmpty()) add(a->text());
        if (a->menu()) collectMenuActions(a->menu(), add);
    }
}

// 顺 model 递归下钻采集词条。折叠树里未展开的节点在 view 层不可见，
// 但其文本仍在 model 中。这里从根索引一路 child() 向下，能拿到所有层级
// 的 DisplayRole 文本，且不改动任何节点/展开状态。带深度与预算保护。
static void collectModelDeep(QAbstractItemModel *model, const QModelIndex &parent,
                             const std::function<void(const QString &)> &add,
                             int depth, int &budget,
                             int maxDepth = 64) {
    if (!model || depth > maxDepth || budget <= 0)
        return;
    const int rows = model->rowCount(parent);
    const int cols = model->columnCount();
    for (int r = 0; r < rows && budget > 0; ++r) {
        const QModelIndex idx = model->index(r, 0, parent);
        for (int c = 0; c < cols && budget > 0; ++c) {
            const QModelIndex child = model->index(r, c, parent);
            const QVariant v = child.data(Qt::DisplayRole);
            if (v.isValid())
                add(v.toString());
            --budget;
        }
        // 递归下钻当前行的子节点（第 0 列作为树根）。
        collectModelDeep(model, idx, add, depth + 1, budget, maxDepth);
    }
}

// 手动“未翻译文本嗅探”（Shift + `）：只读地遍历当前界面，把尚未收录的
// 英文原文追加到桌面 <Desktop>\Mari_untranslated_zh.json（sp-translation-v1，空值）。
// 每次只新增已存在的词条（绝不覆盖、保留已填写的译法）。只在快捷键触发，
// 不改动任何控件/数据。
static void captureUntranslated() {
    std::map<std::string, std::string> pending;
    auto add = [&](const QString &s) {
        if (!isTranslatableString(s)) return;
        if (!lookupTranslation(s).isEmpty()) return;
        const std::string k = s.trimmed().toUtf8().constData();
        if (k.empty()) return;
        pending.emplace(k, "");
    };

    const auto widgets = QApplication::allWidgets();
    int cellBudget = 200000;   // 防止超大树/表格一次卡死 GUI 线程
    for (QWidget *w : widgets) {
        if (auto *lbl = qobject_cast<QLabel *>(w)) add(labelSource(lbl));
        if (auto *btn = qobject_cast<QAbstractButton *>(w)) add(btn->text());
        if (auto *le = qobject_cast<QLineEdit *>(w)) add(le->text());
        if (auto *cb = qobject_cast<QComboBox *>(w)) {
            add(cb->currentText());
            for (int i = 0; i < cb->count(); ++i) add(cb->itemText(i));
        }
        if (auto *tab = qobject_cast<QTabBar *>(w))
            for (int i = 0; i < tab->count(); ++i) add(tab->tabText(i));
        if (!w->toolTip().isEmpty()) add(w->toolTip());
        if (auto *menu = qobject_cast<QMenu *>(w))
            collectMenuActions(menu, add);
        if (auto *mb = qobject_cast<QMenuBar *>(w))
            for (QAction *a : mb->actions()) {
                add(a->text());
                if (a->menu()) collectMenuActions(a->menu(), add);
            }
        if (auto *tb = qobject_cast<QToolBar *>(w))
            for (QAction *a : tb->actions()) add(a->text());
        if (auto *view = qobject_cast<QAbstractItemView *>(w)) {
            if (view->model() && cellBudget > 0)
                collectModelDeep(view->model(), QModelIndex(), add, 0, cellBudget);
        }
    }
    // 启动以来绘制层捕获的未翻译字符串。
    for (const std::string &s : paintSeenSnapshot())
        if (!s.empty() &&
            lookupTranslation(QString::fromUtf8(s.c_str())).isEmpty())
            pending.emplace(s, "");

    wchar_t desktop[MAX_PATH] = {};
    if (FAILED(SHGetFolderPathW(nullptr, CSIDL_DESKTOPDIRECTORY, nullptr, 0, desktop)) ||
        !desktop[0])
        return;
    const std::wstring path =
        std::wstring(desktop) + L"\\Mari_untranslated_zh.json";

    // 读入上次采集的结果，只新增、不覆盖（保留可能已填写的译法）。
    std::map<std::string, std::string> merged;
    {
        QFile f(QString::fromStdWString(path));
        if (f.open(QIODevice::ReadOnly)) {
            QJsonParseError err{};
            const QJsonDocument doc = QJsonDocument::fromJson(f.readAll(), &err);
            if (err.error == QJsonParseError::NoError && doc.isObject()) {
                const QJsonObject tr = doc.object()
                                           .value(QLatin1String("translations"))
                                           .toObject();
                for (auto it = tr.constBegin(); it != tr.constEnd(); ++it)
                    merged[it.key().toStdString()] = it.value().toString().toStdString();
            }
        }
    }
    int added = 0;
    for (const auto &kv : pending)
        if (merged.emplace(kv.first, "").second) ++added;

    // 有新增才写文件（避免无意义改写已存在的桌面文件）；无论新增多少都弹窗反馈。
    if (added > 0) {
        std::string json = "{\n  \"$schema\": \"sp-translation-v1\",\n"
                           "  \"id\": \"mari-untranslated\",\n"
                           "  \"language\": \"zh-CN\",\n"
                           "  \"description\": \"Shift+` 增量采集的未翻译词条（待填写）\",\n"
                           "  \"translations\": {\n";
        bool first = true;
        for (const auto &kv : merged) {
            if (!first) json += ",\n";
            json += "    \"" + jsonEscape(kv.first) + "\": \"" + jsonEscape(kv.second) + "\"";
            first = false;
        }
        json += "\n  }\n}\n";

        HANDLE h = CreateFileW(path.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS,
                               FILE_ATTRIBUTE_NORMAL, nullptr);
        if (h != INVALID_HANDLE_VALUE) {
            DWORD wr = 0;
            const bool wrote = WriteFile(h, json.data(), (DWORD)json.size(), &wr, nullptr) &&
                               wr == json.size();
            CloseHandle(h);
            (void)wrote;
        }
    }

    // 延迟到按键事件处理完再弹窗，避免在事件过滤器里弹模态对话框。
    const int addedCount = added;
    const int totalCount = static_cast<int>(merged.size());
    const std::wstring savedPath = path;
    QTimer::singleShot(0, QApplication::instance(), [addedCount, totalCount, savedPath]() {
        QMessageBox::information(
            nullptr, QStringLiteral("未翻译词条"),
            QStringLiteral("已捕获 ") + QString::number(addedCount) +
                QStringLiteral(" 条（共 ") + QString::number(totalCount) +
                QStringLiteral(" 条）。\n已保存到桌面：\n") +
                QString::fromStdWString(savedPath));
    });
}

// 正式词库非空时只返回可信词条；词库为空的实验构建继续使用“汉”前缀，
// 用于检查纯显示层覆盖率。两种模式都不会修改控件或模型中的原始文本。
QString displayTranslation(const QString &text) {
    if (!g_enabled)
        return {};
    if (text.isEmpty())
        return {};
    const QString trimmed = text.trimmed();
    if (trimmed.size() <= 1)
        return {};
    if (containsCjk(trimmed))
        return {};

    if (!g_translations.isEmpty())
        return lookupTranslation(text);

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
typedef int (__cdecl *FmWidth)(const QFontMetrics *, const QString &, int);
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
typedef qreal (__cdecl *FmFWidth)(const QFontMetricsF *, const QString &, int);
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
FmWidth g_fmWidth = nullptr;
FmBRectRaw g_fmBRect = nullptr;
FmBRectRectRaw g_fmBRectRect = nullptr;
FmBRectXYWHRaw g_fmBRectXYWH = nullptr;
FmSizeRaw g_fmSize = nullptr;
FmTBRectRaw g_fmTBRect = nullptr;
FmElideRaw g_fmElide = nullptr;
FmFHAdv g_fmfHAdv = nullptr;
FmFWidth g_fmfWidth = nullptr;
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
        const QString result = lookupTranslation(source);
        return result.isNull() ? sourceValue : QVariant(result);
    }
};

QSize proxyDisplayTextSize(const QFontMetrics &metrics, const QString &text);

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
        if (!original_ || !index.isValid())
            return {};
        const QAbstractItemModel *model = index.model();
        if (proxy_.sourceModel() != model)
            proxy_.setSourceModel(const_cast<QAbstractItemModel *>(model));
        QSize result = original_->sizeHint(option, proxy_.mapFromSource(index));
        result.setWidth(qMax(result.width(), proxyDisplayTextSize(
            option.fontMetrics, index.data(Qt::DisplayRole).toString()).width()));
        return result;
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

void pruneComboDisplayBindings() {
    for (auto it = g_comboPaintBindings.begin();
         it != g_comboPaintBindings.end();) {
        if (it->view && it->installed)
            ++it;
        else
            it = g_comboPaintBindings.erase(it);
    }
}

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
// 仅用 QProxyStyle 的公开测量接口计算 combo 显示文本尺寸。
// 不把它安装为全局样式，避免改变 Mari 的自定义绘制和尺寸。
// ---------------------------------------------------------------------------
class ChineseProxyStyle final : public QProxyStyle {
public:
    using QProxyStyle::QProxyStyle;

    QRect itemTextRect(const QFontMetrics &fm, const QRect &r, int flags,
                       bool enabled, const QString &text) const override {
        const QString translated = displayTranslation(text);
        const QString draw = translated.isEmpty() ? text : translated;
        return QProxyStyle::itemTextRect(fm, r, flags, enabled, draw);
    }
};

bool g_proxyStyleInstalled = false;
QPointer<ChineseProxyStyle> g_chineseProxyStyle;

QSize proxyDisplayTextSize(const QFontMetrics &metrics, const QString &text) {
    if (!g_chineseProxyStyle)
        return metrics.size(Qt::TextSingleLine, text);
    return g_chineseProxyStyle->itemTextRect(
        metrics, QRect(0, 0, 32767, 32767),
        Qt::AlignLeft | Qt::AlignVCenter | Qt::TextSingleLine,
        true, text).size();
}

void installProxyStyle() {
    if (g_proxyStyleInstalled || !QApplication::instance())
        return;
    QStyle *current = QApplication::style();
    const QString key = current ? current->objectName() : QString();
    QStyle *base = QStyleFactory::create(
        key.isEmpty() ? QStringLiteral("fusion") : key);
    if (!base)
        base = QStyleFactory::create(QStringLiteral("fusion"));
    if (base) {
        g_chineseProxyStyle = new ChineseProxyStyle(base);
        g_chineseProxyStyle->setParent(QApplication::instance());
        g_proxyStyleInstalled = true;
    }
}

void installAllComboDisplayDelegates() {
    if (!g_enabled)
        return;
    pruneComboDisplayBindings();
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
// QFontMetrics 测量钩子：布局用英文原文算 sizeHint，纯绘制层翻译后中文比
// 英文更宽，会截断/错位。这里在"测量"边界把文本翻译成中文，让 layout /
// elide 看到的是中文宽度，界面布局才正确。翻译命中时额外加一个中文字符
// 的宽度余量，避免中文顶到边缘。
// ---------------------------------------------------------------------------
QString measureText(const QString &text) {
    return displayTranslation(text);
}

int cjkPad(const QFontMetrics *fm) {
    if (g_fmHAdv || g_fmWidth) {
        const int w = g_fmHAdv
            ? g_fmHAdv(fm, QStringLiteral("中"), -1)
            : g_fmWidth(fm, QStringLiteral("中"), -1);
        if (w > 0) return w;
    }
    return fm->height();
}
int cjkPadF(const QFontMetricsF *fm) {
    if (g_fmfHAdv || g_fmfWidth) {
        const qreal w = g_fmfHAdv
            ? g_fmfHAdv(fm, QStringLiteral("中"), -1)
            : g_fmfWidth(fm, QStringLiteral("中"), -1);
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
int hookedFontWidth(const QFontMetrics *fm, const QString &text, int len) {
    QString t = text;
    const QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (len >= 0 && len > t.size()) len = static_cast<int>(t.size());
    return g_fmWidth
        ? g_fmWidth(fm, t, len) + (tr.isEmpty() ? 0 : cjkPad(fm))
        : 0;
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
    if (g_fmBRectXYWH) g_fmBRectXYWH(fm, result, x, y, w, h, flags, t,
                                     tabstops, tabarray);
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
qreal hookedFontFWidth(const QFontMetricsF *fm, const QString &text, int len) {
    QString t = text;
    const QString tr = measureText(text);
    if (!tr.isEmpty()) t = tr;
    if (len >= 0 && len > t.size()) len = static_cast<int>(t.size());
    return g_fmfWidth
        ? g_fmfWidth(fm, t, len) + (tr.isEmpty() ? 0 : cjkPadF(fm))
        : 0;
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
using GraphicsSimpleTextPaint = void (*)(QGraphicsSimpleTextItem *, QPainter *,
                                         const QStyleOptionGraphicsItem *, QWidget *);

DrawPoint g_drawPoint = nullptr;
DrawPointF g_drawPointF = nullptr;
DrawPointF2 g_drawPointF2 = nullptr;
DrawRect g_drawRect = nullptr;
DrawRectFOption g_drawRectFOption = nullptr;
DrawRectFAlign g_drawRectFAlign = nullptr;
DrawXY g_drawXY = nullptr;
DrawXYWH g_drawXYWH = nullptr;
GraphicsSimpleTextPaint g_graphicsSimpleTextPaint = nullptr;

enum class NodeTextRole { Unknown, Title, Input, Output };

bool isAttributionText(const QString &text) {
    return text == QStringLiteral("Bilibili神说要凑数汉化") ||
           text == QStringLiteral("Github仓库");
}

void beginAttributionPaint(QPainter *painter, const QString &text) {
    if (!painter || !isAttributionText(text))
        return;
    painter->save();
    painter->setPen(QColor(0x66, 0xAA, 0xFF));
}

void endAttributionPaint(QPainter *painter, const QString &text) {
    if (painter && isAttributionText(text))
        painter->restore();
}

NodeTextRole nodeTextRole(const QGraphicsSimpleTextItem *textItem) {
    bool belongsToNode = false;
    for (QGraphicsItem *item = textItem ? textItem->parentItem() : nullptr;
         item; item = item->parentItem()) {
        const QByteArray className(typeid(*item).name());
        if (className.contains("MriNgInputPort"))
            return NodeTextRole::Input;
        if (className.contains("MriNgOutputPort"))
            return NodeTextRole::Output;
        if (className.contains("MriNgExtendedNode") ||
            className.contains("MriNgNode"))
            belongsToNode = true;
    }
    return belongsToNode ? NodeTextRole::Title : NodeTextRole::Unknown;
}

void hookedDrawPoint(QPainter *p, const QPoint &pt, const QString &text) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawPoint(p, pt, t.isEmpty() ? text : t);
    endAttributionPaint(p, text);
}
void hookedDrawPointF(QPainter *p, const QPointF &pt, const QString &text) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawPointF(p, pt, t.isEmpty() ? text : t);
    endAttributionPaint(p, text);
}
void hookedDrawPointF2(QPainter *p, const QPointF &pt, const QString &text,
                       int flags, int just) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawPointF2(p, pt, t.isEmpty() ? text : t, flags, just);
    endAttributionPaint(p, text);
}
void hookedDrawRect(QPainter *p, const QRect &r, int flags, const QString &text,
                    QRect *br) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawRect(p, r, flags, t.isEmpty() ? text : t, br);
    endAttributionPaint(p, text);
}
void hookedDrawRectFOption(QPainter *p, const QRectF &r, const QString &text,
                           const QTextOption &opt) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawRectFOption(p, r, t.isEmpty() ? text : t, opt);
    endAttributionPaint(p, text);
}
void hookedDrawRectFAlign(QPainter *p, const QRectF &r, int flags,
                          const QString &text, QRectF *br) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawRectFAlign(p, r, flags, t.isEmpty() ? text : t, br);
    endAttributionPaint(p, text);
}
void hookedDrawXY(QPainter *p, int x, int y, const QString &text) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawXY(p, x, y, t.isEmpty() ? text : t);
    endAttributionPaint(p, text);
}
void hookedDrawXYWH(QPainter *p, int x, int y, int w, int h, int flags,
                    const QString &text, QRect *br) {
    QString t = displayTranslation(text);
    beginAttributionPaint(p, text);
    g_drawXYWH(p, x, y, w, h, flags, t.isEmpty() ? text : t, br);
    endAttributionPaint(p, text);
}

void hookedGraphicsSimpleTextPaint(QGraphicsSimpleTextItem *self, QPainter *painter,
                                   const QStyleOptionGraphicsItem *option,
                                   QWidget *widget) {
    if (!self || !painter || !g_graphicsSimpleTextPaint) {
        if (g_graphicsSimpleTextPaint)
            g_graphicsSimpleTextPaint(self, painter, option, widget);
        return;
    }
    const QString display = displayTranslation(self->text());
    const NodeTextRole role = nodeTextRole(self);
    if (display.isEmpty() || role == NodeTextRole::Unknown) {
        g_graphicsSimpleTextPaint(self, painter, option, widget);
        return;
    }
    QGraphicsSimpleTextItem translatedItem(display);
    translatedItem.setFont(self->font());
    translatedItem.setBrush(self->brush());
    translatedItem.setPen(self->pen());
    qreal xOffset = 0.0;
    const qreal sourceWidth = self->boundingRect().width();
    const qreal displayWidth = translatedItem.boundingRect().width();
    if (role == NodeTextRole::Title)
        xOffset = (sourceWidth - displayWidth) * 0.5;
    else if (role == NodeTextRole::Output)
        xOffset = sourceWidth - displayWidth;
    painter->save();
    painter->translate(xOffset, 0.0);
    translatedItem.paint(painter, option, widget);
    painter->restore();
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

std::vector<HMODULE> loadedModules() {
    std::vector<HMODULE> modules(256);
    DWORD needed = 0;
    for (;;) {
        if (!EnumProcessModules(GetCurrentProcess(), modules.data(),
                                static_cast<DWORD>(modules.size() * sizeof(HMODULE)),
                                &needed))
            return {};
        if (needed <= modules.size() * sizeof(HMODULE)) {
            modules.resize(needed / sizeof(HMODULE));
            return modules;
        }
        modules.resize((needed / sizeof(HMODULE)) + 64);
    }
}

bool isCommittedAddress(const void *address) {
    if (!address)
        return false;
    MEMORY_BASIC_INFORMATION info{};
    return VirtualQuery(address, &info, sizeof(info)) == sizeof(info) &&
           info.State == MEM_COMMIT &&
           !(info.Protect & (PAGE_NOACCESS | PAGE_GUARD));
}

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

bool installNodeGraphTextHook() {
    if (g_nodeTextHookInstalled)
        return true;
    HMODULE nodeGraph = GetModuleHandleW(L"MriNodeGraph.dll");
    HMODULE qtWidgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!nodeGraph || !qtWidgets)
        return false;
    void *original = reinterpret_cast<void *>(GetProcAddress(
        qtWidgets,
        "?paint@QGraphicsSimpleTextItem@@UEAAXPEAVQPainter@@PEBVQStyleOptionGraphicsItem@@PEAVQWidget@@@Z"));
    if (!original)
        return false;
    g_graphicsSimpleTextPaint =
        reinterpret_cast<GraphicsSimpleTextPaint>(original);
    g_nodeTextHookInstalled = replaceImportInModule(
        nodeGraph, g_hookSlots, original,
        reinterpret_cast<void *>(&hookedGraphicsSimpleTextPaint));
    return g_nodeTextHookInstalled;
}

bool replaceImportAllModules(std::vector<ImportHookSlot> &list,
                             void *original, void *replacement) {
    bool any = false;
    for (HMODULE module : loadedModules()) {
        if (replaceImportInModule(module, list, original, replacement))
            any = true;
    }
    return any;
}

bool restoreImportHooks(std::vector<ImportHookSlot> &list) {
    for (std::size_t i = list.size(); i > 0; --i) {
        const std::size_t cur = i - 1;
        const ImportHookSlot hook = list[cur];
        if (!isCommittedAddress(hook.slot) || *hook.slot != hook.replacement) {
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
        {(void *)g_fmWidth, (void *)&hookedFontWidth},
        {(void *)g_fmBRect, (void *)&hookedFontBRect},
        {(void *)g_fmBRectRect, (void *)&hookedFontBRectRect},
        {(void *)g_fmBRectXYWH, (void *)&hookedFontBRectXYWH},
        {(void *)g_fmSize, (void *)&hookedFontSize},
        {(void *)g_fmTBRect, (void *)&hookedFontTBRect},
        {(void *)g_fmElide, (void *)&hookedFontElide},
        {(void *)g_fmfHAdv, (void *)&hookedFontFHAdv},
        {(void *)g_fmfWidth, (void *)&hookedFontFWidth},
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
        (void *)g_fmHAdv, (void *)g_fmWidth,
        (void *)g_fmBRect, (void *)g_fmBRectRect,
        (void *)g_fmBRectXYWH, (void *)g_fmSize, (void *)g_fmTBRect,
        (void *)g_fmElide, (void *)g_fmfHAdv, (void *)g_fmfWidth,
        (void *)g_fmfBRect,
        (void *)g_fmfBRectRect, (void *)g_fmfSize, (void *)g_fmfTBRect,
        (void *)g_fmfElide,
    };
    bool found = false;
    for (const void *p : ptrs) {
        if (!p)
            continue;
        found = true;
        if (!isExecutableCodeAddr(p))
            return false;
    }
    return found;
}

void installFontMeasurementHooks() {
    if (g_fontHooksInstalled)
        return;
    HMODULE qtGui = GetModuleHandleW(L"Qt5Gui.dll");
    if (!qtGui)
        return;
    g_fmHAdv = (FmHAdv)GetProcAddress(qtGui,
        "?horizontalAdvance@QFontMetrics@@QEBAHAEBVQString@@H@Z");
    g_fmWidth = (FmWidth)GetProcAddress(qtGui,
        "?width@QFontMetrics@@QEBAHAEBVQString@@H@Z");
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
    g_fmfWidth = (FmFWidth)GetProcAddress(qtGui,
        "?width@QFontMetricsF@@QEBANAEBVQString@@H@Z");
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

    g_fontMeasureReady = fontSymbolsAreValid();
    g_fontHooksInstalled = g_fontMeasureReady;
    if (g_fontHooksInstalled)
        patchFontModules();
}

bool loadTranslationsFromJson(const QString &path) {
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return false;
    QJsonParseError error{};
    const QJsonDocument doc = QJsonDocument::fromJson(file.readAll(), &error);
    if (error.error != QJsonParseError::NoError || !doc.isObject())
        return false;
    const QJsonObject root = doc.object();
    const QJsonValue trans = root.value(QLatin1String("translations"));
    if (!trans.isObject())
        return false;
    const QJsonObject entries = trans.toObject();
    bool any = false;
    for (auto it = entries.begin(); it != entries.end(); ++it) {
        if (!it.value().isString())
            continue;
        const QString key = it.key();
        const QString value = it.value().toString();
        // 跳过空键/空值。
        if (key.isEmpty() || value.isEmpty())
            continue;
        g_translations.insert(key, value);
        any = true;
    }
    return any;
}

std::wstring modulePathW() {
    std::vector<wchar_t> buf(1024);
    while (buf.size() <= 32768) {
        DWORD n = GetModuleFileNameW(g_moduleHandle, buf.data(),
                                     static_cast<DWORD>(buf.size()));
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
    // 词库合并后重建归一化模糊索引与排序键表。
    rebuildLookupIndex();
}

QPointer<QMenuBar> g_attributionMenuBar;
QPointer<QAction> g_languageAction;
QPointer<QAction> g_authorAction;
QPointer<QAction> g_githubAction;

void refreshTranslatedDisplay() {
    for (QWidget *widget : QApplication::allWidgets()) {
        if (!widget)
            continue;
        if (qobject_cast<QMenuBar *>(widget) || qobject_cast<QMenu *>(widget))
            continue;
        widget->updateGeometry();
        if (widget->layout())
            widget->layout()->invalidate();
    }
}

// 一次枚举全部模块，同时补齐绘制与字体测量 Hook。旧实现每个符号各枚举
// 一遍模块，启动阶段每两秒会产生二十余次重复枚举。
void patchLateLoadedModules() {
    struct Symbol {
        void *original;
        void *replacement;
        std::vector<ImportHookSlot> *hookList;
    };
    const Symbol symbols[] = {
        {(void *)g_drawPoint, (void *)&hookedDrawPoint, &g_hookSlots},
        {(void *)g_drawPointF, (void *)&hookedDrawPointF, &g_hookSlots},
        {(void *)g_drawPointF2, (void *)&hookedDrawPointF2, &g_hookSlots},
        {(void *)g_drawRect, (void *)&hookedDrawRect, &g_hookSlots},
        {(void *)g_drawRectFOption, (void *)&hookedDrawRectFOption, &g_hookSlots},
        {(void *)g_drawRectFAlign, (void *)&hookedDrawRectFAlign, &g_hookSlots},
        {(void *)g_drawXY, (void *)&hookedDrawXY, &g_hookSlots},
        {(void *)g_drawXYWH, (void *)&hookedDrawXYWH, &g_hookSlots},
        {(void *)g_fmHAdv, (void *)&hookedFontHAdv, &g_fontHookSlots},
        {(void *)g_fmBRect, (void *)&hookedFontBRect, &g_fontHookSlots},
        {(void *)g_fmBRectRect, (void *)&hookedFontBRectRect, &g_fontHookSlots},
        {(void *)g_fmBRectXYWH, (void *)&hookedFontBRectXYWH, &g_fontHookSlots},
        {(void *)g_fmSize, (void *)&hookedFontSize, &g_fontHookSlots},
        {(void *)g_fmTBRect, (void *)&hookedFontTBRect, &g_fontHookSlots},
        {(void *)g_fmElide, (void *)&hookedFontElide, &g_fontHookSlots},
        {(void *)g_fmfHAdv, (void *)&hookedFontFHAdv, &g_fontHookSlots},
        {(void *)g_fmfBRect, (void *)&hookedFontFBRect, &g_fontHookSlots},
        {(void *)g_fmfBRectRect, (void *)&hookedFontFBRectRect, &g_fontHookSlots},
        {(void *)g_fmfSize, (void *)&hookedFontFSize, &g_fontHookSlots},
        {(void *)g_fmfTBRect, (void *)&hookedFontFTBRect, &g_fontHookSlots},
        {(void *)g_fmfElide, (void *)&hookedFontFElide, &g_fontHookSlots},
    };

    const std::vector<HMODULE> modules = loadedModules();
    for (HMODULE module : modules) {
        for (const Symbol &symbol : symbols) {
            if (!symbol.original)
                continue;
            if (symbol.hookList == &g_fontHookSlots && !g_fontMeasureReady)
                continue;
            replaceImportInModule(module, *symbol.hookList,
                                  symbol.original, symbol.replacement);
        }
    }
}

void repaintTranslatedDisplay() {
    for (QWidget *widget : QApplication::allWidgets()) {
        if (widget && widget->isVisible())
            widget->update();
    }
    QTimer::singleShot(0, QApplication::instance(), [] {
        for (QWidget *widget : QApplication::allWidgets()) {
            if (widget && widget->isVisible())
                widget->update();
        }
    });
}

void toggleTranslation() {
    g_enabled = !g_enabled;

    for (QWidget *widget : QApplication::allWidgets()) {
        if (!widget)
            continue;
        QEvent event(QEvent::FontChange);
        QApplication::sendEvent(widget, &event);
    }

    refreshTranslatedDisplay();

    for (QWidget *widget : QApplication::allWidgets()) {
        if (auto *menuBar = qobject_cast<QMenuBar *>(widget)) {
            QEvent event(QEvent::StyleChange);
            QApplication::sendEvent(menuBar, &event);
        }
    }

    for (QWidget *widget : QApplication::topLevelWidgets()) {
        if (!widget || !widget->isVisible())
            continue;
        if (QLayout *layout = widget->layout()) {
            layout->invalidate();
            layout->activate();
        }
        if (!widget->isMaximized() && !widget->isFullScreen())
            widget->adjustSize();
    }

    repaintTranslatedDisplay();
}

QString toggleKeyName(int key) {
    if (key >= Qt::Key_F1 && key <= Qt::Key_F12)
        return QStringLiteral("F") + QString::number(key - Qt::Key_F1 + 1);
    return QKeySequence(key).toString(QKeySequence::NativeText);
}

class ToggleHotkeyDialog final : public QDialog {
public:
    explicit ToggleHotkeyDialog(QWidget *parent) : QDialog(parent) {
        g_hotkeyDialogOpen = true;
        setWindowTitle(QStringLiteral("设置 中/英 切换快捷键"));
        setAttribute(Qt::WA_DeleteOnClose);
        auto *layout = new QVBoxLayout(this);
        layout->addWidget(new QLabel(
            QStringLiteral("点击下方按钮后按下新快捷键（Esc 取消）："), this));
        captureButton_ = new QPushButton(
            QStringLiteral("当前：") + toggleKeyName(g_toggleKey), this);
        auto *ok = new QPushButton(QStringLiteral("确定"), this);
        auto *reset = new QPushButton(QStringLiteral("重置"), this);
        layout->addWidget(captureButton_);
        auto *row = new QHBoxLayout;
        row->addWidget(ok);
        row->addWidget(reset);
        layout->addLayout(row);
        ok->setDefault(true);
        reset->setAutoDefault(false);
        captureButton_->setAutoDefault(false);
        QObject::connect(captureButton_, &QPushButton::clicked,
                         this, [this] { startCapture(); });
        QObject::connect(ok, &QPushButton::clicked, this, [this] {
            stopCapture();
            accept();
        });
        QObject::connect(reset, &QPushButton::clicked, this, [this] {
            g_toggleKey = Qt::Key_F3;
            stopCapture();
        });
        QObject::connect(this, &QObject::destroyed, [] {
            g_hotkeyDialogOpen = false;
        });
    }
private:
    QPushButton *captureButton_ = nullptr;
    bool capturing_ = false;

    void startCapture() {
        capturing_ = true;
        QApplication::instance()->installEventFilter(this);
        captureButton_->setText(QStringLiteral("请按下新的快捷键…"));
    }
    void stopCapture() {
        if (capturing_) {
            QApplication::instance()->removeEventFilter(this);
            capturing_ = false;
        }
        captureButton_->setText(
            QStringLiteral("当前：") + toggleKeyName(g_toggleKey));
    }
    bool eventFilter(QObject *, QEvent *event) override {
        if (!capturing_ || event->type() != QEvent::KeyPress)
            return false;
        auto *keyEvent = static_cast<QKeyEvent *>(event);
        if (keyEvent->key() == Qt::Key_Escape) {
            stopCapture();
            return true;
        }
        g_toggleKey = keyEvent->key();
        stopCapture();
        return true;
    }
    void reject() override {
        stopCapture();
        QDialog::reject();
    }
};

void openToggleHotkeyDialog() {
    static QPointer<ToggleHotkeyDialog> dialog;
    if (dialog) {
        dialog->raise();
        dialog->activateWindow();
        return;
    }
    QWidget *parent = g_attributionMenuBar
        ? g_attributionMenuBar->window() : nullptr;
    dialog = new ToggleHotkeyDialog(parent);
    QObject::connect(dialog, &QObject::destroyed, [] { dialog = nullptr; });
    dialog->show();
    dialog->raise();
}

class LanguageMenuMouseFilter final : public QObject {
public:
    using QObject::QObject;
    bool eventFilter(QObject *object, QEvent *event) override {
        auto *menuBar = qobject_cast<QMenuBar *>(object);
        if (!menuBar)
            return false;
        if (event->type() == QEvent::MouseMove) {
            auto *mouseEvent = static_cast<QMouseEvent *>(event);
            const bool overLink =
                (g_authorAction && menuBar->actionGeometry(g_authorAction)
                                       .contains(mouseEvent->pos())) ||
                (g_githubAction && menuBar->actionGeometry(g_githubAction)
                                       .contains(mouseEvent->pos()));
            if (overLink)
                menuBar->setCursor(Qt::PointingHandCursor);
            else
                menuBar->unsetCursor();
            return false;
        }
        if (event->type() == QEvent::Leave) {
            menuBar->unsetCursor();
            return false;
        }
        if (event->type() != QEvent::MouseButtonPress || !g_languageAction)
            return false;
        auto *mouseEvent = static_cast<QMouseEvent *>(event);
        if (mouseEvent->button() == Qt::MiddleButton &&
            menuBar->actionGeometry(g_languageAction).contains(mouseEvent->pos())) {
            openToggleHotkeyDialog();
            return true;
        }
        return false;
    }
};

bool installAttributionActions() {
    QMenuBar *menuBar = nullptr;
    QAction *helpAction = nullptr;
    for (QWidget *widget : QApplication::allWidgets()) {
        auto *candidate = qobject_cast<QMenuBar *>(widget);
        if (!candidate)
            continue;
        bool hasFile = false;
        QAction *candidateHelp = nullptr;
        for (QAction *action : candidate->actions()) {
            QString label = action ? action->text() : QString();
            label.remove(QLatin1Char('&'));
            if (label.compare(QStringLiteral("File"), Qt::CaseInsensitive) == 0)
                hasFile = true;
            if (label.compare(QStringLiteral("Help"), Qt::CaseInsensitive) == 0)
                candidateHelp = action;
        }
        if (hasFile && candidateHelp) {
            menuBar = candidate;
            helpAction = candidateHelp;
            break;
        }
    }
    if (!menuBar)
        return false;

    if (!g_languageAction) {
        g_languageAction = new QAction(QStringLiteral("中/英"), menuBar);
        g_languageAction->setObjectName(QStringLiteral("mari_chinese_language"));
        g_languageAction->setToolTip(
            QStringLiteral("左键切换中英文，中键设置快捷键"));
        QObject::connect(g_languageAction, &QAction::triggered,
                         [] { toggleTranslation(); });
    }
    if (!g_authorAction) {
        g_authorAction = new QAction(
            QStringLiteral("Bilibili神说要凑数汉化"), menuBar);
        g_authorAction->setObjectName(QStringLiteral("mari_chinese_author"));
        QObject::connect(g_authorAction, &QAction::triggered, [] {
            QDesktopServices::openUrl(QUrl(QStringLiteral(
                "https://space.bilibili.com/281243426?spm_id_from=333.1007.0.0")));
        });
    }
    if (!g_githubAction) {
        g_githubAction = new QAction(QStringLiteral("Github仓库"), menuBar);
        g_githubAction->setObjectName(QStringLiteral("mari_chinese_github"));
        QObject::connect(g_githubAction, &QAction::triggered, [] {
            QDesktopServices::openUrl(
                QUrl(QStringLiteral("https://github.com/iillya/MariChinese")));
        });
    }
    g_languageAction->setParent(menuBar);
    g_authorAction->setParent(menuBar);
    g_githubAction->setParent(menuBar);
    if (!menuBar->property("mari_chinese_mouse_filter").toBool()) {
        menuBar->installEventFilter(new LanguageMenuMouseFilter(menuBar));
        menuBar->setMouseTracking(true);
        menuBar->setProperty("mari_chinese_mouse_filter", true);
    }

    const QList<QAction *> before = menuBar->actions();
    const int helpIndex = before.indexOf(helpAction);
    QAction *insertBefore = helpIndex >= 0 && helpIndex + 1 < before.size()
        ? before.at(helpIndex + 1) : nullptr;
    const QList<QAction *> current = menuBar->actions();
    const QList<QAction *> customActions = {
        g_languageAction, g_authorAction, g_githubAction
    };
    for (QAction *action : customActions) {
        if (current.contains(action))
            continue;
        if (insertBefore)
            menuBar->insertAction(insertBefore, action);
        else
            menuBar->addAction(action);
    }
    g_attributionMenuBar = menuBar;
    const QList<QAction *> installed = menuBar->actions();
    return installed.contains(g_languageAction) &&
           installed.contains(g_authorAction) &&
           installed.contains(g_githubAction);
}

// ---------------------------------------------------------------------------
// 原生消息层键盘拦截
// Mari 主界面是原生窗口（OpenGL 视口），Qt 的 QKeyEvent 不会派发进来，
// 因此 SpeedTree 那种 QApplication::installEventFilter 方式拿不到按键。
// 这里改用 QAbstractNativeEventFilter 拦截 Windows WM_KEYDOWN，在消息层
// 识别 Shift + ` 与中/英切换键（F3 等），不依赖窗口焦点或控件类型。
// ---------------------------------------------------------------------------
static UINT qtKeyToVk(int key) {
    if (key >= Qt::Key_F1 && key <= Qt::Key_F12)
        return VK_F1 + (key - Qt::Key_F1);
    if (key >= Qt::Key_A && key <= Qt::Key_Z)
        return 'A' + (key - Qt::Key_A);
    if (key >= Qt::Key_0 && key <= Qt::Key_9)
        return '0' + (key - Qt::Key_0);
    if (key == Qt::Key_Space) return VK_SPACE;
    if (key == Qt::Key_Tab) return VK_TAB;
    if (key == Qt::Key_Return) return VK_RETURN;
    if (key == Qt::Key_Backspace) return VK_BACK;
    if (key == Qt::Key_Escape) return VK_ESCAPE;
    if (key == Qt::Key_Delete) return VK_DELETE;
    if (key == Qt::Key_Insert) return VK_INSERT;
    if (key == Qt::Key_Home) return VK_HOME;
    if (key == Qt::Key_End) return VK_END;
    if (key == Qt::Key_PageUp) return VK_PRIOR;
    if (key == Qt::Key_PageDown) return VK_NEXT;
    if (key == Qt::Key_Left) return VK_LEFT;
    if (key == Qt::Key_Right) return VK_RIGHT;
    if (key == Qt::Key_Up) return VK_UP;
    if (key == Qt::Key_Down) return VK_DOWN;
    return 0;
}

class NativeKeyFilter final : public QAbstractNativeEventFilter {
public:
    // 通过 WM_KEYDOWN/WM_KEYUP 跟踪 Shift 状态，不依赖全局物理键状态，
    // 这样无论真实输入还是程序投递的消息都能正确判定组合键。
    bool shiftDown_ = false;

    bool nativeEventFilter(const QByteArray &eventType, void *message,
                           long *result) override {
        Q_UNUSED(eventType);
        Q_UNUSED(result);
        if (!message)
            return false;
        MSG *msg = static_cast<MSG *>(message);
        const bool isDown = (msg->message == WM_KEYDOWN ||
                             msg->message == WM_SYSKEYDOWN);
        const bool isUp = (msg->message == WM_KEYUP ||
                           msg->message == WM_SYSKEYUP);
        if (!isDown && !isUp)
            return false;

        const UINT vk = static_cast<UINT>(msg->wParam);
        if (vk == VK_SHIFT) {
            shiftDown_ = isDown;
            return false;
        }
        // 自动重复的按住事件忽略，只在真正的按下瞬间触发一次。
        if ((msg->lParam & 0x40000000) != 0)   // bit30 = 上一次按键状态
            return false;

        // Shift + ` (~)：未翻译词条嗅探。VK_OEM_3 是 `/~ 键（ESC 下方）。
        if (vk == VK_OEM_3 && shiftDown_) {
            captureUntranslated();
            return true;
        }

        // 中/英切换快捷键：把 Qt::Key 转成 VK 后比对（Shift 组合不触发）。
        const UINT toggleVk = qtKeyToVk(g_toggleKey);
        if (!shiftDown_ && toggleVk && vk == toggleVk) {
            toggleTranslation();
            return true;
        }
        return false;
    }
};

class ApplicationEventFilter final : public QObject {
public:
    using QObject::QObject;
    bool eventFilter(QObject *object, QEvent *event) override {
        if (event->type() == QEvent::Show) {
            if (auto *combo = qobject_cast<QComboBox *>(object))
                installComboDisplayDelegate(combo->view());
            if (!g_nodeTextHookInstalled && installNodeGraphTextHook())
                patchLateLoadedModules();
        } else if ((event->type() == QEvent::ActionAdded ||
                    event->type() == QEvent::ActionRemoved) &&
                   qobject_cast<QMenuBar *>(object)) {
            QTimer::singleShot(0, QApplication::instance(), [] {
                installAttributionActions();
            });
        }
        if (event->type() != QEvent::KeyRelease)
            return false;
        auto *keyEvent = static_cast<QKeyEvent *>(event);
        if (g_hotkeyDialogOpen || keyEvent->isAutoRepeat())
            return false;
        // Shift + `（常见布局上报为 Key_AsciiTilde，也接受 Key_QuoteLeft）。
        const bool tildeKey =
            (keyEvent->key() == Qt::Key_QuoteLeft ||
             keyEvent->key() == Qt::Key_AsciiTilde);
        if (tildeKey && (keyEvent->modifiers() & Qt::ShiftModifier)) {
            captureUntranslated();
            return true;
        }
        if (keyEvent->key() == g_toggleKey) {
            toggleTranslation();
            return true;
        }
        return false;
    }
};

void runOnGuiThread(QApplication *app) {
    const std::wstring dir = modulePathW();
    const std::wstring folder = dir.find_last_of(L"\\/") == std::wstring::npos
        ? dir : dir.substr(0, dir.find_last_of(L"\\/"));
    loadDictionariesFromDir(folder);
    installProxyStyle();
    installHooks();
    installFontMeasurementHooks();
    installAllComboDisplayDelegates();
    app->installEventFilter(new ApplicationEventFilter(app));
    // 原生消息层按键拦截：覆盖天然不派发 QKeyEvent 的原生/3D 视口窗口。
    if (QAbstractEventDispatcher *dispatcher = QAbstractEventDispatcher::instance())
        dispatcher->installNativeEventFilter(new NativeKeyFilter);
    installAttributionActions();
    // 晚加载 DLL（如按需加载的插件）会绕过启动时的 IAT 扫描，定期重扫。
    auto *rescanTimer = new QTimer(app);
    rescanTimer->setInterval(2000);
    QObject::connect(rescanTimer, &QTimer::timeout, [] {
        patchLateLoadedModules();
        installAllComboDisplayDelegates();
        installAttributionActions();
    });
    rescanTimer->start();
    QTimer::singleShot(60000, app, [rescanTimer] {
        rescanTimer->stop();
        rescanTimer->deleteLater();
    });

    // MriNodeGraph.dll is loaded only when a project opens. Poll only until its
    // display-only QGraphicsSimpleTextItem paint hook is installed.
    auto *nodeTimer = new QTimer(app);
    nodeTimer->setInterval(2000);
    QObject::connect(nodeTimer, &QTimer::timeout, [nodeTimer] {
        if (installNodeGraphTextHook()) {
            patchLateLoadedModules();
            nodeTimer->stop();
            nodeTimer->deleteLater();
        }
    });
    if (!installNodeGraphTextHook()) {
        nodeTimer->start();
        const QPointer<QTimer> nodeTimerGuard(nodeTimer);
        QTimer::singleShot(60000, app, [nodeTimerGuard] {
            if (nodeTimerGuard) {
                nodeTimerGuard->stop();
                nodeTimerGuard->deleteLater();
            }
        });
    } else {
        nodeTimer->deleteLater();
    }
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
    // The context overload is available on the Qt 5.6 compatibility baseline
    // and guarantees execution on QApplication's thread.
    QTimer::singleShot(0, app, [app] { runOnGuiThread(app); });
    return 0;
}

} // namespace

BOOL WINAPI DllMain(HINSTANCE hinst, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        g_moduleHandle = hinst;
        DisableThreadLibraryCalls(hinst);
        HANDLE h = CreateThread(nullptr, 0, worker, nullptr, 0, nullptr);
        if (h)
            CloseHandle(h);
    }
    return TRUE;
}

