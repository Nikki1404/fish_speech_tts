py -3.11 prepare_chunks_local.py --csv data/inspira_transcripts.csv --wav-dir raw_wavs --out-dir loadtest_chunks --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --chunk-sec 10 --language en-US

notepad loadtest_chunks\REVIEW_LOW_SCORE.txt

py -3.11 load_test_until_failure.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --until-failure --start-concurrency 1 --step 1 --max-concurrency 50 --rounds 1 --rest 5 --confirm-failure

py -3.11 load_test_until_failure.py --mode ws --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --until-failure --start-concurrency 1 --step 1 --max-concurrency 50 --rounds 1 --rest 5 --confirm-failure


(venv) PS C:\Users\re_nikitav\Documents\nemotron_finetuned> pip install -r requirements_load_test
Fatal error in launcher: Unable to create process using '"C:\Users\re_nikitav\Desktop\bu-digital-cx-speech-asr-realtime-custom-vad\scripts\venv\Scripts\python.exe"  "C:\Users\re_nikitav\Desktop\asr\bu-digital-cx-speech-asr-realtime-custom-vad\scripts\venv\Scripts\pip.exe" install -r requirements_load_test': The system cannot find the file specified.


python load_test_autoscaling.py --mode ws --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1" --start-concurrency 1 --step 5 --max-concurrency 60 --stage-seconds 90 --metrics-delay 135 --rest-seconds 10 --stop-when-scaled

python load_test_autoscaling.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1" --start-concurrency 37 --step 1 --max-concurrency 41 --stage-seconds 90 --metrics-delay 135 --rest-seconds 10 --stop-when-scaled

  python load_test_autoscaling.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1" --start-concurrency 1 --step 5 --max-concurrency 60 --stage-seconds 90 --metrics-delay 135 --rest-seconds 10 --stop-when-scaled
py -3.11 load_test_until_failure_with_scaling.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --until-failure --start-concurrency 1 --step 1 --max-concurrency 50 --rounds 1 --rest 5 --confirm-failure --monitor-scaling --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1"



docker run -d --gpus all --name qwen3-tts -p 8003:8003 qwen3-tts


python client.py --server ws://<EC2-IP>:8001/ws/tts --text "I cannot believe we finally made it!" --language English --speaker Aiden --instruct "Speak happily and with excitement." --output excited.wav


  PS C:\Users\re_nikitav\Documents\quen_3_tts> python client.py --server ws://localhost:8003/ws/tts --text "Hi Hello, thank you for calling Inspira Financial. What can I help you with today? I would also like to withdraw money from my account To help you with that, I'll need to verify your identity." --language English --speaker Aiden --instruct "Speak in very professional tone." --output excited.wav --play
[connect] ws://localhost:8003/ws/tts
[connection-latency] 551.37 ms
[accepted] request_id=bfed4d67-1c9a-4dc6-b508-93b41b626799 speaker=Aiden language=English
[audio-start] sample_rate=24000 audio_duration_s=12.56
[first-audio] 25027.79 ms

================================================================================
CLIENT LATENCY
================================================================================
Connection latency : 551.37 ms
Send call          : 0.41 ms
CLIENT TTFB        : 266.24 ms
CLIENT TTFT/TTFA   : 25027.79 ms
Audio -> Done      : 812.78 ms
CLIENT TOTAL       : 25840.57 ms

================================================================================
SERVER LATENCY
================================================================================
SERVER TTFB        : 0.1 ms
SERVER TTFT/TTFA   : 24031.86 ms
SERVER FIRST AUDIO : 24031.86 ms
SERVER INFERENCE   : 24027.23 ms
SERVER AUDIO SEND  : 28.72 ms
SERVER TOTAL       : 24060.58 ms
AUDIO DURATION     : 12.56 s
RTF                : 1.913





