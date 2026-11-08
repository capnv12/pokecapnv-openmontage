"""Dex format mock-ups v2: Pokédex (National numbers), polished look.
Pillow renders frames, ffmpeg encodes. Run from anywhere with the project venv python."""
import math, os, sys, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/Users/marerobert/OpenMontage"
OUT = f"{ROOT}/channels/poke-capnv/dex/mockups/v3"
TMP = "/private/tmp/claude-501/-Users-marerobert-OpenMontage/6d40c82b-2e24-4f21-a574-033556d68811/scratchpad/dexmock/v3"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
W, H = 1080, 1920
FREDOKA = "/private/tmp/claude-501/-Users-marerobert-OpenMontage/6d40c82b-2e24-4f21-a574-033556d68811/scratchpad/fonts/Fredoka.ttf"
_fc = {}
def font(sz, weight="Bold"):
    k = (sz, weight)
    if k not in _fc:
        f = ImageFont.truetype(FREDOKA, sz); f.set_variation_by_name(weight); _fc[k] = f
    return _fc[k]

YEL = (255, 203, 5); GREEN = (52, 211, 120); GREEN2 = (22, 160, 90); GREY = (150, 156, 168); GREY2 = (98, 104, 116)
GOLD = (255, 196, 64); GOLD2 = (214, 140, 20); WHITE = (255, 255, 255); INK = (12, 14, 20)

SRC = {
    "golisopod": (f"{ROOT}/projects/poke-capnv-draw-17/public/images/golisopod_freeze_1080x1920.png", (125, 285, 880, 1365), "Golisopod", 768, "Alola"),
    "technoradar": (f"{ROOT}/projects/poke-capnv-draw-17/public/images/technoradar_freeze_1080x1920.png", (190, 310, 860, 1205), "Techno Radar", None, None),
    "ursaluna": (f"{ROOT}/projects/poke-capnv-draw-17/public/images/ursaluna_freeze_1080x1920.png", (240, 330, 920, 1235), "Ursaluna", 901, "Paldea"),
    "veluza": (f"{ROOT}/projects/poke-capnv-draw-16/public/images/veluza_freeze_1080x1920.png", (125, 320, 890, 1380), "Veluza", 976, "Paldea"),
    "fezandipiti": (f"{ROOT}/projects/poke-capnv-draw-16/public/images/fezandipiti_freeze_1080x1920.png", (130, 530, 920, 1670), "Fezandipiti", 1016, "Paldea"),
}
FRAMES = {k: Image.open(v[0]).convert("RGBA") for k, v in SRC.items()}
def card_crop(k):
    return FRAMES[k].crop(SRC[k][1])

TILE_W, TILE_H, TILE_R = 118, 165, 14
SS = 4  # supersampling factor for every vector shape: smooth edges, no jaggies
def rounded_mask(size, r):
    m = Image.new("L", (size[0] * SS, size[1] * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] * SS - 1, size[1] * SS - 1), r * SS, fill=255)
    return m.resize(size, Image.LANCZOS)
def aa_rounded_rect(im, box, r, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = [int(round(v)) for v in box]; pad = width + 2
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    tmp = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).rounded_rectangle((pad * SS, pad * SS, (w - pad) * SS - 1, (h - pad) * SS - 1), r * SS, fill=fill, outline=outline, width=max(1, int(width * SS)))
    im.alpha_composite(tmp.resize((w, h), Image.LANCZOS), (x0 - pad, y0 - pad))
def aa_ellipse(im, box, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = [int(round(v)) for v in box]; pad = width + 2
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    tmp = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).ellipse((pad * SS, pad * SS, (w - pad) * SS - 1, (h - pad) * SS - 1), fill=fill, outline=outline, width=max(1, int(width * SS)))
    im.alpha_composite(tmp.resize((w, h), Image.LANCZOS), (x0 - pad, y0 - pad))
def aa_shape(im, origin, size, draw_fn):
    """draw_fn(d, s) draws at scale s into a temp canvas of `size`; composited at origin."""
    tmp = Image.new("RGBA", (size[0] * SS, size[1] * SS), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(tmp), SS)
    im.alpha_composite(tmp.resize(size, Image.LANCZOS), (int(origin[0]), int(origin[1])))
