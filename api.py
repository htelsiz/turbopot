import os
import requests
import json
import subprocess
import psutil
import time
from dotenv import load_dotenv
import io

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
    with requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": tts_model,
            "voice": voice,
            "input": generated_text
        },
        stream=True
    ) as speech_response:
        speech_response.raise_for_status()
        print(f"Speech generated. Time taken: {time.time() - start_time:.2f} seconds")

        # Play the audio using ffplay
        print("Starting audio playback...")
        show_streaming_processes()
        start_time = time.time()
        
        try:
            print("Streaming audio directly from OpenAI")
            ffplay_process = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Stream the audio data to ffplay
            for chunk in speech_response.iter_content(chunk_size=4096):
                if chunk:
                    ffplay_process.stdin.write(chunk)
            
            ffplay_process.stdin.close()
            ffplay_process.wait()

            stdout, stderr = ffplay_process.communicate()
            print("FFplay output:")
            print(stdout.decode())
            if stderr:
                print("FFplay errors:")
                print(stderr.decode())

        except Exception as e:
            print(f"Error during audio playback: {e}")
        
        print(f"Audio playback finished. Time taken: {time.time() - start_time:.2f} seconds")
        show_streaming_processes()

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
    streaming_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'ffplay' in proc.info['name'].lower() or 'ffmpeg' in proc.info['name'].lower():
                streaming_processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Command: {' '.join(proc.info['cmdline'])}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if streaming_processes:
        for process in streaming_processes:
            print(process)
    else:
        print("No streaming processes found.")
    print()

