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


Hi Ashutosh,

I completed an initial comparison of **Fish Speech 1.5, Fish S1 Mini, and Qwen3-TTS 0.6B CustomVoice** using the same test text.

| Area                           | Fish Speech 1.5          | Fish S1 Mini             | Qwen3-TTS 0.6B                                 |
| ------------------------------ | ------------------------ | ------------------------ | ---------------------------------------------- |
| **Server TTFA**                | 20.19s                   | **9.39s (Best)**         | 24.03s                                         |
| **Client TTFA**                | 21.37s                   | **11.47s (Best)**        | 25.03s                                         |
| **Client Total**               | 24.82s                   | **24.73s**               | 25.84s                                         |
| **Emotion Control**            | Limited/less direct      | Emotion markers          | **Natural-language `instruct`**                |
| **Emotion Adherence (tested)** | Not specifically tested  | Subtle/inconsistent      | **Best**                                       |
| **Speakers**                   | Reference-audio oriented | Reference-audio oriented | **Multiple built-in speakers**                 |
| **Voice Cloning**              | Yes                      | Yes                      | **Yes (via Qwen Base/voice-cloning workflow)** |

**Key takeaway:**

* **Fish S1 Mini** currently has the best TTFA and starts audio much earlier.
* **Qwen3-TTS** was noticeably better for emotion/tone control. Instructions like *“Speak professionally and empathetically”* were reflected much more accurately than S1 Mini's `(excited)`, `(empathetic)`, etc. markers.
* Qwen CustomVoice also provides multiple built-in speakers (e.g. Aiden), while both Fish and Qwen support voice-cloning workflows.

So currently: **Fish S1 Mini → latency advantage; Qwen3-TTS → emotion/style and speaker-control advantage.** Qwen's main issue is the current ~24s server TTFA, which needs optimization.



https://console.cloud.google.com/artifacts/docker/emr-dgt-autonomous-uctr1-snbx/us-central1/qwen-3-tts?project=emr-dgt-autonomous-uctr1-snbx
docker tag qwen3-tts:latest us-central1-docker.pkg.dev/emr-dgt-autonomous-uctr1-snbx/qwen-3-tts/qwen3-tts:latest
https://qwen3-tts-150916788856.us-central1.run.app
                                                                                                              
                                                                                                              
Connection / startup    : 622.89 ms
Connection -> response  : 264.91 ms
Connection -> audio     : 11623.30 ms
E2E TTFB                : 887.80 ms
E2E TTFT/TTFA           : 12246.19 ms
E2E TOTAL               : 12658.61 ms

python qwen_cloudrun_loadtest.py --url wss://qwen3-tts-150916788856.us-central1.run.app/ws/tts --project emr-dgt-autonomous-uctr1-snbx --service qwen3-tts --region us-central1 --levels 1 5 10 15 20 22 24 25 26 28 30 35 40 45 50 60 70 80
  python client.py --text "Hello, thank you for calling Inspira Financial. How can I help you today?" --language English --speaker Aiden --instruct "Speak in a professional customer service tone." --output warm.wav --play
