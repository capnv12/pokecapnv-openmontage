"""Pack entrance mock-up: the pack is held up, the Pokédex scans it, it shrinks into its slot
in today's line-up, the other packs slide in. Same band, type and scrim as direction B."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_mockups_v3 as L
import make_mockups_v4 as V
from make_lineup_v5 import mini, scrim, PACKS, BASE

OUT = f"{L.ROOT}/channels/poke-capnv/dex/mockups/v6"; os.makedirs(OUT, exist_ok=True)
TMP = L.TMP.replace("/v3", "/v6"); os.makedirs(TMP, exist_ok=True)
W, H = L.W, L.H
font, clamp, ease_out, ease_in_out = L.font, L.clamp, L.ease_out, L.ease_in_out
YEL, WHITE = L.YEL, L.WHITE
PB = PACKS[0][2]  # pack region in the held-up frame

def beam_layer(y, a, x0, x1):
    """soft yellow scan beam at height y, bright core, feathered ends"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band_h = 100
    yy = np.arange(H)[:, None]; xx = np.arange(W)[None, :]
    v = np.clip(1 - np.abs(yy - y) / (band_h / 2), 0, 1) ** 2
    hx = np.clip((xx - x0) / 50, 0, 1) * np.clip((x1 - xx) / 50, 0, 1)
    alpha = (v * hx * 210 * a).astype(np.uint8)
    col = np.zeros((H, W, 4), dtype=np.uint8); col[..., 0] = 255; col[..., 1] = 215; col[..., 2] = 60; col[..., 3] = alpha
    lay = Image.fromarray(col, "RGBA")
    d = ImageDraw.Draw(lay)
    core = (255, 240, 170, int(255 * a))
    d.line([(x0 + 10, y), (x1 - 10, y)], fill=core, width=4)
    return lay

