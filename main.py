from fastapi import Request

@app.post("/tts")
async def generate_speech(request: Request):

    body = await request.json()
    print("VAPI BODY:", body)

    text = (
        body.get("text")
        or body.get("message")
        or body.get("input")
        or body.get("transcript")
        or "Hello"
    )

    url = "https://api.sarvam.ai/text-to-speech"

    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "target_language_code": "te-IN"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()
