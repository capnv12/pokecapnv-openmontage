"""Post-process ElevenLabs v3 VO lines AND carry their word alignment through the edit.

eleven_v3 ignores `speed`, so lines are tightened and sped up here. Every edit is done at known
positions so the ElevenLabs word timings (raw/<id>.mp3.alignment.json) can be remapped exactly:
  1. trim leading silence to LEAD s before speech
  2. shorten every internal pause longer than MAX_PAUSE to MAX_PAUSE (keep its two edges)
  3. cut the tail glitch: a short burst after the final silence that starts after the last word
  4. atempo SPEED (pitch preserved), 40 ms fade-out
Writes <vo_dir>/<id>.mp3 and <vo_dir>/<id>.mp3.alignment.json (display spellings from the script,
audio tags dropped) - the format scripts/build_timeline.py already reads.
Usage: python scripts/process_vo.py [vo_dir] [section ids...]"""
import json, re, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
VO = R / (sys.argv[1] if len(sys.argv) > 1 else "assets/audio/vo_v4")
ONLY = set(sys.argv[2:])
SPEED, MAX_PAUSE, LEAD, THRESH = 1.15, 0.15, 0.03, "-38dB"
script = json.load(open(R / "artifacts/script.json"))

def is_tag(w): return w.startswith("[") or w.endswith("]")

def duration(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))

def silences(f, min_d):
    log = subprocess.run(["ffmpeg", "-nostats", "-i", str(f), "-af", f"silencedetect=n={THRESH}:d={min_d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    d = duration(f)
    return [(s, en[i] if i < len(en) else d) for i, s in enumerate(st)]

for sec in script["sections"]:
    sid = sec["id"]
    if ONLY and sid not in ONLY: continue
    raw = VO / "raw" / f"{sid}.mp3"
    al = json.load(open(str(raw) + ".alignment.json"))
    words = [w for w in (al.get("words") or al.get("word_timestamps")) if not is_tag(w["word"])]
    display = sec["text"].split()
    assert len(display) == len(words), f"{sid}: {len(display)} script words vs {len(words)} aligned words"
    d = duration(raw)
    sil = silences(raw, 0.08)
    # 1. head
    head = 0.0
    if sil and sil[0][0] <= 0.01: head = max(0.0, min(sil[0][1], words[0]["start"]) - LEAD)
    # 3. tail: final silence starting after the last word began, followed by <0.25 s of sound (glitch) or nothing
    tail = d
    last_start = words[-1]["start"]
    for s, e in sil:
        if s > last_start + 0.1 and (d - e < 0.25):
            tail = min(d, s + 0.06); break
    # 2. internal pauses
    cuts = []  # removed intervals (raw time)
    for s, e in sil:
        if s <= head or e >= tail: continue
        if e - s > MAX_PAUSE:
            cuts.append((s + MAX_PAUSE / 2, e - MAX_PAUSE / 2))
    keep, cur = [], head
    for s, e in cuts: keep.append((cur, s)); cur = e
    keep.append((cur, tail))

    def remap(t):
        t = min(max(t, head), tail)
        removed = sum(min(e, t) - s for s, e in cuts if t > s)
        return round((t - head - removed) / SPEED, 3)

    parts = "".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(keep))
    out_len = sum(b - a for a, b in keep) / SPEED
    fc = parts + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,atempo={SPEED},afade=t=out:st={max(0, out_len - 0.04):.4f}:d=0.04[out]"
    out = VO / f"{sid}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-filter_complex", fc, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "128k", str(out)], check=True)
    new_words = [{"word": disp, "start": remap(w["start"]), "end": remap(w["end"])} for disp, w in zip(display, words)]
    json.dump({"text": sec["text"], "words": new_words,
               "source": "ElevenLabs alignment remapped through process_vo.py",
               "processing": {"head": round(head, 3), "tail": round(tail, 3), "pause_cuts": [[round(s, 3), round(e, 3)] for s, e in cuts], "speed": SPEED}},
              open(str(out) + ".alignment.json", "w"), indent=1)
    print(f"{sid}: raw {d:.2f}s -> {duration(out):.2f}s | {len(cuts)} pause cuts | tail cut {d - tail:.3f}s | last word ends {new_words[-1]['end']:.2f}s")
