# turbopot
"smart" talking instapot
# Project Setup

## Prerequisites

Make sure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)
- ffmpeg (for audio playback)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Install `ffmpeg`:
    - On macOS (using Homebrew):
      ```sh
      brew install ffmpeg
      ```
    - On Ubuntu or Debian:
      ```sh
      sudo apt-get update
      sudo apt-get install ffmpeg
      ```
    - On Windows:
      Download from https://ffmpeg.org/download.html and add to PATH

## Environment Variables

Create a `.env` file in the root directory of your project and add your OpenAI API key:
    ```sh
    OPENAI_API_KEY=your_openai_api_key
    ```

## Running the Test Script

You can run the test script with a custom greeting prompt:
    ```sh
    python test_generate_spoken_audio.py "Your custom greeting here"
    ```

If no prompt is provided, it will use a default greeting:
    ```sh
    python test_generate_spoken_audio.py
    ```
# Rap Lyric Generator and Text-to-Speech

This project generates rap lyrics based on a given prompt and then converts the generated text to speech using OpenAI's API.

## Features

- Generate rap lyrics based on user prompts
- Convert generated lyrics to speech
- Content moderation to ensure appropriate content
- Customizable voice options
- Option for high-quality audio output

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the test script with a prompt:

```
python test_generate_spoken_audio.py "your prompt here"
```

You can also specify the voice and audio quality:

```
python test_generate_spoken_audio.py "your prompt here" "nova" true
```

Available voices: alloy, echo, fable, onyx, nova, shimmer

## Files

- `api.py`: Contains the main functionality for generating rap lyrics and converting them to speech.
- `test_generate_spoken_audio.py`: A test script to demonstrate the functionality.
- `requirements.txt`: Lists the required Python packages.

## Note

This project uses OpenAI's API, which may incur costs. Please be aware of your API usage and any associated fees.
