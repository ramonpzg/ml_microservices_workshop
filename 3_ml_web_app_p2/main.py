from nicegui import ui
import pandas as pd
import numpy as np
import requests
from pedalboard.io import AudioFile
import os
import io
from IPython.display import Audio
import tempfile


(
    ui.label('🎧 Music Platform')
      .style('color: #ab003c; font-size: 350%; font-weight: 450')
      .classes('self-center')
)

ui.markdown("## 🎻 A New Way to Find Music 🎶").classes('self-center')
ui.markdown(
    """
    🎯 **The purpose** of this app is to showcase one of the many (cool 😎 and fun 💃🏻🕺🏽) ways in which you 
    can create machine learning microservices for different creative purposes.
    """
).style("max-width: 1000px; font-size: 120%").classes('self-center')


metadata = pd.read_csv("payload.csv")
artist_song = sorted(metadata['artist_song'].tolist())

def create_music_card(song):
    with ui.column():
        with ui.card().tight().style("height: 350px; width: 300px"):
            ui.image(song['photos']).classes('w-[300px] h-[210px]')
            with ui.card_section():
                ui.label(f"Artist: {song['artist']}")
                ui.label(f"Song Name: {song['name']}")
                ui.label(f"Genre: {song['genre']}")
        first_song = ui.audio(song['urls'])#.classes('w-64'):
        first_song.on('ended', lambda _: ui.notify('Audio playback completed!'))

def create_tmp_audio(audio_data, sr):
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmpf:
        with AudioFile(tmpf.name, 'w', samplerate=sr, num_channels=1) as func:
            func.write(audio_data)
    return tmpf.name

def get_vectors():
    """Callback function for our search box"""
    song = song_selection.value.split(' - ')[-1] # get the name of the song selected
    get_index = metadata.loc[metadata['name'] == song, 'index'].iloc[0] # get the index of such a song
    song_selected = metadata.iloc[get_index]

    # Clear the result from the previous artist selected
    main_artist.clear()

    with main_artist:
        create_music_card(song_selected)

def download_song(song_to_get):
    song_url = metadata.loc[metadata['artist_song'] == song_to_get, 'urls'].iloc[0]
    with requests.get(song_url, stream=True) as music:
        fil = io.BytesIO(music.content)
        with AudioFile(fil, "r") as f:
            song = f.read(f.frames)
            sample_rate = f.samplerate
    return song, sample_rate

def split_song():
    third_artist.clear()
    song, sample_rate = download_song(song_selection.value)
    endpoint = "http://localhost:5070/v2/models/music_splitter/infer"
    input_request = {
        "inputs": [{
            "name": "song", "parameters": {"content_type": "np"}, "datatype": "FP32",
            "shape": song.shape, "data": song.tolist()
        }]
    }
    res = requests.post(endpoint, json=input_request).json()
    song_array = np.array(res['outputs'][0]['data'])
    song_shape = res['outputs'][0]['shape']
    song_reshaped = song_array.reshape(song_shape)
    with ui.column():
        ui.markdown('### Vocals')
        vaudio = ui.audio(create_tmp_audio(song_reshaped[0], 44100))
        ui.markdown('### Instruments')
        iaudio = ui.audio(create_tmp_audio(song_reshaped[2], 44100))


def get_song_genre():
    second_artist.clear()
    song, sample_rate = download_song(song_selection.value)
    input_request = {
        "inputs": [ 
            {
                "name": "song",
                "shape": song[0][None].shape,
                "parameters": {"content_type": "np"},
                "data": song[0][None].tolist(),
                "datatype": "FP64"
            }
        ]
    }
    endpoint = "http://localhost:5080/v2/models/music_classifier/infer"
    res = requests.post(endpoint, json=input_request)
    rows = []
    for score, label in zip(res.json()['outputs'][0]['data'], res.json()['outputs'][1]['data']):
        results = {}
        results['genre'] = label.title()
        results['score'] = round(score * 100, 2)
        rows.append(results)

    columns = [
        {'name': 'genre', 'label': 'Genre', 'field': 'genre', 'align': 'left'},
        {'name': 'score','label': 'Score', 'field': 'score', 'sortable': True},
    ]
    with second_artist:
        ui.markdown(f'### Your Song: {song_selection.value}')
        the_table = ui.table(columns=columns, rows=rows, row_key='name')


with ui.tabs().classes('w-full self-center justify-center items-center') as tabs:
    one   = ui.tab('One')
    two   = ui.tab('Two')
    three = ui.tab('Three')
    four  = ui.tab('Four')
    five  = ui.tab('Five')
    six   = ui.tab('Six')
    seven = ui.tab('Seven')


with ui.tab_panels(tabs, value=one).classes('w-full self-center justify-center'):
    with ui.tab_panel(one).classes('flex items-center justify-center h-screen'):
        with ui.column().classes('items-center justify-center'):
            ui.markdown('### Select a song')
            song_selection = ui.select(
                artist_song, value='Dave Van Ronk - Buckets of Rain', on_change=get_vectors
            ).style("width: 700px")
        main_artist = ui.row().classes('w-full justify-center').style("margin: 0 auto; padding: 2rem;")

    with ui.tab_panel(two):
        with ui.column().classes('items-center justify-center'):
            ui.markdown('### Classify a song')
            table_button = ui.button('Classify Song Selected', on_click=get_song_genre).style("width: 700px").classes('w-full justify-center')
        second_artist = ui.column().classes('items-center w-full justify-center').style("margin: 0 auto; padding: 2rem;")

    with ui.tab_panel(three):
        with ui.column().classes('items-center justify-center'):
            ui.markdown('### Split a song')
            vocals_instr = ui.button('Split Song Selected', on_click=split_song).style("width: 700px").classes('w-full justify-center')
        third_artist = ui.column().classes('items-center w-full justify-center').style("margin: 0 auto; padding: 2rem;")

    with ui.tab_panel(four):
        ui.label('Second tab')

    with ui.tab_panel(five):
        ui.label('Second tab')

    with ui.tab_panel(six):
        ui.label('Second tab')

    with ui.tab_panel(seven):
        ui.label('Second tab')


dark = ui.dark_mode()
ui.label('Switch mode:')
ui.button('Dark', on_click=dark.enable)
ui.button('Light', on_click=dark.disable)


ui.colors(
    primary='#ab003c',
    secondary='#2c387e',
    accent='#f50057',
    dark='#f73378',
    positive='#f73378',
    negative='#ba000d'

)

ui.run(
    title='Qdrant for Music',
    # favicon='https://avatars.githubusercontent.com/u/73504361?s=280&v=4',
    # dark=True
)