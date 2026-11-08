"""Beat 2 mock-up: 'today's packs' line-up, built only from each pack's own pack-front frame.
Same bottom band, same type and scrim as the Pokédex row (direction B)."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_mockups_v3 as L
import make_mockups_v4 as V

OUT = f"{L.ROOT}/channels/poke-capnv/dex/mockups/v5"; os.makedirs(OUT, exist_ok=True)
TMP = L.TMP.replace("/v3", "/v5"); os.makedirs(TMP, exist_ok=True)
PK = "/private/tmp/claude-501/-Users-marerobert-OpenMontage/6d40c82b-2e24-4f21-a574-033556d68811/scratchpad/dexmock/packs"
W, H = L.W, L.H
font, clamp, ease_out, ease_in_out = L.font, L.clamp, L.ease_out, L.ease_in_out
YEL, WHITE = L.YEL, L.WHITE

# pack-front frames and the pack region in each (x0,y0,x1,y1), 3:4 crops around the pack
PACKS = [
    ("Paradox Rift", Image.open(f"{PK}/p_8.0.jpg").convert("RGBA"), (330, 960, 960, 1800)),
    ("Prismatic Evolutions", Image.open(f"{PK}/r_30.jpg").convert("RGBA"), (0, 1020, 560, 1766)),
]
BASE = PACKS[0][1]  # the footage under beat 2 is pack 1 being shown

def mini(img, box, w):
    c = img.crop(box); h = int(w * 4 / 3); c = c.resize((w, h), Image.LANCZOS)
    c.putalpha(L.rounded_mask(c.size, int(w * 0.07)))
    L.aa_rounded_rect(c, (0, 0, w - 1, h - 1), int(w * 0.07), outline=(255, 255, 255, 70), width=1)
    return c

def scrim(im, top, bot, a):
    s = Image.new("RGBA", im.size, (0, 0, 0, 0)); sa = np.zeros((H, W), dtype=np.float32)
    n = bot - top; up = min(90, n // 3); down = min(110, n // 3)
    ramp = np.concatenate([np.linspace(0, 1, up), np.ones(max(0, n - up - down)), np.linspace(1, 0, down)])
    sa[top:bot, :] = (ramp * 0.74 * a)[:, None]; s.putalpha(Image.fromarray((sa * 255).astype(np.uint8)))
    return Image.alpha_composite(im, s)

def lineup(frames=84, n_packs=2, active=0):
    out = []
    MW = 300 if n_packs == 2 else 240; MH = int(MW * 4 / 3); GAP = 60 if n_packs == 2 else 36
    total = n_packs * MW + (n_packs - 1) * GAP; x0 = (W - total) // 2
    ROW_TOP = 1215; HEAD_Y = ROW_TOP - 74
    for f in range(frames):
        im = BASE.copy()
        t_in = ease_out(clamp(f / 10)); t_out = ease_out(clamp((f - 66) / 12)); a = t_in * (1 - t_out)
        if a <= 0: out.append(im); continue
        im = scrim(im, HEAD_Y - 70, ROW_TOP + MH + 150, a)
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        # header: left the Pokédex total, right how many packs today
        V.tracked(d, (90, HEAD_Y), "POKÉDEX  134 / 1025", font(34, "SemiBold"), (232, 235, 240, int(255 * a)), tracking=3)
        rt = f"TODAY  {n_packs} PACKS"; fr = font(40, "Bold"); tw = V.tracked(ImageDraw.Draw(Image.new("RGBA", (10, 10))), (0, 0), rt, fr, (0, 0, 0, 0), tracking=2)
        V.tracked(d, (990 - tw, HEAD_Y - 6), rt, fr, YEL + (int(255 * a),), tracking=2)
        im = Image.alpha_composite(im, layer)
        for i in range(n_packs):
            name, img, box = PACKS[i % len(PACKS)]
            # slide in from alternating sides, settle, with a slight stagger
            ti = ease_out(clamp((f - 2 - i * 4) / 12)) * (1 - t_out)
            dx = (-1 if i % 2 == 0 else 1) * (1 - ti) * 260
            x = x0 + i * (MW + GAP) + int(dx); y = ROW_TOP
            m = mini(img, box, MW)
            if ti < 1: m.putalpha(Image.eval(m.split()[3], lambda p, ti=ti: int(p * ti)))
            sh = L.shadow((MW, MH), int(MW * 0.07), alpha=int(140 * ti), blur=14); im.alpha_composite(sh, (x - 28, y - 14))
            im.alpha_composite(m, (x, y))
            d = ImageDraw.Draw(im)
            if i == active and f >= 16:
                pa = min(1.0, (f - 16) / 6) * (1 - t_out)
                L.aa_rounded_rect(im, (x - 4, y - 4, x + MW + 3, y + MH + 3), int(MW * 0.07) + 4, outline=YEL + (int(255 * pa),), width=2)
            lab_a = int(255 * ti)
            V.tracked(d, (x + MW / 2, y + MH + 16), f"PACK {i + 1}", font(22, "SemiBold"), (200, 204, 214, lab_a), tracking=3, anchor="c")
            fn = font(28 if n_packs == 2 else 22, "Bold"); col = (WHITE + (lab_a,)) if i == active else (205, 209, 218, lab_a)
            words = name.upper().split(); lines = [name.upper()] if len(name) <= 12 or len(words) == 1 else [" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])]
            for li, ln in enumerate(lines):
                V.tracked(d, (x + MW / 2, y + MH + 46 + li * (fn.size + 4)), ln, fn, col, tracking=1, anchor="c")
        out.append(im)
    return out

if __name__ == "__main__":
    fr = lineup()
    V.write_video.__globals__["OUT"] = OUT; V.write_video.__globals__["TMP"] = TMP
    V.write_video(fr, "lineup_2packs")
    V.sheet.__globals__["OUT"] = OUT
    V.sheet([6, 16, 40, 74], fr, ["0.2 s  packs slide in from both sides", "0.55 s  settled, pack 1 framed, set names", "1.3 s  holds while the voice names the sets", "2.5 s  fades out as the tear starts"], "lineup_storyboard.jpg", "BEAT 2  ·  TODAY'S PACKS  ·  built from the pack-front frames only")
    fr3 = lineup(n_packs=3)
    V.write_video(fr3, "lineup_3packs")
    Image.fromarray(np.array(fr3[40].convert("RGB"))).resize((540, 960), Image.LANCZOS).save(f"{OUT}/lineup_3packs_frame.jpg", quality=90)
    print("ok")