(tts_env) PS C:\Users\re_nikitav\Desktop\tts\Fish_audio_s1mini> python client.py Text: Hi Hello, thank you for calling Inspira Financial. What can I help you with today? I would also like to withdraw money from my account To help you with that, I'll need to verify your identity [connect] ws://127.0.0.1:8001/ws/tts [output] C:\Users\re_nikitav\Desktop\tts\Fish_audio_s1mini\fish-s1-mini-stream.wav [live-playback] enabled [connection-latency] 665.03 ms [accepted] {"type": "accepted", "request_id": "7211e1ae-1f9b-45c5-a0b6-f43c328afed4", "model": "fishaudio/s1-mini", "device": "cuda", "sample_rate": 44100, "channels": 1, "sample_width": 2, "delivery": "pcm-stream"} [ttfa] {"type": "ttfa", "request_id": "7211e1ae-1f9b-45c5-a0b6-f43c328afed4", "server_ttfa_ms": 9390.51, "inference_ttfa_ms": 9390.36} [client-ttfa] 11469.59 ms [audible-ttfa] 11470.35 ms [done] {"type": "done", "request_id": "7211e1ae-1f9b-45c5-a0b6-f43c328afed4", "server_ttfa_ms": 9390.51, "inference_ttfa_ms": 9390.36, "server_total_latency_ms": 20893.57, "inference_latency_ms": 20893.41, "connection_to_done_ms": 21166.9, "sample_rate": 44100, "header_bytes": 44, "audio_bytes": 933888, "audio_segments": 3} Connection latency : 665.03 ms Client first-PCM TTFA : 11469.59 ms Audible TTFA : 11470.35 ms Server TTFA : 9390.51 ms Inference TTFA : 9390.36 ms Inference total latency : 20893.41 ms Server total latency : 20893.57 ms Client total latency : 24734.93 ms Saved WAV: C:\Users\re_nikitav\Desktop\tts\Fish_audio_s1mini\fish-s1-mini-stream.wav Header bytes: 44 Audio bytes: 933,888 Audio segments: 3 Sample rate: 44100 Hz Frames: 466944


(tts_env) PS C:\Users\re_nikitav\Desktop\tts\fish_speech_1.5> python .\client.py Text: Hi Hello, thank you for calling Inspira Financial. What can I help you with today? I would also like to withdraw money from my account To help you with that, I'll need to verify your identity. [connect] ws://127.0.0.1:8000/ws/tts [output] C:\Users\re_nikitav\Desktop\tts\fish_speech_1.5\fish-speech-15.wav [playback] enabled [connection-latency] 662.03 ms [accepted] {"type": "accepted", "request_id": "3b768fcd-92a0-4cc4-b137-dda45dfd813d", "device": "cuda", "model": "fishaudio/fish-speech-1.5", "format": "wav", "delivery": "complete-wav-chunked"} [ttfa] {"type": "ttfa", "request_id": "3b768fcd-92a0-4cc4-b137-dda45dfd813d", "server_ttfa_ms": 20185.19, "inference_first_result_ms": 20176.69, "inference_latency_ms": 20176.73} [client-ttfa] 21373.76 ms [done] {"type": "done", "request_id": "3b768fcd-92a0-4cc4-b137-dda45dfd813d", "server_ttfa_ms": 20185.19, "inference_first_result_ms": 20176.69, "inference_latency_ms": 20176.73, "wav_encoding_latency_ms": 8.06, "generation_latency_ms": 20185.06, "server_total_latency_ms": 20239.39, "connection_to_done_ms": 20572.8, "sample_rate": 44100, "chunks": 19, "bytes": 1179692} ================================================================ LATENCY SUMMARY ================================================================ Connection latency : 662.03 ms Client TTFA : 21373.76 ms End-to-end TTFA : 22036.61 ms Server TTFA : 20185.19 ms Inference first result : 20176.69 ms Inference latency : 20176.73 ms WAV encoding latency : 8.06 ms Generation latency : 20185.06 ms Client total latency : 24817.81 ms End-to-end latency : 25480.66 ms Server total latency : 20239.39 ms Connection to done : 20572.80 ms ================================================================ Saved WAV : C:\Users\re_nikitav\Desktop\tts\fish_speech_1.5\fish-speech-15.wav File size : 1,179,692 bytes Received bytes : 1,179,692 Received chunks : 19 Sample rate : 44100 Hz Channels : 1 Sample width : 2 bytes Frames : 589824 ================================================================ [playback] sample_rate=44100 Hz, channels=1, frames=589824 [playback] completed
