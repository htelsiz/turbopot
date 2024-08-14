# turbopot 🐌💯🔥 - CLI tool & server with ambiguous capabilities (inspired by Turbo the Snail)

turbopot is a versatile tool that offers both a command-line interface and a web server with ambiguous capabilities. It provides a range of functionalities that can be easily integrated into various projects.

Repository: https://github.com/htelsiz/turbopot.git

## 🚀 Features

- 📝 AI-powered content generation for various types (e.g., blogs, poems, stories)
- 🗣️ Text-to-speech conversion with multiple voice options
- 🎚️ High-quality audio generation option
- 🖥️ Command-line interface for quick generation
- 🌐 Web API for integration into other applications
- 🎙️ Audio transcription from files or microphone input

## Prerequisites

Before using TurboPot, you need to have the following installed on your system:

1. FFmpeg: For playing and processing audio content.
2. PortAudio: Required for microphone input functionality.

### Installing FFmpeg

#### On macOS:
```
brew install ffmpeg
```

#### On Windows:
1. Download FFmpeg from https://ffmpeg.org/download.html#build-windows
2. Extract to a location (e.g., C:\ffmpeg)
3. Add the bin folder to your system PATH

#### On Linux (Ubuntu/Debian):
```
sudo apt update && sudo apt install ffmpeg
```

### Installing PortAudio

#### On macOS:
```
brew install portaudio
```

#### On Windows:
PortAudio is included with the Python package `sounddevice`, which is listed in the requirements.txt file.

#### On Linux (Ubuntu/Debian):
```
sudo apt update && sudo apt install libportaudio2
```

## 🛠️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/htelsiz/turbopot.git
   cd turbopot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   Create a `.env` file in the project root and add your API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## 🎙️ Usage

### Command-line Interface

Generate content:
```
python main.py generate-content --subject "Artificial Intelligence" --type "blog" --voice "nova" --high-quality
python main.py generate-content --subject "Dolphins" --type "scientific overview" --voice "fable" --high-quality --max-length 256
python main.py generate-content --subject "the lines at the post office" --type "meme idea" --voice "shimmer" --high-quality --max-length 256

```

Options:
- `--subject`: The topic for your content (required)
- `--type`: Type of content to generate (default: "general")
- `--voice`: Voice for text-to-speech (default: "alloy")
- `--high-quality`: Use high-quality audio generation (flag)
- `--output`: Save the generated audio to a file
- `--max-length`: Maximum number of characters for the generated content

Transcribe audio file:
```
python main.py transcribe-audio /path/to/your/audio/file.mp3
```

Record audio and transcribe:
```
python main.py record-and-transcribe --duration 10
```

Options:
- `--duration`: Duration of recording in seconds (default: 5)
- `--sample_rate`: Sample rate of the recording (default: 44100)

### Web API

Start the server:
```
python main.py run-server
```

Access the API documentation at `http://127.0.0.1:8000/docs`

Endpoints:
- `/generate_content`: Generate content and audio
- `/transcribe`: Transcribe an uploaded audio file

## 🧪 Testing

Run the test script:
```
python test_generate_spoken_audio.py "Your test prompt here"
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/turbopot/issues).

## 📬 Contact

Got questions? Too bad!
