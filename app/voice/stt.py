import os
import tempfile
from faster_whisper import WhisperModel


class STTEngine:
    def __init__(self, model_size: str = "base"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe_bytes(self, audio_bytes: bytes, suffix: str = ".wav") -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            segments, _ = self.model.transcribe(tmp_path, beam_size=5)
            return " ".join(seg.text.strip() for seg in segments).strip()
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
