import openai
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def generate_spoken_audio(text, voice="alloy", model="tts-1", output_format="mp3"):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    client = openai.OpenAI(api_key=api_key)
    speech_file_path = Path(__file__).parent / f"speech.{output_format}"
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    with open(speech_file_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    return speech_file_path
