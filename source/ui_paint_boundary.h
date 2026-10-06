#pragma once

#include <QtGui/QPaintDevice>
#include <QtGui/QPainter>
#include <QtCore/QString>
#include <QtWidgets/QWidget>

namespace MariUiPaintBoundary {

// QPainter images can be either display caches or exported data. Only a known
// visible widget callback permits a temporary image/pixmap to display Chinese.
inline const QPaintDevice*& displayCacheDevice() {
    static thread_local const QPaintDevice* device = nullptr;
    return device;
}

class WidgetPaintScope final {
public:
    WidgetPaintScope(const QPainter* painter, const QWidget* widget = nullptr)
        : previous_(displayCacheDevice()) {
        const auto* device = painter ? painter->device() : nullptr;
        if ((device && device->devType() == QInternal::Widget) ||
            (widget && widget->isVisible()))
            displayCacheDevice() = device;
        else if (device != previous_)
            displayCacheDevice() = nullptr;
    }
    ~WidgetPaintScope() { displayCacheDevice() = previous_; }
    WidgetPaintScope(const WidgetPaintScope&) = delete;
    WidgetPaintScope& operator=(const WidgetPaintScope&) = delete;
private:
    const QPaintDevice* previous_;
};

inline bool IsWidgetPaintDevice(const QPaintDevice *device) {
    return device && device->devType() == QInternal::Widget;
}

inline bool IsWidgetPainter(const QPainter *painter) {
    return painter && IsWidgetPaintDevice(painter->device());
}

inline bool IsDisplayPaintDevice(const QPaintDevice* device) {
    if (IsWidgetPaintDevice(device)) return true;
    if (!device || device != displayCacheDevice()) return false;
    return device->devType() == QInternal::Image || device->devType() == QInternal::Pixmap;
}

inline bool IsDisplayPainter(const QPainter* painter) {
    return painter && IsDisplayPaintDevice(painter->device());
}

template <typename Lookup>
QString DisplayTextForDevice(const QPaintDevice *device, const QString &source,
                             Lookup lookup) {
    if (!IsDisplayPaintDevice(device))
        return source;
    const QString display = lookup(source);
    return display.isEmpty() ? source : display;
}

} // namespace MariUiPaintBoundary
