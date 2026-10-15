# LoL 语音问答助手

合规的游戏外语音问答工具：按住热键说话，本地识别成文字，交给 DeepSeek 回答，答案显示在置顶悬浮窗里。

**不读游戏进程、不读内存、不识别屏幕，零封号风险。**

## 已定方案

| 维度 | 决定 |
|---|---|
| 性质 | 游戏外 LLM 语音问答 |
| 触发 | 全局热键 PTT，按住说话、松开结束 |
| 语音识别 | 本地 SenseVoice-small（sherpa-onnx，CPU int8） |
| 大模型 | DeepSeek `deepseek-chat`，用户自定义 key |
| 悬浮窗 | PySide6 置顶无边框窗口 |
| 交付 | PyInstaller 打包 exe（阶段 5，需在 Windows 上打包） |

## 落地阶段

1. ✅ 环境：装依赖、配 key
2. ✅ 最小链路：按住说话 → 本地识别 → DeepSeek → 控制台输出
3. ✅ 悬浮窗：PySide6 置顶窗口显示答案
4. ✅ 整合 + 状态反馈：录音中/识别中/回答中状态提示
5. ⬜ 打包：PyInstaller 打 Windows exe（需在 Windows 上做）

## 运行

```bash
python3 -m venv .venv && source .venv/bin/activate   # 建议用虚拟环境
pip install -r requirements.txt

cp config.example.json config.json   # 然后编辑 config.json 填入你的 DeepSeek api_key
python3 main.py
```

启动后弹出一个置顶悬浮窗，按住 `=` 键说话、松开出答案。悬浮窗可拖动、可点「置顶」切换、点「✕」退出。

语音识别模型 SenseVoice-small（约 228MB）需先下载到 `models/sensevoice/`（只需一次）。国内用 hf-mirror：

```bash
mkdir -p models/sensevoice
curl -L -o models/sensevoice/model.int8.onnx https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/resolve/main/model.int8.onnx
curl -L -o models/sensevoice/tokens.txt https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/resolve/main/tokens.txt
```

macOS 上需要给终端授权：
- **麦克风**权限（录音）
- **辅助功能**权限（pynput 全局监听键盘）

## 注意

- 游戏需开「无边框窗口模式（Borderless）」，悬浮窗才能浮在游戏上方（阶段 3 生效）。
- 最终 exe 必须在 Windows 机器上用 PyInstaller 打包，无法在 Mac 上交叉打包。
