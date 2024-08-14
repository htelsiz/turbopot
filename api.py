import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from colorama import init, Fore, Style
import time

# Initialize colorama
init(autoreset=True)

load_dotenv()

class ContentGenerator:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_text_stream(self, prompt, content_type="general", model="gpt-4", max_length=None):
        print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to create some amazing {content_type} content... 🔥{Style.RESET_ALL}")
        try:
            messages = [
                {"role": "system", "content": f"You are a creative assistant skilled in generating various types of content. You are now tasked with creating {content_type} content. Respond with appropriate content in the style and format typical for {content_type}."},
                {"role": "user", "content": f"Generate {content_type} content based on this prompt: {prompt}"}
            ]
            if max_length:
                messages[0]["content"] += f" Your response must not exceed {max_length} characters."
            
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=max_length // 4 if max_length else None  # Approximate token limit based on character limit
            )
            
            print(f"{Fore.YELLOW}Streaming content:{Style.RESET_ALL}")
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
            print("\n")  # Add a newline after the content
        except Exception as e:
            print(f"{Fore.RED}Error generating text: {str(e)}{Style.RESET_ALL}")
            raise

    async def generate_speech_stream(self, text, voice="alloy", high_quality=False):
        print("Generating speech from text...")
        tts_model = "tts-1-hd" if high_quality else "tts-1"
        try:
            speech_response = await self.client.audio.speech.create(
                model=tts_model,
                voice=voice,
                input=text
            )
            content = speech_response.content
            chunk_size = 1024
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i+chunk_size]
                yield chunk
        except Exception as e:
            print(f"{Fore.RED}Error generating speech: {str(e)}{Style.RESET_ALL}")
            raise

    async def generate_spoken_content_stream(self, text, content_type="general", voice="alloy", model="gpt-4", high_quality=False, max_length=None):
        print(f"{Fore.CYAN}🐌💯 We're about to create some amazing {content_type} content for: '{text}'{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality}, max length: {max_length if max_length else 'unlimited'} 🐌💯{Style.RESET_ALL}")

        start_time = time.time()
        text_stream = self.generate_text_stream(text, content_type, model, max_length)
        
        generated_text = ""
        async for content in text_stream:
            generated_text += content
            yield ("text", content)

        async for chunk in self.generate_speech_stream(generated_text, voice, high_quality):
            yield ("audio", chunk)

        end_time = time.time()
        print(f"{Fore.GREEN}🐌💯 Content audio generated and streamed 🔥{Style.RESET_ALL}")
        print(f"Total generation time: {end_time - start_time:.2f} seconds")

async def generate_spoken_content_stream(text, content_type="general", voice="alloy", model="gpt-4", high_quality=False, max_length=None):
    generator = ContentGenerator(os.getenv("OPENAI_API_KEY"))
    async for chunk_type, chunk in generator.generate_spoken_content_stream(text, content_type, voice, model, high_quality, max_length):
        yield chunk_type, chunk

