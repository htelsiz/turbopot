from api import generate_spoken_audio


def test_generate_spoken_audio():
    text = "Hello, my name is Turbopot. I am an Instant Pot with extraordinary capabilities. How can I help you today?"
    generate_spoken_audio(text)
    print("Audio played successfully.")

