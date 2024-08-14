# TurboPot - Rap Lyric Generator and Text-to-Speech

This project generates rap lyrics based on a given prompt and then converts the generated text to speech using OpenAI's API. It now uses FastAPI for a web interface and Typer for a command-line interface.

## Prerequisites

Make sure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)

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

3. Create a `.env` file in the root directory of your project and add your OpenAI API key:
    ```sh
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

### Web Interface

To start the FastAPI server:

```sh
python main.py run-server
```

Then, you can access the API documentation at `http://127.0.0.1:8000/docs`.

### Command-Line Interface

To generate rap lyrics from the command line:

```sh
python main.py generate-rap "Your prompt here" --voice "alloy" --high-quality
```

Available voices: alloy, echo, fable, onyx, nova, shimmer

## Features

- Generate rap lyrics based on user prompts
- Convert generated lyrics to speech
- Customizable voice options
- Option for high-quality audio output
- Web API for integration with other applications
- Command-line interface for easy use

## Files

- `main.py`: Contains the FastAPI application and Typer CLI.
- `api.py`: Contains the core functionality for generating rap lyrics and converting them to speech.
- `requirements.txt`: Lists the required Python packages.

## Note

This project uses OpenAI's API, which may incur costs. Please be aware of your API usage and any associated fees.
