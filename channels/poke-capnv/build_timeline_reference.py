"""Build artifacts/props.json (the edit timeline) for the atelier composition - v2.
v2 (2026-10-16): cold-open Deerling tease, packs in DRAW order 24 -> 20 -> 48 -> 4, VO v4 (first person,
eleven_v3, scripts/process_vo.py alignment), measured SFX levels with per-frame ducking under speech.
v1 kept at scripts/build_timeline_v1.py. Idempotent; pure computation."""
import json, re, math
from pathlib import Path
R = Path(__file__).resolve().parents[1]; FPS = 30
F = lambda s: int(round(s * FPS))
VODIR = "vo_v4"
CLIPS = {"ball": ("ballcam_000-035.mp4", 0), "c24": ("cardcam_p24_073-090.mp4", 73), "c48": ("cardcam_p48_104-120.mp4", 104),
         "c20": ("cardcam_p20_144-159.mp4", 144), "c04": ("cardcam_p04_171-191.mp4", 171), "p24a": ("packcam_p24_042-044.mp4", 42),
         "p24b": ("packcam_p24_061-067.mp4", 61), "p48a": ("packcam_p48_052-054.mp4", 52), "p48b": ("packcam_p48_092-099.mp4", 92),
         "p20": ("packcam_p20_130-139.mp4", 130), "p04": ("packcam_p04_159-167.mp4", 159), "end": ("endcam_187-191.mp4", 187.5)}
AL = {}
for i in range(1, 18):
    sid = f"s{i:02d}"
    AL[sid] = json.load(open(R / f"assets/audio/{VODIR}/{sid}.mp3.alignment.json"))["words"]
DUR = {sid: json.load(open(R / f"assets/audio/{VODIR}/vo_index.json"))[sid]["duration"] for sid in AL}

def w_at(sid, word):
    """offset (s) of the first word in line `sid` starting with `word`"""
    for w in AL[sid]:
        if re.sub(r"[^a-z0-9]", "", w["word"].lower()).startswith(word.lower()): return w["start"]
    raise KeyError((sid, word))

segs = []; t = 0.0
def seg(clip, a, b, rate=1.0, zoom=None, label=""):
    global t
    f, off = CLIPS[clip]; d = (b - a) / rate
    segs.append({"kind": "video", "src": f"video/{f}", "from": F(t), "dur": F(t + d) - F(t), "trimBefore": F(a - off), "rate": rate, "zoom": zoom, "label": label})
    s = t; t += d; return {"start": s, "end": t, "a": a, "rate": rate}
def still(path, dur, zoom=None, label=""):
    global t
    segs.append({"kind": "still", "src": path, "from": F(t), "dur": F(t + dur) - F(t), "zoom": zoom, "label": label}); s = t; t += dur
    return {"start": s, "end": t}
m = lambda S, src: S["start"] + (src - S["a"]) / S["rate"]
VO = {}; warn = []
def say(sid, at):
    prev = [(k, a + DUR[k]) for k, a in VO.items()]
    if prev:
        k, end = max(prev, key=lambda x: x[1])
        if at < end + 0.15:
            warn.append(f"{sid} pushed {end + 0.15 - at:.2f}s later (after {k})"); at = end + 0.15
    VO[sid] = round(at, 3); return at + DUR[sid]

def card_run(clip, a, b, base, label, sid, anchors):
    """Card flips whose footage FOLLOWS the VO: each named card (word, source time it is on screen) is speed-ramped
    so it appears exactly when its name is spoken. Unnamed stretches keep `base` speed. Returns src->out mapper."""
    global t
    t0 = t
    say(sid, t0 + (anchors[0][1] - a) / base - w_at(sid, anchors[0][0]))
    ls = VO[sid]
    pts = [(a, t0)] + [(src, ls + w_at(sid, w)) for w, src in anchors]
    pieces = []
    for (s0, o0), (s1, o1) in zip(pts, pts[1:]):
        want = (s1 - s0) / max(o1 - t, 1e-3)
        rate = min(3.2, max(0.5, want))
        if abs(rate - want) > 0.01: warn.append(f"{sid}: ramp {want:.2f}x clamped to {rate:.2f}x before src {s1}")
        pieces.append((seg(clip, s0, s1, rate, label=label), s1))
    pieces.append((seg(clip, pts[-1][0], b, base, label=label), b))
    def mr(src):
        for P_, end in pieces:
            if src < end or P_ is pieces[-1][0]: return m(P_, src)
    rates = [round(P_["rate"], 2) for P_, _ in pieces]
    print(f"  {label}: speed pieces {rates}")
    return mr, ls + DUR[sid]

