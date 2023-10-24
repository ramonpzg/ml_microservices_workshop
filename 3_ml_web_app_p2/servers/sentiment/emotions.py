
from mlserver import MLModel
from mlserver.codecs import decode_args
from transformers import pipeline
from typing import List
import pandas as pd

class EmotionClassifier(MLModel):
    async def load(self):
        self.model = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

    @decode_args
    async def predict(self, lyrics: List[str]) -> pd.DataFrame:
        result = self.model(lyrics)
        return pd.DataFrame(result[0])
