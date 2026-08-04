(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# nproc
free -h
df -h /

               total        used        free      shared  buff/cache   available
Mem:            30Gi        10Gi       4.2Gi       377Mi        16Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       518G  441G   77G  86% /
DOCKER_BUILDKIT=1 docker build \
  --progress=plain \
  -t fish-s2-cpu:latest \

#11 1.554 Download complete. Moving file to /app/checkpoints/s2-pro/tokenizer_config.json
#11 1.843 Download complete. Moving file to /app/checkpoints/s2-pro/overview.png
#11 31.53 Download complete. Moving file to /app/checkpoints/s2-pro/tokenizer.json
#11 103.7   2026-08-04T09:58:03.913337Z ERROR  Fatal Client Error: s3::get_range api call failed: error sending request for url (https://us.aws.cdn.hf.co/xorbs/default/99de89b329b8ea27b29a6fdd10a803ed662c1b56095fab78aee1361b42db5ac4?user_id=public&repo_id=69ae5f4aa257ccb6cd5b2abc&X-Xet-Session-Id=01KZ637T1HBJJH1Q6XY79S70D5&Expires=1785841048&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly91cy5hd3MuY2RuLmhmLmNvL3hvcmJzL2RlZmF1bHQvOTlkZTg5YjMyOWI4ZWEyN2IyOWE2ZmRkMTBhODAzZWQ2NjJjMWI1NjA5NWZhYjc4YWVlMTM2MWI0MmRiNWFjNFxcP3VzZXJfaWQ9cHVibGljJnJlcG9faWQ9NjlhZTVmNGFhMjU3Y2NiNmNkNWIyYWJjJlgtWGV0LVNlc3Npb24tSWQ9MDFLWjYzN1QxSEJKSkgxUTZYWTc5UzcwRDUiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkVwb2NoVGltZSI6MTc4NTg0MTA0OH0sIkJ5dGVSYW5nZSI6eyJFeHBlY3RlZEhlYWRlciI6ImJ5dGVzPTAtNTgzNDQ2NDcifX19XX0_&Signature=MEQCIBeOJcz7gHEDAJhYKPcz3nKmZmKpOm6pFKAtrfQgw0MZAiAVmfVGq2nyGPrZ-130P1hCDfHwgCHhBG-FzNNQIx3EOA__&Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F)
#11 103.7     at /home/runner/work/xet-core/xet-core/cas_client/src/retry_wrapper.rs:74
#11 103.7
#11 103.7   2026-08-04T09:58:03.913787Z ERROR  Fatal Client Error: s3::get_range api call failed: error sending request for url (https://us.aws.cdn.hf.co/xorbs/default/3fa77a5ad77320275208971a0ee83db4dc10309c7122091a197d7757cde129e3?user_id=public&repo_id=69ae5f4aa257ccb6cd5b2abc&X-Xet-Session-Id=01KZ637T1HBJJH1Q6XY79S70D5&Expires=1785841048&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly91cy5hd3MuY2RuLmhmLmNvL3hvcmJzL2RlZmF1bHQvM2ZhNzdhNWFkNzczMjAyNzUyMDg5NzFhMGVlODNkYjRkYzEwMzA5YzcxMjIwOTFhMTk3ZDc3NTdjZGUxMjllM1xcP3VzZXJfaWQ9cHVibGljJnJlcG9faWQ9NjlhZTVmNGFhMjU3Y2NiNmNkNWIyYWJjJlgtWGV0LVNlc3Npb24tSWQ9MDFLWjYzN1QxSEJKSkgxUTZYWTc5UzcwRDUiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkVwb2NoVGltZSI6MTc4NTg0MTA0OH0sIkJ5dGVSYW5nZSI6eyJFeHBlY3RlZEhlYWRlciI6ImJ5dGVzPTAtNTcyMDIyNjgifX19XX0_&Signature=MEYCIQCsRIbv8DVBrKv7SMUsJjugd0Wjb-b3FJamnfiqX6fw5AIhALKBQNH%7EopcJgKL5N1%7Ecb48aZjPXU%7ExM9%7EghXwNYzU3g&Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F)
#11 103.7     at /home/runner/work/xet-core/xet-core/cas_client/src/retry_wrapper.rs:74
#11 103.7
#11 148.3 Download complete. Moving file to /app/checkpoints/s2-pro/codec.pth
Fetching 13 files:  46%|████▌     | 6/13 [02:27<02:51, 24.50s/it]
#11 150.0 Download complete. Moving file to /app/checkpoints/s2-pro/model-00002-of-00002.safetensors
#11 150.0 Traceback (most recent call last):
#11 150.0   File "/app/.venv/bin/hf", line 10, in <module>
#11 150.0     sys.exit(main())
#11 150.0              ^^^^^^
#11 150.0   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/cli/hf.py", line 59, in main
#11 150.0     service.run()
#11 150.0   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/cli/download.py", line 136, in run
#11 150.0     print(self._download())  # Print path to downloaded files
#11 150.0           ^^^^^^^^^^^^^^^^
#11 150.0   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/cli/download.py", line 169, in _download
#11 150.0     return snapshot_download(
#11 150.0            ^^^^^^^^^^^^^^^^^^
#11 150.0   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
#11 150.1     return fn(*args, **kwargs)
#11 150.1            ^^^^^^^^^^^^^^^^^^^
#11 150.1   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/_snapshot_download.py", line 332, in snapshot_download
#11 150.1     thread_map(
#11 150.1   File "/app/.venv/lib/python3.12/site-packages/tqdm/contrib/concurrent.py", line 69, in thread_map
#11 150.1     return _executor_map(ThreadPoolExecutor, fn, *iterables, **tqdm_kwargs)
#11 150.1            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#11 150.1   File "/app/.venv/lib/python3.12/site-packages/tqdm/contrib/concurrent.py", line 51, in _executor_map
#11 150.1     return list(tqdm_class(ex.map(fn, *iterables, chunksize=chunksize), **kwargs))
#11 150.1            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#11 150.1   File "/app/.venv/lib/python3.12/site-packages/tqdm/std.py", line 1181, in __iter__
#11 150.1     for obj in iterable:
#11 150.1                ^^^^^^^^
#11 150.1   File "/usr/local/lib/python3.12/concurrent/futures/_base.py", line 619, in result_iterator
#11 150.2     yield _result_or_cancel(fs.pop())
#11 150.2           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#11 150.2   File "/usr/local/lib/python3.12/concurrent/futures/_base.py", line 317, in _result_or_cancel
#11 150.2     return fut.result(timeout)
#11 150.2            ^^^^^^^^^^^^^^^^^^^
#11 150.2   File "/usr/local/lib/python3.12/concurrent/futures/_base.py", line 449, in result
#11 150.2     return self.__get_result()
#11 150.2            ^^^^^^^^^^^^^^^^^^^
#11 150.2   File "/usr/local/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
#11 150.2     raise self._exception
#11 150.2   File "/usr/local/lib/python3.12/concurrent/futures/thread.py", line 59, in run
#11 150.2     result = self.fn(*self.args, **self.kwargs)
#11 150.2              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#11 150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/_snapshot_download.py", line 306, in _inner_hf_hub_download
#11 150.2     return hf_hub_download(
#11 150.2            ^^^^^^^^^^^^^^^^
#11 150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
#11 150.2     return fn(*args, **kwargs)
#11 150.2            ^^^^^^^^^^^^^^^^^^^
#11 150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 990, in hf_hub_download
#11 150.2     return _hf_hub_download_to_local_dir(
#11 150.2            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#11 150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1300, in _hf_hub_download_to_local_dir
#11 150.2     _download_to_tmp_and_move(
#11 150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1723, in _download_to_tmp_and_move
#11 150.2     xet_get(
#11 150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 629, in xet_get
#11 150.2     download_files(
#11 150.2 RuntimeError: Data processing error: CAS service error : ReqwestMiddleware Error: error sending request for url (https://us.aws.cdn.hf.co/xorbs/default/99de89b329b8ea27b29a6fdd10a803ed662c1b56095fab78aee1361b42db5ac4?user_id=public&repo_id=69ae5f4aa257ccb6cd5b2abc&X-Xet-Session-Id=01KZ637T1HBJJH1Q6XY79S70D5&Expires=1785841048&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly91cy5hd3MuY2RuLmhmLmNvL3hvcmJzL2RlZmF1bHQvOTlkZTg5YjMyOWI4ZWEyN2IyOWE2ZmRkMTBhODAzZWQ2NjJjMWI1NjA5NWZhYjc4YWVlMTM2MWI0MmRiNWFjNFxcP3VzZXJfaWQ9cHVibGljJnJlcG9faWQ9NjlhZTVmNGFhMjU3Y2NiNmNkNWIyYWJjJlgtWGV0LVNlc3Npb24tSWQ9MDFLWjYzN1QxSEJKSkgxUTZYWTc5UzcwRDUiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkVwb2NoVGltZSI6MTc4NTg0MTA0OH0sIkJ5dGVSYW5nZSI6eyJFeHBlY3RlZEhlYWRlciI6ImJ5dGVzPTAtNTgzNDQ2NDcifX19XX0_&Signature=MEQCIBeOJcz7gHEDAJhYKPcz3nKmZmKpOm6pFKAtrfQgw0MZAiAVmfVGq2nyGPrZ-130P1hCDfHwgCHhBG-FzNNQIx3EOA__&Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F)
#11 ERROR: process "/bin/sh -c mkdir -p /app/checkpoints/s2-pro &&     hf download \"${MODEL_REPO}\"         --revision \"${MODEL_REVISION}\"         --local-dir /app/checkpoints/s2-pro &&     test -f /app/checkpoints/s2-pro/codec.pth" did not complete successfully: exit code: 1
------
 > [stage-0 5/7] RUN --mount=type=cache,target=/root/.cache/huggingface     mkdir -p /app/checkpoints/s2-pro &&     hf download "fishaudio/s2-pro"         --revision "main"         --local-dir /app/checkpoints/s2-pro &&     test -f /app/checkpoints/s2-pro/codec.pth:
150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 990, in hf_hub_download
150.2     return _hf_hub_download_to_local_dir(
150.2            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1300, in _hf_hub_download_to_local_dir
150.2     _download_to_tmp_and_move(
150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1723, in _download_to_tmp_and_move
150.2     xet_get(
150.2   File "/app/.venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 629, in xet_get
150.2     download_files(
150.2 RuntimeError: Data processing error: CAS service error : ReqwestMiddleware Error: error sending request for url (https://us.aws.cdn.hf.co/xorbs/default/99de89b329b8ea27b29a6fdd10a803ed662c1b56095fab78aee1361b42db5ac4?user_id=public&repo_id=69ae5f4aa257ccb6cd5b2abc&X-Xet-Session-Id=01KZ637T1HBJJH1Q6XY79S70D5&Expires=1785841048&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly91cy5hd3MuY2RuLmhmLmNvL3hvcmJzL2RlZmF1bHQvOTlkZTg5YjMyOWI4ZWEyN2IyOWE2ZmRkMTBhODAzZWQ2NjJjMWI1NjA5NWZhYjc4YWVlMTM2MWI0MmRiNWFjNFxcP3VzZXJfaWQ9cHVibGljJnJlcG9faWQ9NjlhZTVmNGFhMjU3Y2NiNmNkNWIyYWJjJlgtWGV0LVNlc3Npb24tSWQ9MDFLWjYzN1QxSEJKSkgxUTZYWTc5UzcwRDUiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkVwb2NoVGltZSI6MTc4NTg0MTA0OH0sIkJ5dGVSYW5nZSI6eyJFeHBlY3RlZEhlYWRlciI6ImJ5dGVzPTAtNTgzNDQ2NDcifX19XX0_&Signature=MEQCIBeOJcz7gHEDAJhYKPcz3nKmZmKpOm6pFKAtrfQgw0MZAiAVmfVGq2nyGPrZ-130P1hCDfHwgCHhBG-FzNNQIx3EOA__&Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F)
------
ERROR: failed to build: failed to solve: process "/bin/sh -c mkdir -p /app/checkpoints/s2-pro &&     hf download \"${MODEL_REPO}\"         --revision \"${MODEL_REVISION}\"         --local-dir /app/checkpoints/s2-pro &&     test -f /app/checkpoints/s2-pro/codec.pth" did not complete successfully: exit code: 1

docker run -d \
  --name fish-s2-cpu \
  --restart unless-stopped \
  --cpus=12 \
  --shm-size=8g \
  -p 8000:8000 \
  -e DEVICE=cpu \
  -e OMP_NUM_THREADS=12 \
  -e MKL_NUM_THREADS=12 \
  -e OPENBLAS_NUM_THREADS=12 \
  fish-s2-cpu:latest

docker run -d \
  --name fish-s2-cpu \
  --restart unless-stopped \
  --cpus=16 \
  --memory=48g \
  --memory-swap=48g \
  --shm-size=16g \
  -p 8000:8000 \
  -e OMP_NUM_THREADS=16 \
  -e MKL_NUM_THREADS=16 \
  -e OPENBLAS_NUM_THREADS=16 \
  fish-s2-cpu:latest

docker run -d \
  --name fish-s2-cpu \
  --restart unless-stopped \
  --cpus=12 \
  --memory=32g \
  --memory-swap=32g \
  --shm-size=8g \
  -p 8000:8000 \
  -e OMP_NUM_THREADS=12 \
  -e MKL_NUM_THREADS=12 \
  -e OPENBLAS_NUM_THREADS=12 \
  fish-s2-cpu:latest



curl -X POST http://127.0.0.1:8000/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello there.",
    "format": "wav",
    "streaming": false,
    "chunk_length": 100,
    "max_new_tokens": 256
  }' \
  --output cpu-http-test.wav




python3 -m venv .client-venv
source .client-venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements-client.txt



python client.py \
  --url ws://127.0.0.1:8000/ws/tts \
  --text "Hello there." \
  --max-new-tokens 256 \
  --output cpu-websocket-test.wav