def make_tile(img, dim=False):
    t = img.resize((TILE_W, TILE_H), Image.LANCZOS).convert("RGBA")
    if dim: t = Image.blend(t, Image.new("RGBA", t.size, (40, 44, 56, 255)), 0.5)
    t.putalpha(rounded_mask(t.size, TILE_R))
    aa_rounded_rect(t, (0, 0, TILE_W - 1, TILE_H - 1), TILE_R, outline=(255, 255, 255, 80), width=1)
    return t
def empty_tile(num):
    t = Image.new("RGBA", (TILE_W, TILE_H), (0, 0, 0, 0))
    aa_rounded_rect(t, (0, 0, TILE_W - 1, TILE_H - 1), TILE_R, fill=(255, 255, 255, 20))
    d = ImageDraw.Draw(t)
    f1 = font(18, "SemiBold"); f2 = font(30, "Bold")
    s1 = "No."; s2 = f"{num:04d}"
    d.text(((TILE_W - d.textlength(s1, font=f1)) / 2, TILE_H / 2 - 34), s1, font=f1, fill=(170, 176, 190, 200))
    d.text(((TILE_W - d.textlength(s2, font=f2)) / 2, TILE_H / 2 - 12), s2, font=f2, fill=(190, 196, 210, 230))
    return t
TILES = {k: make_tile(card_crop(k)) for k in SRC}

