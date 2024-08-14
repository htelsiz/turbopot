import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from colorama import init, Fore, Style
from functools import lru_cache
import time

# Initialize colorama
init(autoreset=True)

load_dotenv()

class ContentGenerator:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_text(self, prompt, content_type="general", model="gpt-4"):
        print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to create some amazing {content_type} content... 🔥{Style.RESET_ALL}")
        try:
            chat_response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": f"You are a creative assistant skilled in generating various types of content. You are now tasked with creating {content_type} content. Respond with appropriate content in the style and format typical for {content_type}."},
                        {"role": "user", "content": f"Generate {content_type} content based on this prompt: {prompt}"}
                    ]
                ),
                timeout=30  # 30 seconds timeout
            )
            return chat_response.choices[0].message.content.strip()
        except asyncio.TimeoutError:
            print(f"{Fore.RED}Error: API call timed out{Style.RESET_ALL}")
            raise
        except Exception as e:
            print(f"{Fore.RED}Error generating text: {str(e)}{Style.RESET_ALL}")
            raise

    async def generate_speech(self, text, voice="alloy", high_quality=False):
        print("Generating speech from text...")
        tts_model = "tts-1-hd" if high_quality else "tts-1"
        try:
            speech_response = await asyncio.wait_for(
                self.client.audio.speech.create(
                    model=tts_model,
                    voice=voice,
                    input=text
                ),
                timeout=30  # 30 seconds timeout
            )
            return speech_response.content
        except asyncio.TimeoutError:
            print(f"{Fore.RED}Error: API call timed out{Style.RESET_ALL}")
            raise
        except Exception as e:
            print(f"{Fore.RED}Error generating speech: {str(e)}{Style.RESET_ALL}")
            raise

    @lru_cache(maxsize=100)
    def _cache_key(self, text, content_type, voice, model, high_quality):
        return f"{text}:{content_type}:{voice}:{model}:{high_quality}"

    async def generate_spoken_content(self, text, content_type="general", voice="alloy", model="gpt-4", high_quality=False):
        cache_key = self._cache_key(text, content_type, voice, model, high_quality)
        cached_result = self._cache_key.cache_get(cache_key)
        if cached_result is not None:
            print(f"{Fore.GREEN}🐌💯 Returning cached content 🔥{Style.RESET_ALL}")
            return cached_result

        print(f"{Fore.CYAN}🐌💯 We're about to create some amazing {content_type} content for: '{text}'{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality} 🐌💯{Style.RESET_ALL}")

        start_time = time.time()
        text_task = asyncio.create_task(self.generate_text(text, content_type, model))
        generated_text, audio_content = await asyncio.gather(
            text_task,
            self.generate_speech(await text_task, voice, high_quality)
        )
        end_time = time.time()

        print(f"Generated content:\n{generated_text}\n")
        print(f"{Fore.GREEN}🐌💯 Content audio generated and ready to stream 🔥{Style.RESET_ALL}")
        print(f"Total generation time: {end_time - start_time:.2f} seconds")

        result = (generated_text, audio_content)
        self._cache_key.cache_set(cache_key, result)
        return result

async def generate_spoken_content(text, content_type="general", voice="alloy", model="gpt-4", high_quality=False):
    generator = ContentGenerator(os.getenv("OPENAI_API_KEY"))
    return await generator.generate_spoken_content(text, content_type, voice, model, high_quality)

