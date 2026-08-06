(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/Fish_audio_s1mini# docker logs 4074373a9d40
Traceback (most recent call last):
  File "/app/.venv/bin/uvicorn", line 6, in <module>
    sys.exit(main())
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 1569, in __call__
    return self.main(*args, **kwargs)
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 1490, in main
    rv = self.invoke(ctx)
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 1353, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 907, in invoke
    return callback(*args, **kwargs)
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/main.py", line 440, in main
    run(
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/main.py", line 609, in run
    config.load_app()
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/config.py", line 428, in load_app
    return import_from_string(self.app)
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/app/fish-speech/app/main.py", line 18, in <module>
    from fish_speech.utils.schema import ServeTTSRequest
  File "/app/fish-speech/fish_speech/utils/schema.py", line 12, in <module>
    from fish_speech.content_sequence import TextPart, VQPart
  File "/app/fish-speech/fish_speech/content_sequence.py", line 7, in <module>
    from fish_speech.tokenizer import (
ImportError: cannot import name 'IM_END_TOKEN' from 'fish_speech.tokenizer' (/app/fish-speech/fish_speech/tokenizer.py)
