from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TTSRequest(BaseModel):
    """WebSocket request mapped directly to Fish Speech ServeTTSRequest."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    reference_id: str | None = Field(default=None, max_length=255)
    chunk_length: int = Field(default=200, ge=100, le=1000)
    format: Literal["wav"] = "wav"
    latency: Literal["normal", "balanced"] = "normal"
    seed: int | None = None
    use_memory_cache: Literal["on", "off"] = "off"
    normalize: bool = True
    streaming: bool = True
    max_new_tokens: int = Field(default=1024, ge=1, le=8192)
    top_p: float = Field(default=0.8, ge=0.1, le=1.0)
    repetition_penalty: float = Field(default=1.1, ge=0.9, le=2.0)
    temperature: float = Field(default=0.8, ge=0.1, le=1.0)


class GatewayEvent(BaseModel):
    type: str
    request_id: str | None = None
