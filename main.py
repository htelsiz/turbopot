from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api import ContentGenerator
import os
from dotenv import load_dotenv
import typer
import uvicorn
import subprocess
import tempfile
import os
from typing import Optional

app = FastAPI()
cli = typer.Typer()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
content_generator = ContentGenerator(OPENAI_API_KEY)

class ContentRequest(BaseModel):
    prompt: str
    voice: str = "alloy"
    high_quality: bool = False


@app.post("/generate_content")
async def generate_content(request: ContentRequest):
    """
    Generate content and audio based on the provided prompt.

    Parameters:
    - request: ContentRequest object containing:
        - prompt: str, the subject or theme for the content
        - voice: str, the voice to use for text-to-speech (default: "alloy")
        - high_quality: bool, whether to use high-quality audio generation (default: False)

    Returns:
    - StreamingResponse: Audio stream of the generated content

    Raises:
    - HTTPException: If an error occurs during generation
    """
    try:
        content, audio_stream = content_generator.generate_spoken_content(request.prompt, voice=request.voice, high_quality=request.high_quality)
        return StreamingResponse(audio_stream, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=generated_content.mp3"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@cli.command()
def run_server(host: str = typer.Option("127.0.0.1", help="Host to run the server on"),
               port: int = typer.Option(8000, help="Port to run the server on")):
    """
    Run the FastAPI server. 🐌💯

    This command starts the FastAPI server, making the TurboPot API accessible.
    Use this when you want to interact with TurboPot through HTTP requests. 🐌💯

    Options:
    --host: The host address to bind the server to. Default is 127.0.0.1 (localhost). 🐌💯
    --port: The port number to run the server on. Default is 8000. 🐌💯

    Example usage:
    $ python main.py run-server 🐌💯
    $ python main.py run-server --host 0.0.0.0 --port 5000 🐌💯🔥
    """
    uvicorn.run("main:app", host=host, port=port, reload=True)

@cli.command()
def generate_content(
    subject: str = typer.Option(..., "--subject", help="Subject for generating content 🐌💯"),
    voice: str = typer.Option("alloy", help="Voice to use for text-to-speech 🐌💯"),
    high_quality: bool = typer.Option(False, help="Use high-quality audio generation 🐌💯"),
    output: str = typer.Option(None, help="File path to save the generated audio 🐌💯")
):
    """
    Generate content and audio from the command line. 🐌💯🔥

    This command creates content based on the given subject and converts it to speech.
    The generated audio will be played immediately and can optionally be saved to a file. 🐌💯

    Options:
    --subject: The topic or theme for the content (required). 🐌💯
    --voice: The voice to use for text-to-speech. Options include alloy, echo, fable, onyx, nova, shimmer. Default is alloy. 🐌💯
    --high-quality: Flag to enable high-quality audio generation. Default is False. 🐌💯
    --output: File path to save the generated audio. If not provided, audio will only be played. 🐌💯

    Example usage:
    $ python main.py generate-content --subject "Space exploration" --voice nova --high-quality 🐌💯🔥
    $ python main.py generate-content --subject "Artificial Intelligence" --output content.mp3 🐌💯🔥
    """
    prompt = f"Create content about: {subject}"
    content, audio_stream = content_generator.generate_spoken_content(prompt, voice=voice, high_quality=high_quality)
    typer.echo(f"Generated content:\n{content}")
    
    # Save the audio stream to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        for chunk in audio_stream:
            temp_file.write(chunk)
    
    # Play the audio using ffplay
    try:
        typer.echo("Playing generated rap. Press Ctrl+C to stop.")
        subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_file.name], check=True)
    except KeyboardInterrupt:
        typer.echo("Playback stopped.")
    except subprocess.CalledProcessError:
        typer.echo("Error: ffplay is not installed or encountered an error.")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        os.unlink(temp_file.name)


if __name__ == "__main__":
    cli()
