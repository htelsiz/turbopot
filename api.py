import openai
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import hashlib
import os
from some_tts_library import tts_generate  # Assuming this is the TTS library you are using

def generate_spoken_audio(text, voice="alloy", model="tts-1", output_format="mp3"):
    # Hash the text to create a unique filename
    hash_object = hashlib.md5(text.encode())
    filename = f"{hash_object.hexdigest()}.{output_format}"
    
    # Check if the file already exists
    if not os.path.exists(filename):
        # Generate the audio file
        tts_generate(text, voice=voice, model=model, output_file=filename)
    
    return filename
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
