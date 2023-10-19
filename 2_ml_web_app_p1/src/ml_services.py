
from mlserver import MLServer, Settings, ModelSettings, MLModel
from mlserver.codecs import decode_args

from transformers import AutoProcessor, MusicgenForConditionalGeneration
from diffusers import AudioLDM2Pipeline
import numpy as np
import torch

from typing import List, Optional
import asyncio 

MUSICGEN = "facebook/musicgen-small"
AUDIOLDM2 = "cvssp/audioldm2"

class MusicGenServer(MLModel):
    async def load(self):
        self.processor = AutoProcessor.from_pretrained(MUSICGEN)
        self.model     = MusicgenForConditionalGeneration.from_pretrained(MUSICGEN)

    @decode_args
    async def predict(self, text: List[str], guidance_scale: np.ndarray, max_new_tokens: np.ndarray) -> np.ndarray:
        inputs = self.processor(text=text, padding=True, return_tensors="pt")
        audio_values = self.model.generate(
            **inputs, do_sample=True, guidance_scale=guidance_scale[0][0], max_new_tokens=max_new_tokens[0][0]
        ).numpy()
        sampling_rate = self.model.config.audio_encoder.sampling_rate
        return audio_values[0]

async def main():
    settings = Settings(debug=True)
    my_server = MLServer(settings=settings)
    musicgen_generator = ModelSettings(name='musicgen_model', implementation=MusicGenServer)
    await my_server.start(models_settings=[musicgen_generator])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
