import sys
from api import generate_spoken_audio


def test_generate_spoken_audio(text, voice="alloy", high_quality=False):
    result = generate_spoken_audio(text, voice=voice, high_quality=high_quality)
    if result is None:
        print("Content was flagged as inappropriate. No audio generated.")
    else:
        print("Audio played successfully.")
        print("Generated rap lyrics:", result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        voice = sys.argv[2] if len(sys.argv) > 2 else "alloy"
        high_quality = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False
    else:
        prompt = "hit me with the danny phantom intro rap"
        voice = "alloy"
        high_quality = False
    
    test_generate_spoken_audio(prompt, voice, high_quality)
