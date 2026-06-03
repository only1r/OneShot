import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent / ".env"
if not dotenv_path.exists():
    raise RuntimeError(
        f"{dotenv_path} not found. Create a .env file with GEMINI_API_KEY in the project folder."
    )

if not load_dotenv(dotenv_path=dotenv_path):
    raise RuntimeError(
        f"Could not load {dotenv_path}. Ensure it contains GEMINI_API_KEY."
    )

# Validate Gemini API key at startup
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to .env or export it in your environment before starting the server."
    )

# Initialize FastAPI
app = FastAPI(title="AI Synth Copilot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=gemini_api_key)

# Define the request model
class SoundRequest(BaseModel):
    prompt: str

@app.post("/generate-patch")
async def generate_patch(request: SoundRequest):
    # The JSON schema contract
    schema_definition = """
    {
        "oscillator": {
            "type": "sine|square|sawtooth|triangle",
            "voices": int (1 to 8, use higher numbers for thick/wide sounds like supersaws),
            "unison": int (0 to 50, use higher numbers for detuned, chorused, or aggressive sounds)
        },
        "envelope": {
            "attack": float (0.0 to 2.0 seconds), 
            "decay": float (0.0 to 2.0 seconds), 
            "sustain": float (0.0 to 1.0 volume level), 
            "release": float (0.0 to 5.0 seconds)
        },
        "filter": {
            "type": "lowpass", 
            "cutoff": int (100 to 10000 Hz)
        }
    }
    """
    
    # The System Instruction
    system_instruction = f"""
    You are an expert synthesizer sound designer. 
    Convert the user's natural language sound description into a precise mathematical JSON configuration.
    Use the oscillator fields to describe both the number of unison voices and the detune spread.
    For thick, wide, or chorus-like sounds, choose higher values for `voices` and `unison` as appropriate.
    You must ONLY reply with valid JSON matching this exact schema:
    {schema_definition}
    """

    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )
        
        response = model.generate_content(request.prompt)
        
        # Parse the string into a Python dictionary
        patch_data = json.loads(response.text)
        return patch_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate sound patch: {str(e)}")