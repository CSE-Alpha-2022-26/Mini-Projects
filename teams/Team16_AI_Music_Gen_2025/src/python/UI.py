import pretty_midi
import gradio as gr
import plotly.graph_objects as go
from mgen import generate_music, process_humming
from utils import refine_prompt, finalize_prompt
def update_and_visualize(audio_path, midi_path, final_prompt):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        fig = go.Figure()
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                fig.add_trace(go.Bar(
                    x=[note.end - note.start],
                    y=[note.pitch],
                    base=[note.start],
                    orientation='h',
                    width=0.6,
                    marker=dict(color='brown')
                ))
        fig.update_layout(
            title="MIDI Piano Roll",
            xaxis_title="Time (sec)",
            yaxis_title="Pitch (MIDI)",
            yaxis=dict(autorange="reversed"),
            height=400
        )
        return fig
    except Exception as e:
        print("MIDI visualization error:", e)
        return go.Figure()

# -----------------------------
# Visualization for Humming Page (MIDI + Waveform)
# -----------------------------
def visualize_hum(audio_path, midi_path):
    try:
        fig = go.Figure()

        # MIDI Piano Roll
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                fig.add_trace(go.Bar(
                    x=[note.end - note.start],
                    y=[note.pitch],
                    base=[note.start],
                    orientation='h',
                    width=0.6,
                    marker=dict(color='green')
                ))

        fig.update_layout(
            title="MIDI Piano Roll (from Humming)",
            xaxis_title="Time (sec)",
            yaxis_title="Pitch (MIDI)",
            yaxis=dict(autorange="reversed"),
            height=400
        )
        return fig
    except Exception as e:
        print("Humming visualization error:", e)
        return go.Figure()

# (Rest of your Gradio app remains unchanged)
# You can now use update_and_visualize() and visualize_hum() directly in your interface definitions where gr.Plot is used

# -----------------------------
# Custom CSS and Theme
# -----------------------------
css = """
.output-audio { max-width: 600px !important; }
.download-column { margin-left: 20px; }
"""

theme = gr.themes.Soft(primary_hue="purple", secondary_hue="blue", neutral_hue="gray")

# -----------------------------
# Custom CSS and Theme
# -----------------------------
css = """
.output-audio { max-width: 600px !important; }
.download-column { margin-left: 20px; }
"""

theme = gr.themes.Soft(primary_hue="purple", secondary_hue="blue", neutral_hue="gray")

# -----------------------------
# Gradio Interface Definition
# -----------------------------
with gr.Blocks(css=css, theme=theme) as demo:
    # Home Page
    with gr.Column(visible=True) as home:
        gr.Markdown("""
        # Welcome to the AI Music Generator! ✨

        Create music using AI by either describing your track in text or uploading a humming melody.

        **How to Use:**
        - Choose a mode: **Text-to-Music** or **Humming-to-Music**.
        - Fill in details for text mode or upload your humming for humming mode.
        - Finalize your prompt and generate your track.
        - Listen to your music and download the audio and MIDI files.
        - Visualize the music with a piano-roll chart (and waveform in humming mode).
        """)
        with gr.Row():
            text_btn = gr.Button("🎤 Text to Music")
            hum_btn = gr.Button("🎶 Humming to Music")
        gr.Markdown("""
        **Text Mode:**
        - Describe your track and add details like mood, instruments, tempo, and genre.
        - Generate music to listen and download.
        """)
        gr.Markdown("""
        **Humming Mode:**
        - Upload your humming melody.
        - Generate music based on your humming.
        - Download the resulting audio and MIDI files.
        """)

    # Humming-to-Music Page
    with gr.Column(visible=False) as hum_page:
        gr.Markdown("## 🎶 Humming to Music")
        hum_input = gr.Audio(label="Upload Humming Only", type="filepath")
        genre_dropdown = gr.Textbox(label="Genre (e.g. Jazz, Classical, Rock)", placeholder="Jazz")
        instrument_input = gr.Textbox(label="Instruments (comma separated, or 'Auto')", placeholder="Piano, Drums")
        process_btn = gr.Button("🎼 Process Humming")
        output_hum_music = gr.Audio(label="Generated Music", type="filepath")
        midi_hum_file = gr.File(label="Download MIDI")
        hum_vis = gr.Plot(label="Music Visualization (MIDI + Waveform)")
        back_btn2 = gr.Button("⬅️ Back to Home")

        process_btn.click(
            process_humming,
            inputs=[hum_input, genre_dropdown, instrument_input],
            outputs=[output_hum_music, midi_hum_file, hum_vis]
        )

    # Text-to-Music Page
    with gr.Column(visible=False) as text_page:
        gr.Markdown("## 🎤 Text Prompt to Music Generator")
        conversation_history = gr.State([{
            "user": "",
            "assistant": "🎉 Welcome! Let's create your perfect track.\n\n📝 Describe your music idea (e.g., 'calm study music')"
        }])
        chat_history = gr.Textbox(label="Conversation", lines=10, interactive=False)
        user_message = gr.Textbox(label="Your Message")
        send_btn = gr.Button("Send")
        reset_btn = gr.Button("🔄 Reset Conversation")
        finalize_btn = gr.Button("✨ Finalize Prompt")
        final_prompt_box = gr.Textbox(label="Final Prompt", interactive=False)
        generate_btn = gr.Button("🎧 Generate Music", interactive=False)

        with gr.Row():
            output_audio = gr.Audio(label="Generated Music", type="filepath", interactive=False, elem_classes="output-audio")
            with gr.Column(elem_classes="download-column"):
                midi_file = gr.File(label="Download MIDI", file_count="single")
        midi_plot = gr.Plot(label="Music Visualization")
        back_btn1 = gr.Button("⬅️ Back to Home")

        send_btn.click(
            refine_prompt,
            [conversation_history, user_message],
            [conversation_history, chat_history],
            show_progress=True
        )
        finalize_btn.click(
            finalize_prompt,
            [conversation_history],
            [final_prompt_box]
        )
        finalize_btn.click(lambda: gr.update(interactive=True), outputs=[generate_btn])
        reset_btn.click(
            lambda: (
                [{"user": "", "assistant": "🎉 Welcome! Let's create your perfect track.\n\n📝 Describe your music idea (e.g., 'calm study music')"}],
                "User: \nAssistant: 🎉 Welcome! Let's create your perfect track.\n\n📝 Describe your music idea (e.g., 'calm study music')",
                "",
                gr.update(interactive=False)
            ),
            outputs=[conversation_history, chat_history, final_prompt_box, generate_btn]
        )
        generate_btn.click(
            generate_music,
            [final_prompt_box],
            [output_audio, midi_file, final_prompt_box]
        ).then(
            update_and_visualize,
            [output_audio, midi_file, final_prompt_box],
            [midi_plot]
        )

    # Navigation Handlers
    def goto_text():
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
    def goto_hum():
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
    def goto_home():
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

    text_btn.click(goto_text, outputs=[home, text_page, hum_page])
    hum_btn.click(goto_hum, outputs=[home, text_page, hum_page])
    back_btn1.click(goto_home, outputs=[home, text_page, hum_page])
    back_btn2.click(goto_home, outputs=[home, text_page, hum_page])

demo.launch()
