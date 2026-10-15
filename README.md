# LoL 语音问答助手

合规的游戏外语音问答工具：按住热键说话，本地识别成文字，交给千问（Qwen）回答，答案显示在置顶悬浮窗里。

**不读游戏进程、不读内存、不识别屏幕，零封号风险。**

## 方案

| 维度 | 决定 |
|---|---|
| 性质 | 游戏外 LLM 语音问答 |
| 触发 | 全局热键 PTT，按住 `=` 说话、松开结束 |
| 语音识别 | 本地 SenseVoice-small（sherpa-onnx，CPU int8） |
| 大模型 | 阿里云百炼 千问 `qwen-plus`，支持联网搜索 |
| 悬浮窗 | PySide6 置顶无边框窗口，可拖动 / 置顶 / 收起 / 缩放 |
| 交付 | Inno Setup 安装程序 `installer/LOL-Setup.exe` |

## 功能

- 按住 `=` 说话 → 本地识别 → 展示识别文字 → 千问回答
- 联网搜索：问「版本 / 胜率 / 出装」等时效性问题时，优先用最新数据
- 设置界面：配置千问 API Key、systemPrompt、联网搜索开关
- 语音纠错：systemPrompt 让模型自动纠正识别错的英雄名 / 技能名等游戏术语

## 配置

- 首次运行自动生成 `config.json`，无需手动复制模板
- 也可点悬浮窗右上角「设置」按钮，在界面里填写
- 千问 API Key 获取地址：https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key
- 安装版：配置存 `%APPDATA%\LOL助手\config.json`
- 源码运行：配置在项目根目录 `config.json`

## 运行（源码）

```bash
# 装依赖（建议虚拟环境）
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 下载识别模型到 models/sensevoice/（只需一次）
mkdir -p models/sensevoice
curl -L -o models/sensevoice/model.int8.onnx https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/resolve/main/model.int8.onnx
curl -L -o models/sensevoice/tokens.txt https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/resolve/main/tokens.txt

# 启动
.venv\Scripts\python.exe main.py
```

## 打包（Windows，Inno Setup）

详见 `installer/lol-assistant.iss`。

```bash
# 1. 打包 onedir
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onedir --windowed --name lol-assistant --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineWidgets --exclude-module PySide6.QtWebEngine --exclude-module PySide6.QtPdf --exclude-module PySide6.QtPdfWidgets --exclude-module tkinter main.py

# 2. 模型放到打包产物里
cp -r models/sensevoice dist/lol-assistant/models/

# 3. 编译安装程序
"D:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer/lol-assistant.iss
# → installer/LOL-Setup.exe
```

## 注意

- 游戏需开「无边框窗口模式（Borderless）」，悬浮窗才能浮在游戏上方。
- 安装程序用 Inno Setup 生成，需在 Windows 上完成。
