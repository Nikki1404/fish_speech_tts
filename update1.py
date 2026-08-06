#20 7.213
#20 7.248 ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
#20 7.248 gradio 6.17.3 requires starlette<2.0,>=1.0.1, but you have starlette 0.47.3 which is incompatible.
#20 7.249 Successfully installed fastapi-0.116.1 httptools-0.8.0 numpy-1.26.4 starlette-0.47.3 uvloop-0.22.1 watchfiles-1.2.0 websockets-16.1.1
#20 DONE 7.4s

#21 [stage-0 13/18] RUN python - <<'PY'
#21 2.839 torch: 2.8.0+cu126
#21 2.839 torch CUDA: 12.6
#21 2.839 torchaudio: 2.8.0+cu126
#21 2.839 torchvision: 0.23.0+cu126
#21 DONE 3.4s

#22 [stage-0 14/18] RUN --mount=type=secret,id=hf_token     --mount=type=cache,target=/root/.cache/huggingface     HF_TOKEN="$(cat /run/secrets/hf_token)" &&     mkdir -p /app/checkpoints/s1-mini &&     hf download "fishaudio/s1-mini"         --revision "main"         --token "${HF_TOKEN}"         --local-dir /app/checkpoints/s1-mini         --max-workers 1 &&     test -f /app/checkpoints/s1-mini/model.pth &&     test -f /app/checkpoints/s1-mini/codec.pth &&     test -f /app/checkpoints/s1-mini/config.json &&     test -f /app/checkpoints/s1-mini/tokenizer.tiktoken &&     test -f /app/checkpoints/s1-mini/special_tokens.json
#22 0.272 cat: /run/secrets/hf_token: No such file or directory
#22 ERROR: process "/bin/sh -c HF_TOKEN=\"$(cat /run/secrets/hf_token)\" &&     mkdir -p /app/checkpoints/s1-mini &&     hf download \"${MODEL_REPO}\"         --revision \"${MODEL_REVISION}\"         --token \"${HF_TOKEN}\"         --local-dir /app/checkpoints/s1-mini         --max-workers 1 &&     test -f /app/checkpoints/s1-mini/model.pth &&     test -f /app/checkpoints/s1-mini/codec.pth &&     test -f /app/checkpoints/s1-mini/config.json &&     test -f /app/checkpoints/s1-mini/tokenizer.tiktoken &&     test -f /app/checkpoints/s1-mini/special_tokens.json" did not complete successfully: exit code: 1
------
 > [stage-0 14/18] RUN --mount=type=secret,id=hf_token     --mount=type=cache,target=/root/.cache/huggingface     HF_TOKEN="$(cat /run/secrets/hf_token)" &&     mkdir -p /app/checkpoints/s1-mini &&     hf download "fishaudio/s1-mini"         --revision "main"         --token "${HF_TOKEN}"         --local-dir /app/checkpoints/s1-mini         --max-workers 1 &&     test -f /app/checkpoints/s1-mini/model.pth &&     test -f /app/checkpoints/s1-mini/codec.pth &&     test -f /app/checkpoints/s1-mini/config.json &&     test -f /app/checkpoints/s1-mini/tokenizer.tiktoken &&     test -f /app/checkpoints/s1-mini/special_tokens.json:
0.272 cat: /run/secrets/hf_token: No such file or directory
------
ERROR: failed to build: failed to solve: process "/bin/sh -c HF_TOKEN=\"$(cat /run/secrets/hf_token)\" &&     mkdir -p /app/checkpoints/s1-mini &&     hf download \"${MODEL_REPO}\"         --revision \"${MODEL_REVISION}\"         --token \"${HF_TOKEN}\"         --local-dir /app/checkpoints/s1-mini         --max-workers 1 &&     test -f /app/checkpoints/s1-mini/model.pth &&     test -f /app/checkpoints/s1-mini/codec.pth &&     test -f /app/checkpoints/s1-mini/config.json &&     test -f /app/checkpoints/s1-mini/tokenizer.tiktoken &&     test -f /app/checkpoints/s1-mini/special_tokens.json" did not complete successfully: exit code: 1
