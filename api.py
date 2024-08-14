import os
import requests
import json
import subprocess
import psutil
from dotenv import load_dotenv

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
                {"role": "system", "content": "You are a creative assistant skilled in writing rap lyrics. When given a prompt, respond with a rap verse in the style requested."},
                {"role": "user", "content": f"Write a rap verse based on this prompt: {text}"}
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

    # Play the audio using ffmpeg
    print("Starting audio playback...")
    show_streaming_processes()
    subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Audio playback finished.")
    show_streaming_processes()

    # Clean up
    os.remove(temp_file)

    return generated_text


def moderate_content(text):
    moderation_response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"input": text}
    )
    moderation_response.raise_for_status()
    return moderation_response.json()["results"][0]["flagged"]

def show_streaming_processes():
    print("Current streaming processes:")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'ffplay' in proc.info['name'].lower() or 'ffmpeg' in proc.info['name'].lower():
                print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Command: {' '.join(proc.info['cmdline'])}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print()

