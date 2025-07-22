# AI Music Generator
A powerful AI-driven tool that transforms your musical ideas—from simple text descriptions or hummed melodies—into complete musical compositions.

## About The Project
This project leverages the power of Large Language Models (LLMs) and advanced audio analysis to bridge the gap between human creativity and music production. Whether you're a professional musician looking for inspiration or a hobbyist wanting to create a quick tune, this tool offers an intuitive interface to bring your ideas to life.

The application provides two distinct modes for music generation:

* **Text-to-Music:** Engage in a conversation with an AI to specify genre, mood, tempo, and instruments, which are then refined by the Gemini API into a perfect prompt.

* **Humming-to-Music:** Simply hum a melody, and the AI will analyze its pitch, key, and tempo to construct a detailed prompt and generate a full track around it.

The final output includes a professional-grade MIDI file, perfect for use in a Digital Audio Workstation (DAW), and a high-quality ```.wav``` audio file synthesized using FluidSynth for easy listening.

## How It Works
The application uses two distinct pipelines, both of which use a Transformer model to produce the final MIDI file.

### 1. Text-to-Music Pipeline
* **Guided Input:** A chatbot guides you through providing keywords (mood, genre, instruments, etc.).

* **Prompt Refinement:** The collected keywords are sent to the Google Gemini API, which crafts a detailed, descriptive prompt optimized for the music generation model.

* **MIDI Generation:** The refined prompt is processed by the ```amaai-lab/text2midi``` Transformer model to generate a MIDI file.

* **Studio Synthesis:** FluidSynth synthesizes the MIDI file into a high-quality ```.wav``` audio file using a SoundFont.

### 2. Humming-to-Music Pipeline
* **Audio Analysis:** Your uploaded humming is analyzed using:

 * ```crepe```: For highly accurate pitch detection to identify the core notes.

 * ```librosa```: To extract musical features like tempo and dynamics.

* **Prompt Engineering:** The system determines the musical key, tempo, and notes, and compiles them into a descriptive text prompt.

* **Generation & Synthesis:** This engineered prompt is then fed into the same Gemini API -> Transformer -> FluidSynth pipeline to produce the final ```.mid``` and ```.wav``` files.

## Tech Stack
* **Backend:** Python

* **Web UI:** Gradio

* **AI & ML:**

  * **Prompt Engineering:** Google Gemini

  * **MIDI Generation:** Hugging Face Transformers, PyTorch (```amaai-lab/text2midi```)

  * **Pitch Analysis:** CREPE

  * **Audio Analysis:** Librosa

* **Audio Synthesis:** FluidSynth

* **Utilities:** PrettyMIDI, Plotly, NumPy, Pydub

## Getting Started
To get a local copy up and running, follow these steps.

**Prerequisites**
You must have the following software installed on your system:

* **Python 3.8+ and pip**

* **FluidSynth:** This is a command-line tool required for audio synthesis.

You can download it from the official FluidSynth website or install it via a package manager (e.g., ```sudo apt-get install fluidsynth``` on Debian/Ubuntu, ```brew install fluidsynth``` on macOS).

**Installation**
**1. Clone the repository:**

```
Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
**2. Set up the Gemini API Key:**

* Create a file named ```.env``` in the root of the project directory.

* Add your Google Gemini API key to this file:

```
Code snippet

# .env file
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```
**3. Download the SoundFont:**

* The project requires a SoundFont file to synthesize MIDI into audio.

* Download ```FluidR3_GM.sf2``` from this link (or another trusted source).

* Place the ```FluidR3_GM.sf2``` file in the root directory of the project.

**4. Create a virtual environment and install dependencies:**

* Create and activate a virtual environment:
```
Bash

# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS & Linux
python3 -m venv venv
source venv/bin/activate
```
* Use the Installation command to download all the requirements
```
Bash

pip install -r requirements.txt
```
## Usage
Once the installation is complete, run the Gradio UI:
```
Bash

python UI.py
```
This will start a local web server. Open the URL provided in your terminal (usually ```http://127.0.0.1:7860```) in your browser to use the application.

## Project Structure
.\
├── utils/\
│   ├── __init__.py\
│   ├── audio_convert.py  # Utility for MP3 to WAV conversion.\
│   ├── chatter.py        # Manages the conversational text-to-music prompt creation.\
│   ├── color_gen.py      # Utility to generate visually distinct colors (for future use).\
│   ├── fluid.py          # Interface for FluidSynth to convert MIDI to WAV.\
│   └── gemmini.py        # Handles prompt refinement via the Google Gemini API.\
├── .gitignore\
├── README.md             # You are here!\
├── UI.py                 # The main Gradio application entry point.\
├── mgen.py               # Core logic for music generation and humming analysis.\
└── requirements.txt      # Contains all the requirements\
