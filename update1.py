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



 => => extracting sha256:3d6ab8c799cda2f4c6a6277b0e24dd2231c5de83b0316968b7cce81156bb8be0                                                              0.0s
 => => extracting sha256:7209097bfb98d6f8b422984480f1fddead5ea62f8900ff6b6548e060b71aca76                                                              0.0s
 => => extracting sha256:545a3ada5b6bc612a11c13a659775d67eeda5a61615e7f49c76ecd24adcad626                                                              0.0s
 => => extracting sha256:4614b301ea4206e46e0a8db954fcb25bb0a89da5d116f75fc3e5820ff0f416b0                                                             13.9s
 => [internal] load build context                                                                                                                      0.0s
 => => transferring context: 94B                                                                                                                       0.0s
 => [2/9] WORKDIR /app                                                                                                                                 6.8s
 => [3/9] RUN apt-get update && apt-get install -y --no-install-recommends     python3     python3-pip     python3-dev     ffmpeg     libsndfile1    127.3s
 => ERROR [4/9] RUN python3 -m pip install --upgrade pip setuptools wheel --break-system-packages                                                      3.0s
------
 > [4/9] RUN python3 -m pip install --upgrade pip setuptools wheel --break-system-packages:
0.614 Requirement already satisfied: pip in /usr/lib/python3/dist-packages (24.0)
0.781 Collecting pip
0.855   Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
0.857 Requirement already satisfied: setuptools in /usr/lib/python3/dist-packages (68.1.2)
1.153 Collecting setuptools
1.165   Downloading setuptools-84.0.0-py3-none-any.whl.metadata (6.6 kB)
1.168 Requirement already satisfied: wheel in /usr/lib/python3/dist-packages (0.42.0)
1.209 Collecting wheel
1.221   Downloading wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)
1.294 Collecting packaging>=24.0 (from wheel)
1.307   Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
1.321 Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
1.690    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 5.0 MB/s eta 0:00:00
1.702 Downloading setuptools-84.0.0-py3-none-any.whl (818 kB)
1.760    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 818.2/818.2 kB 14.3 MB/s eta 0:00:00
1.772 Downloading wheel-0.47.0-py3-none-any.whl (32 kB)
1.783 Downloading packaging-26.3-py3-none-any.whl (129 kB)
1.786    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 130.0/130.0 kB 249.0 MB/s eta 0:00:00
1.846 Installing collected packages: setuptools, pip, packaging, wheel
1.846   Attempting uninstall: setuptools
1.849     Found existing installation: setuptools 68.1.2
1.852     Uninstalling setuptools-68.1.2:
2.215       Successfully uninstalled setuptools-68.1.2
2.844   Attempting uninstall: pip
2.848     Found existing installation: pip 24.0
2.849 ERROR: Cannot uninstall pip 24.0, RECORD file not found. Hint: The package was installed by debian.
------
Dockerfile:23
--------------------
  21 |         && rm -rf /var/lib/apt/lists/*
  22 |
  23 | >>> RUN python3 -m pip install --upgrade pip setuptools wheel --break-system-packages
  24 |
  25 |     COPY requirement.txt .
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c python3 -m pip install --upgrade pip setuptools wheel --break-system-packages" did not complete successfully: exit code: 1
