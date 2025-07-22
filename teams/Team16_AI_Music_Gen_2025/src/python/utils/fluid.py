import subprocess

def convert_midi_to_wav(midi_path, output_path, soundfont_path="FluidR3_GM.sf2"):
    subprocess.run([
        "fluidsynth",
        "-ni",
        soundfont_path,
        midi_path,
        "-F", output_path,
        "-r", "44100"
    ], check=True)


'''
# Example usage
convert_midi_to_wav(
    soundfont_path="FluidR3_GM.sf2",
    midi_path="output.mid",
    output_path="output.wav"
)
'''