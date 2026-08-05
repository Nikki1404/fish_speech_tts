(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_1.5# docker logs 655a9e76f135
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
  File "/app/fish-speech/app/main.py", line 20, in <module>
    from tools.server.model_manager import ModelManager
  File "/app/fish-speech/tools/server/model_manager.py", line 2, in <module>
    from funasr import AutoModel
  File "/app/.venv/lib/python3.10/site-packages/funasr/__init__.py", line 39, in <module>
    from funasr.auto.auto_model import AutoModel
  File "/app/.venv/lib/python3.10/site-packages/funasr/auto/auto_model.py", line 19, in <module>
    from funasr.utils.load_utils import load_bytes
  File "/app/.venv/lib/python3.10/site-packages/funasr/utils/load_utils.py", line 8, in <module>
    import torchaudio
  File "/app/.venv/lib/python3.10/site-packages/torchaudio/__init__.py", line 7, in <module>
    from . import _extension  # noqa  # usort: skip
  File "/app/.venv/lib/python3.10/site-packages/torchaudio/_extension/__init__.py", line 30, in <module>
    _IS_TORCHAUDIO_EXT_AVAILABLE = _load_lib("_torchaudio")
  File "/app/.venv/lib/python3.10/site-packages/torchaudio/_extension/utils.py", line 56, in _load_lib
    torch.ops.load_library(paths[0])
  File "/app/.venv/lib/python3.10/site-packages/torch/_ops.py", line 1295, in load_library
    ctypes.CDLL(path)
  File "/usr/lib/python3.10/ctypes/__init__.py", line 374, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libcudart.so.13: cannot open shared object file: No such file or directory
