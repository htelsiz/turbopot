import openai
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import hashlib
import os

def generate_spoken_audio(text, voice="alloy", model="tts-1", output_format="mp3"):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    response = openai.Audio.create(
        model=model,
        voice=voice,
        input=text
    )

    speech_file_path = Path(__file__).parent / f"speech.{output_format}"
    with open(speech_file_path, "wb") as f:
        f.write(response['audio'])

    return speech_file_path
