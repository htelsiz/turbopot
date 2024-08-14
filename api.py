import os
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ContentGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_text(self, prompt, model="gpt-4"):
        print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to create some amazing content... 🔥{Style.RESET_ALL}")
        chat_response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a creative assistant skilled in generating various types of content. When given a prompt, respond with appropriate content in the style requested. If no specific style or content type is mentioned, create engaging and informative content that best fits the prompt."},
                    {"role": "user", "content": f"Generate content based on this prompt: {prompt}"}
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

    def generate_spoken_content(self, text, voice="alloy", model="gpt-4", high_quality=False):
        print(f"{Fore.CYAN}🐌💯 We're about to create some amazing content for: '{text}'{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality} 🐌💯{Style.RESET_ALL}")

        generated_text = self.generate_text(text, model)
        print(f"Generated content:\n{generated_text}\n")

        audio_stream = self.generate_speech(generated_text, voice, high_quality)
        
        print(f"{Fore.GREEN}🐌💯 Content audio generated and ready to stream 🔥{Style.RESET_ALL}")
        
        return generated_text, audio_stream

def generate_spoken_content(text, voice="alloy", model="gpt-4", high_quality=False):
    generator = ContentGenerator(OPENAI_API_KEY)
    return generator.generate_spoken_content(text, voice, model, high_quality)

