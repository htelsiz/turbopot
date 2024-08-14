import os
from api import generate_spoken_audio


def test_generate_spoken_audio():
    text = "Hello, my name is Turbopot. I am an Instant Pot with extraordinary capabilities. How can I help you today?"
    output_file = generate_spoken_audio(text)

    assert os.path.exists(output_file), "The audio file was not created."
    print(f"Audio file created at: {output_file}")

