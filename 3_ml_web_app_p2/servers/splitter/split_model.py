from mlserver import MLModel
from mlserver.codecs import decode_args
import numpy as np
import demucs.api
import torch


class SongSplitter(MLModel):
    async def load(self):
        self.separator = demucs.api.Separator(device='cpu')

    @decode_args
    async def predict(self, song: np.ndarray) -> np.ndarray:
        tensong = torch.from_numpy(song)
        original, result = self.separator.separate_tensor(tensong)
        return self.post_processor(result)

    def post_processor(self, tensor_dict: dict[torch.Tensor]) -> np.ndarray:
        tensor_dict["instruments"] = tensor_dict["bass"] + tensor_dict["drums"] + tensor_dict["other"]
        del tensor_dict["bass"],  tensor_dict["drums"],  tensor_dict["other"]
        return torch.vstack([tensor_dict['vocals'], tensor_dict['instruments']]).numpy()