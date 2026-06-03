import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI
app = FastAPI(title="AI Synth Copilot API")

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Define the request model
class SoundRequest(BaseModel):
    prompt: str

@app.post("/generate-patch")
async def generate_patch(request: SoundRequest):
    # The JSON schema contract
    schema_definition = """
    {
        "oscillator": {"type": "sine|square|sawtooth|triangle"},
        "envelope": {
            "attack": float (0.0 to 2.0 seconds), 
            "decay": float (0.0 to 2.0 seconds), 
            "sustain": float (0.0 to 1.0 volume level), 
            "release": float (0.0 to 5.0 seconds)
        },
        "filter": {
            "type": "lowpass|highpass|bandpass", 
            "cutoff": int (20 to 20000 Hz)
        }
    }
    """
    
    # The System Instruction
    system_instruction = f"""
    You are an expert synthesizer sound designer. 
    Convert the user's natural language sound description into a precise mathematical JSON configuration.
    You must ONLY reply with valid JSON matching this exact schema:
    {schema_definition}
    """

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )
        
        response = model.generate_content(request.prompt)
        
        # Parse the string into a Python dictionary
        patch_data = json.loads(response.text)
        return patch_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate sound patch: {str(e)}")