Additional update:

I tested the smaller Fish Speech 1.5 model on the available A10G GPU. The model loaded and generated valid audio successfully through both the FastAPI/WebSocket flow, with playback and file saving working correctly.

For a short sentence, server-side inference took approximately 8.6 seconds, while a longer prompt took approximately 20.2 seconds. This is a significant improvement over the S2 Pro CPU setup, which took around 720 seconds for a very short response. However, the current implementation sends audio only after complete generation, so TTFA is still around 8–20 seconds
