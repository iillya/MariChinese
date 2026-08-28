#pragma once

class QApplication;

// Installs the DPI-only canvas hooks on the QApplication GUI thread.
// Logging is enabled only by the standalone experiment build.
void StartMariDpiFeature(QApplication *app, double scaleFactor,
                         bool enableDiagnostics);
