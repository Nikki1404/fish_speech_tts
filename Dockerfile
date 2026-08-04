# syntax=docker/dockerfile:1.7

FROM fishaudio/fish-speech:latest-server-cpu

ENV http_proxy="http://163.116.128.80:8080"
ENV https_proxy="http://163.116.128.80:8080"

USER root

WORKDIR /app

# Ensure commands installed in Fish Speech's virtual environment,
# including uvicorn, are available directly.
ENV PATH="/app/.venv/bin:${PATH}"

COPY requirements.txt /app/requirements.txt

RUN uv pip install \
    --python /app/.venv/bin/python \
    --no-cache \
    --requirement /app/requirements.txt

ARG MODEL_REPO=fishaudio/s2-pro
ARG MODEL_REVISION=main

RUN --mount=type=cache,target=/root/.cache/huggingface \
    mkdir -p /app/checkpoints/s2-pro && \
    hf download "${MODEL_REPO}" \
        --revision "${MODEL_REVISION}" \
        --local-dir /app/checkpoints/s2-pro && \
    test -f /app/checkpoints/s2-pro/codec.pth

COPY app /app/app

RUN chown -R 1000:1000 \
    /app/app \
    /app/checkpoints/s2-pro

USER 1000:1000

ENV PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    DEVICE=cpu \
    MAX_TEXT_LENGTH=1000 \
    LLAMA_CHECKPOINT_PATH=/app/checkpoints/s2-pro \
    DECODER_CHECKPOINT_PATH=/app/checkpoints/s2-pro/codec.pth \
    DECODER_CONFIG_NAME=modded_dac_vq \
    OMP_NUM_THREADS=16 \
    MKL_NUM_THREADS=16 \
    OPENBLAS_NUM_THREADS=16 \
    TOKENIZERS_PARALLELISM=false

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
