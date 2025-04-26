import aiohttp
import asyncio
import inspect
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the API URL from environment variables
API_URL = os.getenv("TTS_MIDDLEWARE_URL")

# Define the before_tts_cb function
async def before_tts_cb(agent, text_input) -> str:
    """
    Callback function to handle text processing before TTS (Text-to-Speech) synthesis.
    It validates the text input by calling the API to check the duration and trim the text
    if necessary.

    :param agent: The voice agent (unused in this case)
    :param text_input: The input text that will be processed
    :return: The processed text to be used by TTS
    """

    try:
        # First, resolve any awaitable input (but only once)
        if inspect.isawaitable(text_input):
            # Store the awaited result immediately
            text_input = await text_input
    except Exception as e:
        print(f"Error awaiting input: {e}")
        return str(text_input) if text_input else ""

    try:
        # If the input is an async generator, collect the chunks into a single string
        if hasattr(text_input, "__aiter__"):
            collected = []
            async for chunk in text_input:
                collected.append(chunk)
            text = "".join(collected)
        elif isinstance(text_input, str):
            text = text_input
        else:
            text = str(text_input)

        # Process the text (split into words and estimate the duration)
        words = text.split()
        estimated_duration = len(words) * 0.25  # Estimate duration (0.25 seconds per word)

        payload = {
            "text": text,
            "duration": estimated_duration
        }

        # Make an API request to the server to validate and possibly trim the text
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/validate_audio",  # Ensure this matches the endpoint in the Flask server
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5.0)
            ) as response:
                response.raise_for_status()  # Raise exception for HTTP error responses
                validated_data = await response.json()  # Get JSON response from server
                return str(validated_data.get("text", text))  # Return the processed text

    except Exception as e:
        print(f"Error in before_tts_cb: {e}")
        return str(text_input) if text_input else ""