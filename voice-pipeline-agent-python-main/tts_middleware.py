import inspect
import aiohttp

async def before_tts_cb(agent, text_input) -> str:
    # First, resolve any awaitable input (but only once)
    try:
        if inspect.isawaitable(text_input):
            # Store the awaited result immediately
            text_input = await text_input
    except Exception as e:
        print(f"Error awaiting input: {e}")
        return str(text_input) if text_input else ""

    # Now handle the resolved input
    try:
        if hasattr(text_input, "__aiter__"):
            # Handle async generator
            collected = []
            async for chunk in text_input:
                collected.append(chunk)
            text = "".join(collected)
        elif isinstance(text_input, str):
            text = text_input
        else:
            text = str(text_input)

        # Rest of your processing
        words = text.split()
        estimated_duration = len(words) * 0.25

        payload = {
            "text": text,
            "duration": estimated_duration
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://64cd-5-77-204-166.ngrok-free.app",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5.0)
            ) as response:
                response.raise_for_status()
                validated_data = await response.json()
                return str(validated_data.get("text", text))

    except Exception as e:
        print(f"Error in before_tts_cb: {e}")
        return str(text_input) if text_input else ""