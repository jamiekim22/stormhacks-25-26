import logging
import os
import sys
from copy import copy
from pathlib import Path
from queue import Queue
from threading import Event
from typing import Optional
from VAD.vad_handler import VADHandler
from arguments_classes.module_arguments import ModuleArguments
from arguments_classes.vad_arguments import VADHandlerArguments
from arguments_classes.whisper_stt_arguments import WhisperSTTHandlerArguments
from arguments_classes.open_api_language_model_arguments import (
    OpenApiLanguageModelHandlerArguments,
)
from arguments_classes.elevenlabs_tts_arguments import ElevenLabsTTSHandlerArguments
import torch
import nltk
from rich.console import Console
from transformers import (
    HfArgumentParser,
)


from utils.thread_manager import ThreadManager

# Ensure that the necessary NLTK resources are available
try:
    nltk.data.find("tokenizers/punkt_tab")
except (LookupError, OSError):
    nltk.download("punkt_tab")
try:
    nltk.data.find("tokenizers/averaged_perceptron_tagger_eng")
except (LookupError, OSError):
    nltk.download("averaged_perceptron_tagger_eng")

# caching allows ~50% compilation time reduction
# see https://docs.google.com/document/d/1y5CRfMLdwEoF1nTk9q8qEu1mgMUuUtvhklPKJ2emLU8/edit#heading=h.o2asbxsrp1ma
CURRENT_DIR = Path(__file__).resolve().parent
os.environ["TORCHINDUCTOR_CACHE_DIR"] = os.path.join(CURRENT_DIR, "tmp")

console = Console()
logging.getLogger("numba").setLevel(logging.WARNING)  # quiet down numba logs


def rename_args(args, prefix):
    """
    Rename arguments by removing the prefix and prepares the gen_kwargs.
    """
    gen_kwargs = {}
    for key in copy(args.__dict__):
        if key.startswith(prefix):
            value = args.__dict__.pop(key)
            new_key = key[len(prefix) + 1 :]  # Remove prefix and underscore
            if new_key.startswith("gen_"):
                gen_kwargs[new_key[4:]] = value  # Remove 'gen_' and add to dict
            else:
                args.__dict__[new_key] = value

    args.__dict__["gen_kwargs"] = gen_kwargs


def parse_arguments():
    parser = HfArgumentParser(
        (
            ModuleArguments,
            VADHandlerArguments,
            WhisperSTTHandlerArguments,
            OpenApiLanguageModelHandlerArguments,
            ElevenLabsTTSHandlerArguments,
        )
    )

    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # Parse configurations from a JSON file if specified
        return parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        # Parse arguments from command line if no JSON file is provided
        return parser.parse_args_into_dataclasses()


def setup_logger(log_level):
    global logger
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # torch compile logs
    if log_level == "debug":
        torch._logging.set_logs(graph_breaks=True, recompiles=True)


def prepare_module_args(module_kwargs, *handler_kwargs):
    # Simplified device handling for the specific configuration
    if module_kwargs.device:
        for kwargs in handler_kwargs:
            if hasattr(kwargs, "device"):
                kwargs.device = module_kwargs.device


def prepare_all_args(
    module_kwargs,
    whisper_stt_handler_kwargs,
    open_api_language_model_handler_kwargs,
    elevenlabs_tts_handler_kwargs,
):
    prepare_module_args(
        module_kwargs,
        whisper_stt_handler_kwargs,
        open_api_language_model_handler_kwargs,
        elevenlabs_tts_handler_kwargs,
    )

    rename_args(whisper_stt_handler_kwargs, "stt")
    rename_args(open_api_language_model_handler_kwargs, "open_api")
    rename_args(elevenlabs_tts_handler_kwargs, "elevenlabs_tts")


def initialize_queues_and_events():
    return {
        "stop_event": Event(),
        "should_listen": Event(),
        "recv_audio_chunks_queue": Queue(),
        "send_audio_chunks_queue": Queue(),
        "spoken_prompt_queue": Queue(),
        "text_prompt_queue": Queue(),
        "lm_response_queue": Queue(),
    }


