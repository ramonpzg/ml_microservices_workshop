from src.plotting import make_waveform, make_spectogram
from src.helpers import make_sound, audio_effect

import gradio as gr

examples = [
    "Hello", "By"
]

with gr.Blocks(theme='gstaff/xkcd') as demo:
    gr.Markdown("# Music Generation and Editing App")
    gr.Markdown("First Demo of the Day ~ TODO: Write Instructions Here")

    with gr.Column():
        gr.Markdown("# Step 1 - Describe the music you want 😎 🎸 🎹 🎵")
        with gr.Row(equal_height=True):
            with gr.Column(min_width=900):
                text = gr.Textbox(
                    label="Name",
                    info="Audio Prompt for the kind of song you want your model to produce.",
                    lines=3,
                    placeholder="Type your song description in here.",
                    # value="John Doe",
                    interactive=True,
                )
                make_music   = gr.Button("Create Music")
            with gr.Column():
                tokens      = gr.Slider(label="Max Number of New Tokens", value=200, minimum=5, maximum=1000, step=1)
                guidance    = gr.Slider(label="Guidance Scale", value=3, minimum=1, maximum=50, step=1)
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
                create_plots.click(fn=make_spectogram, outputs=plot2)

        gr.Markdown()
        gr.Markdown("# Step 3 - Add Some Effects to it 📼 🎧 🎷 🎼")
        with gr.Column():
            update_music = gr.Button("Update your Music")
            output_video = gr.Video(label="Output", elem_id="output-video")
            update_music.click(audio_effect, outputs=[output_video])

        gr.Markdown()
        gr.Markdown("# Step 4 - Create a MIDI Representation! 🎛️ 🎶 🎼")
        gr.HTML(value="""<iframe src="https://basicpitch.spotify.com/" height="1000" width="100%"></iframe>""")

demo.launch()