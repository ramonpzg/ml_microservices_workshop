import gradio as gr
from mlserver.codecs import StringCodec, NumpyCodec
import requests
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pedalboard.io import AudioFile
import tempfile
from os.path import join
from faker import Faker
from pathlib import Path
from glob import glob
import os

faker = Faker()


# def find_song(func):

#     files = Path("./music").glob("*.mp3")
#     latest_file = max([f for f in files], key=lambda item: item.stat().st_ctime)
#     with AudioFile(file_name, "w", samplerate=sample_rate, num_channels=1) as f:
#             f.write(audio_array)
#     new_stuf = func()





def make_sound(text, guidance_scale, max_new_tokens, sample_rate):
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

    file_name = join('./music', f"{faker.user_name()}.mp3")
    with AudioFile(file_name, "w", samplerate=sample_rate, num_channels=1) as f:
        f.write(audio_array)
    return sample_rate, audio_array
    
sample_rate = 32_000

def audio_effect(audio_piece):
    pass

def make_waveform():
    # waveform = waveform.numpy()
    files =  glob("./music/*.mp3")
    latest_file = max(files, key=os.path.getctime)
    with AudioFile(latest_file, "r") as f:
        waveform = f.read(f.frames)
        sample_rate = f.samplerate

    num_channels, num_frames = waveform.shape
    time_axis = np.arange(0, num_frames) / sample_rate
    with plt.xkcd():
        figure = Figure() 
        axes = figure.subplots(num_channels, 1)
        if num_channels == 1:
            axes = [axes]
        for c in range(num_channels):
            axes[c].plot(time_axis, waveform[c], linewidth=1)
            axes[c].grid(True)
            if num_channels > 1:
                axes[c].set_ylabel(f"Channel {c+1}")
        figure.suptitle("waveform")
    return figure

def plot_specgram():
    # waveform = waveform.numpy()
    files =  glob("./music/*.mp3")
    latest_file = max(files, key=os.path.getctime)
    with AudioFile(latest_file, "r") as f:
        waveform = f.read(f.frames)
        sample_rate = f.samplerate

    num_channels, num_frames = waveform.shape
    with plt.xkcd():
        figure = Figure() 
        axes = figure.subplots(num_channels, 1)
        # figure, axes = plt.subplots(num_channels, 1)
        if num_channels == 1:
            axes = [axes]
        for c in range(num_channels):
            axes[c].specgram(waveform[c], Fs=sample_rate)
            if num_channels > 1:
                axes[c].set_ylabel(f"Channel {c+1}")
        figure.suptitle("Spectrogram")
    return figure

examples = [
    "Hello", "By"
]

with gr.Blocks(theme='gstaff/xkcd') as demo:
    gr.Markdown("# Music Generation and Tagging App")
    gr.Markdown("First Demo of the Day ~ TODO: Write Instructions Here")

    with gr.Column():
        gr.Markdown("# Step 1 - Describe the music you want 😎 🎸 🎹 🎵")

        with gr.Row(equal_height=True):
            with gr.Column(min_width=900):
                text = gr.Textbox(
                    label="Name",
                    info="Audio Prompt for the kind of song you want your model to produce.",
                    lines=3,
                    placeholder="Type your song in here.",
                    # value="John Doe",
                    interactive=True,
                )
                make_music   = gr.Button("Create Music")
            with gr.Column():
                tokens      = gr.Slider(label="Max Number of New Tokens", value=200, minimum=5, maximum=1000, step=1)
                guidance    = gr.Slider(label="Period of plot", value=3, minimum=1, maximum=50, step=1)
                sample_rate = gr.Radio([16000, 32000, 44100], label="Sample Rate", value=32000)
            
        audio_output = gr.Audio()
        make_music.click(fn=make_sound, inputs=[text, guidance, tokens, sample_rate], outputs=audio_output, api_name="create_music")
        
        gr.Markdown()
        gr.Markdown("# Step 2 - Visualize your creation 📈 👀 👌")
        with gr.Row():
            with gr.Column():
                create_plots = gr.Button("Visualize Waveform")
                plot1 = gr.Plot()
                create_plots.click(fn=make_waveform, outputs=plot1)
            with gr.Column():
                create_plots = gr.Button("Visualize Spectogram")
                plot2 = gr.Plot()
                create_plots.click(fn=plot_specgram, outputs=plot2)

        gr.Markdown()
        gr.Markdown("# Step 3 - Add Some Effects to it 📼 🎧 🎷 🎼")
        with gr.Column():
            update_music = gr.Button("Update your Music")
            # outputs_2  = gr.Audio()
            # update_music.click(fn=audio_effect, inputs=outputs, outputs=outputs_2, api_name="update_music")
        
        gr.Markdown()
        gr.Markdown("# Step 4 - Create a MIDI Representation! 🎛️ 🎶 🎼")
        gr.HTML(value="""<iframe src="https://basicpitch.spotify.com/" height="700" width="100%"></iframe>""")


demo.launch()