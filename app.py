from flask import Flask, request, render_template, send_file
from spleeter.separator import Separator
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import librosa
import soundfile as sf
import os

app = Flask(__name__)

# Define the index route
@app.route('/')
def index():
    return render_template('index.html')

# Define the route to handle audio enhancement
@app.route('/enhance_audio', methods=['POST'])
def enhance_audio_route():
    if 'audio_file' not in request.files:
        return "No file uploaded!", 400
    
    # Get uploaded file
    audio_file = request.files['audio_file']
    file_path = f"uploads/{audio_file.filename}"
    audio_file.save(file_path)

    # Run enhancement
    enhanced_audio_path = enhance_audio(file_path)
    
    # Send the enhanced file back to the user
    return send_file(enhanced_audio_path, as_attachment=True)

def load_audio(file_path):
    """Load audio using librosa."""
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr

def save_audio(file_path, audio, sr):
    """Save audio using soundfile."""
    sf.write(file_path, audio, sr)

def isolate_voice(file_path):
    """Isolate the voice using Spleeter."""
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(file_path, 'output')
    return 'output/' + file_path.split('/')[-1].replace('.mp3', '/vocals.wav')

def reduce_noise(audio, sr):
    """Reduce noise using noisereduce library."""
    return nr.reduce_noise(y=audio, sr=sr)

def enhance_audio(file_path):
    # Load audio
    audio, sr = load_audio(file_path)

    # Reduce noise
    noise_reduced_audio = reduce_noise(audio, sr)

    # Isolate voice
    vocals_path = isolate_voice(file_path)
    vocals, sr_vocals = load_audio(vocals_path)

    # Basic equalization and compression
    equalized_vocals = vocals * 1.2  # Apply basic equalization
    compressed_vocals = np.clip(equalized_vocals, -0.5, 0.5)  # Apply basic compression

    # Save enhanced audio
    output_path = "enhanced_audio.wav"
    save_audio(output_path, compressed_vocals, sr_vocals)

    print("Enhanced audio saved at:", output_path)
    return output_path

if __name__ == "__main__":
    # Ensure upload directory exists
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
