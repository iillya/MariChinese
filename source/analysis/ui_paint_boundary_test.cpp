#include "../ui_paint_boundary.h"

#include <QtGui/QImage>
#include <QtGui/QPicture>
#include <QtGui/QPixmap>
#include <QtWidgets/QApplication>

class WidgetPaintDevice final : public QPaintDevice {
public:
    int devType() const override { return QInternal::Widget; }
    QPaintEngine *paintEngine() const override { return nullptr; }
};

int main(int argc, char** argv) {
    QApplication app(argc, argv);
    QWidget owner;
    owner.show();
    WidgetPaintDevice widget;
    QImage image(32, 32, QImage::Format_ARGB32);
    QPicture picture;
    const QString source = QStringLiteral("File");
    int lookups = 0;
    auto translate = [&lookups](const QString &) {
        ++lookups;
        return QStringLiteral("文件");
    };

    if (!MariUiPaintBoundary::IsWidgetPaintDevice(&widget) ||
        MariUiPaintBoundary::IsWidgetPaintDevice(&image) ||
        MariUiPaintBoundary::IsWidgetPaintDevice(&picture) ||
        MariUiPaintBoundary::IsWidgetPaintDevice(nullptr) ||
        MariUiPaintBoundary::IsWidgetPainter(nullptr))
        return 1;

    if (MariUiPaintBoundary::DisplayTextForDevice(&image, source, translate) != source ||
        MariUiPaintBoundary::DisplayTextForDevice(&picture, source, translate) != source ||
        lookups != 0)
        return 4;
    if (MariUiPaintBoundary::DisplayTextForDevice(&widget, source, translate) !=
            QStringLiteral("文件") || lookups != 1)
        return 5;

    QPainter imagePainter(&image);
    if (!imagePainter.isActive() ||
        MariUiPaintBoundary::IsWidgetPainter(&imagePainter))
        return 2;
    imagePainter.end();

    QPainter picturePainter(&picture);
    if (!picturePainter.isActive() ||
        MariUiPaintBoundary::IsWidgetPainter(&picturePainter))
        return 3;
    picturePainter.end();
    QPixmap cache(32, 32);
    {
        QPainter cachePainter(&image);
        MariUiPaintBoundary::WidgetPaintScope scope(&cachePainter, &owner);
        if (MariUiPaintBoundary::DisplayTextForDevice(&image, source, translate) !=
                QStringLiteral("文件") ||
            MariUiPaintBoundary::DisplayTextForDevice(&cache, source, translate) != source ||
            MariUiPaintBoundary::DisplayTextForDevice(&picture, source, translate) != source)
            return 6;
    }
    if (MariUiPaintBoundary::DisplayTextForDevice(&image, source, translate) != source)
        return 7;
    owner.hide();
    {
        QPainter cachePainter(&image);
        MariUiPaintBoundary::WidgetPaintScope scope(&cachePainter, &owner);
        if (MariUiPaintBoundary::DisplayTextForDevice(&image, source, translate) != source)
            return 8;
    }
    return 0;
}
