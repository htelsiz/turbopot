import openai
import os
from io import BytesIO
from gtts import gTTS
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()
# Set up the OpenAI client
if hasattr(openai, 'OpenAI'):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai

def generate_spoken_audio(text, voice="alloy", model="gpt-4-turbo-preview"):
    response = client.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )

    generated_text = response.choices[0].message.content.strip()

    tts = gTTS(generated_text)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    audio = AudioSegment.from_file(audio_fp, format="mp3")

    # Play the audio using pydub
    play(audio)
