# Mari DPI vtable 独立实验

此实验不包含任何汉化功能，只做两件事：

1. 按 `Mari7.5v2_4K.bat` 设置 Qt 原生缩放环境变量；
2. 仅让 `QOpenGLWidget` 视口返回 DPR=1，避免 Qt 创建 2 倍 FBO、而 Mari 仍按逻辑像素渲染，导致内容缩在左下角。

当前按视图实验：UV、Perspective、Ortho/UV 和 2D 使用 DPR=1。Ortho 的 0.5 仅保留为 Qt 下限验证，实际会被限制为 DPR=1。

测试目标固定为 `C:\Program Files\Mari7.1v1\Bundle\bin\Mari7.1v1.exe`。

实验状态每 2 秒追加记录到 `dpi_vtable_history.log`。
