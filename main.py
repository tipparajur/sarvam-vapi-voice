from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

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
        "model": "bulbul:v3"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()

@app.post("/tts")
def generate_speech(request: SpeechRequest):

    url = "https://api.sarvam.ai/text-to-speech"

    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": request.text,
        "target_language_code": request.language
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()