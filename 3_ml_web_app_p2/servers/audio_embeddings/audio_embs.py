from mlserver import MLModel
from mlserver.codecs import decode_args
from panns_inference import AudioTagging
import numpy as np


class MusicEmbeddings(MLModel):
    async def load(self):
        self.model = AudioTagging(checkpoint_path=None, device='cuda')

    @decode_args
    async def predict(self, song: np.ndarray) -> np.ndarray:
        clipwise_output, embedding = self.model.inference(song)
        return embedding