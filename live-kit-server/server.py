from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pydub import AudioSegment
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS if needed

@app.route("/validate_audio", methods=["POST"])
def validate_audio():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400
    
    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_file)
        duration_seconds = len(audio) / 1000  # Get duration in seconds
        print(f"Duration received: {duration_seconds} seconds")

        # If duration exceeds 60 seconds, trim the audio
        if duration_seconds > 60:
            # Trim to the middle segment (e.g., middle 60 seconds)
            middle_start = (len(audio) // 2) - (30 * 1000)  # 30 seconds before the middle
            middle_end = (len(audio) // 2) + (30 * 1000)  # 30 seconds after the middle
            trimmed_audio = audio[middle_start:middle_end]
        else:
            trimmed_audio = audio

        # Save the trimmed audio into an in-memory byte stream
        trimmed_audio_io = io.BytesIO()
        trimmed_audio.export(trimmed_audio_io, format="wav")
        trimmed_audio_io.seek(0)

        # Return the trimmed audio as a response
        return send_file(trimmed_audio_io, mimetype="audio/wav", as_attachment=True, download_name="trimmed_audio.wav")

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)