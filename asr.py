"""本地语音识别：SenseVoice-small（sherpa-onnx，CPU）。"""

import threading
from pathlib import Path

import sherpa_onnx

MODEL_DIR = Path(__file__).parent / "models" / "sensevoice"
SAMPLE_RATE = 16000

_recognizer = None
_lock = threading.Lock()


def load_model():
    global _recognizer
    with _lock:
        if _recognizer is None:
            _recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
                model=str(MODEL_DIR / "model.int8.onnx"),
                tokens=str(MODEL_DIR / "tokens.txt"),
                num_threads=4,
                use_itn=True,
                language="zh",
            )
    return _recognizer


def transcribe(audio) -> str:
    recognizer = load_model()
    stream = recognizer.create_stream()
    stream.accept_waveform(SAMPLE_RATE, audio)
    recognizer.decode_stream(stream)
    return stream.result.text.strip()
