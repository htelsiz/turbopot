import sys
from api import generate_spoken_audio


def test_generate_spoken_audio(text):
    generate_spoken_audio(text)
    print("Audio played successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "Hello, my name is Turbopot. I am an Instant Pot with extraordinary capabilities. How can I help you today?"
    
    test_generate_spoken_audio(prompt)
