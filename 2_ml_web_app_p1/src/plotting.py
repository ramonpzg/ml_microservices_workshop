from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pedalboard.io import AudioFile
import numpy as np

from glob import glob
import os


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
        figure.suptitle("Waveform")
    return figure


def make_spectogram():
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