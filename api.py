import os
from openai import OpenAI
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()

class ContentGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, prompt, content_type="general", model="gpt-4"):
        print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to create some amazing {content_type} content... 🔥{Style.RESET_ALL}")
        try:
            chat_response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a creative assistant skilled in generating various types of content. You are now tasked with creating {content_type} content. Respond with appropriate content in the style and format typical for {content_type}."},
                    {"role": "user", "content": f"Generate {content_type} content based on this prompt: {prompt}"}
                ]
            )
            return chat_response.choices[0].message.content.strip()
        except Exception as e:
            print(f"{Fore.RED}Error generating text: {str(e)}{Style.RESET_ALL}")
            raise

    def generate_speech(self, text, voice="alloy", high_quality=False):
        print("Generating speech from text...")
        tts_model = "tts-1-hd" if high_quality else "tts-1"
        try:
            speech_response = self.client.audio.speech.create(
                model=tts_model,
                voice=voice,
                input=text
            )
            return speech_response.content
        except Exception as e:
            print(f"{Fore.RED}Error generating speech: {str(e)}{Style.RESET_ALL}")
            raise

    def generate_spoken_content(self, text, content_type="general", voice="alloy", model="gpt-4", high_quality=False):
        print(f"{Fore.CYAN}🐌💯 We're about to create some amazing {content_type} content for: '{text}'{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality} 🐌💯{Style.RESET_ALL}")

        generated_text = self.generate_text(text, content_type, model)
        print(f"Generated content:\n{generated_text}\n")

        audio_content = self.generate_speech(generated_text, voice, high_quality)
        
        print(f"{Fore.GREEN}🐌💯 Content audio generated and ready to stream 🔥{Style.RESET_ALL}")
        
        return generated_text, audio_content

def generate_spoken_content(text, content_type="general", voice="alloy", model="gpt-4", high_quality=False):
    generator = ContentGenerator(os.getenv("OPENAI_API_KEY"))
    return generator.generate_spoken_content(text, content_type, voice, model, high_quality)

