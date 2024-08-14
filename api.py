import openai
import os
import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

def generate_spoken_audio(text, voice="alloy", model="tts-1"):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    response = openai.Audio.create(
        model=model,
        voice=voice,
        input=text
    )

    audio_stream = response['audio']

    # Play the audio stream using sounddevice
    sd.play(audio_stream, samplerate=22050)
    sd.wait()  # Wait until the audio is finished playing
