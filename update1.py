(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/Fish_audio_s1mini# docker logs 2d37e9c0b3e8
INFO:     Started server process [1]
INFO:     Waiting for application startup.
2026-08-06 01:30:09.048 | INFO     | app.main:lifespan:154 - Loading Fish Speech S1 Mini from /app/checkpoints/s1-mini
2026-08-06 01:30:09.050 | WARNING  | fish_speech.models.text2semantic.llama:from_pretrained:508 - Failed to load tokenizer for config injection: The checkpoint you are trying to load has model type `dual_ar` but Transformers does not recognize this architecture. This could be because of an issue with the checkpoint, or because your version of Transformers is out of date.

You can update Transformers with the command `pip install --upgrade transformers`. If this does not work, and the checkpoint is very new, then there may not be a release version that supports this model yet. In this case, you can get the most up-to-date code by installing Transformers from source with the command `pip install git+https://github.com/huggingface/transformers.git`. Semantic IDs might be 0.
2026-08-06 01:30:09.050 | INFO     | fish_speech.models.text2semantic.llama:from_pretrained:520 - Loading model from /app/checkpoints/s1-mini, config: DualARModelArgs(model_type='dual_ar', vocab_size=155776, n_layer=28, n_head=16, dim=1024, intermediate_size=3072, n_local_heads=8, head_dim=128, rope_base=1000000, norm_eps=1e-06, max_seq_len=8192, dropout=0.0, tie_word_embeddings=False, attention_qkv_bias=False, attention_o_bias=False, attention_qk_norm=True, codebook_size=4096, num_codebooks=10, semantic_begin_id=0, semantic_end_id=0, use_gradient_checkpointing=True, initializer_range=0.03125, is_reward_model=False, scale_codebook_embeddings=True, audio_embed_dim=None, n_fast_layer=4, fast_dim=1024, fast_n_head=16, fast_n_local_heads=8, fast_head_dim=64, fast_intermediate_size=3072, fast_attention_qkv_bias=False, fast_attention_qk_norm=False, fast_attention_o_bias=False, norm_fastlayer_input=False)
2026-08-06 01:30:18.978 | INFO     | fish_speech.models.text2semantic.llama:from_pretrained:588 - Model weights loaded - Status: <All keys matched successfully>
2026-08-06 01:30:24.300 | INFO     | fish_speech.models.text2semantic.inference:init_model:366 - Restored model from checkpoint
2026-08-06 01:30:24.300 | INFO     | fish_speech.models.text2semantic.inference:init_model:371 - Using DualARTransformer
2026-08-06 01:30:24.322 | INFO     | tools.server.model_manager:load_llama_model:70 - LLAMA model loaded.
/app/.venv/lib/python3.10/site-packages/torch/nn/utils/weight_norm.py:144: FutureWarning: `torch.nn.utils.weight_norm` is deprecated in favor of `torch.nn.utils.parametrizations.weight_norm`.
  WeightNorm.apply(module, name, dim)
2026-08-06 01:30:46.028 | INFO     | fish_speech.models.dac.inference:load_model:46 - Loaded model: _IncompatibleKeys(missing_keys=[], unexpected_keys=['encoder.block.4.block.5.freqs_cis', 'encoder.block.4.block.5.causal_mask', 'quantizer.pre_module.freqs_cis', 'quantizer.pre_module.causal_mask', 'quantizer.post_module.freqs_cis', 'quantizer.post_module.causal_mask'])
2026-08-06 01:30:46.029 | INFO     | tools.server.model_manager:load_decoder_model:78 - Decoder model loaded.
/app/fish-speech/fish_speech/inference_engine/reference_loader.py:39: UserWarning: torchaudio._backend.list_audio_backends has been deprecated. This deprecation is part of a large refactoring effort to transition TorchAudio into a maintenance phase. The decoding and encoding capabilities of PyTorch for both audio and video are being consolidated into TorchCodec. Please see https://github.com/pytorch/audio/issues/3902 for more information. It will be removed from the 2.9 release.
  backends = torchaudio.list_audio_backends()
2026-08-06 01:30:46.033 | INFO     | fish_speech.models.text2semantic.inference:generate_long:609 - Split into 0 turns, grouped into 1 batches
2026-08-06 01:30:46.033 | INFO     | fish_speech.models.text2semantic.inference:generate_long:621 - --- Sample 0, Batch 0 (12 bytes) ---
2026-08-06 01:30:46.033 | INFO     | fish_speech.models.text2semantic.inference:generate_long:625 - Batch text: Hello world.
2026-08-06 01:30:46.033 | INFO     | fish_speech.models.text2semantic.inference:generate_long:651 - Visualizing prompt structure:
2026-08-06 01:30:46.034 | ERROR    | fish_speech.models.text2semantic.inference:worker:790 - Traceback (most recent call last):
  File "/app/fish-speech/fish_speech/models/text2semantic/inference.py", line 778, in worker
    for chunk in generate_long(
  File "/app/fish-speech/fish_speech/models/text2semantic/inference.py", line 652, in generate_long
    conversation_gen.visualize(
  File "/app/fish-speech/fish_speech/conversation.py", line 119, in visualize
    content_seq.visualize(
  File "/app/fish-speech/fish_speech/content_sequence.py", line 336, in visualize
    encoded = self.encode(
  File "/app/fish-speech/fish_speech/content_sequence.py", line 196, in encode
    tokens = tokenizer.encode(part.text, add_special_tokens=False)
AttributeError: 'NoneType' object has no attribute 'encode'

2026-08-06 01:30:46.034 | ERROR    | app.main:lifespan:172 - Model startup failed
Traceback (most recent call last):

  File "/app/.venv/bin/uvicorn", line 6, in <module>
    sys.exit(main())
    │   │    └ <Command main>
    │   └ <built-in function exit>
    └ <module 'sys' (built-in)>
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 1569, in __call__
    return self.main(*args, **kwargs)
           │    │     │       └ {}
           │    │     └ ()
           │    └ <function Command.main at 0x7af445ec8700>
           └ <Command main>
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 1490, in main
    rv = self.invoke(ctx)
         │    │      └ <click.core.Context object at 0x7af4469c8df0>
         │    └ <function Command.invoke at 0x7af445ec85e0>
         └ <Command main>
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 1353, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           │   │      │    │           │   └ {'host': '0.0.0.0', 'port': 8001, 'workers': 1, 'app': 'app.main:app', 'uds': None, 'fd': None, 'reload': False, 'reload_dirs...
           │   │      │    │           └ <click.core.Context object at 0x7af4469c8df0>
           │   │      │    └ <function main at 0x7af445c0ca60>
           │   │      └ <Command main>
           │   └ <function Context.invoke at 0x7af445ebb910>
           └ <click.core.Context object at 0x7af4469c8df0>
  File "/app/.venv/lib/python3.10/site-packages/click/core.py", line 907, in invoke
    return callback(*args, **kwargs)
           │         │       └ {'host': '0.0.0.0', 'port': 8001, 'workers': 1, 'app': 'app.main:app', 'uds': None, 'fd': None, 'reload': False, 'reload_dirs...
           │         └ ()
           └ <function main at 0x7af445c0ca60>
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/main.py", line 440, in main
    run(
    └ <function run at 0x7af445d24550>
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/main.py", line 621, in run
    server.run()
    │      └ <function Server.run at 0x7af445cb4d30>
    └ <uvicorn.server.Server object at 0x7af445bf34c0>
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/server.py", line 77, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           │           │    │             │                      │    │      └ <function Config.get_loop_factory at 0x7af445fe60e0>
           │           │    │             │                      │    └ <uvicorn.config.Config object at 0x7af445d28400>
           │           │    │             │                      └ <uvicorn.server.Server object at 0x7af445bf34c0>
           │           │    │             └ None
           │           │    └ <function Server.serve at 0x7af445cb4dc0>
           │           └ <uvicorn.server.Server object at 0x7af445bf34c0>
           └ <function asyncio_run at 0x7af445f88f70>
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/_compat.py", line 60, in asyncio_run
    return loop.run_until_complete(main)
           │    │                  └ <coroutine object Server.serve at 0x7af30a7e1a80>
           │    └ <cyfunction Loop.run_until_complete at 0x7af30a8bf700>
           └ <uvloop.Loop running=True closed=False debug=False>
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/lifespan/on.py", line 86, in main
    await app(scope, self.receive, self.send)
          │   │      │    │        │    └ <function LifespanOn.send at 0x7af30a411ea0>
          │   │      │    │        └ <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>
          │   │      │    └ <function LifespanOn.receive at 0x7af30a411f30>
          │   │      └ <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>
          │   └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
          └ <uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware object at 0x7af30a730130>
  File "/app/.venv/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 30, in __call__
    return await self.app(scope, receive, send)
                 │    │   │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
                 │    │   │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
                 │    │   └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
                 │    └ <fastapi.applications.FastAPI object at 0x7af4459680d0>
                 └ <uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware object at 0x7af30a730130>
  File "/app/.venv/lib/python3.10/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
                           │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
                           │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
                           └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
  File "/app/.venv/lib/python3.10/site-packages/starlette/applications.py", line 113, in __call__
    await self.middleware_stack(scope, receive, send)
          │    │                │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │                │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │                └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
          │    └ <starlette.middleware.errors.ServerErrorMiddleware object at 0x7af30a400d30>
          └ <fastapi.applications.FastAPI object at 0x7af4459680d0>
  File "/app/.venv/lib/python3.10/site-packages/starlette/middleware/errors.py", line 151, in __call__
    await self.app(scope, receive, send)
          │    │   │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │   │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │   └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
          │    └ <starlette.middleware.exceptions.ExceptionMiddleware object at 0x7af30a400d00>
          └ <starlette.middleware.errors.ServerErrorMiddleware object at 0x7af30a400d30>
  File "/app/.venv/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 49, in __call__
    await self.app(scope, receive, send)
          │    │   │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │   │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │   └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
          │    └ <fastapi.routing.APIRouter object at 0x7af30a94b430>
          └ <starlette.middleware.exceptions.ExceptionMiddleware object at 0x7af30a400d00>
  File "/app/.venv/lib/python3.10/site-packages/starlette/routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
          │    │                │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │                │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │                └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
          │    └ <bound method Router.app of <fastapi.routing.APIRouter object at 0x7af30a94b430>>
          └ <fastapi.routing.APIRouter object at 0x7af30a94b430>
  File "/app/.venv/lib/python3.10/site-packages/starlette/routing.py", line 725, in app
    await self.lifespan(scope, receive, send)
          │    │        │      │        └ <bound method LifespanOn.send of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │        │      └ <bound method LifespanOn.receive of <uvicorn.lifespan.on.LifespanOn object at 0x7af30a730100>>
          │    │        └ {'type': 'lifespan', 'asgi': {'version': '3.0', 'spec_version': '2.0'}, 'state': {}, 'app': <fastapi.applications.FastAPI obj...
          │    └ <function Router.lifespan at 0x7af42fbf69e0>
          └ <fastapi.routing.APIRouter object at 0x7af30a94b430>
  File "/app/.venv/lib/python3.10/site-packages/starlette/routing.py", line 694, in lifespan
    async with self.lifespan_context(app) as maybe_state:
               │    │                └ <fastapi.applications.FastAPI object at 0x7af4459680d0>
               │    └ <function lifespan at 0x7af30a6b7e20>
               └ <fastapi.routing.APIRouter object at 0x7af30a94b430>

> File "/app/fish-speech/app/main.py", line 157, in lifespan
    state.model_manager = await asyncio.to_thread(
    │     │                     │       └ <function to_thread at 0x7af4460bdea0>
    │     │                     └ <module 'asyncio' from '/usr/lib/python3.10/asyncio/__init__.py'>
    │     └ None
    └ <app.main.ServerState object at 0x7af4459680a0>

  File "/usr/lib/python3.10/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
                 │    │                     └ functools.partial(<built-in method run of _contextvars.Context object at 0x7af30a736180>, <class 'tools.server.model_manager....
                 │    └ <cyfunction Loop.run_in_executor at 0x7af30a720a00>
                 └ <uvloop.Loop running=True closed=False debug=False>
  File "/usr/lib/python3.10/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             │        │            └ None
             │        └ None
             └ None

  File "/app/fish-speech/tools/server/model_manager.py", line 54, in __init__
    self.warm_up(self.tts_inference_engine)
    │    │       │    └ <fish_speech.inference_engine.TTSInferenceEngine object at 0x7af3089b17e0>
    │    │       └ <tools.server.model_manager.ModelManager object at 0x7af30a4010f0>
    │    └ <function ModelManager.warm_up at 0x7af30a6b7ac0>
    └ <tools.server.model_manager.ModelManager object at 0x7af30a4010f0>

  File "/app/fish-speech/tools/server/model_manager.py", line 92, in warm_up
    list(inference(request, tts_inference_engine))
         │         │        └ <fish_speech.inference_engine.TTSInferenceEngine object at 0x7af3089b17e0>
         │         └ ServeTTSRequest(text='Hello world.', chunk_length=200, format='wav', latency='normal', references=[], reference_id=None, seed...
         └ <function inference_wrapper at 0x7af30a987010>

  File "/app/fish-speech/tools/server/inference.py", line 25, in inference_wrapper
    raise HTTPException(
          └ <class 'baize.exceptions.HTTPException'>

baize.exceptions.HTTPException: (<HTTPStatus.INTERNAL_SERVER_ERROR: 500>, '"\'NoneType\' object has no attribute \'encode\'"')
ERROR:    Traceback (most recent call last):
  File "/app/.venv/lib/python3.10/site-packages/starlette/routing.py", line 694, in lifespan
    async with self.lifespan_context(app) as maybe_state:
  File "/usr/lib/python3.10/contextlib.py", line 199, in __aenter__
    return await anext(self.gen)
  File "/app/fish-speech/app/main.py", line 157, in lifespan
    state.model_manager = await asyncio.to_thread(
  File "/usr/lib/python3.10/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
  File "/usr/lib/python3.10/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/app/fish-speech/tools/server/model_manager.py", line 54, in __init__
    self.warm_up(self.tts_inference_engine)
  File "/app/fish-speech/tools/server/model_manager.py", line 92, in warm_up
    list(inference(request, tts_inference_engine))
  File "/app/fish-speech/tools/server/inference.py", line 25, in inference_wrapper
    raise HTTPException(
baize.exceptions.HTTPException: (<HTTPStatus.INTERNAL_SERVER_ERROR: 500>, '"\'NoneType\' object has no attribute \'encode\'"')

ERROR:    Application startup failed. Exiting.
