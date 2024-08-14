# TurboPot 🐌💯🔥 - AI Content Generator

TurboPot is an innovative AI-powered content generator that creates custom content and converts it to speech using various voices. It offers both a command-line interface and a web API for easy integration into your projects.

Repository: https://github.com/htelsiz/turbopot.git

## 🚀 Features

- 📝 AI-powered content generation for various types (e.g., blogs, poems, stories)
- 🗣️ Text-to-speech conversion with multiple voice options
- 🎚️ High-quality audio generation option
- 🖥️ Command-line interface for quick generation
- 🌐 Web API for integration into other applications

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
- `--type`: Type of content to generate (e.g., blog, poem, story) (default: "general")
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
# TurboPot

TurboPot is a powerful content generation tool that uses AI to create various types of content and convert them to speech.

## Prerequisites

Before you can use TurboPot, you need to have FFmpeg installed on your system. FFmpeg is used for playing the generated audio content.

### Installing FFmpeg

#### On macOS:

1. Install Homebrew if you haven't already:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install FFmpeg using Homebrew:
   ```
   brew install ffmpeg
   ```

#### On Windows:

1. Download the FFmpeg build from the official website: https://ffmpeg.org/download.html#build-windows
2. Extract the downloaded zip file to a location on your computer (e.g., C:\ffmpeg)
3. Add the FFmpeg bin folder to your system PATH:
   - Right-click on 'This PC' or 'My Computer' and select 'Properties'
   - Click on 'Advanced system settings'
   - Click on 'Environment Variables'
   - Under 'System variables', find and select 'Path', then click 'Edit'
   - Click 'New' and add the path to the FFmpeg bin folder (e.g., C:\ffmpeg\bin)
   - Click 'OK' to close all dialogs

#### On Linux (Ubuntu/Debian):

1. Update your package list:
   ```
   sudo apt update
   ```
2. Install FFmpeg:
   ```
   sudo apt install ffmpeg
   ```

After installing FFmpeg, you should be able to run the `ffplay` command in your terminal or command prompt.

## Installation

[Add installation instructions for TurboPot here]

## Usage

[Add usage instructions for TurboPot here]
