from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/validate_audio", methods=["POST"])
def validate_audio():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data["text"]
        duration = data.get("duration", 0)

        print(f"Received text (duration={duration} seconds): {text}")

        if duration > 60:
            words = text.split()
            half = len(words) // 2
            trimmed_words = words[half-75:half+75]  # Middle 150 words
            trimmed_text = " ".join(trimmed_words)
            return jsonify({"text": trimmed_text})
        else:
            return jsonify({"text": text})

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)