#!/usr/bin/env python3
import argparse
import re
import shutil
from pathlib import Path

VALID_ID = re.compile(r"^[a-zA-Z0-9\-_ ]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Fish Speech reference voice directory."
    )
    parser.add_argument("--id", required=True, help="Reference ID used by --reference-id")
    parser.add_argument("--audio", required=True, help="Reference audio file")
    parser.add_argument("--text", required=True, help="Exact transcript of the reference audio")
    parser.add_argument("--references-dir", default="references")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not VALID_ID.fullmatch(args.id) or len(args.id) > 255:
        raise SystemExit(
            "Reference ID may contain only letters, numbers, spaces, hyphens, and underscores."
        )

    source = Path(args.audio).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Reference audio not found: {source}")

    destination = Path(args.references_dir).expanduser().resolve() / args.id
    if destination.exists():
        if not args.force:
            raise SystemExit(f"Reference already exists: {destination}. Use --force to replace it.")
        shutil.rmtree(destination)

    destination.mkdir(parents=True)
    audio_destination = destination / f"sample{source.suffix.lower()}"
    shutil.copy2(source, audio_destination)
    (destination / "sample.lab").write_text(args.text.strip(), encoding="utf-8")

    print(f"Created reference ID: {args.id}")
    print(f"Audio: {audio_destination}")
    print(f"Transcript: {destination / 'sample.lab'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
