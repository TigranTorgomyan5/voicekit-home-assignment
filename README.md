# VoiceKit Home Assignment

This repository contains the implementation of a voice assistant using LiveKit's Voice Pipeline Agent. The primary goal of the assignment was to integrate text-to-speech (TTS) functionality with audio validation and trimming, using a Flask backend to handle processing.

## Overview

The project includes:

1. **LiveKit Voice Pipeline Agent**: Integration with the LiveKit Voice Pipeline Agent to handle text-to-speech (TTS) conversion and manage the flow of audio data.
2. **Flask Backend**: A Flask server that processes incoming requests, validates audio durations, and trims audio when necessary.
3. **Environment Variables**: Configuration of API URLs using environment variables for better flexibility and security.

## Workflow

1. **Text Input**: The voice assistant accepts text input which is passed through the `before_tts_cb` callback function.
2. **Estimated Audio Duration**: The callback estimates the duration of the TTS audio based on word count (approximately 0.25 seconds per word) and sends this data to the Flask server for validation.
3. **Audio Validation**: The Flask server checks if the audio duration exceeds 60 seconds. If so, it trims the audio to the middle 60 seconds.
4. **Response**: The server returns the trimmed text or original text depending on the validation, which is then used for further processing.

## Setup

### Prerequisites

- Python 3.12+
- `pip` (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TigranTorgomyan5/voicekit-home-assignment.git
   cd voicekit-home-assignment

## Dependencies

This project utilizes the following repositories for the LiveKit integration:

- **LiveKit Backend**: The backend implementation for the voice assistant using LiveKit's Voice Pipeline Agent. 
  - Repository: [voice-pipeline-agent-python](https://github.com/livekit-examples/voice-pipeline-agent-python)
  - Install the necessary libraries by following the installation instructions in the repository.

- **LiveKit Frontend**: The frontend implementation of the voice assistant.
  - Repository: [voice-assistant-frontend](https://github.com/livekit-examples/voice-assistant-frontend)
  - Install the necessary libraries by following the installation instructions in the repository.

Make sure to check the respective documentation in each repository to install and set up the required dependencies for both the backend and frontend.
