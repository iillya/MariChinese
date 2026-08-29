#pragma once

class QApplication;

namespace MariDpiHook {

bool Enabled();
void Initialize(QApplication *application);

} // namespace MariDpiHook
