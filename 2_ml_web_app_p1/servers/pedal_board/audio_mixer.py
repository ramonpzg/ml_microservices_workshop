
from pedalboard import Pedalboard, Distortion, Delay, Reverb, Chorus, Gain, PitchShift, Compressor, Mix
from pedalboard.io import AudioFile

from mlserver.codecs import decode_args
from mlserver import MLModel

from typing import List, Optional
import numpy as np

class AudioMixer(MLModel):
    async def load(self):
        self.delay_and_pitch_shift = Pedalboard([
            Delay(delay_seconds=0.25, mix=1.0), PitchShift(semitones=7), Gain(gain_db=-3),
        ])

    @decode_args
    async def predict(self, song: np.ndarray, sample_rate: np.ndarray) -> np.ndarray:

        self.passthrough = Gain(gain_db=0)
        self.board = Pedalboard([
            Compressor(),
            Mix([self.passthrough, self.delay_and_pitch_shift]),
            Reverb()
        ])
        self.new_audio = self.board(song, sample_rate=sample_rate[0][0])
        return self.new_audio
