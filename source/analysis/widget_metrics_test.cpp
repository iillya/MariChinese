#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include "../hook.cpp"
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QTabBar>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QListWidget>
#include <QtCore/QThread>
#include <cstdio>
#include <QtGui/QImage>
#include <QtWidgets/QGraphicsRectItem>

static bool enabled = true;
static QString lookup(const QString& text) {
    return enabled && text == QLatin1String("UV")
        ? QStringLiteral("纹理坐标与投影设置") : QString();
}

class DeleteSiblingOnFontChange final : public QObject {
public:
    QPointer<QWidget> first{new QWidget};
    QPointer<QWidget> second{new QWidget};
    int callbacks = 0;
    ~DeleteSiblingOnFontChange() override {
        delete first.data();
        delete second.data();
    }
    bool eventFilter(QObject* watched, QEvent* event) override {
        if (event->type() == QEvent::FontChange && !callbacks++) {
            // Host callbacks may remove a panel later in allWidgets().
            if (first && first != watched) delete first.data();
            else if (second && second != watched) delete second.data();
        }
        return false;
    }
};

static std::vector<QString> paintedText;
static void recordRect(QPainter*, const QRect&, int, const QString& text, QRect* bounds) {
    paintedText.push_back(text);
    if (bounds) *bounds = QRect(0, 0, text.size(), 1);
}
static void recordRectF(QPainter*, const QRectF&, int, const QString& text, QRectF* bounds) {
    paintedText.push_back(text);
    if (bounds) *bounds = QRectF(0, 0, text.size(), 1);
}
static void recordXYWH(QPainter*, int, int, int, int, int, const QString& text, QRect* bounds) {
    paintedText.push_back(text);
    if (bounds) *bounds = QRect(0, 0, text.size(), 1);
}
static bool exerciseBounds(QPainter* painter, int expectedWidth) {
    QRect bounds;
    QRectF boundsF;
    hookedDrawRect(painter, QRect(0, 0, 200, 30), 0, QStringLiteral("UV"), &bounds);
    hookedDrawRectFAlign(painter, QRectF(0, 0, 200, 30), 0, QStringLiteral("UV"), &boundsF);
    const bool correct = bounds.width() == expectedWidth && boundsF.width() == expectedWidth;
    hookedDrawXYWH(painter, 0, 0, 200, 30, 0, QStringLiteral("UV"), &bounds);
    return correct && bounds.width() == expectedWidth;
}
class WidgetWithPaintBounds final : public QWidget {
public:
    bool correct = false;
    int expectedWidth = 0;
protected:
    void paintEvent(QPaintEvent*) override {
        QPainter painter(this);
        paintedText.clear();
        correct = exerciseBounds(&painter, expectedWidth);
    }
};

class CacheDelegateProbe final : public QAbstractItemDelegate {
public:
    mutable QString displayed;
    void paint(QPainter*, const QStyleOptionViewItem&, const QModelIndex& index) const override {
        displayed = index.data(Qt::DisplayRole).toString();
    }
    QSize sizeHint(const QStyleOptionViewItem&, const QModelIndex&) const override { return {}; }
};
class MriNgNodeProbe final : public QGraphicsRectItem {};
static bool checkNodeImageCache(const QString& source, const QString& target) {
    MriNgNodeProbe parent;
    QGraphicsSimpleTextItem item(source, &parent);
    QWidget owner;
    owner.setAttribute(Qt::WA_DontShowOnScreen);
    owner.show();
    const auto previous = g_graphicsSimpleTextPaint;
    g_graphicsSimpleTextPaint = [](QGraphicsSimpleTextItem* text, QPainter* painter,
                                  const QStyleOptionGraphicsItem* option, QWidget* widget) {
        text->paint(painter, option, widget);
    };
    const auto render = [&](bool hook, bool display) {
        QImage image(400, 60, QImage::Format_ARGB32_Premultiplied);
        image.fill(Qt::transparent);
        QPainter painter(&image);
        painter.translate(170, 10);
        QStyleOptionGraphicsItem option;
        if (hook) {
            hookedGraphicsSimpleTextPaint(&item, &painter, &option, display ? &owner : nullptr);
        } else {
            QGraphicsSimpleTextItem reference(display ? target : source);
            reference.setFont(item.font());
            reference.setPen(item.pen());
            reference.setBrush(item.brush());
            if (display) painter.translate((item.boundingRect().width() - reference.boundingRect().width()) / 2, 0);
            reference.paint(&painter, &option, nullptr);
        }
        painter.end();
        return image;
    };
    const bool correct = render(true, true) == render(false, true) &&
        render(true, false) == render(false, false) && item.text() == source;
    g_graphicsSimpleTextPaint = previous;
    std::printf("node display image cache/source export: %s\n", correct ? "PASS" : "FAIL");
    return correct;
}

