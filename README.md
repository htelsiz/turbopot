# TurboPot 🐌💯🔥 - AI Rap Generator

TurboPot is an innovative AI-powered rap generator that creates custom rap lyrics and converts them to speech using various voices. It offers both a command-line interface and a web API for easy integration into your projects.

## 🚀 Features

- 🎵 AI-powered rap lyrics generation
- 🗣️ Text-to-speech conversion with multiple voice options
- 🎚️ High-quality audio generation option
- 🖥️ Command-line interface for quick generation
- 🌐 Web API for integration into other applications

## 🛠️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/turbopot.git
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

Generate a rap:
```
python main.py generate-rap --subject "Artificial Intelligence" --voice "nova" --high-quality
```

Options:
- `--subject`: The topic for your rap (required)
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

Got questions? Reach out to us at [your-email@example.com](mailto:your-email@example.com)

🐌💯🔥 Happy Rapping with TurboPot! 🐌💯🔥
