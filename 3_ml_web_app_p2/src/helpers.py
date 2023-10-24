from pedalboard.io import AudioFile
import pandas as pd
import requests
import io
import os
from faker import Faker


def create_tmp_audio(audio_data, sr):
    faker = Faker()
    file_name = os.path.join('./music', f"{faker.user_name()}.mp3")
    with AudioFile(file_name, "w", samplerate=sr, num_channels=1) as f:
        f.write(audio_data)
    return file_name

def download_song(df, song_to_get):
    song_url = df.loc[df['artist_song'] == song_to_get, 'urls'].iloc[0]
    with requests.get(song_url, stream=True) as music:
        fil = io.BytesIO(music.content)
        with AudioFile(fil, "r") as f:
            song = f.read(f.frames)
            sample_rate = f.samplerate
    return song, sample_rate