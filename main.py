"""按住 = 键说话 → 本地识别 → DeepSeek → 悬浮窗显示答案。"""

import sys
import threading

from pynput import keyboard
from PySide6.QtWidgets import QApplication

from audio import Recorder
from asr import load_model, transcribe
from llm import ask
from ui import OverlayWindow

HOTKEY = keyboard.KeyCode.from_char("=")

recorder = Recorder()
recording = False
_lock = threading.Lock()
win = None


def _process(audio):
    win.status.emit("识别中...")
    text = transcribe(audio)
    if not text:
        win.status.emit("没听清，再说一次")
        return
    win.status.emit("回答中...")
    answer = ask(text)
    win.answer.emit(text, answer)


def on_press(key):
    global recording
    if key == HOTKEY:
        with _lock:
            if not recording:
                recording = True
                win.expand()
                recorder.start()
                win.status.emit("正在听，松开结束...")


def on_release(key):
    global recording
    if key == HOTKEY:
        with _lock:
            if not recording:
                return
            recording = False
            audio = recorder.stop()
        if audio is None:
            win.status.emit("没录到声音")
            return
        threading.Thread(target=_process, args=(audio,), daemon=True).start()


def main():
    global win
    app = QApplication(sys.argv)
    win = OverlayWindow()
    win.show()

    def _load_model():
        win.status.emit("正在加载识别模型...")
        load_model()
        win.status.emit("就绪，按住 = 键说话")

    threading.Thread(target=_load_model, daemon=True).start()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
