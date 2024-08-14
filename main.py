from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api import generate_spoken_audio
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

@app.post("/generate_rap")
async def generate_rap(request: RapRequest):
    try:
        lyrics, audio_stream = generate_spoken_audio(request.prompt, voice=request.voice, high_quality=request.high_quality)
        return StreamingResponse(audio_stream, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=generated_rap.mp3"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@cli.command()
def run_server(host: str = typer.Option("127.0.0.1", help="Host to run the server on"),
               port: int = typer.Option(8000, help="Port to run the server on")):
    """
    Run the FastAPI server.
    """
    uvicorn.run("main:app", host=host, port=port, reload=True)

@cli.command()
def generate_rap(
    prompt: str = typer.Argument(..., help="Prompt for generating rap lyrics"),
    voice: str = typer.Option("alloy", help="Voice to use for text-to-speech"),
    high_quality: bool = typer.Option(False, help="Use high-quality audio generation")
):
    """
    Generate rap lyrics and audio from the command line.
    """
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

if __name__ == "__main__":
    cli()
