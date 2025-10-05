# STT/elevenlabs_stt_handler.py
import logging
import os
from io import BytesIO
from time import perf_counter
from typing import Union

import numpy as np
from rich.console import Console
from baseHandler import BaseHandler

try:
    from elevenlabs.client import ElevenLabs
except Exception as e:
    raise ImportError("elevenlabs package not installed. Run `pip install elevenlabs`") from e

console = Console()
logger = logging.getLogger(__name__)

__all__ = ["ElevenLabsSTTHandler"]


class ElevenLabsSTTHandler(BaseHandler):
    """
    Speech-to-Text via ElevenLabs Scribe (remote service).

    setup(model_name="scribe_v1", device="cpu", compute_type="auto", gen_kwargs={})
    process(audio) -> yields transcript string
    cleanup()
    """

    def setup(
        self,
        model_name: str = "scribe_v1",
        device: str = "cpu",
        compute_type: str = "auto",
        gen_kwargs: dict = None,
    ):
        # Remote service: device/compute_type kept for API parity only
        self.model_id = model_name or "scribe_v1"
        self.gen_kwargs = self._default_gen_kwargs(gen_kwargs or {})

        api_key = self.gen_kwargs.pop("api_key", None) or os.getenv("ELEVENLABS_API_KEY")
        base_url = self.gen_kwargs.pop("base_url", "https://api.elevenlabs.io")
        if not api_key:
            logger.warning("ELEVENLABS_API_KEY not set; provide via env or gen_kwargs['api_key']")
        self.client = ElevenLabs(api_key=api_key, base_url=base_url)

    def process(self, audio: Union[bytes, bytearray, np.ndarray, str, BytesIO]):
        logger.debug("Inferring ElevenLabs STT...")
        pipeline_start = perf_counter()

        file_obj, file_format = self._to_filelike(audio)
        kwargs = dict(self.gen_kwargs)
        if file_format and "file_format" not in kwargs:
            kwargs["file_format"] = file_format  # e.g., "pcm_s16le_16"

        try:
            resp = self.client.speech_to_text.convert(
                file=file_obj,
                model_id=self.model_id,
                **kwargs,
            )
        finally:
            try:
                if isinstance(file_obj, BytesIO):
                    file_obj.close()
            except Exception:
                pass

        pred_text = (resp.get("text") or "").strip() if isinstance(resp, dict) else str(resp).strip()
        logger.debug("Finished ElevenLabs STT in %.3fs", perf_counter() - pipeline_start)

        if pred_text:
            console.print(f"[yellow]USER: {pred_text}")
            yield pred_text
        else:
            logger.debug("No text detected. Skipping...")

    def cleanup(self):
        logger.info("Stopping ElevenLabsSTTHandler")
        del self.client

    # ---------- helpers ----------
    def _default_gen_kwargs(self, g: dict) -> dict:
        g = dict(g)
        # Compat: if someone passed return_timestamps
        if "return_timestamps" in g and "timestamps_granularity" not in g:
            g["timestamps_granularity"] = "word" if g.pop("return_timestamps") else "none"

        g.setdefault("language_code", None)          # auto-detect
        g.setdefault("timestamps_granularity", "none")
        g.setdefault("diarize", False)
        g.setdefault("tag_audio_events", True)
        # Leave file_format unset unless raw PCM known; we’ll set it in process if ndarray/bytes
        return g

    def _to_filelike(self, audio):
        # Path
        if isinstance(audio, str) and os.path.exists(audio):
            return open(audio, "rb"), None

        # File-like
        if hasattr(audio, "read"):
            return audio, None

        # Raw bytes -> assume 16k PCM mono int16 unless told otherwise
        if isinstance(audio, (bytes, bytearray)):
            return BytesIO(audio), "pcm_s16le_16"

        # NumPy array -> to int16 PCM
        if isinstance(audio, np.ndarray):
            if audio.dtype != np.int16:
                if np.issubdtype(audio.dtype, np.floating):
                    a = np.clip(audio, -1.0, 1.0)
                    audio = (a * 32767.0).astype(np.int16)
                else:
                    audio = audio.astype(np.int16)
            return BytesIO(audio.tobytes()), "pcm_s16le_16"

        # Fallback
        return BytesIO(bytes(audio)), None