ZIN = {"from": 1.0, "to": 1.15, "origin": "50% 55%"}; ZHOLD = {"from": 1.15, "to": 1.15, "origin": "50% 55%"}
ZHIT = {"from": 1.0, "to": 1.10, "origin": "50% 48.33%"}; ZHITH = {"from": 1.10, "to": 1.10, "origin": "50% 48.33%"}
ev = {"reveal": [], "pack": [], "tear": [], "energy": [], "cards": [], "impact": [], "dud": [], "hit": [], "riser": [], "repeat": [], "sets": [], "music_cut": None, "fera": None}

# --- cold open: Deerling freeze (no tag/glow/name), hard cut to the drum on "this"
s01 = 0.15; e = say("s01", s01)
tease_len = e + 0.15
seg("c48", 114.9, 114.9 + tease_len * 0.5, 0.5, {"from": 1.0, "to": 1.12, "origin": "50% 48.33%"}, "tease")
tease_end = t
drum_cut = t
# --- ball 24 (drum runs until "twenty-four" can land on the reveal without overlapping s01)
lead24 = w_at("s02", "twenty")          # s02 offset of the number word
reveal_in_clip = 6.9 - 5.6
opener = max(1.2, (e + 0.15 + lead24) - reveal_in_clip - t)
seg("ball", 2.0, 2.0 + opener, label="opener")
B = seg("ball", 5.6, 7.8, label="ball24"); r = m(B, 6.9); ev["reveal"].append({"t": r, "n": 24}); e = say("s02", r - lead24)
P = seg("p24a", 42.6, 43.9, label="pack24"); ev["pack"].append(P["start"]); e = say("s03", max(P["start"], e + 0.15))
ev["sets"].append({"t": P["start"] + 0.15, "n": 24, "set": "Twilight Masquerade", "era": "Scarlet & Violet"})
T = seg("p24b", 61.5, 66.3, 2.0, label="tear24"); ev["tear"].append(T["start"])
mr, e = card_run("c24", 74.4, 85.0, 1.0, "cards24", "s04", [("nosepass", 75.8), ("probopass", 80.7)])
ev["energy"].append(mr(74.4)); ev["cards"].append({"t": mr(74.5), "n": 1, "pack": 24})
for i, s in enumerate([75.2, 76.4, 77.4, 78.4, 79.4, 80.6, 81.6, 82.8, 84.0]): ev["cards"].append({"t": mr(s), "n": i + 2, "pack": 24})
S = seg("c24", 85.0, 85.5, 0.4, ZIN, label="rare24"); imp = S["end"]; ev["cards"].append({"t": S["start"], "n": 11, "pack": 24, "rare": True})
ev["riser"].append(imp - 1.8); ev["impact"].append(imp); e = say("s05", imp - w_at("s05", "hisuian"))
still("images/arcanine_freeze_1080x1920.png", max(1.5, e + 0.3 - imp), ZHOLD, "freeze24")
ev["dud"].append({"tag_t": imp + 0.3, "stamp_t": VO["s05"] + w_at("s05", "regular"), "end": t, "name": "Hisuian Arcanine", "num": "100/167"})
# --- ball 20
B = seg("ball", 14.8, 16.2, label="ball20"); r = m(B, 15.6); ev["reveal"].append({"t": r, "n": 20}); e = say("s06", r - w_at("s06", "twenty"))
seg("ball", 18.2, 18.8, label="ball20tray")
P = seg("p20", 131.2, 132.6, label="pack20"); ev["pack"].append(P["start"])
ev["sets"].append({"t": P["start"] + 0.15, "n": 20, "set": "Mega Evolution", "era": "Mega Evolution"})
T = seg("p20", 133.0, 138.2, 3.5, label="tear20"); ev["tear"].append(T["start"])
mr, e = card_run("c20", 144.6, 155.3, 1.2, "cards20", "s07", [("bulbasaur", 145.7), ("pok", 147.7), ("latios", 150.6)])
ev["energy"].append(mr(144.8)); ev["cards"].append({"t": mr(144.8), "n": 1, "pack": 20})
for i, s in enumerate([145.6, 146.8, 148.0, 149.0, 150.0, 151.2, 152.2, 153.4, 154.6]): ev["cards"].append({"t": mr(s), "n": i + 2, "pack": 20})
S = seg("c20", 155.3, 156.3, 0.6, ZIN, label="rare20"); imp = S["end"]; ev["cards"].append({"t": m(S, 155.6), "n": 11, "pack": 20, "rare": True})
ev["riser"].append(imp - 1.8); ev["impact"].append(imp); e = say("s08", imp - w_at("s08", "kyogre"))
still("images/kyogre_freeze_1080x1920.png", max(1.5, e + 0.3 - imp), ZHOLD, "freeze20")
ev["dud"].append({"tag_t": imp + 0.3, "stamp_t": VO["s08"] + w_at("s08", "regular"), "end": t, "name": "Kyogre", "num": "034/132"})
# --- ball 48 + the hit
B = seg("ball", 20.6, 22.6, label="ball48"); r = m(B, 22.0); ev["reveal"].append({"t": r, "n": 48}); e = say("s09", r - w_at("s09", "forty"))
P = seg("p48a", 52.0, 53.2, label="pack48"); ev["pack"].append(P["start"])
ev["sets"].append({"t": P["start"] + 0.15, "n": 48, "set": "Temporal Forces", "era": "Scarlet & Violet"})
T = seg("p48b", 92.5, 98.5, 4.0, label="tear48"); ev["tear"].append(T["start"])
mr, e10 = card_run("c48", 104.9, 113.9, 1.0, "cards48", "s10", [("mudbray", 106.3), ("minccino", 107.3), ("rockruff", 108.3), ("litten", 109.3),
                                                                ("iron", 111.2), ("boxed", 112.2), ("full", 113.2)])
