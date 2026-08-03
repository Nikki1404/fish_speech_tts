#!/usr/bin/env bash
set -euo pipefail

docker run --rm --gpus all nvidia/cuda:12.9.0-base-ubuntu24.04 nvidia-smi
