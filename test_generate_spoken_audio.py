import sys
from api import generate_spoken_audio


def test_generate_spoken_audio(text, high_quality=False):
    result = generate_spoken_audio(text, high_quality=high_quality)
    if result is None:
        print("Content was flagged as inappropriate. No audio generated.")
    else:
        print("Audio played successfully.")
        print("Generated text:", result)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        prompt = sys.argv[1]
        high_quality = sys.argv[2].lower() == 'true'
    else:
        prompt = "Hello, my name is Turbopot. I am an Instant Pot with extraordinary capabilities. How can I help you today?"
        high_quality = False
    
    test_generate_spoken_audio(prompt, high_quality)
