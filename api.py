import openai
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

def generate_spoken_audio(text, voice="alloy", model="gpt-3.5-turbo"):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )

    generated_text = response.choices[0].message['content'].strip()

    response = openai.Audio.create(
        model="text-to-speech",
        input=generated_text,
        voice=voice
    )

    audio_content = response['audio_content']
    audio_fp = BytesIO(audio_content)
    audio = AudioSegment.from_file(audio_fp, format="mp3")

    # Play the audio using pydub
    play(audio)