def entrance(frames=92, n_packs=2):
    out = []
    MW = 300 if n_packs == 2 else 240; MH = int(MW * 4 / 3); GAP = 60 if n_packs == 2 else 36
    total = n_packs * MW + (n_packs - 1) * GAP; x0 = (W - total) // 2
    ROW_TOP = 1215; HEAD_Y = ROW_TOP - 74
    px0, py0, px1, py1 = PB; pw, ph = px1 - px0, py1 - py0
    pack_crop = BASE.crop(PB).copy(); pack_crop.putalpha(L.rounded_mask(pack_crop.size, 26))
    for f in range(frames):
        im = BASE.copy()
        # 1. scan beam sweeps the pack (0-14), scanned part faintly lit
        if f <= 16:
            t = ease_in_out(clamp(f / 14)); y = int(py0 + ph * t)
            tint = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tint)
            ta = int(34 * (1 if f <= 14 else 1 - (f - 14) / 2))
            m = L.rounded_mask((pw, ph), 26); sub = Image.new("RGBA", (pw, ph), (255, 215, 60, ta)); sub.putalpha(Image.eval(m, lambda p: int(p * ta / 255)))
            sub = sub.crop((0, 0, pw, max(1, y - py0))); tint.alpha_composite(sub, (px0, py0))
            im = Image.alpha_composite(im, tint)
            if f <= 14: im = Image.alpha_composite(im, beam_layer(y, 1.0, px0 - 40, px1 + 40))
        # 2. rim pulse when the scan completes (14-24)
        if 14 <= f <= 24:
            pa = 1 - (f - 14) / 10
            L.aa_rounded_rect(im, (px0 - 6, py0 - 6, px1 + 5, py1 + 5), 30, outline=YEL + (int(255 * pa),), width=4)
        # 3. band + header come in as the pack shrinks into slot 1 (18-32)
        tb = ease_out(clamp((f - 18) / 14)); t_out = ease_out(clamp((f - 78) / 12)); a = tb * (1 - t_out)
        if a > 0:
            im = scrim(im, HEAD_Y - 70, ROW_TOP + MH + 150, a)
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            V.tracked(d, (90, HEAD_Y), "POKÉDEX  134 / 1025", font(34, "SemiBold"), (232, 235, 240, int(255 * a)), tracking=3)
            rt = f"TODAY  {n_packs} PACKS"; fr = font(40, "Bold"); tw = V.tracked(ImageDraw.Draw(Image.new("RGBA", (10, 10))), (0, 0), rt, fr, (0, 0, 0, 0), tracking=2)
            V.tracked(d, (990 - tw, HEAD_Y - 6), rt, fr, YEL + (int(255 * a),), tracking=2)
            im = Image.alpha_composite(im, layer)
        # flight of pack 1: full size -> slot 1
        tf = ease_in_out(clamp((f - 18) / 14))
        if 18 <= f and tf < 1:
            w = int(pw + (MW - pw) * tf); h = int(w * 4 / 3)
            x = int(px0 + (x0 - px0) * tf); y = int(py0 + (ROW_TOP - py0) * tf)
            fc = pack_crop.resize((w, h), Image.LANCZOS)
            sh = L.shadow((w, h), 26, alpha=int(150 * tf), blur=16); im.alpha_composite(sh, (x - 28, y - 14))
            im.alpha_composite(fc, (x, y))
        d = ImageDraw.Draw(im)
        for i in range(n_packs):
            name, img, box = PACKS[i % len(PACKS)]
            if i == 0:
                ti = 1.0 if f >= 32 else 0.0
            else:
                ti = ease_out(clamp((f - 30 - (i - 1) * 4) / 12))
            ti *= (1 - t_out)
            if ti <= 0: continue
            dx = 0 if i == 0 else (1 - ti) * 260
            x = x0 + i * (MW + GAP) + int(dx); y = ROW_TOP
            m = mini(img, box, MW)
            if ti < 1: m.putalpha(Image.eval(m.split()[3], lambda p, ti=ti: int(p * ti)))
            sh = L.shadow((MW, MH), int(MW * 0.07), alpha=int(140 * ti), blur=14); im.alpha_composite(sh, (x - 28, y - 14))
            im.alpha_composite(m, (x, y))
            d = ImageDraw.Draw(im)
            if i == 0 and f >= 34:
                pa = min(1.0, (f - 34) / 6) * (1 - t_out)
                L.aa_rounded_rect(im, (x - 4, y - 4, x + MW + 3, y + MH + 3), int(MW * 0.07) + 4, outline=YEL + (int(255 * pa),), width=2)
            lab_a = int(255 * ti) if i else int(255 * clamp((f - 32) / 6) * (1 - t_out))
            V.tracked(d, (x + MW / 2, y + MH + 16), f"PACK {i + 1}", font(22, "SemiBold"), (200, 204, 214, lab_a), tracking=3, anchor="c")
            fn = font(28 if n_packs == 2 else 22, "Bold"); col = (WHITE + (lab_a,)) if i == 0 else (205, 209, 218, lab_a)
            words = name.upper().split(); lines = [name.upper()] if len(name) <= 12 or len(words) == 1 else [" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])]
            for li, ln in enumerate(lines):
                V.tracked(d, (x + MW / 2, y + MH + 46 + li * (fn.size + 4)), ln, fn, col, tracking=1, anchor="c")
        out.append(im)
    return out

if __name__ == "__main__":
    V.write_video.__globals__["OUT"] = OUT; V.write_video.__globals__["TMP"] = TMP; V.sheet.__globals__["OUT"] = OUT
    fr = entrance()
    V.write_video(fr, "entrance_scan_2packs")
    V.sheet([7, 16, 25, 50], fr, ["0.25 s  pack held up, the Dex scans it", "0.55 s  scan done, rim pulse", "0.85 s  pack shrinks into slot 1", "1.7 s  pack 2 slides in; voice names the sets"], "entrance_storyboard.jpg", "PACK ENTRANCE  ·  the Pokédex scans the pack, then it takes its place in today's line-up")
    fr3 = entrance(n_packs=3)
    V.write_video(fr3, "entrance_scan_3packs")
    print("ok")
