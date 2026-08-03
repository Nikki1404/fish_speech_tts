#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p checkpoints/s2-pro

docker compose --profile download run --rm model-downloader

echo "Model downloaded to: $(pwd)/checkpoints/s2-pro"
