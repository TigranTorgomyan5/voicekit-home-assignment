import requests

text = "This is a test sentence. " * 300

payload = {
    "text": text,
    "duration": 75
}

url = "https://9de7-5-77-204-166.ngrok-free.app/validate_audio"

response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

if response.ok:
    result = response.json().get("trimmed_text")
    print("✅ Server responded with trimmed text:")
    print(result)
else:
    print("❌ Server error:", response.status_code, response.text)