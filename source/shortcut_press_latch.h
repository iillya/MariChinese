#pragma once

// Deduplicates one physical shortcut press across Mari's native Windows and
// Qt event paths. Some Mari controls forward the same press through both paths
// and do not consistently mark every repeated Qt event as auto-repeat.
class ShortcutPressLatch final {
public:
    bool begin(int key, bool autoRepeat) noexcept {
        if (key == heldKey_ || autoRepeat) return false;
        heldKey_ = key;
        return true;
    }

    bool end(int key) noexcept {
        if (key != heldKey_) return false;
        heldKey_ = 0;
        return true;
    }

    bool holds(int key) const noexcept { return key == heldKey_; }
    void reset() noexcept { heldKey_ = 0; }

private:
    int heldKey_ = 0;
};