py -3.11 cold_start_client.py --mode openai --file "C:\Users\re_nikitav\Documents\test.wav" --openai-url "https://nemotron-3-5-150916788856.us-central1.run.app/v1/audio/transcriptions" --language en-US --runs 2
py -3.11 cold_start_client.py --mode websocket --mic --language en-US --duration 10 --runs 2 --delay 2
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              (base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# python3 -m pip install -U huggingface_hub
Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
Requirement already satisfied: huggingface_hub in /root/anaconda3/lib/python3.7/site-packages (0.16.4)
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
Requirement already satisfied: filelock in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (3.0.12)
Requirement already satisfied: fsspec in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (2023.1.0)
Requirement already satisfied: requests in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (2.31.0)
Requirement already satisfied: tqdm>=4.42.1 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (4.67.0)
Requirement already satisfied: pyyaml>=5.1 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (5.3)
Requirement already satisfied: typing-extensions>=3.7.4.3 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (4.7.1)
Requirement already satisfied: packaging>=20.9 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (24.0)
Requirement already satisfied: importlib-metadata in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (1.5.0)
Requirement already satisfied: zipp>=0.5 in /root/anaconda3/lib/python3.7/site-packages (from importlib-metadata->huggingface_hub) (3.15.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (3.4.0)
Requirement already satisfied: idna<4,>=2.5 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (2.8)
Requirement already satisfied: urllib3<3,>=1.21.1 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (2.0.7)
Requirement already satisfied: certifi>=2017.4.17 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (2024.8.30)
DEPRECATION: pyodbc 4.0.0-unsupported has a non-standard version number. pip 24.1 will enforce this behaviour change. A possible replacement is to upgrade to a newer version of pyodbc or contact the author to suggest that they release a version with a conforming version number. Discussion can be found at https://github.com/pypa/pip/issues/12063
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# hf --version
hf: command not found
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# unset http_proxy
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# unset https_proxy
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# hf --version
hf: command not found
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# python3 -m pip install -U huggingface_hub
Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
Requirement already satisfied: huggingface_hub in /root/anaconda3/lib/python3.7/site-packages (0.16.4)
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/huggingface-hub/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/huggingface-hub/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/huggingface-hub/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/huggingface-hub/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProtocolError('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))': /simple/huggingface-hub/
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7d44a7dea0d0>: Failed to establish a new connection: [Errno -2] Name or service not known')': /huggingface-hub/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7d44a7dea310>: Failed to establish a new connection: [Errno -2] Name or service not known')': /huggingface-hub/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7d44a7de0a90>: Failed to establish a new connection: [Errno -2] Name or service not known')': /huggingface-hub/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7d44a7de0890>: Failed to establish a new connection: [Errno -2] Name or service not known')': /huggingface-hub/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7d44a7de0510>: Failed to establish a new connection: [Errno -2] Name or service not known')': /huggingface-hub/
Requirement already satisfied: filelock in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (3.0.12)
Requirement already satisfied: fsspec in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (2023.1.0)
Requirement already satisfied: requests in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (2.31.0)
Requirement already satisfied: tqdm>=4.42.1 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (4.67.0)
Requirement already satisfied: pyyaml>=5.1 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (5.3)
Requirement already satisfied: typing-extensions>=3.7.4.3 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (4.7.1)
Requirement already satisfied: packaging>=20.9 in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (24.0)
Requirement already satisfied: importlib-metadata in /root/anaconda3/lib/python3.7/site-packages (from huggingface_hub) (1.5.0)
Requirement already satisfied: zipp>=0.5 in /root/anaconda3/lib/python3.7/site-packages (from importlib-metadata->huggingface_hub) (3.15.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (3.4.0)
Requirement already satisfied: idna<4,>=2.5 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (2.8)
Requirement already satisfied: urllib3<3,>=1.21.1 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (2.0.7)
Requirement already satisfied: certifi>=2017.4.17 in /root/anaconda3/lib/python3.7/site-packages (from requests->huggingface_hub) (2024.8.30)
DEPRECATION: pyodbc 4.0.0-unsupported has a non-standard version number. pip 24.1 will enforce this behaviour change. A possible replacement is to upgrade to a newer version of pyodbc or contact the author to suggest that they release a version with a conforming version number. Discussion can be found at https://github.com/pypa/pip/issues/12063
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# ls
Fish_audio_s1mini  fish_speech_1.5  nemotron_finetuned  nemotron_finetuned_fixed  nemotron_finetuned_updated  quen_3_tts
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# cd quen_3_tts/
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# vi Dockerfile
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# export http_proxy=http_proxy="http://163.116.128.80:8080
> ^C
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# export http_proxy=http://163.116.128.80:8080
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# export https_proxy=http://163.116.128.80:8080
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# python3 -m pip install -U huggingface_hub
Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
Requirement already satisfied: huggingface_hub in /root/anaconda3/lib/python3.7/site-packages (0.16.4)
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
^CERROR: Operation cancelled by user
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# export https_proxy="http://163.116.128.80:8080"
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# export http_proxy="http://163.116.128.80:8080"
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# python3 -m pip install -U huggingface_hub
Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
Requirement already satisfied: huggingface_hub in /root/anaconda3/lib/python3.7/site-packages (0.16.4)
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'))': /huggingface-hub/
^CERROR: Operation cancelled by user
