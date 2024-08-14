import os
import requests
import json
from dotenv import load_dotenv
import pygame

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_spoken_audio(text, voice="alloy", model="gpt-4", high_quality=False):
    # Check content moderation
    if moderate_content(text):
        print("Input content flagged as inappropriate. Cannot process request.")
        return None

    # Generate text response
    chat_response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ]
        }
    )
    chat_response.raise_for_status()
    generated_text = chat_response.json()["choices"][0]["message"]["content"].strip()

    # Check moderation for generated text
    if moderate_content(generated_text):
        print("Generated content flagged as inappropriate. Cannot create audio.")
        return None

    # Generate speech from the text
    tts_model = "tts-1-hd" if high_quality else "tts-1"
    speech_response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": tts_model,
            "voice": voice,
            "input": generated_text
        }
    )
    speech_response.raise_for_status()

    # Save the audio to a temporary file
    temp_file = "temp_speech.mp3"
    with open(temp_file, "wb") as f:
        f.write(speech_response.content)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.quit()
    os.remove(temp_file)

    return generated_text


