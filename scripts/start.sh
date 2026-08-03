#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

if [ ! -f checkpoints/s2-pro/codec.pth ]; then
  echo "Missing checkpoints/s2-pro/codec.pth"
  echo "Run: ./scripts/download_model.sh"
  exit 1
fi

docker compose up --build
