Hi <Manager Name>, apologies for the delayed response. I completely missed your messages from Friday because of an ongoing network outage in my area caused by an ISP/vendor issue. Connectivity has been intermittent over the past few days, and I wasn't able to receive or respond to messages in time. Sorry for the inconvenience.

Here's an update on the Fish Speech TTS work:

* Set up a standalone Fish Speech TTS application with a single FastAPI server exposing both HTTP (`/v1/tts`) and WebSocket (`/ws/tts`) endpoints.
* Built and validated the Docker image, integrated model download during the build, and configured a client for WebSocket-based testing with latency measurements (TTFA, inference latency, total latency).
* Verified the end-to-end request flow and latency reporting through both HTTP and WebSocket.

**Challenges encountered:**

1. **GPU deployment**

   * Attempted to run the latest Fish Speech S2 Pro model on the available A10G GPU.
   * Model loading starts successfully, but initialization fails with a CUDA out-of-memory error while allocating the KV cache.
   * The GPU currently has only ~215 MB free because it is already occupied by the production Nemotron ASR and Triton containers, which cannot be stopped as they are actively in use.

2. **CPU deployment**

   * Switched to a CPU-only deployment using the official Fish Speech CPU image.
   * The model loads successfully, but startup takes approximately **833 seconds (~14 minutes)**, making it impractical for production use on the current machine configuration.

3. **Official Fish Audio API**

   * Evaluated the hosted API as the quickest alternative for validation.
   * Authentication succeeded, but inference could not be tested because the account has insufficient API credits.

I'm continuing to investigate optimization options (reduced memory usage, smaller models, and deployment alternatives) to find a practical way to run the model within the current infrastructure constraints.
