# Project: Twilio Media Stream Echo Server (FastAPI)
# This version echoes back exactly what the user says, with no speech recognition.
# It records the Twilio audio stream to disk and streams it back in real time.
#
# Run with:
#   uvicorn twilio_media_stream_fastapi:app --host 0.0.0.0 --port 8000
# Use ngrok for tunneling (e.g. ngrok http 8000) and replace URLs accordingly.

import base64
import json
import asyncio
import wave
import audioop
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import Response

from dotenv import load_dotenv

load_dotenv()


try:
    import pyaudio

    pyaudio_available = True
except ImportError:
    pyaudio_available = False

app = FastAPI()

OUT_DIR = Path("recordings")
OUT_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 8000
SAMPLE_WIDTH = 2  # 16-bit PCM after conversion
CHANNELS = 1

connection_state: Dict[WebSocket, Dict[str, Any]] = {}


def mulaw_to_pcm(mulaw_data: bytes) -> bytes:
    """Convert mu-law encoded audio to 16-bit PCM."""
    return audioop.ulaw2lin(mulaw_data, SAMPLE_WIDTH)


def pcm_to_mulaw(pcm_data: bytes) -> bytes:
    """Convert 16-bit PCM audio to mu-law encoding."""
    return audioop.lin2ulaw(pcm_data, SAMPLE_WIDTH)


@app.websocket("/media")
async def media_ws(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")

    state: Dict[str, Any] = {
        "buffer": bytearray(),
        "wav_path": None,
        "wav_file": None,
        "sid": None,
        "pa_obj": None,
        "pa_stream": None,
    }
    connection_state[websocket] = state

    try:
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)
            event = data.get("event")

            if event == "start":
                call_sid = data.get("start", {}).get("callSid")
                state["sid"] = call_sid
                filename = f"call_{call_sid or 'unknown'}_{int(asyncio.get_event_loop().time() * 1000)}.wav"
                wav_path = OUT_DIR / filename
                state["wav_path"] = wav_path
                wf = wave.open(str(wav_path), "wb")
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(SAMPLE_WIDTH)
                wf.setframerate(SAMPLE_RATE)
                state["wav_file"] = wf
                print(f"Recording to {wav_path}")

            elif event == "media":
                payload_b64 = data.get("media", {}).get("payload")
                if not payload_b64:
                    continue

                # Decode base64 mu-law audio from Twilio
                mulaw_data = base64.b64decode(payload_b64)

                # Convert mu-law to PCM for processing
                pcm_data = mulaw_to_pcm(mulaw_data)

                # Save PCM data to WAV file
                wav_file = state.get("wav_file")
                if wav_file:
                    wav_file.writeframes(pcm_data)

                # Playback to system audio in real-time
                if pyaudio_available:
                    if state.get("pa_stream") is None:
                        import pyaudio

                        pa = pyaudio.PyAudio()
                        state["pa_obj"] = pa
                        stream = pa.open(
                            format=pa.get_format_from_width(SAMPLE_WIDTH),
                            channels=CHANNELS,
                            rate=SAMPLE_RATE,
                            output=True,
                        )
                        state["pa_stream"] = stream
                    else:
                        stream = state["pa_stream"]
                    stream.write(pcm_data)

                # Convert PCM back to mu-law for sending to Twilio
                echo_mulaw = pcm_to_mulaw(pcm_data)

                # Send the mu-law audio back to Twilio to echo
                await websocket.send_text(
                    json.dumps(
                        {
                            "event": "media",
                            "media": {
                                "payload": base64.b64encode(echo_mulaw).decode("utf-8")
                            },
                        }
                    )
                )

            elif event == "stop":
                wav_file = state.get("wav_file")
                if wav_file:
                    wav_file.close()
                print(f"Stopped recording {state.get('wav_path')}")
                await websocket.close()
                break

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        st = connection_state.pop(websocket, None)
        if st:
            if st.get("pa_stream"):
                try:
                    st["pa_stream"].stop_stream()
                    st["pa_stream"].close()
                    st["pa_obj"].terminate()
                except Exception:
                    pass
            if st.get("wav_file"):
                try:
                    st["wav_file"].close()
                except Exception:
                    pass


if __name__ == "__main__":
    print("Run with uvicorn twilio_media_stream_fastapi:app --host 0.0.0.0 --port 8000")
    print("Set TWILIO_STREAM_URL to your wss://<ngrok>/ws endpoint.")