ev["energy"].append(mr(105.0)); ev["cards"].append({"t": mr(105.0), "n": 1, "pack": 48})
for i, s in enumerate([105.4, 106.6, 107.6, 108.6, 109.6, 110.6, 111.8, 112.8]): ev["cards"].append({"t": mr(s), "n": i + 2, "pack": 48})
# slow-mo build into the hit: stretched so "Card ten and- no way." plays over it and "Deerling!" lands on the reveal
need = (e10 + 0.15 + w_at("s11", "deerling")) - t
slow_rate = max(0.2, min(0.4, 0.8 / max(need, 2.0)))
S = seg("c48", 113.9, 114.7, slow_rate, label="slow48"); imp = S["end"]; print(f"  slow48: {slow_rate:.2f}x for {S['end'] - S['start']:.2f}s"); ev["cards"].append({"t": m(S, 114.4), "n": 10, "pack": 48, "rare": True})
ev["riser"].append(imp - 1.8); ev["impact"].append(imp)
e = say("s11", imp - w_at("s11", "deerling"))
ev["music_cut"] = [max(imp - 2.0, e10 + 0.1), e + 0.35]
L = seg("c48", 114.7, 116.1, 0.7, ZHIT, label="hit48")
still("images/deerling_freeze_1080x1920.png", max(1.5, e + 0.6 - t), ZHITH, "freeze48")
ev["hit"].append({"tag_t": imp + 0.35, "glow_from": L["end"], "end": t, "name": "Deerling", "num": "165/162", "rarity": "ILLUSTRATION RARE"})
Fe = seg("c48", 117.3, min(120.0, 117.3 + DUR["s12"] + 0.3), label="fera48"); ev["cards"].append({"t": Fe["start"], "n": 11, "pack": 48})
ev["fera"] = {"t": Fe["start"] + 0.2, "end": Fe["end"]}; e = say("s12", Fe["start"] + 0.1)
# --- ball 4
B = seg("ball", 29.0, 31.0, label="ball4"); r = m(B, 30.2); ev["reveal"].append({"t": r, "n": 4}); e = say("s13", r - w_at("s13", "four"))
P = seg("p04", 159.4, 160.8, label="pack4"); ev["pack"].append(P["start"])
ev["sets"].append({"t": P["start"] + 0.15, "n": 4, "set": "Twilight Masquerade", "era": "Scarlet & Violet"})
T = seg("p04", 161.0, 166.4, 3.6, label="tear4"); ev["tear"].append(T["start"])
mr, e = card_run("c04", 172.1, 182.9, 1.0, "cards4", "s14", [("nosepass", 174.2), ("jynx", 176.2), ("floette", 177.2)])
ev["energy"].append(mr(172.2)); ev["cards"].append({"t": mr(172.2), "n": 1, "pack": 4})
for i, s in enumerate([173.0, 174.4, 175.4, 176.4, 177.6, 178.6, 179.8, 180.8, 182.0]): ev["cards"].append({"t": mr(s), "n": i + 2, "pack": 4})
for a, b in [(173.9, 175.9), (175.9, 176.9), (176.9, 177.9)]: ev["repeat"].append({"t": mr(a), "end": mr(b)})
S = seg("c04", 182.9, 183.4, 0.4, ZIN, label="rare4"); imp = S["end"]; ev["cards"].append({"t": S["start"] + 0.25, "n": 11, "pack": 4, "rare": True})
ev["riser"].append(imp - 1.8); ev["impact"].append(imp); e = say("s15", imp - w_at("s15", "iron"))
still("images/ironleaves_freeze_1080x1920.png", max(1.5, e + 0.4 - imp), ZHOLD, "freeze4")
ev["dud"].append({"tag_t": imp + 0.3, "stamp_t": VO["s15"] + w_at("s15", "regular"), "end": t, "name": "Iron Leaves", "num": "019/167"})
# --- summary, then sign-off (s17 starts on the summary and finishes on the Deerling held to camera)
sum_start = t; e16 = say("s16", sum_start + 0.25)
s17 = e16 + 0.35; e17 = s17 + DUR["s17"]
END_A, END_B = 187.8, 191.1
end_start = max(s17 + 0.8, e17 + 0.25 - (END_B - END_A))
Ssum = still("images/deerling_freeze_1080x1920.png", end_start - sum_start, None, "summary")
say("s17", s17)
E = seg("end", END_B - (max(e17 + 0.25, end_start + 1.0) - end_start), END_B, label="signoff")
total = t

