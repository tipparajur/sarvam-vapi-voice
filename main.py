import base64
from fastapi.responses import Response
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

app = FastAPI()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

class SpeechRequest(BaseModel):
    text: str
    language: str = "te-IN"

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/test")
def test():
    return {
        "api_key_loaded": SARVAM_API_KEY is not None
    }
@app.get("/test-tts")
def test_tts():

    url = "https://api.sarvam.ai/text-to-speech"

    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": "నమస్కారం. ఇది సర్వమ్ తెలుగు వాయిస్ పరీక్ష.",
        "target_language_code": "te-IN",
        "model": "bulbul:v3" ,
        "speaker": "priya"
    }

    response = requests.post(
    url,
    headers=headers,
    json=payload
)

    print("SARVAM STATUS:", response.status_code)
    print("SARVAM RESPONSE:", response.text[:500])

    return {
    "status": response.status_code,
    "response_text": response.text[:1000]
}

from fastapi import Request

@app.post("/tts")
async def generate_speech(request: Request):

    body = await request.json()

    print("REQUEST RECEIVED")

    message = body.get("message", {})
    print("TEXT FOUND:", message.get("text"))
    text = (
    body.get("text")
    or message.get("text")
    or body.get("input")
    or body.get("transcript")
    or "Hello"
)

    payload = {
        "text": text,
        "target_language_code": "te-IN",
        "model": "bulbul:v3" ,
        "speaker": "priya"
    }
    
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        "https://api.sarvam.ai/text-to-speech",
        headers=headers,
        json=payload
    )
    
    data = response.json()
    
    audio_base64 = data["audios"][0]
    
    audio_bytes = base64.b64decode(audio_base64)
    
    return Response(
        content=audio_bytes,
        media_type="audio/wav"
    )
    
