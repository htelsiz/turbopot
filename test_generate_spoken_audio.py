import sys
from api import generate_spoken_audio


def test_generate_spoken_audio(text):
    result = generate_spoken_audio(text)
    if result is None:
        print("Content was flagged as inappropriate. No audio generated.")
    else:
        print("Audio played successfully.")
        print("Generated text:", result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "Hello, my name is Turbopot. I am an Instant Pot with extraordinary capabilities. How can I help you today?"
    
    test_generate_spoken_audio(prompt)
