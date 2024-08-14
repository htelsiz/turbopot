from openai import OpenAI
import os
from dotenv import load_dotenv
import pygame

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def moderate_content(text):
    response = client.moderations.create(input=text)
    return response.results[0].flagged

def generate_spoken_audio(text, voice="alloy", model="gpt-4"):
    # Check content moderation
    if moderate_content(text):
        print("Content flagged as inappropriate. Cannot generate audio.")
        return None
    # Generate text response
    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    generated_text = chat_response.choices[0].message.content.strip()

    # Check moderation for generated text
    if moderate_content(generated_text):
        print("Generated content flagged as inappropriate. Cannot create audio.")
        return None

    # Generate speech from the text
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=generated_text
    )

    # Save the audio to a temporary file
    temp_file = "temp_speech.mp3"
    speech_response.stream_to_file(temp_file)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up
    pygame.mixer.quit()
    os.remove(temp_file)

    return generated_text


