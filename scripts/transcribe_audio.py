#!/usr/bin/env python3
"""Transcribe meeting audio for meeting-minutes-from-audio skill.

Uses afconvert (macOS) to WAV when needed, then openai-whisper via numpy
(avoids Whisper's ffmpeg dependency which often fails on this machine).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import wave
from pathlib import Path


def to_wav(src: Path, wav: Path) -> None:
    wav.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".wav":
        if src.resolve() != wav.resolve():
            wav.write_bytes(src.read_bytes())
        return
    # 16kHz mono PCM — Whisper-friendly
    cmd = [
        "afconvert",
        "-f",
        "WAVE",
        "-d",
        "LEI16@16000",
        "-c",
        "1",
        str(src),
        str(wav),
    ]
    subprocess.run(cmd, check=True)


def load_wav_np(path: Path):
    import numpy as np

    with wave.open(str(path), "rb") as wf:
        nch = wf.getnchannels()
        sw = wf.getsampwidth()
        rate = wf.getframerate()
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)

    if sw != 2:
        raise SystemExit(f"expected 16-bit PCM, got sampwidth={sw}")
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if nch > 1:
        audio = audio.reshape(-1, nch).mean(axis=1)
    if rate != 16000:
        # simple resample via linear interp
        duration = len(audio) / float(rate)
        target = int(duration * 16000)
        x_old = np.linspace(0, 1, num=len(audio), endpoint=False)
        x_new = np.linspace(0, 1, num=target, endpoint=False)
        audio = np.interp(x_new, x_old, audio).astype(np.float32)
    return audio


def main() -> int:
    p = argparse.ArgumentParser(description="Whisper transcribe meeting audio")
    p.add_argument("audio", type=Path, help="Input audio path")
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--model", default="medium", help="tiny|base|small|medium|large")
    p.add_argument("--language", default="zh", help="zh|yue|en|… or empty to auto")
    p.add_argument("--device", default="cpu")
    args = p.parse_args()

    src = args.audio.expanduser().resolve()
    if not src.exists():
        print(f"missing file: {src}", file=sys.stderr)
        return 1

    out = args.out_dir.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    wav = out / "meeting.wav"
    transcript_path = out / "transcript.txt"

    print(f"[1/3] convert → {wav}", flush=True)
    to_wav(src, wav)

    print(f"[2/3] load audio + whisper model={args.model}", flush=True)
    import whisper

    audio = load_wav_np(wav)
    model = whisper.load_model(args.model, device=args.device)
    lang = args.language.strip() or None
    kwargs = {"fp16": False}
    if lang:
        kwargs["language"] = lang

    print("[3/3] transcribe…", flush=True)
    result = model.transcribe(audio, **kwargs)
    text = (result.get("text") or "").strip()
    transcript_path.write_text(text + "\n", encoding="utf-8")

    # optional segments for debugging
    segs = result.get("segments") or []
    if segs:
        lines = []
        for s in segs:
            t0 = s.get("start", 0)
            t1 = s.get("end", 0)
            lines.append(f"[{t0:7.1f}-{t1:7.1f}] {(s.get('text') or '').strip()}")
        (out / "transcript_segments.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OK language={result.get('language')} chars={len(text)} → {transcript_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
