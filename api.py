import os
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RapGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_text(self, prompt, model="gpt-4"):
        print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to write some fire lyrics... 🔥{Style.RESET_ALL}")
        chat_response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a creative assistant skilled in writing rap lyrics. When given a prompt, respond with a rap verse in the style requested."},
                    {"role": "user", "content": f"Write a rap verse based on this prompt: {prompt}"}
                ]
            }
        )
        chat_response.raise_for_status()
        return chat_response.json()["choices"][0]["message"]["content"].strip()

    def generate_speech(self, text, voice="alloy", high_quality=False):
        print("Generating speech from text...")
        tts_model = "tts-1-hd" if high_quality else "tts-1"
        speech_response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": tts_model,
                "voice": voice,
                "input": text
            },
            stream=True
        )
        speech_response.raise_for_status()
        return speech_response.iter_content(chunk_size=4096)

    def generate_spoken_audio(self, text, voice="alloy", model="gpt-4", high_quality=False):
        print(f"{Fore.CYAN}🐌💯 Yo, we're about to drop some sick beats for: '{text}'{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality} 🐌💯{Style.RESET_ALL}")

        generated_text = self.generate_text(text, model)
        print(f"Generated lyrics:\n{generated_text}\n")

        audio_stream = self.generate_speech(generated_text, voice, high_quality)
        
        print(f"{Fore.GREEN}🐌💯 Rap audio generated and ready to stream 🔥{Style.RESET_ALL}")
        
        return generated_text, audio_stream

def generate_spoken_audio(text, voice="alloy", model="gpt-4", high_quality=False):
    generator = RapGenerator(OPENAI_API_KEY)
    return generator.generate_spoken_audio(text, voice, model, high_quality)