# --- checks
if VO["s17"] + DUR["s17"] > E["end"] + 0.02: warn.append("s17 runs past the sign-off footage")
for k, a in VO.items():
    if a < 0: warn.append(f"{k} starts before 0")

# --- captions: word level from the ElevenLabs alignment (already display spellings), 2-3 words per chunk
caps = []
for sid, at in sorted(VO.items(), key=lambda kv: kv[1]):
    W = [dict(x) for x in AL[sid]]
    if sid == "s11":  # "one sixty-five out of one sixty-two," -> "165/162,"
        i = [k for k, w in enumerate(W) if w["word"].startswith("sixty-five")][0] - 1
        W[i:i + 5] = [{"word": "165/162,", "start": W[i]["start"], "end": W[i + 4]["end"]}]
    if sid == "s02": W = [dict(w, word=w["word"].replace("twenty-four", "24")) for w in W]
    if sid == "s14": W = [dict(w, word=w["word"].replace("twenty-four", "24")) for w in W]
    chunk = []
    def flush(nxt):
        if chunk: caps.append({"from": F(at + chunk[0]["start"]), "to": F(at + (nxt if nxt is not None else chunk[-1]["end"] + 0.25)),
                               "words": [{"text": c["word"], "s": F(at + c["start"]), "e": F(at + c["end"])} for c in chunk]})
    for k, w in enumerate(W):
        chunk.append(w); end_punct = bool(re.search(r"[.!?,:\-]$", w["word"]))
        long_enough = chunk[-1]["end"] - chunk[0]["start"] >= 0.55
        if (len(chunk) >= 3 and long_enough) or len(chunk) >= 4 or (end_punct and len(chunk) >= 2 and long_enough) or w["word"].endswith(("!", "?", ".")):
            nxt = W[k + 1]["start"] if k + 1 < len(W) else None; flush(nxt); chunk = []
    flush(None)
