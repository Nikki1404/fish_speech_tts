import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import websockets

ROOT = Path(__file__).resolve().parents[1]


def wait_http(url: str, timeout: float = 20.0) -> None:
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1).read()
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Timed out waiting for {url}")


async def ws_test() -> None:
    output = ROOT / "output" / "smoke.wav"
    output.parent.mkdir(exist_ok=True)
    received = bytearray()
    done = False
    async with websockets.connect("ws://127.0.0.1:18880/ws/tts", max_size=None) as ws:
        await ws.send(json.dumps({"text": "Smoke test", "streaming": True}))
        async for message in ws:
            if isinstance(message, bytes):
                received.extend(message)
            else:
                event = json.loads(message)
                if event.get("type") == "error":
                    raise RuntimeError(event)
                if event.get("type") == "done":
                    done = True
    output.write_bytes(received)
    assert done
    assert received[:4] == b"RIFF"
    assert len(received) > 1000
    print(f"Smoke test passed: {output} ({len(received)} bytes)")


def main() -> int:
    env = os.environ.copy()
    env["FISH_HTTP_URL"] = "http://127.0.0.1:18080"
    mock = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "tests.mock_fish_server:app", "--host", "127.0.0.1", "--port", "18080"],
        cwd=ROOT,
        env=env,
    )
    gateway = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "18880"],
        cwd=ROOT,
        env=env,
    )
    try:
        wait_http("http://127.0.0.1:18080/v1/health")
        wait_http("http://127.0.0.1:18880/health")
        asyncio.run(ws_test())
        return 0
    finally:
        gateway.terminate()
        mock.terminate()
        gateway.wait(timeout=5)
        mock.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
