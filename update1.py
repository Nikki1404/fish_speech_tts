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


docker run --rm \
  --gpus all \
  qwen3-tts \
  python -c "
import torch
print('Torch version :', torch.__version__)
print('Torch CUDA    :', torch.version.cuda)
print('CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU           :', torch.cuda.get_device_name(0))
"


(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/quen_3_tts# docker logs dff0c4df4792

==========
== CUDA ==
==========

CUDA Version 12.4.1

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.


********
Warning: flash-attn is not installed. Will only run the manual PyTorch version. Please install flash-attn for faster inference.
********

==========================================================================================
Qwen3-TTS CustomVoice WebSocket Server
==========================================================================================
CUDA available : True
GPU            : NVIDIA A10G
Model path     : /app/models/Qwen3-TTS-12Hz-1.7B-CustomVoice
Traceback (most recent call last):
  File "/opt/venv/bin/uvicorn", line 8, in <module>
    sys.exit(main())
  File "/opt/venv/lib/python3.10/site-packages/click/core.py", line 1569, in __call__
    return self.main(*args, **kwargs)
  File "/opt/venv/lib/python3.10/site-packages/click/core.py", line 1490, in main
    rv = self.invoke(ctx)
  File "/opt/venv/lib/python3.10/site-packages/click/core.py", line 1353, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/opt/venv/lib/python3.10/site-packages/click/core.py", line 907, in invoke
    return callback(*args, **kwargs)
  File "/opt/venv/lib/python3.10/site-packages/uvicorn/main.py", line 440, in main
    run(
  File "/opt/venv/lib/python3.10/site-packages/uvicorn/main.py", line 609, in run
    config.load_app()
  File "/opt/venv/lib/python3.10/site-packages/uvicorn/config.py", line 428, in load_app
    return import_from_string(self.app)
  File "/opt/venv/lib/python3.10/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/app/server.py", line 29, in <module>
    model = Qwen3TTSModel.from_pretrained(
  File "/opt/venv/lib/python3.10/site-packages/qwen_tts/inference/qwen3_tts_model.py", line 112, in from_pretrained
    model = AutoModel.from_pretrained(pretrained_model_name_or_path, **kwargs)
  File "/opt/venv/lib/python3.10/site-packages/transformers/models/auto/auto_factory.py", line 604, in from_pretrained
    return model_class.from_pretrained(
  File "/opt/venv/lib/python3.10/site-packages/qwen_tts/core/models/modeling_qwen3_tts.py", line 1876, in from_pretrained
    model = super().from_pretrained(
  File "/opt/venv/lib/python3.10/site-packages/transformers/modeling_utils.py", line 277, in _wrapper
    return func(*args, **kwargs)
  File "/opt/venv/lib/python3.10/site-packages/transformers/modeling_utils.py", line 5048, in from_pretrained
    ) = cls._load_pretrained_model(
  File "/opt/venv/lib/python3.10/site-packages/transformers/modeling_utils.py", line 5468, in _load_pretrained_model
    _error_msgs, disk_offload_index = load_shard_file(args)
  File "/opt/venv/lib/python3.10/site-packages/transformers/modeling_utils.py", line 843, in load_shard_file
    disk_offload_index = _load_state_dict_into_meta_model(
  File "/opt/venv/lib/python3.10/site-packages/torch/utils/_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
  File "/opt/venv/lib/python3.10/site-packages/transformers/modeling_utils.py", line 748, in _load_state_dict_into_meta_model
    param = param[...]
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 594.00 MiB. GPU 0 has a total capacity of 22.09 GiB of which 104.19 MiB is free. Including non-PyTorch memory, this process has 0 bytes memory in use. Of the allocated memory 2.97 GiB is allocated by PyTorch, and 9.72 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