rate = max(len(c["words"]) / max((c["to"] - c["from"]) / FPS, 0.3) for c in caps)

# --- speech envelope (word spans, small gaps bridged) -> per-frame duck amount 0..1
N = F(total)
spans = sorted((at + w["start"] - 0.05, at + w["end"] + 0.08) for sid, at in VO.items() for w in AL[sid])
merged = []
for a, b in spans:
    if merged and a <= merged[-1][1] + 0.25: merged[-1][1] = max(merged[-1][1], b)
    else: merged.append([a, b])
raw = [0.0] * N
for a, b in merged:
    for fr in range(max(0, F(a)), min(N, F(b) + 1)): raw[fr] = 1.0
duck = [0.0] * N; cur = 0.0
ATT, REL = 1 / 3, 1 / 8          # 3-frame attack, 8-frame release
for fr in range(N):
    cur = min(raw[fr], cur + ATT) if raw[fr] < cur else min(1.0, cur + ATT)
    if raw[fr] < cur: cur = max(raw[fr], cur - REL)
    duck[fr] = round(cur, 3)
# look-ahead so the duck is fully down when the first word starts
for fr in range(N - 3):
    duck[fr] = max(duck[fr], duck[fr + 3] * 0.999)

# --- music: bed under VO, out before the hit
MUSIC_START = 0.0
LEV = json.load(open(R / "artifacts/audio_levels.json"))
vol = []
mc = ev["music_cut"]
for fr in range(N):
    x = fr / FPS; v = 0.30 - (0.30 - 0.13) * duck[fr]
    if any(r <= x <= r + 1.8 for r in ev["riser"]): v = min(v, 0.07)
    if mc[0] <= x < mc[1]: v = 0.0
    if x < tease_end: v = 0.0
    vol.append(round(v, 3))
sm = []
for i in range(N): w = vol[max(0, i - 4):i + 5]; sm.append(round(sum(w) / len(w), 3))

# music track is PAUSED during the hit's music cut and resumes from the same point, so the 100 s bed covers the video
BED = 100.0
music_pieces = [{"from": F(MUSIC_START), "trimBefore": 0, "dur": F(mc[0]) - F(MUSIC_START)}]
resume_at = mc[0] - MUSIC_START
music_pieces.append({"from": F(mc[1]), "trimBefore": F(resume_at), "dur": min(N - F(mc[1]), F(BED - resume_at))})
if mc[1] + (BED - resume_at) < total: warn.append(f"music ends {total - (mc[1] + BED - resume_at):.1f}s before the video")
# --- sfx: volume from MEASURED max momentary loudness (artifacts/audio_levels.json)
VO_M = LEV["_vo_median"]
FREE = {"drum_sting": -16, "ball_pop": -22, "whoosh": -19, "foil_tear": -18, "card_slide": -24, "card_tick": -25, "riser": -19,
        "impact": -16, "shimmer": -20, "dud_sting": -19, "chip_pop": -25}
UNDER_VO = VO_M - 10        # ducked target while words are spoken (>= 10 dB under the voice)
def vol_for(n):
    v = 10 ** ((FREE[n] - LEV[n]) / 20)
    return round(min(1.0, v), 3)
