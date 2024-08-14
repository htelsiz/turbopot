from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api import generate_spoken_audio
import typer
import uvicorn

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
    typer.echo("Audio generated and streamed. You can't hear it in the CLI, but it's ready for streaming!")

if __name__ == "__main__":
    cli()
