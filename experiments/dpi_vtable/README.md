# Mari DPI vtable 独立实验

该目录与正式汉化代码完全隔离，不加载词典，也不安装样式、绘制、字体测量或数据 Hook。

## 当前行为

1. 启动器按 `Mari7.5v2_4K.bat` 设置 Qt 原生缩放：
   - `QT_ENABLE_HIGHDPI_SCALING=1`
   - `QT_AUTO_SCREEN_SCALE_FACTOR=1`
   - `QT_SCALE_FACTOR=2`
2. 仅对运行时类型为 `MriCanvasWidget` 的画布修改两个虚函数：
   - 画布 DPR 固定为 `1`；
   - `Ortho` 画布传给原始 `resizeGL` 的宽高乘以 `2`。
3. `metric` 与 `resizeGL` 的 vtable 下标均在运行时从 Qt 对象识别，不使用固定数字。
4. 新画布通过 Qt 生命周期事件注册，不再每秒遍历全部控件。

## 日志

实验每 2 秒把已登记画布的状态追加到 DLL 同目录的 `dpi_vtable_history.log`。日志达到 4 MiB 后轮换为 `.log.1`，最多保留两份。

## 构建与测试

运行 `build.bat`，输出位于 `build\dpi-experiment`。测试目标固定为：

`C:\Program Files\Mari7.1v1\Bundle\bin\Mari7.1v1.exe`

请勿把该实验 DLL 放入正式汉化安装包。
