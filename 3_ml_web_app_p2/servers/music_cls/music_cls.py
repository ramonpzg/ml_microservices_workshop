from mlserver import MLModel
from mlserver.codecs import decode_args
from transformers import pipeline
import numpy as np
import pandas as pd

class MusicClassifier(MLModel):
    async def load(self):
        self.model = pipeline("audio-classification", model="ramonpzg/wav2musicgenre")

    @decode_args
    async def predict(self, song: np.ndarray) -> pd.DataFrame:
        result = self.model(song[0])
        return pd.DataFrame(result)