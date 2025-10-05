from dataclasses import dataclass, field

@dataclass
class ElevenLabsTTSHandlerArguments:
    # Base params
    elevenlabs_tts_device: str = field(default="cpu")  # ignored by remote service
    elevenlabs_tts_stream: bool = field(default=True)
    elevenlabs_tts_chunk_size: int = field(default=1024)

    # gen_kwargs
    elevenlabs_tts_gen_voice_id: str = field(default="JBFqnCBsd6RMkjVDRZzb")
    elevenlabs_tts_gen_model_id: str = field(default="eleven_multilingual_v2")
    elevenlabs_tts_gen_output_format: str = field(default="pcm_16000")
    elevenlabs_tts_gen_base_url: str = field(default="https://api.elevenlabs.io")
    elevenlabs_tts_gen_api_key: str = field(default=None)  # prefer env ELEVENLABS_API_KEY
    elevenlabs_tts_gen_warmup_text: str = field(default=None)
