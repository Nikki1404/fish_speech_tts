# syntax=docker/dockerfile:1.7

FROM fishaudio/fish-speech:server-cpu-v2.0.0-beta
ENV http_proxy="http://163.116.128.80:8080"
ENV https_proxy="http://163.116.128.80:8080"

USER root
WORKDIR /app

ENV PATH="/app/.venv/bin:${PATH}"

ENV HF_HUB_DISABLE_XET=1 \
    HF_HUB_DOWNLOAD_TIMEOUT=1800 \
    HF_HUB_ETAG_TIMEOUT=120

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
        --local-dir /app/checkpoints/s2-pro \
        --max-workers 1 && \
    test -f /app/checkpoints/s2-pro/codec.pth && \
    test -f /app/checkpoints/s2-pro/model-00001-of-00002.safetensors && \
    test -f /app/checkpoints/s2-pro/model-00002-of-00002.safetensors

COPY app /app/app

RUN chown -R 1000:1000 \
    /app/app \
    /app/checkpoints/s2-pro

USER 1000:1000

ENV PYTHONUNBUFFERED=1 \
    DEVICE=cpu \
    MAX_TEXT_LENGTH=1000 \
    LLAMA_CHECKPOINT_PATH=/app/checkpoints/s2-pro \
    DECODER_CHECKPOINT_PATH=/app/checkpoints/s2-pro/codec.pth \
    DECODER_CONFIG_NAME=modded_dac_vq \
    OMP_NUM_THREADS=12 \
    MKL_NUM_THREADS=12 \
    OPENBLAS_NUM_THREADS=12 \
    TOKENIZERS_PARALLELISM=false

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
