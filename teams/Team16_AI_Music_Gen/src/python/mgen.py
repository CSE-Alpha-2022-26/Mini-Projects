import numpy as np

import pickle
import torch
import torch.nn as nn
from model.transformer_model import Transformer

import librosa
import numpy as np
import crepe
from collections import Counter

import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from transformers import T5Tokenizer

from huggingface_hub import hf_hub_download
from utils import gemmini_prompt,convert_midi_to_wav

# -----------------------------
# Dummy Music Generation Function
# -----------------------------
def generate_music(prompt):
    repo_id = "amaai-lab/text2midi"
    model_path = hf_hub_download(repo_id=repo_id, filename="pytorch_model.bin")
    tokenizer_path = hf_hub_download(repo_id=repo_id, filename="vocab_remi.pkl")

    device = 'cuda'
    # Load the tokenizer dictionary
    with open(tokenizer_path, "rb") as f:
        r_tokenizer = pickle.load(f)

    # Get the vocab size
    vocab_size = len(r_tokenizer)
    print("Vocab size: ", vocab_size)
    model = Transformer(vocab_size, 768, 8, 2048, 18, 1024, False, 8, device=device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")

    print('Model loaded.')


   
    print('Generating for prompt: ' + prompt)

    inputs = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True)
    input_ids = nn.utils.rnn.pad_sequence(inputs.input_ids, batch_first=True, padding_value=0)
    input_ids = input_ids.to(device)
    attention_mask =nn.utils.rnn.pad_sequence(inputs.attention_mask, batch_first=True, padding_value=0) 
    attention_mask = attention_mask.to(device)

    # Generate the midi
    output = model.generate(input_ids, attention_mask, max_len=250,temperature = 0.7)
    output_list = output[0].tolist()
    generated_midi = r_tokenizer.decode(output_list)
    generated_midi.dump_midi("output.mid")
    op="output.wav"
    convert_midi_to_wav("output.mid", op)
    #put text 2 midi code here 
    return op,"output.mid",prompt	


