
from mlserver import MLModel
from pedalboard import Pedalboard, Distortion, Delay, Reverb, Chorus, Gain, PitchShift, Compressor, Mix
from pedalboard.io import AudioFile
from mlserver.codecs import decode_args
from typing import List, Optional
import numpy as np
from pydantic import BaseModel


# class AudioSettings(BaseModel):
#     song: np.ndarray
#     sample_rate: int
#     drive_db
#     delay_seconds
#     feedback
#     mix
#     room_size

class AudioMixer(MLModel):
    async def load(self):
        self.check = True

    @decode_args
    async def predict(
        self, 
        song: np.ndarray, 
        sample_rate: np.ndarray,
        # db: List[str], 
        # delay: Optional[np.ndarray] = 5, 
    ) -> np.ndarray:
        # self.board = Pedalboard([
        #     Distortion(drive_db=10), Delay(delay_seconds=1, feedback=0.1, mix=0.1),
        #     Reverb(room_size=0.10), Chorus(), Gain(), PitchShift()
        # ])

        passthrough = Gain(gain_db=0)

        delay_and_pitch_shift = Pedalboard([
            Delay(delay_seconds=0.25, mix=1.0), PitchShift(semitones=7), Gain(gain_db=-3),
        ])

        delay_longer_and_more_pitch_shift = Pedalboard([
            Delay(delay_seconds=0.5, mix=1.0), PitchShift(semitones=12), Gain(gain_db=-6),
        ])

        self.board = Pedalboard([
            # Put a compressor at the front of the chain:
            Compressor(),
            # Run all of these pedalboards simultaneously with the Mix plugin:
            Mix([
                passthrough, delay_and_pitch_shift, delay_longer_and_more_pitch_shift
            ]),
            # Add a reverb on the final mix:
            Reverb()
        ])
        self.new_audio = self.board(song, sample_rate=sample_rate[0][0])
        return self.new_audio
