from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api import generate_spoken_content_stream
import os
from dotenv import load_dotenv
import typer
import uvicorn
import subprocess
import tempfile
import asyncio
from typing import Optional
import time

app = FastAPI()
cli = typer.Typer()

load_dotenv()

class ContentRequest(BaseModel):
    prompt: str
    content_type: str = "general"
    voice: str = "alloy"
    high_quality: bool = False


@app.post("/generate_content")
async def generate_content(request: ContentRequest):
    """
    Generate content and audio based on the provided prompt and content type.

    Parameters:
    - request: ContentRequest object containing:
        - prompt: str, the subject or theme for the content
        - content_type: str, the type of content to generate (default: "general")
        - voice: str, the voice to use for text-to-speech (default: "alloy")
        - high_quality: bool, whether to use high-quality audio generation (default: False)

    Returns:
    - StreamingResponse: Audio stream of the generated content

    Raises:
    - HTTPException: If an error occurs during generation
    """
    try:
        start_time = time.time()
        content_stream = generate_spoken_content_stream(
            request.prompt,
            content_type=request.content_type,
            voice=request.voice,
            high_quality=request.high_quality
        )

        async def stream_generator():
            async for chunk in content_stream:
                yield chunk
            end_time = time.time()
            print(f"Total API processing time: {end_time - start_time:.2f} seconds")

        return StreamingResponse(stream_generator(), media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=generated_content.mp3"})
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out")
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
    content_type: str = typer.Option("general", "--type", help="Type of content to generate (e.g., blog, poem, story) 🐌💯"),
    voice: str = typer.Option("alloy", help="Voice to use for text-to-speech 🐌💯"),
    high_quality: bool = typer.Option(False, help="Use high-quality audio generation 🐌💯"),
    output: str = typer.Option(None, help="File path to save the generated audio 🐌💯")
):
    """
    Generate content and audio from the command line. 🐌💯🔥

    This command creates content based on the given subject and content type, then converts it to speech.
    The generated audio will be played immediately and can optionally be saved to a file. 🐌💯

    Options:
    --subject: The topic or theme for the content (required). 🐌💯
    --type: The type of content to generate (e.g., blog, poem, story). Default is general. 🐌💯
    --voice: The voice to use for text-to-speech. Options include alloy, echo, fable, onyx, nova, shimmer. Default is alloy. 🐌💯
    --high-quality: Flag to enable high-quality audio generation. Default is False. 🐌💯
    --output: File path to save the generated audio. If not provided, audio will only be played. 🐌💯

    Example usage:
    $ python main.py generate-content --subject "Space exploration" --type "poem" --voice nova --high-quality 🐌💯🔥
    $ python main.py generate-content --subject "Artificial Intelligence" --type "blog" --output content.mp3 🐌💯🔥
    """
    prompt = f"Create {content_type} content about: {subject}"
    try:
        start_time = time.time()
        content_stream = asyncio.run(generate_spoken_content_stream(prompt, content_type=content_type, voice=voice, high_quality=high_quality))
        
        content = ""
        audio_chunks = []
        async for chunk in content_stream:
            if isinstance(chunk, str):
                content += chunk
            else:
                audio_chunks.append(chunk)
        
        end_time = time.time()
        typer.echo(f"Generated {content_type} content:\n{content}")
        typer.echo(f"Total generation time: {end_time - start_time:.2f} seconds")
        
        # Save the audio stream to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            for chunk in audio_chunks:
                temp_file.write(chunk)
        
        # Play the audio using ffplay
        try:
            typer.echo("Playing generated content. Press Ctrl+C to stop.")
            subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_file.name], check=True)
        except KeyboardInterrupt:
            typer.echo("Playback stopped.")
        except subprocess.CalledProcessError:
            typer.echo("Error: ffplay is not installed or encountered an error.")
        except Exception as e:
            typer.echo(f"An error occurred: {str(e)}")
        finally:
            os.unlink(temp_file.name)
    except asyncio.TimeoutError:
        typer.echo("Error: Request timed out")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    cli()
