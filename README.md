# TurboPot 🐌💯🔥 - CLI tool & server with ambiguous capabilities

TurboPot is a versatile tool that offers both a command-line interface and a web server with ambiguous capabilities. It provides a range of functionalities that can be easily integrated into various projects.

Repository: https://github.com/htelsiz/turbopot.git

## 🚀 Features

- 📝 AI-powered content generation for various types (e.g., blogs, poems, stories)
- 🗣️ Text-to-speech conversion with multiple voice options
- 🎚️ High-quality audio generation option
- 🖥️ Command-line interface for quick generation
- 🌐 Web API for integration into other applications

## Prerequisites

Before using TurboPot, you need to have FFmpeg installed on your system for playing the generated audio content.

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
```

Options:
- `--subject`: The topic for your content (required)
- `--type`: Type of content to generate (default: "general")
- `--voice`: Voice for text-to-speech (default: "alloy")
- `--high-quality`: Use high-quality audio generation (flag)
- `--output`: Save the generated audio to a file

### Web API

Start the server:
```
python main.py run-server
```

Access the API documentation at `http://127.0.0.1:8000/docs`

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

🐌💯🔥 Happy Content Creating with TurboPot! 🐌💯🔥
