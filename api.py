import os
import requests
import json
import subprocess
import psutil
import time
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_spoken_audio(text, voice="alloy", model="gpt-4", high_quality=False):
    print(f"Generating spoken audio for prompt: '{text}'")
    print(f"Using voice: {voice}, model: {model}, high quality: {high_quality}")

    # Check content moderation
    print("Checking content moderation...")
    start_time = time.time()
    if moderate_content(text):
        print("Input content flagged as inappropriate. Cannot process request.")
        return None
    print(f"Content moderation passed. Time taken: {time.time() - start_time:.2f} seconds")

    # Generate text response
    print("Generating rap lyrics...")
    start_time = time.time()
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
    print(f"Rap lyrics generated. Time taken: {time.time() - start_time:.2f} seconds")
    print(f"Generated lyrics:\n{generated_text}\n")

    # Check moderation for generated text
    print("Checking moderation for generated text...")
    start_time = time.time()
    if moderate_content(generated_text):
        print("Generated content flagged as inappropriate. Cannot create audio.")
        return None
    print(f"Content moderation passed. Time taken: {time.time() - start_time:.2f} seconds")

    # Generate speech from the text
    print("Generating speech from text...")
    start_time = time.time()
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
    print(f"Speech generated. Time taken: {time.time() - start_time:.2f} seconds")

    # Save the audio to a temporary file
    temp_file = "temp_speech.mp3"
    with open(temp_file, "wb") as f:
        f.write(speech_response.content)
    print(f"Audio saved to temporary file: {temp_file}")

    # Play the audio using ffmpeg
    print("Starting audio playback...")
    show_streaming_processes()
    start_time = time.time()
    subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Audio playback finished. Time taken: {time.time() - start_time:.2f} seconds")
    show_streaming_processes()

    # Clean up
    os.remove(temp_file)
    print(f"Temporary file {temp_file} removed.")

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

