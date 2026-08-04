(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# client_loop: send disconnect: Connection reset
PS C:\Users\re_nikitav> ssh 10.90.126.61
corp\re_nikitav@10.90.126.61's password:
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1053-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue Aug  4 08:28:22 UTC 2026

 * Ubuntu Pro delivers the most comprehensive open source security and
   compliance features.

   https://ubuntu.com/aws/pro

Expanded Security Maintenance for Applications is not enabled.

133 updates can be applied immediately.
6 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

49 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm

New release '24.04.4 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


1 updates could not be installed automatically. For more details,
see /var/log/unattended-upgrades/unattended-upgrades.log

*** System restart required ***
Last login: Tue Aug  4 00:29:07 2026 from 10.54.74.117
re_nikitav@EC03-E01-AICOE1:~$ sudo su
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav# docker ps -a
CONTAINER ID   IMAGE                          COMMAND                  CREATED       STATUS                   PORTS                                                             NAMES
baf67d16e481   fish_speech_tts                "/app/.venv/bin/pyth…"   8 hours ago   Up 8 hours (unhealthy)   8000/tcp, 8080/tcp, 0.0.0.0:8001->8001/tcp, [::]:8001->8001/tcp   musing_neumann
c219f35c2de1   cx_asr_realtime_nemotron_3.5   "/opt/nvidia/nvidia_…"   12 days ago   Up 12 days               0.0.0.0:8002->8002/tcp, [::]:8002->8002/tcp                       nemotron-base
e0b95fa09f9d   3d2ff0d4d458                   "/opt/nvidia/nvidia_…"   6 weeks ago   Up 6 weeks               0.0.0.0:5007->50051/tcp, [::]:5007->50051/tcp                     infallible_hoover
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
