from mlserver.codecs import StringCodec, NumpyCodec
from pedalboard.io import AudioFile
from faker import Faker
import numpy as np
import requests

from glob import glob
import os

def make_sound(text, guidance_scale, max_new_tokens, sample_rate):
    faker = Faker()
    endpoint = "http://localhost:8080/v2/models/musicgen_model/infer"
    input_request = {
        'inputs': [
            StringCodec.encode_input(name='text', payload=[text], use_bytes=False).dict(),
            NumpyCodec.encode_input(name='guidance_scale', payload=np.array([guidance_scale])).dict(),
            NumpyCodec.encode_input(name='max_new_tokens', payload=np.array([max_new_tokens])).dict()
        ]
    }
    result = requests.post(endpoint, json=input_request).json()
    audio_array = np.array(result['outputs'][0]['data'])

    file_name = os.path.join('./music', f"{faker.user_name()}.mp3")
    with AudioFile(file_name, "w", samplerate=sample_rate, num_channels=1) as f:
        f.write(audio_array)
    return sample_rate, audio_array


def audio_effect():
    endpoint = "http://localhost:7050/v2/models/novice_dj/infer"
    files =  glob("./music/*.mp3")
    latest_file = max(files, key=os.path.getctime)
    with AudioFile(latest_file, "r") as f:
        waveform = f.read(f.frames)
        sample_rate = f.samplerate
    input_request = {
        'inputs': [
            NumpyCodec.encode_input(name='song', payload=waveform).dict(),
            NumpyCodec.encode_input(name='sample_rate', payload=np.array([sample_rate])).dict()
        ]
    }
    result = requests.post(endpoint, json=input_request).json()
    audio_array = np.array(result['outputs'][0]['data'])
    return gr.make_waveform((sample_rate, audio_array), bg_image="bg.png")