curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }' \
  --output hello.mp3


curl --ssl-no-revoke \
  --fail-with-body \
  --request POST "https://api.fish.audio/v1/tts" \
  --header "Authorization: Bearer $FISH_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2-pro" \
  --data '{
    "text": "Hello from Fish Audio!",
    "format": "mp3"
  }' \
  --dump-header response-headers.txt \
  --output hello.mp3 \
  --write-out "\nHTTP status: %{http_code}\nContent type: %{content_type}\nDownloaded: %{size_download} bytes\n"

curl --ssl-no-revoke \
  -X POST "https://api.fish.audio/v1/tts" \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2-pro" \
  -d '{
    "text":"Hello from Fish Audio!",
    "format":"mp3"
  }'


(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# docker logs baf67d16e481
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:32: SyntaxWarning: invalid escape sequence '\_'
  """
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1012: SyntaxWarning: invalid escape sequence '\_'
  """Wrapper around scipy.signal.get_window so one can also get the
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1092: SyntaxWarning: invalid escape sequence '\_'
  """Compute how the STFT should be padded, based on match\_stride.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1131: SyntaxWarning: invalid escape sequence '\_'
  """Computes the short-time Fourier transform of the audio data,
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1222: SyntaxWarning: invalid escape sequence '\_'
  """Computes inverse STFT and sets it to audio\_data.
INFO:     Started server process [1]
INFO:     Waiting for application startup.
2026-08-04 01:00:38.825 | INFO     | __main__:lifespan:132 - Loading Fish Speech S2 Pro from /app/checkpoints/s2-pro
2026-08-04 01:00:39.654 | INFO     | fish_speech.models.text2semantic.llama:from_pretrained:504 - Injected Semantic IDs into Config: 151678-155773
2026-08-04 01:00:39.654 | INFO     | fish_speech.models.text2semantic.llama:from_pretrained:520 - Loading model from /app/checkpoints/s2-pro, config: DualARModelArgs(model_type='dual_ar', vocab_size=155776, n_layer=36, n_head=32, dim=2560, intermediate_size=9728, n_local_heads=8, head_dim=128, rope_base=1000000, norm_eps=1e-06, max_seq_len=32768, dropout=0.0, tie_word_embeddings=True, attention_qkv_bias=False, attention_o_bias=False, attention_qk_norm=True, codebook_size=4096, num_codebooks=10, semantic_begin_id=151678, semantic_end_id=155773, use_gradient_checkpointing=True, initializer_range=0.01976423537605237, is_reward_model=False, scale_codebook_embeddings=True, audio_embed_dim=2560, n_fast_layer=4, fast_dim=2560, fast_n_head=32, fast_n_local_heads=8, fast_head_dim=128, fast_intermediate_size=9728, fast_attention_qkv_bias=False, fast_attention_qk_norm=False, fast_attention_o_bias=False, norm_fastlayer_input=True)
2026-08-04 01:01:30.735 | INFO     | fish_speech.models.text2semantic.llama:from_pretrained:552 - Loading sharded safetensors weights
2026-08-04 01:01:33.304 | INFO     | fish_speech.models.text2semantic.llama:from_pretrained:588 - Model weights loaded - Status: <All keys matched successfully>
2026-08-04 01:02:42.867 | INFO     | fish_speech.models.text2semantic.inference:init_model:366 - Restored model from checkpoint
2026-08-04 01:02:42.868 | INFO     | fish_speech.models.text2semantic.inference:init_model:371 - Using DualARTransformer
Exception in thread Thread-2 (worker):
Traceback (most recent call last):
  File "/usr/lib/python3.12/threading.py", line 1073, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.12/threading.py", line 1010, in run
    self._target(*self._args, **self._kwargs)
  File "/app/fish_speech/models/text2semantic/inference.py", line 762, in worker
    model.setup_caches(
  File "/app/fish_speech/models/text2semantic/llama.py", line 711, in setup_caches
    super().setup_caches(max_batch_size, max_seq_len, dtype)
  File "/app/fish_speech/models/text2semantic/llama.py", line 318, in setup_caches
    b.attention.kv_cache = KVCache(
                           ^^^^^^^^
  File "/app/fish_speech/models/text2semantic/llama.py", line 202, in __init__
    self.register_buffer("k_cache", torch.zeros(cache_shape, dtype=dtype))
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.12/site-packages/torch/utils/_device.py", line 103, in __torch_function__
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
torch.AcceleratorError: CUDA error: out of memory
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
