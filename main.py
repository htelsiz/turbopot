from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from api import generate_spoken_audio, generate_story
import typer
import uvicorn
import subprocess
import tempfile
import os

app = FastAPI()
cli = typer.Typer()

class RapRequest(BaseModel):
    prompt: str
    voice: str = "alloy"
    high_quality: bool = False

class StoryRequest(BaseModel):
    prompt: str
    genre: str = "fantasy"
    length: str = "short"

@app.post("/generate_rap")
async def generate_rap(request: RapRequest):
    """
    Generate rap lyrics and audio based on the provided prompt.

    Parameters:
    - request: RapRequest object containing:
        - prompt: str, the subject or theme for the rap
        - voice: str, the voice to use for text-to-speech (default: "alloy")
        - high_quality: bool, whether to use high-quality audio generation (default: False)

    Returns:
    - StreamingResponse: Audio stream of the generated rap

    Raises:
    - HTTPException: If an error occurs during generation
    """
    try:
        lyrics, audio_stream = generate_spoken_audio(request.prompt, voice=request.voice, high_quality=request.high_quality)
        return StreamingResponse(audio_stream, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=generated_rap.mp3"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_story")
async def generate_story_endpoint(request: StoryRequest):
    """
    Generate a story based on the provided prompt and parameters.

    Parameters:
    - request: StoryRequest object containing:
        - prompt: str, the subject or theme for the story
        - genre: str, the genre of the story (default: "fantasy")
        - length: str, the length of the story (default: "short")

    Returns:
    - JSONResponse: Generated story text

    Raises:
    - HTTPException: If an error occurs during generation
    """
    try:
        story = generate_story(request.prompt, genre=request.genre, length=request.length)
        return JSONResponse(content={"story": story})
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
def generate_rap(
    subject: str = typer.Option(..., "--subject", help="Subject for generating rap lyrics 🐌💯"),
    voice: str = typer.Option("alloy", help="Voice to use for text-to-speech 🐌💯"),
    high_quality: bool = typer.Option(False, help="Use high-quality audio generation 🐌💯"),
    output: str = typer.Option(None, help="File path to save the generated audio 🐌💯")
):
    """
    Generate rap lyrics and audio from the command line. 🐌💯🔥

    This command creates rap lyrics based on the given subject and converts them to speech.
    The generated audio will be played immediately and can optionally be saved to a file. 🐌💯

    Options:
    --subject: The topic or theme for the rap lyrics (required). 🐌💯
    --voice: The voice to use for text-to-speech. Options include alloy, echo, fable, onyx, nova, shimmer. Default is alloy. 🐌💯
    --high-quality: Flag to enable high-quality audio generation. Default is False. 🐌💯
    --output: File path to save the generated audio. If not provided, audio will only be played. 🐌💯

    Example usage:
    $ python main.py generate-rap --subject "Space exploration" --voice nova --high-quality 🐌💯🔥
    $ python main.py generate-rap --subject "Artificial Intelligence" --output rap.mp3 🐌💯🔥
    """
    prompt = f"Write a rap about: {subject}"
    lyrics, audio_stream = generate_spoken_audio(prompt, voice=voice, high_quality=high_quality)
    typer.echo(f"Generated rap lyrics:\n{lyrics}")
    
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

@cli.command()
def generate_story(
    prompt: str = typer.Option(..., "--prompt", help="Prompt for generating the story"),
    genre: str = typer.Option("fantasy", help="Genre of the story"),
    length: str = typer.Option("short", help="Length of the story (short, medium, long)"),
    output: str = typer.Option(None, help="File path to save the generated story")
):
    """
    Generate a story from the command line.

    This command creates a story based on the given prompt, genre, and length.
    The generated story will be displayed in the console and can optionally be saved to a file.

    Options:
    --prompt: The prompt or theme for the story (required).
    --genre: The genre of the story. Default is fantasy.
    --length: The length of the story (short, medium, long). Default is short.
    --output: File path to save the generated story. If not provided, story will only be displayed.

    Example usage:
    $ python main.py generate-story --prompt "A magical forest" --genre fantasy --length medium
    $ python main.py generate-story --prompt "A detective in space" --genre scifi --output story.txt
    """
    story = generate_story(prompt, genre=genre, length=length)
    typer.echo(f"Generated story:\n\n{story}")

    if output:
        with open(output, 'w') as f:
            f.write(story)
        typer.echo(f"Story saved to {output}")

if __name__ == "__main__":
    cli()
