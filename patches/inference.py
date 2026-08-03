from http import HTTPStatus

import numpy as np
from kui.asgi import HTTPException

from fish_speech.inference_engine import TTSInferenceEngine
from fish_speech.utils.schema import ServeTTSRequest

AMPLITUDE = 32768


def inference_wrapper(req: ServeTTSRequest, engine: TTSInferenceEngine):
    """Convert inference-engine events into the self-hosted HTTP audio stream."""

    count = 0
    for result in engine.inference(req):
        match result.code:
            case "header":
                if isinstance(result.audio, tuple):
                    yield result.audio[1]

            case "error":
                raise HTTPException(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    content=str(result.error),
                )

            case "segment":
                count += 1
                if isinstance(result.audio, tuple):
                    yield (result.audio[1] * AMPLITUDE).astype(np.int16).tobytes()

            case "final":
                count += 1
                # For non-streaming requests, this is the only audio payload.
                # For streaming requests, all audio was already emitted as
                # int16 PCM segments, so sending the final waveform duplicates it.
                if not req.streaming and isinstance(result.audio, tuple):
                    yield result.audio[1]
                return None

    if count == 0:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            content="No audio generated, please check the input text.",
        )
