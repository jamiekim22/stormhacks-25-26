from dataclasses import dataclass, field

@dataclass
class ElevenLabsSTTHandlerArguments:
    # Base params (kept for parity, device is ignored by remote service)
    elevenlabs_stt_model_name: str = field(default="scribe_v1")
    elevenlabs_stt_device: str = field(default="cpu")
    elevenlabs_stt_compute_type: str = field(default="auto")

    # gen_kwargs -> use "gen_" prefix so rename_args packs them into gen_kwargs
    elevenlabs_stt_gen_language_code: str = field(default=None)  # auto-detect if None
    elevenlabs_stt_gen_timestamps_granularity: str = field(default="none")  # "word"|"character"|"none"
    elevenlabs_stt_gen_diarize: bool = field(default=False)
    elevenlabs_stt_gen_num_speakers: int = field(default=0)
    elevenlabs_stt_gen_tag_audio_events: bool = field(default=True)
    elevenlabs_stt_gen_file_format: str = field(default="pcm_s16le_16")  # raw 16k mono PCM
    elevenlabs_stt_gen_base_url: str = field(default="https://api.elevenlabs.io")
    elevenlabs_stt_gen_api_key: str = field(default=None)  # prefer env ELEVENLABS_API_KEY
