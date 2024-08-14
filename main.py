from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api import generate_spoken_audio
import typer

app = FastAPI()
cli = typer.Typer()

class RapRequest(BaseModel):
    prompt: str
    voice: str = "alloy"
    high_quality: bool = False

@app.post("/generate_rap")
async def generate_rap(request: RapRequest):
    try:
        result = generate_spoken_audio(request.prompt, voice=request.voice, high_quality=request.high_quality)
        return {"lyrics": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@cli.command()
def run_server(host: str = "127.0.0.1", port: int = 8000):
    """
    Run the FastAPI server.
    """
    import uvicorn
    uvicorn.run("main:app", host=host, port=port, reload=True)

@cli.command()
def generate_rap(prompt: str, voice: str = "alloy", high_quality: bool = False):
    """
    Generate rap lyrics from the command line.
    """
    result = generate_spoken_audio(prompt, voice=voice, high_quality=high_quality)
    typer.echo(f"Generated rap lyrics:\n{result}")

if __name__ == "__main__":
    cli()
