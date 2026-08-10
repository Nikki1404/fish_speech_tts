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


(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# docker logs f6d6b7360f51

==========
== CUDA ==
==========

CUDA Version 12.8.1

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.


********
Warning: flash-attn is not installed. Will only run the manual PyTorch version. Please install flash-attn for faster inference.
********

/bin/sh: 1: sox: not found
SoX could not be found!

    If you do not have SoX, proceed here:
     - - - http://sox.sourceforge.net/ - - -

    If you do (or think that you should) have SoX, double-check your
    path variables.

==========================================================================================
Qwen3-TTS CustomVoice WebSocket Server
==========================================================================================
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:188: UserWarning: CUDA initialization: The NVIDIA driver on your system is too old (found version 12080). Please update your GPU driver by downloading and installing a new version from the URL: http://www.nvidia.com/Download/index.aspx Alternatively, go to: https://pytorch.org to install a PyTorch version that has been compiled with your version of the CUDA driver. (Triggered internally at /__w/pytorch/pytorch/c10/cuda/CUDAFunctions.cpp:119.)
  return torch._C._cuda_getDeviceCount() > 0
Traceback (most recent call last):
  File "/usr/local/bin/uvicorn", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/click/core.py", line 1569, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/click/core.py", line 1490, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/click/core.py", line 1353, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/click/core.py", line 907, in invoke
    return callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/uvicorn/main.py", line 440, in main
    run(
  File "/usr/local/lib/python3.12/dist-packages/uvicorn/main.py", line 609, in run
    config.load_app()
  File "/usr/local/lib/python3.12/dist-packages/uvicorn/config.py", line 428, in load_app
    return import_from_string(self.app)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/dist-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/app/server.py", line 22, in <module>
    raise RuntimeError("CUDA GPU is not available inside the container.")
RuntimeError: CUDA GPU is not available inside the container.
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts#
