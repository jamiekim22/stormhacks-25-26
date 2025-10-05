import asyncio
import base64
import json
import logging
import threading
from queue import Queue
from typing import Optional, Any, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client  # type: ignore[import]
from twilio.twiml.voice_response import VoiceResponse  # type: ignore[import]
import uvicorn
from threading import Event

# numpy is not used; removed to satisfy linters
import audioop

logger = logging.getLogger(__name__)


class TwilioHandler:
    """
    Handles Twilio voice calls integration with the speech-to-speech pipeline.
    Receives audio from Twilio and sends audio back through Twilio's Media Streams.
    """

    def __init__(
        self,
        stop_event: Event,
        queue_in: Queue[bytes],
        queue_out: Queue[bytes],
        should_listen: Event,
        account_sid: str,
        auth_token: str,
        phone_number: str,
        port: int = 8000,
        user_number: Optional[str] = None,
        domain: Optional[str] = None,
    ):
        self.stop_event = stop_event
        self.queue_in: Queue[bytes] = queue_in  # Audio chunks from Twilio
        self.queue_out: Queue[bytes] = queue_out  # Audio chunks to send to Twilio
        self.should_listen = should_listen
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number
        self.port = port
        self.user_number = user_number
        self.twilio_domain = domain

        # Twilio client
        self.client = Client(account_sid, auth_token)

        # WebSocket connection for media streams
        self.websocket: Optional[WebSocket] = None
        self.media_stream_sid: Optional[str] = None

        # Active call tracking
        self.active_call_sid: Optional[str] = None

        # Audio format settings
        self.twilio_smaple_rate = 8_000  # Twilio uses 8kHz
        self.target_sample_rate = 16_000  # Pipeline expects 16kHz

        # Audio buffering - accumulate small Twilio chunks into larger chunks for VAD
        # VAD needs at least 512 samples (32 ms at 16 kHz) to work properly
        self.audio_buffer = b""
        self.min_chunk_size = 1_024  # butes = 512 samples at 16 kHz (32 ms)

        # FastAPI app for webhooks
        self.app = FastAPI()
        # CORS: allow any origin, methods, and headers
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.setup_routes()

        # Thread for running the FastAPI server
        self.server_thread: Optional[threading.Thread] = None

    def convert_twilio_audio_to_pipeline_format(self, audio_data: bytes) -> bytes:
        try:
            pcm_audio = audioop.ulaw2lin(audio_data, 2)  # 2 = 16-bit samples
            resampled_audio, _ = audioop.ratecv(
                pcm_audio,
                2,  # sample width (2 bytes = 16 bits)
                1,  # number of channels (mono)
                self.twilio_smaple_rate,  # input sample rate (8kHz)
                self.target_sample_rate,  # output sample rate (16kHz)
                None,  # state (None or first call)
            )
            return resampled_audio
        except Exception as e:
            logger.error(f"Error converting audio format: {e}")
            return b""

    def convert_pipeline_audio_to_twilio_format(self, audio_data: bytes) -> bytes:
        try:
            resampled_audio, _ = audioop.ratecv(
                audio_data,
                2,  # sample width (2 bytes = 16 bits)
                1,  # number of channels (mono)
                self.target_sample_rate,  # output sample rate (16kHz)
                self.twilio_smaple_rate,  # input sample rate (8kHz)
                None,  # state (None or first call)
            )
            mulaw_audio = audioop.lin2ulaw(resampled_audio, 2)
            return mulaw_audio
        except Exception as e:
            logger.error(f"Error converting audio to Twilio format: {e}")
            return b""

    def setup_routes(self):
        """Setup FastAPI routes for Twilio webhooks."""

        @self.app.post("/voice")
        async def handle_voice_call():
            """Handle incoming voice calls."""
            logger.info("Recieved incoming call webhook")
            response: Any = VoiceResponse()

            # Start media stream use wss for real-time webSocket connection
            connect: Any = response.connect()
            # Ensure the domain uses wss:// protocol for secure webSocket
            if self.twilio_domain:
                # Use domain as is if it alreadyy has wss://, otherwise add it
                stream_url = (
                    self.twilio_domain
                    if self.twilio_domain.startswith("wss://")
                    or self.twilio_domain.startswith("ws://")
                    else f"wss://{self.twilio_domain}"
                )
                stream_url = f"{stream_url}/stream"
            else:
                stream_url = f"ws://localhost:{self.port}/stream"

            connect.stream(url=stream_url)
            logger.info(
                f"Responding with TwiML to connect to WebSocket stream: {stream_url}"
            )

            from starlette.responses import Response

            return Response(content=str(response), media_type="application/xml")

        @self.app.post("/call")
        async def start_outbound_call(request_data: Dict[str, Any]):
            """Start an outbound call to the provided phone number.

            Expected JSON body: {"phone": "+1XXXXXXXXXX"}
            """
            try:
                phone = request_data.get("phone")
                if not phone:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Missing 'phone' in request body"},
                    )

                # Trigger outbound call
                self.initiate_call(to_number=phone)
                return JSONResponse(content={"status": "initiated", "to": phone})
            except Exception as e:
                logger.error(f"Failed to start outbound call: {e}")
                return JSONResponse(
                    status_code=500, content={"error": "Failed to initiate call"}
                )

        @self.app.post("/stream")
        async def handle_media_stream(request_data: Dict[str, Any]):
            """Handle media stream events."""
            event_type = request_data.get("event")

            if event_type == "start":
                self.media_stream_sid = request_data.get("streamSid")
                logger.info(f"Media stream started: {self.media_stream_sid}")
                self.should_listen.set()

            elif event_type == "media":
                # Decode and queue incoming audio
                media_payload = request_data.get("media", {}).get("payload")
                if media_payload:
                    audio_data = base64.b64decode(media_payload)
                    self.queue_in.put(audio_data)

            elif event_type == "stop":
                logger.info("Media stream stopped")
                self.stop_event.set()

            return JSONResponse(content="OK")

        @self.app.websocket("/stream")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for bidirectional media streaming."""
            await websocket.accept()
            self.websocket = websocket
            logger.info("WebSocket connection established")

            try:
                # Start sending audio from queue
                asyncio.create_task(self.send_audio_to_twilio())

                # Listen for incoming messages
                while not self.stop_event.is_set():
                    try:
                        data = await websocket.receive_text()
                        message = json.loads(data)

                        event_type = message.get("event")
                        logger.debug(f"Recieve WebSocket event: {event_type}")

                        if event_type == "start":
                            self.media_stream_sid = message.get("streamSid")
                            logger.info(
                                f"Media stream started: {self.media_stream_sid}"
                            )
                            self.should_listen.set()

                        elif event_type == "media":
                            # Handle incoming audio
                            payload = message.get("media", {}).get("payload")
                            if payload:
                                # decode from base64
                                audio_data = base64.b64decode(payload)
                                converted_audio = (
                                    self.convert_twilio_audio_to_pipeline_format(
                                        audio_data
                                    )
                                )
                                if converted_audio:
                                    self.audio_buffer += converted_audio
                                    while len(self.audio_buffer) >= self.min_chunk_size:
                                        chunk = self.audio_buffer[: self.min_chunk_size]
                                        self.audio_buffer = self.audio_buffer[
                                            self.min_chunk_size :
                                        ]
                                        self.queue_in.put(chunk)
                                        logger.debug(
                                            f"Sent {len(chunk)} bytes to VAD queue"
                                        )

                        elif event_type == "stop":
                            logger.info("Media stream stopped by Twilio")
                            break

                    except WebSocketDisconnect:
                        logger.info("WebSocket disconnected")
                        break
                    except Exception as e:
                        logger.error(f"WebSocket error: {e}")

            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")
            finally:
                self.websocket = None
                logger.info("WebSocket connection closed")

        # Prevent linters from flagging unused local endpoint functions
        _ = (
            handle_voice_call,
            start_outbound_call,
            handle_media_stream,
            websocket_endpoint,
        )

    async def send_audio_to_twilio(self):
        """Send audio from queue to Twilio via WebSocket."""
        while not self.stop_event.is_set() and self.websocket:
            try:
                # Check if there's an audio chunk to send
                if not self.queue_out.empty():
                    audio_chunk: bytes = self.queue_out.get(timeout=0.1)

                    converted_audio = self.convert_pipeline_audio_to_twilio_format(
                        audio_chunk
                    )

                    if converted_audio:
                        # Encode audio as base64
                        audio_b64 = base64.b64encode(converted_audio).decode("utf-8")

                        # Send to Twilio
                        message = {
                            "event": "media",
                            "streamSid": self.media_stream_sid,
                            "media": {"payload": audio_b64},
                        }

                        await self.websocket.send_text(json.dumps(message))
                        logger.debug(
                            f"Sent {len(audio_chunk)} bytes -> {len(converted_audio)} bytes to Twilio"
                        )
                else:
                    await asyncio.sleep(0.01)

            except Exception as e:
                logger.error(f"Error sending audio to Twilio: {e}")
                # Small delay on error to prevent rapid0fire error logging
                await asyncio.sleep(0.1)

    def start_server(self):
        """Start the FastAPI server in a separate thread."""

        def run_server():
            uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        logger.info(f"Twilio webhook server started on port {self.port}")

    def initiate_call(self, to_number: Optional[str] = None):
        """Initiate a call to the provided number (or the configured user number)."""
        target_number = to_number or self.user_number
        if not target_number:
            logger.warning(
                "No target number provided. Supply 'phone' in POST /call or set 'twilio_user_number' in config."
            )
            return

        try:
            logger.info(f"Initiating call to {target_number}...")

            # outbound_twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Connect><Stream url="wss://{self.twilio_domain}/stream" /></Connect></Response>'
            # f'<Response><Connect><Stream url="wss://{self.twilio_domain}/voice" /></Connect></Response>'

            # Use ngrok or your domain for webhooks
            webhook_url = (
                f"{self.twilio_domain.replace('wss://', 'https://').replace('ws://', 'http://')}/voice"
                if self.twilio_domain
                else f"http://localhost:{self.port}/voice"
            )

            call = self.client.calls.create(
                from_=self.phone_number,
                to=target_number,
                url=webhook_url,
                method="POST",
            )

            # Store the call SID for later termination
            self.active_call_sid = call.sid

            logger.info(f"Call initiated! SID: {call.sid}")
            logger.info("Answer the call to start the conversation!")

        except Exception as e:
            logger.error(f"Failed to initiate call: {e}")
            logger.info("Make sure to:")
            logger.info("1. Set your personal number in the config")
            logger.info("2. Configure your domain for webhooks")
            logger.info("3. Or manually call your Twilio number")

    def terminate_call(self):
        """Terminate the active Twilio call."""
        if not self.active_call_sid:
            logger.warning("No active call to terminate")
            return

        try:
            # Update the call status to 'completed' to hang up
            call = self.client.calls(self.active_call_sid).update(status="completed")
            logger.info(f"Call terminated successfully. SID: {self.active_call_sid}")
            self.active_call_sid = None

            # Set stop event to end the pipeline
            self.stop_event.set()

        except Exception as e:
            logger.error(f"Failed to terminate call: {e}")

    def run(self):
        """Main run method for the Twilio handler."""
        logger.info("Starting Twilio handler...")

        # Start the webhook server
        self.start_server()

        # Wait a moment for server to start
        import time

        time.sleep(2)

        # Wait for stop event
        while not self.stop_event.is_set():
            self.stop_event.wait(1)

        # Terminate the call when stop event is set
        if self.active_call_sid:
            logger.info("Stop event detected, terminating call...")
            self.terminate_call()

        logger.info("Twilio handler stopped")

    def stop(self):
        """Stop the Twilio handler."""
        self.stop_event.set()
        if self.websocket:
            asyncio.create_task(self.websocket.close())
        logger.info("Twilio handler stopped")
