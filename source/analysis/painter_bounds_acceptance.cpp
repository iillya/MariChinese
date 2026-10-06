// Real release-DLL / QPainter comparison. Synthetic QWidget frames stay in memory.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtGui/QImage>
#include <QtGui/QPainter>
#include <QtCore/QFile>
#include <QtCore/QFileInfo>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QElapsedTimer>
#include <QtCore/QStandardPaths>
#include <cstdio>
#include <vector>

#define CHECK(x) do { if (!(x)) { std::fprintf(stderr, "FAIL %d: %s\n", __LINE__, #x); return 1; } } while(false)

struct PaintCase {
    int overload = 0;
    int pixels = 18;
    qreal dpr = 1, scale = 1;
    bool wrapped = false, clipped = false;
    QString family;
};
static QRectF drawText(QPainter& painter, const PaintCase& test, const QString& text) {
    const QRect area(15, 12, test.wrapped ? 110 : 245, 160);
    const int flags = Qt::AlignLeft | Qt::AlignTop | (test.wrapped ? Qt::TextWordWrap : Qt::TextSingleLine);
    QRect bounds;
    QRectF boundsF;
    switch (test.overload) {
    case 0: painter.drawText(area, flags, text, &bounds); return bounds;
    case 1: painter.drawText(QRectF(area), flags, text, &boundsF); return boundsF;
    default: painter.drawText(area.x(), area.y(), area.width(), area.height(), flags, text, &bounds); return bounds;
    }
}
static void configure(QPainter& painter, const PaintCase& test) {
    QFont font(test.family); font.setPixelSize(test.pixels);
    painter.setFont(font);
    painter.setPen(QColor(212, 223, 237));
    painter.scale(test.scale, test.scale);
    if (test.clipped) painter.setClipRect(QRect(20, 18, 102, 90));
}
static QImage imageFor(const PaintCase& test) {
    QImage image(int(300 * test.dpr), int(220 * test.dpr), QImage::Format_ARGB32_Premultiplied);
    image.setDevicePixelRatio(test.dpr);
    image.fill(QColor(34, 39, 44));
    return image;
}
class PaintWidget final : public QWidget {
public:
    PaintCase test;
    QString source;
    QRectF bounds;
    bool widgetDevice = false;
    PaintWidget() { resize(300, 220); setAutoFillBackground(false); }
    QImage frame() {
        QImage image = imageFor(test);
        render(&image, QPoint(), QRegion(), QWidget::DrawChildren);
        return image;
    }
protected:
    void paintEvent(QPaintEvent*) override {
        QPainter painter(this);
        widgetDevice = painter.device()->devType() == QInternal::Widget;
        painter.fillRect(rect(), QColor(34, 39, 44));
        configure(painter, test);
        bounds = drawText(painter, test, source);
    }
};
static QImage exportFrame(const PaintCase& test, const QString& text, QRectF* bounds) {
    QImage image = imageFor(test);
    QPainter painter(&image);
    configure(painter, test);
    *bounds = drawText(painter, test, text);
    return image;
}
static bool nonblank(const QImage& image) {
    const QRgb background = qRgb(34, 39, 44);
    for (int y = 0; y < image.height(); ++y)
        for (int x = 0; x < image.width(); ++x)
            if (image.pixel(x,y) != background) return true;
    return false;
}
int main(int argc, char** argv) {
    QStandardPaths::setTestModeEnabled(true);
    QApplication app(argc, argv);
    CHECK(argc == 2);
    const QFileInfo hook(QString::fromLocal8Bit(argv[1]));
    QFile dict(hook.absolutePath() + QStringLiteral("/translations/dictionary_zh.json"));
    CHECK(dict.open(QIODevice::ReadOnly));
    const QJsonObject entries = QJsonDocument::fromJson(dict.readAll()).object().value(QStringLiteral("translations")).toObject();
    const QString source = QStringLiteral("Add Material specific Tags which can be used for filtering and organizing the Mari Shelf.");
    const QString target = entries.value(source).toString();
    CHECK(!target.isEmpty() && target != source);
    std::vector<PaintCase> cases;
    for (int overload = 0; overload < 3; ++overload)
      for (int size : {12, 18, 28})
       for (qreal dpr : {1.0, 2.0})
        for (qreal scale : {1.0, 1.5})
         for (bool wrap : {false, true})
          for (bool clip : {false, true})
           for (const QString& font : {QStringLiteral("Segoe UI"), QStringLiteral("Microsoft YaHei")})
             cases.push_back({overload,size,dpr,scale,wrap,clip,font});
    std::vector<QImage> originalExport;
    std::vector<QRectF> originalBounds;
    for (const auto& test : cases) {
        QRectF bounds;
        originalExport.push_back(exportFrame(test, source, &bounds));
        originalBounds.push_back(bounds);
    }
    QMainWindow window;
    window.menuBar()->addAction(QStringLiteral("File"));
    window.menuBar()->addAction(QStringLiteral("Help"));
    window.show();
    HMODULE module = LoadLibraryW(hook.absoluteFilePath().toStdWString().c_str());
    CHECK(module);
    QElapsedTimer timer; timer.start();
    while (!window.findChild<QAction*>(QStringLiteral("mari_chinese_language")) && timer.elapsed() < 5000) {
        app.processEvents(); Sleep(5);
    }
    CHECK(window.findChild<QAction*>(QStringLiteral("mari_chinese_language")));
    PaintWidget translated, native;
    translated.source = source; native.source = target;
    translated.show(); native.show();
    int failures = 0;
    for (size_t i = 0; i < cases.size(); ++i) {
        translated.test = native.test = cases[i];
        const QImage actual = translated.frame(), expected = native.frame();
        QRectF exportBounds;
        const QImage exportActual = exportFrame(cases[i],source,&exportBounds);
        const bool ok = actual == expected && translated.bounds == native.bounds && nonblank(expected) &&
            translated.widgetDevice && native.widgetDevice && translated.source == source &&
            exportActual == originalExport[i] && exportBounds == originalBounds[i];
        if (!ok) {
            ++failures;
            std::fprintf(stderr,"FAIL case %zu overload=%d font=%s pixels=%d dpr=%.1f scale=%.1f wrap=%d clip=%d pixelsEqual=%d boundsEqual=%d exportEqual=%d\n",
                i,cases[i].overload,qPrintable(cases[i].family),cases[i].pixels,cases[i].dpr,cases[i].scale,
                int(cases[i].wrapped),int(cases[i].clipped),int(actual==expected),int(translated.bounds==native.bounds),int(exportActual==originalExport[i]));
        }
    }
    std::printf("%s Qt %s: real release DLL, %zu QPainter CN/native pixel+boundingRect comparisons, export originals retained; failures=%d\n",
        failures ? "FAIL" : "PASS", qVersion(),cases.size(),failures);
    return failures ? 1 : 0;
}