def notes_to_key(note_sequence):
    """
            Analyzes a sequence of notes and predicts the most likely musical key.
            Returns:
                - Predicted key (e.g., "C Major")
                - Confidence score (0-1)
                - All possible keys sorted by likelihood
    """
            # Remove octave numbers (e.g., "C4" → "C")
    pitch_classes = [note.split('-')[0] for note in note_sequence if note]
            
            # Music theory: Circle of Fifths profile for key detection
    KEY_PROFILES = {
                'C Major':   [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
                'C Minor':   [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17],
                'C# Major':  [2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29],
                'C# Minor':  [3.17, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34],
                'D Major':   [2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66],
                'D Minor':   [3.34, 3.17, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69],
                'D# Major':  [3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39],
                'D# Minor':  [2.69, 3.34, 3.17, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98],
                'E Major':   [2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19],
                'E Minor':   [3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75],
                'F Major':   [5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52],
                'F Minor':   [4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54],
                'F# Major':  [2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09],
                'F# Minor':  [2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53],
                'G Major':   [4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38],
                'G Minor':   [3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52, 5.38, 2.60],
                'G# Major':  [4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33],
                'G# Minor':  [2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52, 5.38],
                'A Major':   [2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48],
                'A Minor':   [5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52],
                'A# Major':  [3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23],
                'A# Minor':  [2.68, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68],
                'B Major':   [2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35],
                'B Minor':   [2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33],
                'Cb Major':  [2.88, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
            }
            
            # Count note occurrences
    note_counts = Counter(pitch_classes)
    total_notes = sum(note_counts.values())
            
            # Normalize to 12-dimensional vector (one per semitone)
    input_vector = np.zeros(12)
    for note, count in note_counts.items():
        semitone = librosa.note_to_midi(note) % 12
        input_vector[semitone] = count / total_notes
            
            # Compare against all keys using cosine similarity
    best_key = None
    best_score = -1
    all_scores = {}
            
    for key, profile in KEY_PROFILES.items():
        similarity = np.dot(input_vector, profile) / (
                    np.linalg.norm(input_vector) * np.linalg.norm(profile))
        all_scores[key] = similarity
        if similarity > best_score:
            best_score = similarity
            best_key = key
            
            # Sort keys by confidence
    sorted_keys = sorted(all_scores.items(), key=lambda x: -x[1])
            
    return best_key, best_score, sorted_keys
def process_humming(audio_file,genre_str,instruments):
            y, sr = librosa.load(audio_file, duration=30)
            
            features = {}
            
            # Pitch analysis with CREPE
            time, frequency, confidence,a = crepe.predict(y, sr, viterbi=True)

            # Convert frequencies to note names with octaves
            note_names = []
            for freq in frequency:
                if not np.isnan(freq):
                    note_num = 12 * (np.log2(freq) - np.log2(440.0)) + 69
                    note_names.append(librosa.midi_to_note(int(round(note_num)), unicode=False))
                else:
                    note_names.append(None)
            
            # Note segmentation using note transitions
            note_sequence = []
            current_note = None
            start_time = 0
            
            for i, (time_point, note) in enumerate(zip(time, note_names)):
                if note != current_note:
                    if current_note is not None:
                        duration = time_point - start_time
                        if duration > 0.08:  # 80ms minimum note duration
                            note_sequence.append({
                                'note': current_note,
                                'start': start_time,
                                'end': time_point,
                                'duration': duration
                            })
                    current_note = note
                    start_time = time_point
            
            # Post-processing: Merge nearby same notes
            merged_sequence = []
            for i, note in enumerate(note_sequence):
                if i > 0 and note['note'] == merged_sequence[-1]['note']:
                    if note['start'] - merged_sequence[-1]['end'] < 0.1:  # 100ms gap threshold
                        merged_sequence[-1]['end'] = note['end']
                        merged_sequence[-1]['duration'] += note['duration']
                        continue
                merged_sequence.append(note)
            detected_nodes=[]
            for note in merged_sequence[:10]:  # Print first 10 notes
                detected_nodes.append(note['note'])
            valid_pitches = frequency[confidence > 0.6]
            
            # Melodic features
            features['pitch_mean'] = np.mean(valid_pitches)
            features['pitch_std'] = np.std(valid_pitches)
            features['melody_contour'] = np.mean(np.diff(valid_pitches))
            
            # Rhythmic features
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = tempo
            
            # Timbre analysis
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            features['brightness'] = spectral_centroid
            
            # Dynamics
            rms = librosa.feature.rms(y=y)
            features['dynamic_range'] = np.max(rms) - np.min(rms)
            
            # Map features to musical elements
            tempo_desc = "allegro" if features['tempo'] > 120 else "moderato" if features['tempo'] > 90 else "largo"
            dynamics = "expressive" if features['dynamic_range'] > 0.3 else "subtle"
            #getting the key
            key, score, sorted_keys = notes_to_key(detected_nodes)
            # Create a string representation of the key
            key_str = f"{key}"    
            # Create instrument string
            instrument_str = ""
            if "Auto" in instruments:
                instrument_str=""
            elif len(instruments) == 1:
                instrument_str = f"a solo {instruments[0]}"
            else:
                instrument_str = f"{', '.join(instruments[:-1])} and {instruments[-1]}"
            
            #Create genre string
            
            genre_str = f"a {genre_str}"

            prompt = f"An instrumental piece featuring {instrument_str} in {key_str} with {genre_str} genre. "
            prompt += f"{tempo_desc.capitalize()} tempo with {dynamics} dynamics. "
            prompt += f"Follows notes in the order: {' '.join(detected_nodes).lower()} "
            prompt += "Emphasize harmonic texture over rhythmic complexity."
            prompt = gemmini_prompt(prompt)
            wav_op,midi_op,prompt=generate_music(prompt)
            return wav_op,midi_op