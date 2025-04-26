from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")   # Enable CORS if needed

@app.route("/validate_audio", methods=["POST"])
def validate_audio():
    data = request.get_json()
    text = data.get("text", "")
    estimated_duration = data.get("duration", 0)  # ✅ CORRECT this line (use "duration" key)
    print('Duration received:', estimated_duration)

    if estimated_duration <= 60:
        return jsonify({"trimmed_text": text})

    words = text.split()
    mid = len(words) // 2
    trimmed = " ".join(words[mid - 25:mid + 25]) if len(words) > 50 else text
    return jsonify({"trimmed_text": trimmed})

if __name__ == "__main__":
    app.run(debug=True, port=5000)