int main(int argc, char** argv) {
    QApplication app(argc, argv);
    app.setStyle(QStringLiteral("Fusion"));
    const QString source = QStringLiteral("UV");
    const QString target = lookup(source);
    g_lookup.add(source, target);
    g_lookup.rebuild();
    const QFontMetrics fm(app.font());
    const auto sourceWidth = [&]() {
#if QT_VERSION >= QT_VERSION_CHECK(5, 11, 0)
        return fm.horizontalAdvance(source);
#else
        return fm.width(source);
#endif
    };
    const int originalWidth = sourceWidth();
    const QString originalElide = fm.elidedText(source, Qt::ElideRight, 80);
    installUiMeasurementHooks();
    installProxyStyle();
    if (g_uiMetricSlots.empty()) return 2;
    if (sourceWidth() != originalWidth ||
        fm.elidedText(source, Qt::ElideRight, 80) != originalElide) return 3;
    int failures = checkNodeImageCache(source, target) ? 0 : 1;
    const auto check = [&](const char* type, const QSize& actual, const QSize& expected) {
        const bool same = actual == expected;
        std::printf("%s %s actual=%dx%d expected=%dx%d\n", same ? "PASS" : "FAIL",
            type, actual.width(), actual.height(), expected.width(), expected.height());
        if (!same) ++failures;
    };
    QLabel label(source), labelReference(target);
    QPushButton button(source), buttonReference(target);
    QCheckBox checkBox(source), checkReference(target);
    QRadioButton radio(source), radioReference(target);
    QGroupBox group(source), groupReference(target);
    QTabBar tabs, tabsReference;
    tabs.addTab(source); tabsReference.addTab(target);
    QComboBox combo, comboReference;
    combo.addItem(source); comboReference.addItem(target);
    QMenuBar menu, menuReference;
    menu.addAction(source); menuReference.addAction(target);
    QListWidget list, listReference;
    list.addItem(source); listReference.addItem(target);
    installComboDisplayDelegate(&list);
    check("label", label.sizeHint(), labelReference.sizeHint());
    check("button", button.sizeHint(), buttonReference.sizeHint());
    check("checkbox", checkBox.sizeHint(), checkReference.sizeHint());
    check("radio", radio.sizeHint(), radioReference.sizeHint());
    check("group", group.minimumSizeHint(), groupReference.minimumSizeHint());
    check("tab", tabs.sizeHint(), tabsReference.sizeHint());
    tabs.setShape(QTabBar::RoundedWest); tabsReference.setShape(QTabBar::RoundedWest);
    check("vertical-tab", tabs.sizeHint(), tabsReference.sizeHint());
    check("combo", combo.sizeHint(), comboReference.sizeHint());
    check("menu", menu.sizeHint(), menuReference.sizeHint());
    check("list-row", QSize(list.sizeHintForColumn(0),list.sizeHintForRow(0)),
        QSize(listReference.sizeHintForColumn(0),listReference.sizeHintForRow(0)));
    if (label.text() != source || button.text() != source || tabs.tabText(0) != source ||
        combo.currentText() != source || list.item(0)->text() != source ||
        menu.actions().at(0)->text() != source) ++failures;
    enabled = false;
    DeleteSiblingOnFontChange removal;
    app.installEventFilter(&removal);
    toggleTranslation();
    app.removeEventFilter(&removal);
    if (removal.callbacks == 0 || (removal.first && removal.second)) ++failures;
    QLabel english(source);
    check("existing-label-English", label.sizeHint(), english.sizeHint());
    if (english.sizeHint().width() >= labelReference.sizeHint().width()) ++failures;
    g_enabled = true;
    g_drawRect = recordRect;
    g_drawRectFAlign = recordRectF;
    g_drawXYWH = recordXYWH;
    WidgetWithPaintBounds painted;
    painted.expectedWidth = target.size();
    painted.show();
    app.processEvents();
    if (!painted.correct || paintedText != std::vector<QString>({target, target, target})) ++failures;
    paintedText.clear();
    QImage exported(200, 30, QImage::Format_ARGB32);
    QPainter exportedPainter(&exported);
    if (!exerciseBounds(&exportedPainter, source.size()) ||
        paintedText != std::vector<QString>({source, source, source})) ++failures;
    exportedPainter.end();
    // A known visible list view may use an image cache, without changing its model.
    CacheDelegateProbe original;
    ComboPaintDelegate cachedDelegate(&list, &original);
    list.show();
    QStyleOptionViewItem option;
    option.widget = list.viewport();
    QPainter cachePainter(&exported);
    cachedDelegate.paint(&cachePainter, option, list.model()->index(0, 0));
    if (original.displayed != target || list.item(0)->text() != source) ++failures;
    option.widget = nullptr;
    cachedDelegate.paint(&cachePainter, option, list.model()->index(0, 0));
    if (original.displayed != source) ++failures;
    cachePainter.end();
    std::printf("Widget draw/measure translation and export source boundary: %s\n", failures ? "FAIL" : "PASS");
    std::printf("Qt %s: %u widget import slots, source data retained, failures=%d\n",
        qVersion(), unsigned(g_uiMetricSlots.size()) + WidgetDisplayMetrics::patchedSlots, failures);
    return failures ? 1 : 0;
}
