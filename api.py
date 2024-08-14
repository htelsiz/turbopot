import os
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_spoken_audio(text, voice="alloy", model="gpt-4", high_quality=False):
    print(f"{Fore.CYAN}🐌💯 Yo, we're about to drop some sick beats for: '{text}' 🔥{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality} 🐌💯{Style.RESET_ALL}")

    # Generate text response
    print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to write some fire lyrics... 🔥{Style.RESET_ALL}")

def generate_story(prompt, genre="fantasy", length="short", model="gpt-4"):
    print(f"{Fore.CYAN}🐌💯 Crafting a {length} {genre} story based on: '{prompt}' 🔥{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Using model: {model} 🐌💯{Style.RESET_ALL}")

    # Generate story
    print(f"{Fore.BLUE}🐌💯 AI's weaving a tale... 🔥{Style.RESET_ALL}")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            chat_response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": f"You are a creative assistant skilled in writing {length} {genre} stories. When given a prompt, respond with a story in the requested style."},
                        {"role": "user", "content": f"Write a {length} {genre} story based on this prompt: {prompt}"}
                    ]
                },
                timeout=30  # Add a timeout to prevent hanging
            )
            chat_response.raise_for_status()
            generated_story = chat_response.json()["choices"][0]["message"]["content"].strip()
            print(f"{Fore.GREEN}🐌💯 Story generated successfully!{Style.RESET_ALL}")
            return generated_story
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}🐌💯 Error generating story (attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}")
            if attempt == max_retries - 1:
                raise Exception(f"Failed to generate story after {max_retries} attempts. Last error: {str(e)}")
        except Exception as e:
            print(f"{Fore.RED}🐌💯 Unexpected error (attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}")
            if attempt == max_retries - 1:
                raise Exception(f"Unexpected error after {max_retries} attempts. Last error: {str(e)}")

def generate_spoken_audio(text, voice="alloy", model="gpt-4", high_quality=False):
    print(f"{Fore.CYAN}🐌💯 Yo, we're about to drop some sick beats for: '{text}'{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality} 🐌💯{Style.RESET_ALL}")

    # Generate text response
    print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to write some fire lyrics... 🔥{Style.RESET_ALL}")
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
    print(f"Generated lyrics:\n{generated_text}\n")

    # Generate speech from the text
    print("Generating speech from text...")
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
        },
        stream=True
    )
    speech_response.raise_for_status()
    
    print(f"{Fore.GREEN}🐌💯 Rap audio generated and ready to stream 🔥{Style.RESET_ALL}")
    
    return generated_text, speech_response.iter_content(chunk_size=4096)

