(tts_env) PS C:\Users\re_nikitav\Desktop\tts\fish_speech_1.5> python .\client.py
Text: Hi Hello, thank you for calling Inspira Financial. What can I help you with today? I would also like to withdraw money from my account To help you with that, I'll need to verify your identity.
[connect] ws://127.0.0.1:8000/ws/tts
[output] C:\Users\re_nikitav\Desktop\tts\fish_speech_1.5\fish-speech-15.wav
[playback] enabled
[connection-latency] 662.03 ms
[accepted] {"type": "accepted", "request_id": "3b768fcd-92a0-4cc4-b137-dda45dfd813d", "device": "cuda", "model": "fishaudio/fish-speech-1.5", "format": "wav", "delivery": "complete-wav-chunked"}
[ttfa] {"type": "ttfa", "request_id": "3b768fcd-92a0-4cc4-b137-dda45dfd813d", "server_ttfa_ms": 20185.19, "inference_first_result_ms": 20176.69, "inference_latency_ms": 20176.73}
[client-ttfa] 21373.76 ms
[done] {"type": "done", "request_id": "3b768fcd-92a0-4cc4-b137-dda45dfd813d", "server_ttfa_ms": 20185.19, "inference_first_result_ms": 20176.69, "inference_latency_ms": 20176.73, "wav_encoding_latency_ms": 8.06, "generation_latency_ms": 20185.06, "server_total_latency_ms": 20239.39, "connection_to_done_ms": 20572.8, "sample_rate": 44100, "chunks": 19, "bytes": 1179692}

================================================================
LATENCY SUMMARY
================================================================
Connection latency            : 662.03 ms
Client TTFA                   : 21373.76 ms
End-to-end TTFA               : 22036.61 ms
Server TTFA                   : 20185.19 ms
Inference first result        : 20176.69 ms
Inference latency             : 20176.73 ms
WAV encoding latency          : 8.06 ms
Generation latency            : 20185.06 ms
Client total latency          : 24817.81 ms
End-to-end latency            : 25480.66 ms
Server total latency          : 20239.39 ms
Connection to done            : 20572.80 ms
================================================================
Saved WAV                    : C:\Users\re_nikitav\Desktop\tts\fish_speech_1.5\fish-speech-15.wav
File size                    : 1,179,692 bytes
Received bytes               : 1,179,692
Received chunks              : 19
Sample rate                  : 44100 Hz
Channels                     : 1
Sample width                 : 2 bytes
Frames                       : 589824
================================================================
[playback] sample_rate=44100 Hz, channels=1, frames=589824
[playback] completed


                      update on the Fish Speech TTS work:
 
* Set up a standalone Fish Speech TTS application  FastAPI server exposing both HTTP (`/v1/tts`) and WebSocket (`/ws/tts`) endpoints.

 
Challenges encountered:
 
1. GPU deployment
 
   * Attempted to run the latest Fish Speech S2 Pro model on the available A10G GPU.
   * Model loading starts successfully, but initialization fails with a CUDA out-of-memory error while allocating the KV cache.
   * The GPU currently has only ~215 MB free because it is already occupied by the production Nemotron ASR  containers, which cannot be stopped as they are actively in use.
 
2. CPU deployment
 
   * Switched to a CPU-only deployment using the official Fish Speech CPU image.
   * The model loads successfully, but startup takes approximately **833 seconds (~14 minutes)**, making it impractical for production use on the current machine configuration.
 
3. Official Fish Audio API
 
   * Evaluated the hosted API as the quickest alternative for validation.
   * Authentication succeeded, but inference could not be tested because my account had insufficient API credits.
