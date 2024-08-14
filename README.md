# TurboPot - AI-Powered Rap Generator and Text-to-Speech

TurboPot is an innovative project that combines the power of AI to generate rap lyrics and convert them into speech. It offers both a web interface using FastAPI and a command-line interface using Typer, making it versatile for various use cases.

## Features

- Generate creative rap lyrics based on user prompts
- Convert generated lyrics to speech using OpenAI's Text-to-Speech API
- Customizable voice options for speech generation
- Option for high-quality audio output
- Web API for easy integration with other applications
- User-friendly command-line interface
- Streaming audio response for efficient delivery

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- An OpenAI API key

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/turbopot.git
   cd turbopot
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   Create a `.env` file in the root directory and add your API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Web Interface

Start the FastAPI server:
```sh
python main.py run-server
```

Access the API documentation at `http://127.0.0.1:8000/docs` to interact with the endpoints.

### Command-Line Interface

Generate rap lyrics and audio:
```sh
python main.py generate-rap "Your prompt here" --voice "alloy" --high-quality
```

Options:
- `--voice`: Choose from available voices (alloy, echo, fable, onyx, nova, shimmer)
- `--high-quality`: Enable high-quality audio generation

## Project Structure

- `main.py`: FastAPI application and Typer CLI implementation
- `api.py`: Core functionality for generating rap lyrics and text-to-speech conversion
- `requirements.txt`: List of required Python packages
- `test_generate_spoken_audio.py`: Test script for the audio generation feature

## API Endpoints

- POST `/generate_rap`: Generate rap lyrics and audio based on the provided prompt

## Note on API Usage

This project uses OpenAI's API for both text generation and text-to-speech conversion. Be aware of your API usage and any associated costs. Refer to OpenAI's pricing page for more information.

## Contributing

Contributions to TurboPot are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

## License

[MIT License](LICENSE)
