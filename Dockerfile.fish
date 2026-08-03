ARG FISH_SPEECH_IMAGE=fishaudio/fish-speech:server-cuda
FROM ${FISH_SPEECH_IMAGE}

# The current upstream streaming wrapper sends header + PCM segments and then
# emits the complete final waveform again. Keep non-streaming behavior intact,
# but suppress that duplicate final payload for streaming requests.
COPY --chown=1000:1000 patches/inference.py /app/tools/server/inference.py
