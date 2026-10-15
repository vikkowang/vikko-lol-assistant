"""按住 = 键说话 → 本地识别 → DeepSeek → 悬浮窗显示答案。"""

import sys
import threading
import time

from pynput import keyboard
from PySide6.QtWidgets import QApplication

from settings import SettingsDialog
from ui import OverlayWindow

HOTKEY = keyboard.KeyCode.from_char("=")

recorder = None
recording = False
_lock = threading.Lock()
win = None


def _get_recorder():
    global recorder
    if recorder is None:
        from audio import Recorder
        recorder = Recorder()
    return recorder


def _process(audio):
    from asr import transcribe
    from llm import ask
    win.status.emit("识别中...")
    text = transcribe(audio)
    if not text:
        win.status.emit("没听清，再说一次")
        return
    win.question.emit(text)
    win.status.emit("回答中...")
    try:
        answer = ask(text)
    except Exception as e:
        win.status.emit(f"出错了：{e}")
        return
    win.answer.emit(answer)


def on_press(key):
    global recording
    if key == HOTKEY:
        with _lock:
            if not recording:
                recording = True
                win.expand()
                _get_recorder().start()
                win.status.emit("正在听，松开结束...")


def on_release(key):
    global recording
    if key == HOTKEY:
        with _lock:
            if not recording:
                return
            recording = False
            audio = _get_recorder().stop()
        if audio is None:
            win.status.emit("没录到声音")
            return
        threading.Thread(target=_process, args=(audio,), daemon=True).start()


def main():
    global win
    app = QApplication(sys.argv)
    win = OverlayWindow()
    win.show()
    win.open_settings.connect(lambda: SettingsDialog(win).exec())

    def _load_model():
        from asr import load_model
        win.status.emit("正在加载识别模型...")
        time.sleep(0.05)  # 给主线程一点时间先绘制窗口
        load_model()
        win.status.emit("就绪，按住 = 键说话")

    threading.Thread(target=_load_model, daemon=True).start()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
