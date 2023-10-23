from mlserver import MLModel
from mlserver.codecs import decode_args
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class TextEmbeddings(MLModel):
    async def load(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    @decode_args
    async def predict(self, lyrics: List[str]) -> np.ndarray:
        return self.model.encode(lyrics)