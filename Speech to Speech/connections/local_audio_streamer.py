import threading
import sounddevice as sd
import numpy as np

import time
import logging

logger = logging.getLogger(__name__)


class LocalAudioStreamer:
    def __init__(
        self,
        input_queue,
        output_queue,
        list_play_chunk_size=512,
    ):
        self.list_play_chunk_size = list_play_chunk_size

        self.stop_event = threading.Event()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        def callback(indata, outdata, frames, time, status):
            try:
                if self.output_queue.empty():
                    self.input_queue.put(indata.copy())
                    outdata[:] = 0 * outdata
                else:
                    audio_data = self.output_queue.get()
                    # Ensure audio_data is a numpy array with correct shape
                    if isinstance(audio_data, bytes):
                        # Convert bytes to numpy array
                        audio_data = np.frombuffer(audio_data, dtype=np.int16)
                    elif not isinstance(audio_data, np.ndarray):
                        # Convert other types to numpy array
                        audio_data = np.array(audio_data, dtype=np.int16)
                    
                    # Ensure we have enough data for the output
                    if len(audio_data) >= frames:
                        outdata[:] = audio_data[:frames, np.newaxis]
                    else:
                        # Pad with zeros if not enough data
                        padded_data = np.zeros(frames, dtype=np.int16)
                        padded_data[:len(audio_data)] = audio_data
                        outdata[:] = padded_data[:, np.newaxis]
            except Exception as e:
                # Handle errors gracefully during shutdown
                outdata[:] = 0 * outdata

        logger.debug("Available devices:")
        logger.debug(sd.query_devices())
        with sd.Stream(
            samplerate=16000,
            dtype="int16",
            channels=1,
            callback=callback,
            blocksize=self.list_play_chunk_size,
        ):
            logger.info("Starting local audio stream")
            while not self.stop_event.is_set():
                time.sleep(0.001)
            print("Stopping recording")
