"""麦克风录音：按住开始、松开停止，返回 16kHz 单声道 float32 音频。"""

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000


class Recorder:
    def __init__(self, samplerate: int = SAMPLE_RATE):
        self.samplerate = samplerate
        self._chunks = []
        self._stream = None

    def _callback(self, indata, frames, time, status):
        self._chunks.append(indata.copy())

    def start(self):
        self._chunks = []
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray | None:
        if self._stream is None:
            return None
        self._stream.stop()
        self._stream.close()
        self._stream = None
        if not self._chunks:
            return None
        return np.concatenate(self._chunks, axis=0).flatten()
