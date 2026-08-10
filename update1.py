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
