# turbopot
"smart" talking instapot
# Project Setup

## Prerequisites

Make sure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)
- Homebrew (for macOS users)

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

3. Install `ffmpeg` (required by `pydub`):
    ```sh
    brew install ffmpeg
    ```

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
