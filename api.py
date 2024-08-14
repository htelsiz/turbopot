import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from colorama import init, Fore, Style
import time
import logging

# Initialize colorama
init(autoreset=True)

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_text_stream(self, prompt, content_type="general", model="gpt-4", max_length=None):
        logger.info(f"Starting text generation for {content_type} content")
        print(f"{Fore.BLUE}🐌💯 AI's putting on its thinking cap to create some amazing {content_type} content... 🔥{Style.RESET_ALL}")
        try:
            messages = [
                {"role": "system", "content": f"You are a creative assistant skilled in generating various types of content. You are now tasked with creating {content_type} content. Respond with appropriate content in the style and format typical for {content_type}."},
                {"role": "user", "content": f"Generate {content_type} content based on this prompt: {prompt}"}
            ]
            if max_length:
                messages[0]["content"] += f" Your response must not exceed {max_length} characters."
            
            logger.debug(f"Creating chat completion with model: {model}, max_length: {max_length}")
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=max_length // 4 if max_length else None  # Approximate token limit based on character limit
            )
            
            print(f"{Fore.YELLOW}Streaming content:{Style.RESET_ALL}")
            logger.debug("Starting to stream content")
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    logger.debug(f"Received content chunk: {chunk.choices[0].delta.content}")
                    yield chunk.choices[0].delta.content
            print("\n")  # Add a newline after the content
            logger.info("Text generation completed")
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}", exc_info=True)
            print(f"{Fore.RED}Error generating text: {str(e)}{Style.RESET_ALL}")
            raise

    async def generate_speech_stream(self, text, voice="alloy", high_quality=False):
        logger.info(f"Starting speech generation with voice: {voice}, high_quality: {high_quality}")
        print("Generating speech from text...")
        tts_model = "tts-1-hd" if high_quality else "tts-1"
        try:
            logger.debug(f"Creating speech with model: {tts_model}")
            speech_response = await self.client.audio.speech.create(
                model=tts_model,
                voice=voice,
                input=text
            )
            logger.debug("Speech created, starting to stream audio chunks")
            async for chunk in speech_response.iter_bytes_async(chunk_size=1024):
                logger.debug(f"Yielding audio chunk of size: {len(chunk)} bytes")
                yield chunk
            logger.info("Speech generation completed")
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}", exc_info=True)
            print(f"{Fore.RED}Error generating speech: {str(e)}{Style.RESET_ALL}")
            raise

    async def generate_spoken_content_stream(self, text, content_type="general", voice="alloy", model="gpt-4", high_quality=False, max_length=None):
        logger.info(f"Starting spoken content generation for: '{text}'")
        print(f"{Fore.CYAN}🐌💯 We're about to create some amazing {content_type} content for: '{text}'{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Using voice: {voice}, model: {model}, high quality: {high_quality}, max length: {max_length if max_length else 'unlimited'} 🐌💯{Style.RESET_ALL}")

        start_time = time.time()
        logger.debug("Initiating text stream generation")
        text_stream = self.generate_text_stream(text, content_type, model, max_length)
        
        generated_text = ""
        logger.debug("Processing text stream")
        async for content in text_stream:
            generated_text += content
            logger.debug(f"Yielding text chunk: {content}")
            yield ("text", content)

        logger.debug("Text generation completed, starting speech generation")
        logger.debug("Processing speech stream")
        async for chunk in self.generate_speech_stream(generated_text, voice, high_quality):
            logger.debug(f"Yielding audio chunk of size: {len(chunk)} bytes")
            yield ("audio", chunk)

        end_time = time.time()
        logger.info(f"Content and audio generation completed in {end_time - start_time:.2f} seconds")
        print(f"{Fore.GREEN}🐌💯 Content audio generated and streamed 🔥{Style.RESET_ALL}")
        print(f"Total generation time: {end_time - start_time:.2f} seconds")

async def generate_spoken_content_stream(text, content_type="general", voice="alloy", model="gpt-4", high_quality=False, max_length=None):
    generator = ContentGenerator(os.getenv("OPENAI_API_KEY"))
    async for chunk_type, chunk in generator.generate_spoken_content_stream(text, content_type, voice, model, high_quality, max_length):
        yield chunk_type, chunk

