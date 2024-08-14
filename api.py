import os
import requests
import json
import subprocess
import psutil
import time
import signal
from dotenv import load_dotenv
import io
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_spoken_audio(text, voice="alloy", model="gpt-4", high_quality=False, timeout=60):
    print(f"{Fore.CYAN}🎤 Yo, we're about to drop some sick beats for: '{text}'{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality}{Style.RESET_ALL}")

    # Check content moderation
    print(f"{Fore.YELLOW}🕵️ Checking if this content is family-friendly...{Style.RESET_ALL}")
    start_time = time.time()
    if moderate_content(text):
        print(f"{Fore.RED}🚫 Whoa there! This content's too spicy for our PG-13 rap battle. Keep it clean, fam!{Style.RESET_ALL}")
        return None
    print(f"{Fore.GREEN}✅ Content's clean as a whistle! Time taken: {time.time() - start_time:.2f} seconds{Style.RESET_ALL}")

    # Generate text response
    print(f"{Fore.BLUE}🧠 AI's putting on its thinking cap to write some fire lyrics...{Style.RESET_ALL}")
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
        
        def signal_handler(signum, frame):
            print("\nInterrupted by user. Stopping audio playback...")
            if 'ffplay_process' in locals():
                ffplay_process.terminate()
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, signal_handler)

        try:
            print("Streaming audio directly from OpenAI")
            ffplay_process = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Show streaming processes right after starting ffplay
            show_streaming_processes()

            # Stream the audio data to ffplay
            start_time = time.time()
            for chunk in speech_response.iter_content(chunk_size=4096):
                if chunk:
                    ffplay_process.stdin.write(chunk)
                if time.time() - start_time > timeout:
                    print(f"Playback timeout after {timeout} seconds.")
                    break

            ffplay_process.stdin.close()

            try:
                ffplay_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("FFplay process did not terminate in time. Forcing termination.")
                ffplay_process.terminate()

            stdout, stderr = ffplay_process.communicate()
            print("FFplay output:")
            print(stdout.decode())
            if stderr:
                print("FFplay errors:")
                print(stderr.decode())

        except KeyboardInterrupt:
            print("Playback interrupted by user.")
        except Exception as e:
            print(f"Error during audio playback: {e}")
        
        print(f"Audio playback finished. Time taken: {time.time() - start_time:.2f} seconds")
        show_streaming_processes()

    return generated_text


def moderate_content(text):
    print(f"{Fore.YELLOW}🔍 Scanning for any naughty words...{Style.RESET_ALL}")
    moderation_response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"input": text}
    )
    moderation_response.raise_for_status()
    result = moderation_response.json()["results"][0]["flagged"]
    if result:
        print(f"{Fore.RED}😱 Oops! Looks like someone's been watching too many explicit music videos!{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}😇 All clear! This content is as pure as freshly fallen snow.{Style.RESET_ALL}")
    return result

def show_streaming_processes():
    print(f"{Fore.CYAN}🎵 DJ Check! Who's spinning the tracks right now?{Style.RESET_ALL}")
    streaming_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
        try:
            if 'ffplay' in proc.info['name'].lower() or 'ffmpeg' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else 'N/A'
                status = proc.info['status']
                streaming_processes.append(f"🎧 PID: {proc.info['pid']}, DJ Name: {proc.info['name']}, Vibe Status: {status}, Playlist: {cmdline}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            print(f"{Fore.RED}😱 Yo, we hit a snag checking the DJ booth: {e}{Style.RESET_ALL}")
    
    if streaming_processes:
        for process in streaming_processes:
            print(f"{Fore.GREEN}{process}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}😴 Looks like the party hasn't started yet. No DJs in the house!{Style.RESET_ALL}")
    print()

