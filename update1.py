#18 3.548 Downloading watchfiles-1.2.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (457 kB)
#18 3.604 Downloading websockets-16.1.1-cp310-cp310-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (186 kB)
#18 4.379 Installing collected packages: websockets, uvloop, numpy, httptools, watchfiles, starlette, fastapi
#18 4.605   Attempting uninstall: numpy
#18 4.607     Found existing installation: numpy 2.2.6
#18 4.691     Uninstalling numpy-2.2.6:
#18 6.691       Successfully uninstalled numpy-2.2.6
#18 8.822   Attempting uninstall: starlette
#18 8.824     Found existing installation: starlette 1.4.1
#18 8.829     Uninstalling starlette-1.4.1:
#18 8.883       Successfully uninstalled starlette-1.4.1
#18 8.962   Attempting uninstall: fastapi
#18 8.963     Found existing installation: fastapi 0.141.1
#18 8.972     Uninstalling fastapi-0.141.1:
#18 9.075       Successfully uninstalled fastapi-0.141.1
#18 9.171
#18 9.206 ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
#18 9.206 gradio 6.17.3 requires starlette<2.0,>=1.0.1, but you have starlette 0.47.3 which is incompatible.
#18 9.207 Successfully installed fastapi-0.116.1 httptools-0.8.0 numpy-1.26.4 starlette-0.47.3 uvloop-0.22.1 watchfiles-1.2.0 websockets-16.1.1
#18 DONE 9.3s

#19 [stage-0 11/14] RUN python - <<'PY'
#19 3.992 torch: 2.8.0+cu128
#19 3.992 torch CUDA: 12.8
#19 3.992 torchaudio: 2.8.0+cu128
#19 3.992 CUDA available during build: False
#19 3.992 Traceback (most recent call last):
#19 3.992   File "<stdin>", line 11, in <module>
#19 3.993 AssertionError
#19 ERROR: process "/bin/sh -c python - <<'PY'\nimport torch\nimport torchaudio\n\nprint(\"torch:\", torch.__version__)\nprint(\"torch CUDA:\", torch.version.cuda)\nprint(\"torchaudio:\", torchaudio.__version__)\nprint(\"CUDA available during build:\", torch.cuda.is_available())\n\nassert torch.__version__.startswith(\"2.8.0\")\nassert torchaudio.__version__.startswith(\"2.8.0\")\nassert torch.version.cuda == \"12.6\"\nPY" did not complete successfully: exit code: 1
------
 > [stage-0 11/14] RUN python - <<'PY':
3.992 torch: 2.8.0+cu128
3.992 torch CUDA: 12.8
3.992 torchaudio: 2.8.0+cu128
3.992 CUDA available during build: False
3.992 Traceback (most recent call last):
3.992   File "<stdin>", line 11, in <module>
3.993 AssertionError
------
ERROR: failed to build: failed to solve: process "/bin/sh -c python - <<'PY'\nimport torch\nimport torchaudio\n\nprint(\"torch:\", torch.__version__)\nprint(\"torch CUDA:\", torch.version.cuda)\nprint(\"torchaudio:\", torchaudio.__version__)\nprint(\"CUDA available during build:\", torch.cuda.is_available())\n\nassert torch.__version__.startswith(\"2.8.0\")\nassert torchaudio.__version__.startswith(\"2.8.0\")\nassert torch.version.cuda == \"12.6\"\nPY" did not complete successfully: exit code: 1
