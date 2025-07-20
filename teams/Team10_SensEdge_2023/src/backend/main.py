from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import tempfile
import os
import threading
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import json
import tensorflow as tf
import time
import math
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('sensedge-b82a0-firebase-adminsdk-fbsvc-ed9e7ae481.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Global Variables
is_recording = False
is_gesture_running = False
audio_buffer = []
current_class_code = None


# ------------------- Speech to Text -------------------

def record_audio():
    global is_recording, audio_buffer, current_class_code
    duration = 10
    sample_rate = 16000
    recognizer = sr.Recognizer()

    while is_recording:
        audio_chunk = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()

        audio_buffer.append(audio_chunk)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            sf.write(temp_audio.name, audio_chunk, sample_rate)
            temp_audio_path = temp_audio.name

        try:
            with sr.AudioFile(temp_audio_path) as source:
                audio = recognizer.record(source)
                transcribed_text = recognizer.recognize_google(audio)

                print(f"Transcribed Text: {transcribed_text}")

                db.collection('chat').add({
                    'classCode': current_class_code,
                    'spokenText': transcribed_text,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                })

        except Exception as e:
            print(f"Error in transcription: {e}")

        os.remove(temp_audio_path)

def start_recording():
    global is_recording
    is_recording = True
    threading.Thread(target=record_audio).start()

def stop_recording():
    global is_recording
    is_recording = False
    print("Recording stopped.")


@app.route('/start_recording', methods=['POST'])
def start_recording_route():
    try:
        data = request.json
        class_code = data.get('class_code')
        if not class_code:
            return jsonify({'error': 'Class code is required'}), 400

        global current_class_code
        current_class_code = class_code

        start_recording()
        return jsonify({'message': 'Recording started', 'class_code': class_code}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_recording', methods=['POST'])
def stop_recording_route():
    try:
        stop_recording()
        return jsonify({'message': 'Recording stopped'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- Gesture Recognition (Webcam Live) -------------------
    
def run_gesture_recognition():
    global is_gesture_running, current_class_code

    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    offset = 20
    imgSize = 300
    labels = ["Call", "Hello", "Love", "Luck", "No", "Okay", "Peace", "Yes"]

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    time.sleep(2)  # Let camera initialize

    print("🎥 Gesture recognition started...")

    while is_gesture_running:
        success, img = cap.read()
        if not success:
            print("❌ Error: Failed to read frame from webcam.")
            break

        hands, img = detector.findHands(img)
        label = "Detecting..."

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            y1 = max(0, y - offset)
            y2 = min(img.shape[0], y + h + offset)
            x1 = max(0, x - offset)
            x2 = min(img.shape[1], x + w + offset)
            imgCrop = img[y1:y2, x1:x2]

            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wGap + wCal] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hGap + hCal, :] = imgResize

            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            label = labels[index] if index < len(labels) else "Unknown"
            print("🖐 Predicted Gesture:", label)

            # Store prediction in Firestore
            db.collection('chat').add({
                'classCode': current_class_code,
                'spokenText': label,
                'timestamp': firestore.SERVER_TIMESTAMP,
            })

        # Display label on image
        cv2.putText(img, f"Gesture: {label}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        # Show the webcam window
        cv2.imshow("Gesture Recognition", img)

        # Break loop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_gesture_running = False
            break

    cap.release()
    cv2.destroyAllWindows()
    print("🛑 Gesture recognition stopped.")



@app.route('/start_gesture', methods=['POST'])
def start_gesture_route():
    try:
        data = request.json
        class_code = data.get('class_code')
        if not class_code:
            return jsonify({'error': 'Class code is required'}), 400

        global current_class_code, is_gesture_running
        current_class_code = class_code
        is_gesture_running = True

        # Start gesture recognition in a separate thread
        thread=threading.Thread(target=run_gesture_recognition)
        thread.start()
        return jsonify({'message': 'Gesture recognition started', 'class_code': class_code}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stop_gesture', methods=['POST'])
def stop_gesture_route():
    global is_gesture_running
    is_gesture_running = False
    return jsonify({'message': 'Gesture recognition stopped'}), 200
# ------------------- Run App -------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
