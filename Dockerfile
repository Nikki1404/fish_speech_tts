# syntax=docker/dockerfile:1.7
FROM fishaudio/fish-speech:server-cuda

USER root
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN uv pip install \
    --python /app/.venv/bin/python \
    --no-cache \
    --requirement /app/requirements.txt

ARG MODEL_REPO=fishaudio/s2-pro
ARG MODEL_REVISION=main
RUN --mount=type=cache,target=/root/.cache/huggingface \
    mkdir -p /app/checkpoints/s2-pro && \
    /app/.venv/bin/hf download "${MODEL_REPO}" \
      --revision "${MODEL_REVISION}" \
      --local-dir /app/checkpoints/s2-pro && \
    test -f /app/checkpoints/s2-pro/codec.pth

COPY main.py /app/main.py
RUN chown -R 1000:1000 /app/main.py /app/checkpoints/s2-pro

USER 1000:1000
ENV PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    DEVICE=cuda \
    COMPILE=0 \
    HALF=0 \
    LLAMA_CHECKPOINT_PATH=/app/checkpoints/s2-pro \
    DECODER_CHECKPOINT_PATH=/app/checkpoints/s2-pro/codec.pth \
    DECODER_CONFIG_NAME=modded_dac_vq

EXPOSE 8000
ENTRYPOINT ["/app/.venv/bin/python", "/app/main.py"]
