import io
import math
import struct
import wave

from fastapi import FastAPI
from fastapi.responses import Response, StreamingResponse

app = FastAPI()


def make_wav() -> bytes:
    sample_rate = 16000
    duration = 0.25
    frames = int(sample_rate * duration)
    output = io.BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for index in range(frames):
            sample = int(3000 * math.sin(2 * math.pi * 440 * index / sample_rate))
            wav_file.writeframesraw(struct.pack("<h", sample))
    return output.getvalue()


@app.get("/v1/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/tts")
async def tts(payload: dict):
    audio = make_wav()
    if payload.get("streaming", False):
        async def chunks():
            for start in range(0, len(audio), 512):
                yield audio[start:start + 512]
        return StreamingResponse(chunks(), media_type="audio/wav")
    return Response(audio, media_type="audio/wav")
