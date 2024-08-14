import openai
import os
import sounddevice as sd
from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO
import soundfile as sf

load_dotenv()

def generate_spoken_audio(text, voice="alloy", model="text-davinci-003"):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    response = openai.Completion.create(
        engine=model,
        prompt=text,
        max_tokens=100
    )

    generated_text = response.choices[0].text.strip()

    tts = gTTS(generated_text)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    audio_data, samplerate = sf.read(audio_fp)

    # Play the audio stream using sounddevice
    sd.play(audio_data, samplerate=samplerate)
    sd.wait()  # Wait until the audio is finished playing
