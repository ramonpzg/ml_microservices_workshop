from mlserver import MLModel
from mlserver.codecs import decode_args
from transformers import pipeline
from typing import List
import librosa
import numpy as np


class ASRServer(MLModel):
    async def load(self):
        self.pipe = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

    @decode_args
    async def predict(self, song: np.ndarray, sample_rate: np.ndarray
        # max_new_tokens=2000,
        # generate_kwargs={"task": "transcribe"},
        # chunk_length_s=30,
        # batch_size=8,
        # return_timestamps=True
    ) -> List[str]:
        resampled_song = self.pre_process(song, sample_rate[0][0])
        return [self.pipe(resampled_song, max_new_tokens=2000)['text']]
    
    def pre_process(self, song: np.ndarray, sample_rate) -> np.ndarray:
        return librosa.resample(
            song[0], orig_sr=sample_rate, target_sr=self.pipe.feature_extractor.sampling_rate
        )