def duck_gain(n):
    eff = LEV[n] + 20 * math.log10(vol_for(n))
    return round(min(1.0, 10 ** ((UNDER_VO - eff) / 20)), 3)
sfx = [{"n": "drum_sting", "t": drum_cut}]
sfx += [{"n": "ball_pop", "t": r["t"] - 0.05} for r in ev["reveal"]]
sfx += [{"n": "whoosh", "t": p - 0.1} for p in ev["pack"]]
sfx += [{"n": "foil_tear", "t": p + 0.1} for p in ev["tear"]]
sfx += [{"n": "card_slide", "t": p} for p in ev["energy"]]
sfx += [{"n": "card_tick", "t": c["t"], "maxDur": 0.3} for c in ev["cards"] if not c.get("rare")]
sfx += [{"n": "riser", "t": r} for r in ev["riser"]]
sfx += [{"n": "impact", "t": i - 0.03} for i in ev["impact"]]
sfx += [{"n": "shimmer", "t": ev["impact"][2] + 0.05}, {"n": "shimmer", "t": Ssum["start"] + 0.3}]
sfx += [{"n": "dud_sting", "t": d["stamp_t"]} for d in ev["dud"]]
sfx += [{"n": "chip_pop", "t": s["t"], "maxDur": 0.3} for s in ev["sets"]]
# overlap report: effective loudness of every SFX that plays while words are spoken
overlaps = []
for s in sfx:
    a, b = F(s["t"]), min(N - 1, F(s["t"] + s.get("maxDur", 3)))
    dmax = max(duck[a:b + 1] or [0])
    if dmax > 0.5:
        eff = LEV[s["n"]] + 20 * math.log10(vol_for(s["n"]) * duck_gain(s["n"]))
        overlaps.append((s["n"], round(s["t"], 2), round(eff - VO_M, 1)))
bad = [o for o in overlaps if o[2] > -8]
props = {"fps": FPS, "durationInFrames": N, "segments": segs,
         "vo": [{"id": s, "src": f"audio/{VODIR}/{s}.mp3", "from": F(a)} for s, a in VO.items()],
         "sfx": [{"src": f"audio/sfx/{s['n']}.mp3", "from": F(s["t"]), "volume": vol_for(s["n"]), "duck": duck_gain(s["n"]), "maxDur": F(s.get("maxDur", 3))} for s in sfx],
         "duck": duck,
         "music": {"src": "music/bed_100s.mp3", "volume": sm, "pieces": music_pieces}, "captions": caps,
         "events": {k: ([{kk: (F(vv) if isinstance(vv, float) else vv) for kk, vv in x.items()} if isinstance(x, dict) else F(x) for x in v] if isinstance(v, list) and k != "music_cut" else v) for k, v in ev.items()},
         "fera": {"from": F(ev["fera"]["t"]), "to": F(ev["fera"]["end"])}, "summaryFrom": F(Ssum["start"]), "summaryTo": F(Ssum["end"]),
         "teaseTo": F(tease_end), "episode": 1, "hits": 1, "packs": 4, "balls": [24, 20, 48, 4], "hitBall": 48}
json.dump(props, open(R / "artifacts/props.json", "w"))
print(f"total {total:.2f}s ({N} frames), {len(segs)} segments, {len(caps)} caption chunks, max caption rate {rate:.1f} w/s")
for s, a in sorted(VO.items(), key=lambda kv: kv[1]): print(f"  {s} {a:6.2f}-{a + DUR[s]:6.2f}")
print("labels:", " ".join(f"{s['label']}@{s['from'] / FPS:.1f}" for s in segs))
print(f"SFX under speech: {len(overlaps)}, worst {max((o[2] for o in overlaps), default=None)} dB vs VO; over -8 dB: {bad or 'none'}")
print(f"music bed: under VO {LEV['bed_100s'] + 20 * math.log10(0.13) - VO_M:.1f} dB vs VO; paused {mc[0]:.1f}-{mc[1]:.1f}s, track ends {mc[1] + BED - resume_at:.1f}s, video {total:.1f}s")
print("WARN:", warn or "none")