def build_pipeline(
    module_kwargs,
    vad_handler_kwargs,
    whisper_stt_handler_kwargs,
    open_api_language_model_handler_kwargs,
    elevenlabs_tts_handler_kwargs,
    queues_and_events,
):
    stop_event = queues_and_events["stop_event"]
    should_listen = queues_and_events["should_listen"]
    recv_audio_chunks_queue = queues_and_events["recv_audio_chunks_queue"]
    send_audio_chunks_queue = queues_and_events["send_audio_chunks_queue"]
    spoken_prompt_queue = queues_and_events["spoken_prompt_queue"]
    text_prompt_queue = queues_and_events["text_prompt_queue"]
    lm_response_queue = queues_and_events["lm_response_queue"]
    from connections.local_audio_streamer import LocalAudioStreamer

    local_audio_streamer = LocalAudioStreamer(
        input_queue=recv_audio_chunks_queue, output_queue=send_audio_chunks_queue
    )
    comms_handlers = [local_audio_streamer]
    should_listen.set()

    vad = VADHandler(
        stop_event,
        queue_in=recv_audio_chunks_queue,
        queue_out=spoken_prompt_queue,
        setup_args=(should_listen,),
        setup_kwargs=vars(vad_handler_kwargs),
    )

    stt = get_stt_handler(
        module_kwargs,
        stop_event,
        spoken_prompt_queue,
        text_prompt_queue,
        whisper_stt_handler_kwargs,
    )
    lm = get_llm_handler(
        module_kwargs,
        stop_event,
        text_prompt_queue,
        lm_response_queue,
        open_api_language_model_handler_kwargs,
    )
    tts = get_tts_handler(
        module_kwargs,
        stop_event,
        lm_response_queue,
        send_audio_chunks_queue,
        should_listen,
        elevenlabs_tts_handler_kwargs,
    )

    return ThreadManager([*comms_handlers, vad, stt, lm, tts])


def get_stt_handler(
    module_kwargs,
    stop_event,
    spoken_prompt_queue,
    text_prompt_queue,
    whisper_stt_handler_kwargs,
):
    if module_kwargs.stt == "whisper":
        from STT.whisper_stt_handler import WhisperSTTHandler

        return WhisperSTTHandler(
            stop_event,
            queue_in=spoken_prompt_queue,
            queue_out=text_prompt_queue,
            setup_kwargs=vars(whisper_stt_handler_kwargs),
        )
    else:
        raise ValueError("Only whisper STT is supported.")


def get_llm_handler(
    module_kwargs,
    stop_event,
    text_prompt_queue,
    lm_response_queue,
    open_api_language_model_handler_kwargs,
):
    if module_kwargs.llm == "open_api":
        from LLM.openai_api_language_model import OpenApiModelHandler

        return OpenApiModelHandler(
            stop_event,
            queue_in=text_prompt_queue,
            queue_out=lm_response_queue,
            setup_kwargs=vars(open_api_language_model_handler_kwargs),
        )
    else:
        raise ValueError("Only open_api LLM is supported.")


def get_tts_handler(
    module_kwargs,
    stop_event,
    lm_response_queue,
    send_audio_chunks_queue,
    should_listen,
    elevenlabs_tts_handler_kwargs,
):
    if module_kwargs.tts == "elevenlabs":
        try:
            from TTS.elevenlabs_handler import ElevenLabsTTSHandler
        except Exception as e:
            logger.error("Error importing ElevenLabsTTSHandler")
            raise e
        return ElevenLabsTTSHandler(
            stop_event,
            queue_in=lm_response_queue,
            queue_out=send_audio_chunks_queue,
            setup_args=(should_listen,),
            setup_kwargs=(
                vars(elevenlabs_tts_handler_kwargs)
                if elevenlabs_tts_handler_kwargs
                else {}
            ),
        )
    else:
        raise ValueError("Only elevenlabs TTS is supported.")


def main():
    (
        module_kwargs,
        vad_handler_kwargs,
        whisper_stt_handler_kwargs,
        open_api_language_model_handler_kwargs,
        elevenlabs_tts_handler_kwargs,
    ) = parse_arguments()

    setup_logger(module_kwargs.log_level)

    prepare_all_args(
        module_kwargs,
        whisper_stt_handler_kwargs,
        open_api_language_model_handler_kwargs,
        elevenlabs_tts_handler_kwargs,
    )

    queues_and_events = initialize_queues_and_events()

    pipeline_manager = build_pipeline(
        module_kwargs,
        vad_handler_kwargs,
        whisper_stt_handler_kwargs,
        open_api_language_model_handler_kwargs,
        elevenlabs_tts_handler_kwargs,
        queues_and_events,
    )

    try:
        pipeline_manager.start()
    except KeyboardInterrupt:
        pipeline_manager.stop()


if __name__ == "__main__":
    main()
