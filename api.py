import openai
import os
import pyaudio
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

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True)

    # Play the audio stream
    stream.write(audio_stream)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
