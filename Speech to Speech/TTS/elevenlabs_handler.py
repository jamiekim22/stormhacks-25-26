# elevenlabs_handler.py
import os
import logging
import numpy as np
from typing import Tuple, Union, Dict, Any
from rich.console import Console
from baseHandler import BaseHandler

from elevenlabs.client import ElevenLabs  # pip install elevenlabs

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
console = Console()


class ElevenLabsTTSHandler(BaseHandler):
    """
    Drop-in replacement for ChatTTSHandler that uses ElevenLabs TTS.

    - Streams PCM 16 kHz (S16LE) audio so no resampling needed.
    - Yields fixed-size np.int16 chunks of length `chunk_size`.
    - Supports streaming and non-streaming modes, like your original.

    Config via gen_kwargs:
      - api_key (str, optional)         : falls back to ELEVENLABS_API_KEY env
      - base_url (str, optional)        : default "https://api.elevenlabs.io"
      - voice_id (str, optional)        : default from ELEVENLABS_VOICE_ID or a public voice
      - model_id (str, optional)        : default "eleven_multilingual_v2"
      - output_format (str, optional)   : default "pcm_16000"
      - warmup_text (str, optional)     : small text to preflight the API (None to skip)
    """

    def setup(
        self,
        should_listen,
        device="cpu",  # device is irrelevant for remote TTS, kept for API parity
        gen_kwargs=None,
        stream=True,
        chunk_size=512,
    ):
        self.should_listen = should_listen
        self.device = device
        self.stream = stream
        self.chunk_size = int(chunk_size)

        gen_kwargs = gen_kwargs or {}
        api_key = gen_kwargs.get("api_key") or os.getenv("ELEVENLABS_API_KEY") or ""
        base_url = gen_kwargs.get("base_url", "https://api.elevenlabs.io")
        self.voice_id = (
            gen_kwargs.get("voice_id")
            or os.getenv("ELEVENLABS_VOICE_ID")
            or "JBFqnCBsd6RMkjVDRZzb"
        )
        self.model_id = gen_kwargs.get("model_id", "eleven_multilingual_v2")
        # IMPORTANT: request raw PCM 16k so we can yield int16 frames directly
        self.output_format = gen_kwargs.get("output_format", "pcm_16000")
        self.warmup_text = gen_kwargs.get("warmup_text", None)

        self.client = ElevenLabs(api_key=api_key, base_url=base_url)
        self.warmup()

    def warmup(self):
        """Optional tiny request to ensure credentials/network are good."""
        if not self.warmup_text:
            logger.info(f"Skipping warmup for {self.__class__.__name__}")
            return
        try:
            logger.info(f"Warming up {self.__class__.__name__}")
            # Non-streaming convert avoids keeping a stream open during warmup.
            _ = self.client.text_to_speech.convert(
                text=self.warmup_text,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format=self.output_format,  # "pcm_16000"
            )
        except Exception as e:
            logger.warning(f"ElevenLabs warmup failed: {e}")

    def _yield_pcm_chunks(self, pcm_bytes: bytes):
        """Convert raw little-endian PCM bytes to int16 and yield fixed-size frames."""
        # Ensure even number of bytes (2 bytes per sample)
        if len(pcm_bytes) % 2:
            pcm_bytes += b"\x00"
        samples = np.frombuffer(pcm_bytes, dtype="<i2")  # little-endian int16
        for i in range(0, len(samples), self.chunk_size):
            frame = samples[i : i + self.chunk_size]
            if len(frame) < self.chunk_size:
                yield np.pad(frame, (0, self.chunk_size - len(frame)))
            else:
                yield frame

    @staticmethod
    def _normalize_text(x: Any) -> Tuple[str, str]:
        """
        Accepts:
          - string
          - (text, lang) tuple/list
          - {"text": "...", "lang": "en"} dict
        Returns: (text, lang)
        """
        if isinstance(x, (tuple, list)) and x:
            text = x[0] if len(x) > 0 else ""
            lang = x[1] if len(x) > 1 else "en"
            return str(text), str(lang or "en")
        if isinstance(x, dict):
            text = x.get("text", "")
            lang = x.get("lang", "en")
            return str(text), str(lang or "en")
        return str(x), "en"

    def _voice_for_lang(self, lang: str) -> str:
        """
        Optional hook: map language -> voice_id if you want different voices per locale.
        For now, just return the configured voice.
        """
        return self.voice_id

    def _send_to_api(self, json_data):
        """Send JSON data to the API endpoint."""
        try:
            import requests

            # API endpoint
            api_url = "http://localhost:8001/api/security-assessments"

            # Send POST request
            response = requests.post(
                api_url,
                json=json_data,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code == 200 or response.status_code == 201:
                console.print(
                    f"[green]JSON data sent to API successfully: {response.status_code}"
                )
                logger.info(f"API request successful: {response.status_code}")
            else:
                console.print(
                    f"[yellow]API request failed: {response.status_code} - {response.text}"
                )
                logger.warning(
                    f"API request failed: {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error sending to API: {e}")
            logger.error(f"Failed to send to API: {e}")
        except Exception as e:
            console.print(f"[red]Unexpected error sending to API: {e}")
            logger.error(f"Unexpected error sending to API: {e}")

    def _save_json_to_file(self, json_text):
        """Save JSON output to a file."""
        try:
            import json
            from datetime import datetime

            # Try to complete incomplete JSON
            if not json_text.strip().endswith("}"):
                # Add missing closing brace and any incomplete fields
                json_text = json_text.strip()
                if not json_text.endswith('"'):
                    json_text += '"'
                json_text += "}"

            # Parse the JSON to validate it
            json_data = json.loads(json_text)

            # Add timestamp
            json_data["timestamp"] = datetime.now().isoformat()

            # Save to file
            filename = (
                f"security_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            console.print(f"[green]JSON analysis saved to: {filename}")
            logger.info(f"Security analysis saved to {filename}")

            # Send POST request to API endpoint
            self._send_to_api(json_data)

        except json.JSONDecodeError as e:
            console.print(f"[yellow]Invalid JSON received, saving as text: {e}")
            # Save as text file if JSON is invalid
            filename = (
                f"security_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(json_text)
            console.print(f"[green]Analysis saved as text to: {filename}")
        except Exception as e:
            console.print(f"[red]Error saving JSON: {e}")
            logger.error(f"Failed to save JSON: {e}")

    def process(self, llm_sentence):
        # Normalize first so we don't print tuple/list/dict representations
        text, lang = self._normalize_text(llm_sentence)
        console.print(f"[green]ASSISTANT: {text}")

        # Check for END CALL trigger
        if '["END CALL"]' in text or '["END CALL"]' in str(llm_sentence):
            console.print("[red]END CALL detected! Terminating call...")

            # Check if JSON is in the same response (even if incomplete)
            if "{" in text:
                # Extract JSON from the response (even if incomplete)
                start_idx = text.find("{")
                json_part = text[start_idx:]
                if json_part.strip():
                    self._save_json_to_file(json_part)

            # Trigger call termination by setting stop event
            self.stop_event.set()
            return

        # Check if this is JSON output (after END CALL)
        if text.strip().startswith("{") and text.strip().endswith("}"):
            self._save_json_to_file(text)
            # Now terminate the call after JSON is saved
            console.print("[red]JSON saved! Terminating call...")
            self.stop_event.set()
            return
        voice_id = self._voice_for_lang(lang)

        if self.stream:
            # Stream raw bytes as they’re generated by ElevenLabs
            # We request output_format="pcm_16000" so chunks are already raw PCM at 16k.
            audio_stream = self.client.text_to_speech.stream(
                text=text,
                voice_id=voice_id,
                model_id=self.model_id,
                output_format=self.output_format,  # "pcm_16000"
            )

            remainder = b""
            try:
                for chunk in audio_stream:
                    # SDK yields bytes (audio) and sometimes other events; keep only bytes.
                    if not isinstance(chunk, (bytes, bytearray)):
                        continue
                    data = remainder + bytes(chunk)
                    # keep even number of bytes; convert what we can, stash the rest
                    usable_len = (len(data) // 2) * 2
                    if usable_len:
                        yield from self._yield_pcm_chunks(data[:usable_len])
                    remainder = data[usable_len:]
            finally:
                # Flush any tail bytes
                if remainder:
                    yield from self._yield_pcm_chunks(remainder)
                self.should_listen.set()
        else:
            # One-shot generation; returns the full audio buffer
            audio_bytes = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=self.model_id,
                output_format=self.output_format,  # "pcm_16000"
            )
            yield from self._yield_pcm_chunks(bytes(audio_bytes))
            self.should_listen.set()