def shadow(size, r, alpha=120, blur=14):
    s = Image.new("RGBA", (size[0] + blur * 4, size[1] + blur * 4), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((blur * 2, blur * 2, blur * 2 + size[0], blur * 2 + size[1]), r, fill=(0, 0, 0, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur))

def glass(im, box, r=30, dark=150, blur=16):
    """Frosted glass: blur what is behind the box, darken, light rim."""
    x0, y0, x1, y1 = box
    region = im.crop(box).filter(ImageFilter.GaussianBlur(blur))
    region = Image.alpha_composite(region, Image.new("RGBA", region.size, (10, 12, 18, dark)))
    region.putalpha(rounded_mask(region.size, r))
    sh = shadow((x1 - x0, y1 - y0), r, alpha=110, blur=18)
    im.alpha_composite(sh, (x0 - 36, y0 - 28))
    im.alpha_composite(region, (x0, y0))
    aa_rounded_rect(im, box, r, outline=(255, 255, 255, 38), width=1)  # one hairline rim, nothing else
    return im

def text_center(d, cx, y, s, f, fill, stroke=0, sfill=(0, 0, 0)):
    tw = d.textlength(s, font=f); d.text((cx - tw / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def check_icon(layer, cx, cy, r, col, kind="check", alpha=1.0):
    """White disc with a check / up-arrow / dot, drawn supersampled."""
    size = (2 * r + 8, 2 * r + 8); o = (cx - r - 4, cy - r - 4)
    a = int(255 * alpha); wcol = WHITE + (a,); ccol = col + (a,)
    def fn(d, s):
        c = (r + 4) * s; rr = r * s
        d.ellipse((c - rr, c - rr, c + rr, c + rr), fill=wcol)
        if kind == "check":
            d.line([(c - rr * 0.45, c + rr * 0.02), (c - rr * 0.12, c + rr * 0.36), (c + rr * 0.48, c - rr * 0.36)], fill=ccol, width=int(rr * 0.28), joint="curve")
        elif kind == "up":
            d.polygon([(c, c - rr * 0.55), (c + rr * 0.5, c + 0.05 * rr), (c + rr * 0.2, c + 0.05 * rr), (c + rr * 0.2, c + rr * 0.55), (c - rr * 0.2, c + rr * 0.55), (c - rr * 0.2, c + 0.05 * rr), (c - rr * 0.5, c + 0.05 * rr)], fill=ccol)
        else:
            d.ellipse((c - rr * 0.38, c - rr * 0.38, c + rr * 0.38, c + rr * 0.38), fill=ccol)
    aa_shape(layer, o, size, fn)

def draw_stamp(im, card_box, kind, name=None, sub=None, alpha=1.0, dy=0, y_cap=None):
    x0, y0, x1, y1 = card_box; cx = (x0 + x1) // 2
    cfg = {"caught": ("CAUGHT", GREEN, GREEN2, "check", WHITE), "already": ("ALREADY CAUGHT", GREY, GREY2, "dot", WHITE), "upgraded": ("UPGRADED", GOLD, GOLD2, "up", INK)}
    text, c1, c2, icon, tcol = cfg[kind]
    f = font(50 if kind != "already" else 40, "Bold")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=f); ph = f.size + 30; pw = tw + ph + 56
    py = y1 - 190 + dy
    if y_cap is not None: py = min(py, y_cap - (150 if name else 70)) + dy
    px = cx - pw / 2
    # shadow + gradient pill
    sh = shadow((int(pw), int(ph)), ph // 2, alpha=int(150 * alpha), blur=12); layer.alpha_composite(sh, (int(px) - 24, int(py) - 16))
    grad = Image.new("RGBA", (int(pw), int(ph)), (0, 0, 0, 0))
    arr = np.zeros((int(ph), int(pw), 4), dtype=np.uint8)
    for yy in range(int(ph)):
        t = yy / max(1, ph - 1); col = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
        arr[yy, :, :3] = col; arr[yy, :, 3] = int(255 * alpha)
    grad = Image.fromarray(arr, "RGBA"); grad.putalpha(Image.eval(rounded_mask(grad.size, int(ph // 2)), lambda v: int(v * alpha)))
    layer.alpha_composite(grad, (int(px), int(py)))
    check_icon(layer, int(px + ph / 2 + 8), int(py + ph / 2), int(ph * 0.3), c2, icon, alpha=alpha)
    d = ImageDraw.Draw(layer)
    d.text((px + ph + 16, py + 13), text, font=f, fill=tcol + (int(255 * alpha),))
    if name:
        f2 = font(48, "Bold")
        text_center(d, cx, py + ph + 14, name, f2, (255, 255, 255, int(255 * alpha)), stroke=6, sfill=(0, 0, 0, int(255 * alpha)))
        if sub:
            f3 = font(28, "SemiBold")
            text_center(d, cx, py + ph + 14 + 56, sub, f3, (255, 220, 120, int(255 * alpha)), stroke=4, sfill=(0, 0, 0, int(235 * alpha)))
    return Image.alpha_composite(im, layer), (py, py + ph)

def roll_number(d, x, y, old, new, t, f, fill):
    """Odometer roll: old slides up and fades, new slides in from below."""
    if t <= 0: d.text((x, y), old, font=f, fill=fill); return
    if t >= 1: d.text((x, y), new, font=f, fill=fill); return
    e = 1 - (1 - t) ** 3; h = f.size * 0.9
    d.text((x, y - h * e), old, font=f, fill=fill[:3] + (int(255 * (1 - e)),))
    d.text((x, y + h * (1 - e)), new, font=f, fill=fill[:3] + (int(255 * e),))

def draw_chips(im, dex_old, dex_new, roll_t, region, reg_have, reg_of, trainers=None, upgrades=None, up_roll=0.0):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x, y = 40, 46
    fl = font(26, "SemiBold"); fn = font(58, "Bold"); fs = font(26, "SemiBold")
    d = ImageDraw.Draw(layer)
    w_num = max(d.textlength(str(dex_old), font=fn), d.textlength(str(dex_new), font=fn))
    pw = 34 + d.textlength("DEX", font=fl) + 14 + w_num + 12 + d.textlength("/ 1025", font=fs) + 30; ph = 84
    im = glass(im, (x, y, int(x + pw), y + ph), r=ph // 2, dark=165)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    cx = x + 34
    d.text((cx, y + 30), "DEX", font=fl, fill=(200, 205, 215, 255)); cx += d.textlength("DEX", font=fl) + 14
    roll_number(d, cx, y + 10, str(dex_old), str(dex_new), roll_t, fn, YEL + (255,)); cx += w_num + 12
    d.text((cx, y + 36), "/ 1025", font=fs, fill=(170, 176, 190, 255))
    im = Image.alpha_composite(im, layer)
    # region chip with progress bar
    y2 = y + ph + 12; f2 = font(24, "SemiBold")
    s = f"{region.upper()}   {reg_have} / {reg_of}"
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    tw = d.textlength(s, font=f2); pw2 = tw + 48; ph2 = 52
    im = glass(im, (x, y2, int(x + pw2), y2 + ph2), r=ph2 // 2, dark=140, blur=10)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text((x + 24, y2 + 9), s, font=f2, fill=(235, 237, 242, 255))
    bx0, bx1 = x + 24, x + pw2 - 24; by = y2 + ph2 - 10
    aa_rounded_rect(layer, (bx0, by - 3, bx1, by + 3), 3, fill=(255, 255, 255, 50))
    aa_rounded_rect(layer, (bx0, by - 3, bx0 + max(8, (bx1 - bx0) * reg_have / reg_of), by + 3), 3, fill=YEL + (255,))
    im = Image.alpha_composite(im, layer)
    y3 = y2 + ph2 + 10
    extras = []
    if trainers is not None: extras.append(("TRAINERS", trainers, (160, 200, 255), 0.0))
    if upgrades is not None: extras.append(("UPGRADES", upgrades, GOLD, up_roll))
    for label, val, col, rt in extras:
        f3 = font(22, "SemiBold")
        if isinstance(val, tuple): s3o, s3n = f"{label}  {val[0]}", f"{label}  {val[1]}"
        else: s3o = s3n = f"{label}  {val}"
        tw3 = max(ImageDraw.Draw(im).textlength(s3o, font=f3), ImageDraw.Draw(im).textlength(s3n, font=f3))
        im = glass(im, (x, y3, int(x + tw3 + 40), y3 + 42), r=21, dark=130, blur=8)
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        roll_number(d, x + 20, y3 + 9, s3o, s3n, rt, f3, col + (255,))
        im = Image.alpha_composite(im, layer); y3 += 52
    return im

# ---------- Pokédex strip panel ----------
PX0, PX1 = 90, 990; PANEL_H = 285; P_UP = 1285; P_DOWN = 1660
def slot_centers(py):
    gap = (PX1 - PX0 - 6 * TILE_W) / 7
    return [(int(PX0 + gap + i * (TILE_W + gap) + TILE_W / 2), int(py + 86 + TILE_H / 2)) for i in range(6)]

def draw_panel(im, py, alpha, region, have, of, numbers, filled, target_idx, target_tile=None, flip_x=1.0, flash=0.0, pulse=0.0, glow=0.0, ribbon=None, shimmer=None, bounce=1.0, ring=None, sparks=None, spark_col=YEL, number_labels=True, title="POKÉDEX"):
    """numbers: 6 National numbers; filled: {idx: tile}. Everything drawn into a layer then faded by alpha."""
    base = im
    im = im.copy()
    im = glass(im, (PX0, py, PX1, py + PANEL_H), r=32, dark=150)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    fh = font(26, "SemiBold"); fh2 = font(30, "Bold")
    d.text((PX0 + 30, py + 24), f"{title}  ·  {region.upper()}", font=fh, fill=(215, 219, 228, 255))
    s = f"{have} / {of}"; d.text((PX1 - 30 - d.textlength(s, font=fh2), py + 20), s, font=fh2, fill=YEL + (255,))
    d.line((PX0 + 30, py + 66, PX1 - 30, py + 66), fill=(255, 255, 255, 30), width=1)
    im = Image.alpha_composite(im, layer)
    centers = slot_centers(py)
    # soft glow behind the target slot
    if glow > 0:
        g = Image.new("RGBA", (TILE_W + 200, TILE_H + 200), (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle((90, 90, 110 + TILE_W, 110 + TILE_H), 24, fill=YEL + (int(110 * glow),))
        g = g.filter(ImageFilter.GaussianBlur(34))
        c = centers[target_idx]; im.alpha_composite(g, (c[0] - g.width // 2, c[1] - g.height // 2))
    for i, c in enumerate(centers):
        t = filled.get(i) if i != target_idx else target_tile
        if t is None: t = empty_tile(numbers[i])
        sc = bounce if i == target_idx else 1.0
        tw_ = max(2, int(TILE_W * sc * (flip_x if i == target_idx else 1.0))); th_ = int(TILE_H * sc)
        tt = t.resize((tw_, th_), Image.LANCZOS) if (tw_, th_) != t.size else t
        x = c[0] - tw_ // 2; y = c[1] - th_ // 2
        if i != target_idx or filled.get(i) is not None or target_tile is not None:
            im.alpha_composite(shadow((tw_, th_), TILE_R, alpha=90, blur=8), (x - 16, y - 8))
        im.alpha_composite(tt, (x, y))
        d = ImageDraw.Draw(im)
        if i == target_idx:
            if pulse > 0:
                aa_rounded_rect(im, (x - 3, y - 3, x + tw_ + 2, y + th_ + 2), TILE_R + 3, outline=YEL + (int(230 * pulse),), width=2)
            if flash > 0:
                fl = Image.new("RGBA", (tw_, th_), WHITE + (int(230 * flash),)); fl.putalpha(Image.eval(rounded_mask(fl.size, TILE_R), lambda v: int(v * flash)))
                im.alpha_composite(fl, (x, y))
            if shimmer is not None:
                sh = Image.new("RGBA", (tw_, th_), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
                sx = int(-50 + shimmer * (tw_ + 100))
                sd.polygon([(sx, 0), (sx + 30, 0), (sx - 26, th_), (sx - 56, th_)], fill=(255, 235, 160, 190))
                sd.polygon([(sx + 40, 0), (sx + 48, 0), (sx - 8, th_), (sx - 16, th_)], fill=(255, 255, 255, 120))
                m = np.minimum(np.array(rounded_mask(sh.size, TILE_R)), np.array(sh.split()[3])); sh.putalpha(Image.fromarray(m))
                im.alpha_composite(sh, (x, y))
            if ring is not None:  # one expanding ring that fades
                rr = int(ring * 70); a = int(170 * (1 - ring) ** 1.5)
                aa_rounded_rect(im, (c[0] - TILE_W // 2 - rr, c[1] - TILE_H // 2 - rr, c[0] + TILE_W // 2 + rr, c[1] + TILE_H // 2 + rr), TILE_R + rr, outline=spark_col + (a,), width=2)
            if sparks is not None:  # a few small dots, inside the panel
                rnd = random.Random(7)
                for k in range(9):
                    ang = rnd.random() * 2 * math.pi; dist = (50 + rnd.random() * 50) * sparks; r = 2 + rnd.random() * 3 * (1 - sparks)
                    sx_, sy_ = c[0] + math.cos(ang) * dist, c[1] + math.sin(ang) * dist * 0.6
                    aa_ellipse(im, (sx_ - r, sy_ - r, sx_ + r, sy_ + r), fill=spark_col + (int(255 * (1 - sparks)),))
            if ribbon:  # tag tucked inside the tile's top-left corner
                fr = font(17, "Bold"); tw = d.textlength(ribbon, font=fr)
                rx = x + 6; ry = y + 6
                aa_rounded_rect(im, (rx, ry, rx + tw + 16, ry + 26), 7, fill=(GOLD if ribbon == "UPGRADED" else YEL) + (255,))
                d.text((rx + 8, ry + 3), ribbon, font=fr, fill=INK)
        if number_labels and (i == target_idx or filled.get(i) is not None):
            fn = font(20, "SemiBold" if i != target_idx else "Bold")
            s = f"No. {numbers[i]:04d}"
            text_center(d, c[0], py + PANEL_H - 36, s, fn, (255, 255, 255, 255) if i == target_idx else (160, 166, 180, 255))
    if alpha >= 1: return im
    return Image.blend(base, im, alpha)

def bezier(sx, sy, tx, ty, e, lift=240):
    cxp, cyp = (sx + tx) / 2 + 160, min(sy, ty) - lift
    return ((1 - e) ** 2 * sx + 2 * (1 - e) * e * cxp + e ** 2 * tx, (1 - e) ** 2 * sy + 2 * (1 - e) * e * cyp + e ** 2 * ty)
def ease_in_out(t): return 0.5 - 0.5 * math.cos(math.pi * t)
def ease_out(t): return 1 - (1 - t) ** 3
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))

def flying_card(im, crop, card_box, target_c, t, rot=-10):
    x0, y0, x1, y1 = card_box; cw, ch = x1 - x0, y1 - y0
    sx, sy = (x0 + x1) / 2, (y0 + y1) / 2; tx, ty = target_c
    for ghost, ga in ((0.10, 0.10), (0.06, 0.18), (0.03, 0.30), (0.0, 1.0)):
        tt = clamp(t - ghost)
        if tt <= 0 and ghost > 0: continue
        e = ease_in_out(tt); sc = 1.0 + (TILE_W / cw - 1.0) * e
        px, py = bezier(sx, sy, tx, ty, e)
        w = max(2, int(cw * sc)); h = max(2, int(ch * sc))
        c = crop.resize((w, h), Image.LANCZOS)
        if sc < 0.7:
            c.putalpha(rounded_mask(c.size, int(TILE_R * w / TILE_W)))
        c = c.rotate(rot * (1 - e), expand=True, resample=Image.BICUBIC)
        if ga < 1: c.putalpha(Image.eval(c.split()[3], lambda v: int(v * ga)))
        else:
            sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 140), mask=c.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(14))
            im.alpha_composite(sh, (int(px - c.width / 2) + 14, int(py - c.height / 2) + 22))
        im.alpha_composite(c, (int(px - c.width / 2), int(py - c.height / 2)))
    return im

def lifted_card(im, crop, card_box, t):
    x0, y0, x1, y1 = card_box; cw, ch = x1 - x0, y1 - y0
    sc = 1.0 - 0.05 * t; w, h = int(cw * sc), int(ch * sc)
    c = crop.resize((w, h), Image.LANCZOS); c = Image.alpha_composite(c, Image.new("RGBA", c.size, (0, 0, 0, int(60 * t))))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 30 * t
    sh = Image.new("RGBA", c.size, (0, 0, 0, int(150 * t))).filter(ImageFilter.GaussianBlur(18))
    im.alpha_composite(sh, (int(cx - w / 2) + 14, int(cy - h / 2) + 26))
    im.alpha_composite(c, (int(cx - w / 2), int(cy - h / 2)))
    return im

def info_card(im, card_box, y_top, alpha, tile, line1, line2):
    """Already caught: small glass note showing the existing Dex entry."""
    x0, x1 = card_box[0], card_box[2]; cx = (x0 + x1) // 2
    w, h = 560, 150; bx0 = int(cx - w / 2); by0 = int(y_top)
    base = im; im = im.copy()
    im = glass(im, (bx0, by0, bx0 + w, by0 + h), r=26, dark=150, blur=12)
    small = make_tile(tile.resize((TILE_W, TILE_H)), dim=False).resize((int(TILE_W * 0.72), int(TILE_H * 0.72)), Image.LANCZOS)
    im.alpha_composite(small, (bx0 + 22, by0 + 15))
    d = ImageDraw.Draw(im)
    d.text((bx0 + 130, by0 + 34), line1, font=font(26, "SemiBold"), fill=(215, 219, 228, 255))
    d.text((bx0 + 130, by0 + 74), line2, font=font(32, "Bold"), fill=(255, 255, 255, 255))
    return Image.blend(base, im, alpha) if alpha < 1 else im

# ---------- animations ----------
def panel_y(f, up_start, up_len, down_start, down_len):
    if f < up_start: return None, 0.0
    if f < up_start + up_len:
        t = ease_out((f - up_start) / up_len); return P_DOWN + (P_UP - P_DOWN) * t, t
    if f < down_start: return P_UP, 1.0
    if f < down_start + down_len:
        t = ease_out((f - down_start) / down_len); return P_UP + (P_DOWN - P_UP) * t, 1 - t
    return None, 0.0

def anim_caught(k="golisopod", frames=78):
    base = FRAMES[k]; box = SRC[k][1]; crop = card_crop(k); name, num, region = SRC[k][2], SRC[k][3], SRC[k][4]
    numbers = [num - 3, num - 2, num - 1, num, num + 1, num + 2]; target = 3
    out = []
    for f in range(frames):
        im = base.copy()
        a = clamp(f / 5); im, (sy0, sy1) = draw_stamp(im, box, "caught", name.upper(), f"No. {num:04d}  ·  {region}", alpha=a, dy=int(36 * (1 - a)), y_cap=P_UP)
        py, pa = panel_y(f, 5, 8, 66, 10)
        landed = f >= 30; flight = 12 <= f < 30
        pulse = (0.55 + 0.45 * math.sin(f * 0.55)) if 12 <= f < 30 else 0.0
        flash = clamp(1 - (f - 30) / 6) if 30 <= f < 36 else 0.0
        bounce = 1 + 0.16 * math.sin(math.pi * clamp((f - 30) / 8)) if 30 <= f < 38 else 1.0
        ring = clamp((f - 30) / 14) if 30 <= f < 44 else None
        sparks = clamp((f - 30) / 16) if 30 <= f < 46 else None
        glow = 1.0 if landed else (0.5 if flight else 0.0)
        if py is not None:
            im = draw_panel(im, int(py), pa, region, 12 + (1 if landed else 0), 88, numbers, {}, target, target_tile=TILES[k] if landed else None,
                            flash=flash, pulse=pulse, glow=glow, ribbon="NEW" if f >= 33 else None, bounce=bounce, ring=ring, sparks=sparks)
        if flight and py is not None:
            im = flying_card(im, crop, box, slot_centers(int(py))[target], (f - 12) / 18)
        roll = clamp((f - 31) / 7) if f >= 31 else 0.0
        im = draw_chips(im, 133, 134, roll, region, 12 + (1 if f >= 34 else 0), 88)
        out.append(im)
    return out

def anim_upgraded(k="veluza", frames=92):
    base = FRAMES[k]; box = SRC[k][1]; crop = card_crop(k); name, num, region = SRC[k][2], SRC[k][3], SRC[k][4]
    numbers = [num - 3, num - 2, num - 1, num, num + 1, num + 2]; target = 3
    old_tile = make_tile(crop, dim=True)
    out = []
    for f in range(frames):
        im = base.copy()
        a = clamp(f / 5); im, _ = draw_stamp(im, box, "upgraded", f"{name.upper()} EX", "Double Rare replaces Common", alpha=a, dy=int(36 * (1 - a)), y_cap=P_UP)
        py, pa = panel_y(f, 5, 8, 80, 10)
        flight = 12 <= f < 30
        if 30 <= f < 36: flip = 1 - (f - 30) / 6; tile = old_tile
        elif 36 <= f < 42: flip = (f - 36) / 6; tile = TILES[k]
        else: flip = 1.0; tile = TILES[k] if f >= 42 else old_tile
        shimmer = clamp((f - 42) / 12) if 42 <= f < 54 else None
        bounce = 1 + 0.14 * math.sin(math.pi * clamp((f - 42) / 8)) if 42 <= f < 50 else 1.0
        ring = clamp((f - 42) / 14) if 42 <= f < 56 else None
        sparks = clamp((f - 42) / 16) if 42 <= f < 58 else None
        pulse = (0.55 + 0.45 * math.sin(f * 0.55)) if 12 <= f < 30 else 0.0
        if py is not None:
            im = draw_panel(im, int(py), pa, region, 41, 120, numbers, {}, target, target_tile=tile, flip_x=flip, pulse=pulse, glow=1.0 if f >= 12 else 0.0,
                            ribbon="UPGRADED" if f >= 44 else None, shimmer=shimmer, bounce=bounce, ring=ring, sparks=sparks, spark_col=GOLD)
        if flight and py is not None:
            im = flying_card(im, crop, box, slot_centers(int(py))[target], (f - 12) / 18)
        up_roll = clamp((f - 44) / 7) if f >= 44 else 0.0
        im = draw_chips(im, 134, 134, 0.0, region, 41, 120, upgrades=(17, 18), up_roll=up_roll)
        out.append(im)
    return out

def anim_already(k="technoradar", frames=48):
    base = FRAMES[k]; box = SRC[k][1]; crop = card_crop(k); name = SRC[k][2]
    out = []
    for f in range(frames):
        im = base.copy()
        if 2 <= f < 9: lift = ease_out((f - 2) / 7)
        elif 9 <= f < 16: lift = 1 - ease_out((f - 9) / 7)
        else: lift = 0.0
        if lift > 0.01: im = lifted_card(im, crop, box, lift)
        a = clamp(f / 5); im, (sy0, sy1) = draw_stamp(im, box, "already", None, alpha=a, dy=int(30 * (1 - a)), y_cap=P_UP)
        ia = clamp((f - 10) / 6) if f < 40 else clamp(1 - (f - 40) / 8)
        if f >= 10 and ia > 0:
            im = info_card(im, box, sy1 + 26, ia, make_tile(crop, dim=True), "TRAINER DEX  ·  caught in Dex #7", name)
        im = draw_chips(im, 134, 134, 0.0, "Alola", 12, 88, trainers=22)
        out.append(im)
    return out

def write_video(frames, name, fps=30):
    d = os.path.join(TMP, "frames_" + name); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    for i, im in enumerate(frames): im.convert("RGB").save(os.path.join(d, f"{i:04d}.jpg"), quality=93)
    outp = os.path.join(OUT, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", os.path.join(d, "%04d.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", outp], check=True)
    return outp

def sheet(idx, frames, labels, name, title):
    n = len(idx); fw, fh = 405, 720
    s = Image.new("RGB", (n * fw + (n + 1) * 16, fh + 150), (24, 26, 32)); d = ImageDraw.Draw(s)
    d.text((16, 14), title, font=font(34, "Bold"), fill=WHITE)
    for j, (fi, lab) in enumerate(zip(idx, labels)):
        x = 16 + j * (fw + 16); s.paste(frames[fi].convert("RGB").resize((fw, fh), Image.LANCZOS), (x, 70))
        d.text((x, 70 + fh + 12), lab, font=font(22, "SemiBold"), fill=(220, 222, 228))
    s.save(os.path.join(OUT, name), quality=90)

if __name__ == "__main__":
    which = sys.argv[1:] or ["caught", "upgraded", "already", "sheets", "concat"]
    store = {}
    if "caught" in which: store["caught"] = anim_caught(); print(write_video(store["caught"], "anim_caught"))
    if "upgraded" in which: store["upgraded"] = anim_upgraded(); print(write_video(store["upgraded"], "anim_upgraded"))
    if "already" in which: store["already"] = anim_already(); print(write_video(store["already"], "anim_already"))
    if "sheets" in which:
        if "caught" in store: sheet([4, 11, 22, 36], store["caught"], ["0.15 s  stamp, No. 0768, ding", "0.35 s  Pokédex strip slides up, slot glows", "0.75 s  card flies in with a trail", "1.2 s  flash, sparks, NEW, DEX rolls 133 -> 134"], "storyboard_caught.jpg", "CAUGHT  ·  Golisopod, No. 0768, first time in the run")
        if "upgraded" in store: sheet([4, 22, 33, 48], store["upgraded"], ["0.15 s  gold stamp, what replaces what", "0.75 s  flies to the slot holding Veluza", "1.1 s  old tile flips away", "1.6 s  new tile, shimmer, UPGRADES rolls 17 -> 18"], "storyboard_upgraded.jpg", "UPGRADED  ·  Veluza ex replaces the plain Veluza")
        if "already" in store: sheet([4, 8, 20, 44], store["already"], ["0.15 s  grey stamp, soft tick", "0.25 s  card lifts as if to fly...", "0.7 s  ...drops back; where it already sits", "1.45 s  note fades, nothing else"], "storyboard_already.jpg", "ALREADY CAUGHT  ·  Techno Radar, seen in Dex #7")
        print("sheets ok")
    if "concat" in which:
        lst = os.path.join(TMP, "concat.txt")
        with open(lst, "w") as fh_: fh_.write("".join(f"file '{OUT}/anim_{n}.mp4'\n" for n in ("caught", "upgraded", "already")))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{OUT}/dex_preview_all.mp4"], check=True)
        print("concat ok")
