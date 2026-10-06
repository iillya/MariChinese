"""Passed to Mari's official -x entry point; uses only host and Qt APIs."""
import ctypes
import json
import os
from pathlib import Path
import time
import traceback

from PySide2 import QtCore, QtWidgets

output = Path(os.environ["MARI_ACCEPTANCE_RESULT"])
result = {"qt": QtCore.qVersion(), "pid": os.getpid(), "checks": []}


def check(name, value):
    result["checks"].append({"name": name, "status": "PASS" if value else "FAIL"})
    if not value:
        raise AssertionError(name)


try:
    app = QtWidgets.QApplication.instance()
    check("host QApplication exists", app is not None)
    result["application"] = app.applicationName()
    result["home"] = QtCore.QDir.homePath()
    result["settings_file"] = QtCore.QSettings().fileName()
    dll = ctypes.WinDLL(os.environ["MARI_ACCEPTANCE_DLL"])
    check("production DLL LoadLibrary", dll._handle != 0)
    action = None
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and action is None:
        app.processEvents()
        for widget in app.topLevelWidgets():
            action = widget.findChild(QtWidgets.QAction, "mari_chinese_language")
            if action:
                break
        time.sleep(0.01)
    check("translation action on real host menu", action is not None)
    label = QtWidgets.QLabel("File")
    reference = QtWidgets.QLabel("文件")
    editable = QtWidgets.QLineEdit("File")
    original = (label.text(), editable.text())
    check("Chinese QLabel width matches native", label.sizeHint() == reference.sizeHint())
    chinese_width = label.sizeHint().width()
    action.trigger()
    app.processEvents()
    english_width = label.sizeHint().width()
    check("English toggle updates geometry", english_width != chinese_width)
    action.trigger()
    app.processEvents()
    check("Chinese toggle restores geometry", label.sizeHint().width() == chinese_width)
    check("original label and editable data retained", (label.text(), editable.text()) == original)
    result["widths"] = {"chinese": chinese_width, "english": english_width}
    result["status"] = "PASS"
except Exception:
    result["status"] = "FAIL"
    result["error"] = traceback.format_exc()
finally:
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("MARI_HOST_ACCEPTANCE=" + result["status"])
