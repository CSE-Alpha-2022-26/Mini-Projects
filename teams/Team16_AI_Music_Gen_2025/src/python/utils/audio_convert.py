from pydub import AudioSegment
import os

def mp3_to_wav(mp3_path, output_dir=None):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_path)

    # Define output WAV path
    if output_dir is None:
        output_dir = os.path.dirname(mp3_path)
    wav_path = os.path.join(output_dir, os.path.splitext(os.path.basename(mp3_path))[0] + ".wav")

    # Export as WAV
    audio.export(wav_path, format="wav")
    print(f"Converted to WAV: {wav_path}")
    return wav_path
