"""Dex format mock-ups: layout options (static), verdict storyboards (static) and
verdict animations (frames -> mp4). Pillow only; ffmpeg encodes."""
import math, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/Users/marerobert/OpenMontage"
OUT = f"{ROOT}/channels/poke-capnv/dex/mockups"
TMP = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
def font(sz): return ImageFont.truetype(FONT, sz)

YEL = (255, 203, 5); GREEN = (46, 204, 113); GREY = (120, 126, 134); GOLD = (255, 190, 60)
DARK = (18, 20, 26, 225); WHITE = (255, 255, 255)

# source frames and card boxes (x0, y0, x1, y1) in 1080x1920
SRC = {
    "golisopod": (f"{ROOT}/projects/poke-capnv-draw-17/public/images/golisopod_freeze_1080x1920.png", (125, 285, 880, 1365), "Golisopod", "Rare"),
    "technoradar": (f"{ROOT}/projects/poke-capnv-draw-17/public/images/technoradar_freeze_1080x1920.png", (190, 310, 860, 1205), "Techno Radar", "Uncommon"),
    "ursaluna": (f"{ROOT}/projects/poke-capnv-draw-17/public/images/ursaluna_freeze_1080x1920.png", (240, 330, 920, 1235), "Bloodmoon Ursaluna", "Rare"),
    "veluza": (f"{ROOT}/projects/poke-capnv-draw-16/public/images/veluza_freeze_1080x1920.png", (125, 320, 890, 1380), "Veluza", "Double Rare"),
    "fezandipiti": (f"{ROOT}/projects/poke-capnv-draw-16/public/images/fezandipiti_freeze_1080x1920.png", (130, 530, 920, 1670), "Fezandipiti", "Rare"),
}
FRAMES = {k: Image.open(v[0]).convert("RGBA") for k, v in SRC.items()}
def card_crop(k):
    x0, y0, x1, y1 = SRC[k][1]
    return FRAMES[k].crop((x0, y0, x1, y1))

TILE_W, TILE_H = 112, 156
def make_tile(img, dim=False):
    t = img.resize((TILE_W, TILE_H), Image.LANCZOS).convert("RGBA")
    if dim:
        t = Image.blend(t, Image.new("RGBA", t.size, (60, 60, 70, 255)), 0.55)
    mask = Image.new("L", t.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, TILE_W - 1, TILE_H - 1), 10, fill=255)
    t.putalpha(mask)
    return t
def empty_tile(num):
    t = Image.new("RGBA", (TILE_W, TILE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, TILE_W - 1, TILE_H - 1), 10, fill=(40, 44, 54, 230), outline=(90, 96, 110, 255), width=2)
    f = font(26); s = f"#{num:03d}"
    tw = d.textlength(s, font=f)
    d.text(((TILE_W - tw) / 2, TILE_H / 2 - 16), s, font=f, fill=(150, 156, 170))
    return t

TILES = {k: make_tile(card_crop(k)) for k in SRC}

def pill(draw, xy, text, fill, fnt, pad=(26, 12), text_fill=WHITE, stroke=0):
    x, y = xy
    tw = draw.textlength(text, font=fnt); th = fnt.size
    box = (x, y, x + tw + pad[0] * 2, y + th + pad[1] * 2)
    draw.rounded_rectangle(box, (th + pad[1] * 2) // 2, fill=fill)
    draw.text((x + pad[0], y + pad[1] - 2), text, font=fnt, fill=text_fill)
    return box

def draw_chips(im, dex_total, set_name, have, of, bump=1.0, upgrades=None):
    """Top-left persistent chips: DEX total and set page."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    f1 = font(int(44 * bump)); f0 = font(int(30 * bump))
    x, y = 40, 48
    # DEX chip
    label = "DEX "; num = f"{dex_total}"
    tw_l = d.textlength(label, font=f0); tw_n = d.textlength(num, font=f1)
    w = tw_l + tw_n + 56; h = f1.size + 26
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=DARK)
    d.text((x + 28, y + 13 + (f1.size - f0.size) * 0.65), label, font=f0, fill=WHITE)
    d.text((x + 28 + tw_l, y + 11), num, font=f1, fill=YEL)
    # set chip
    y2 = y + h + 12; f2 = font(26)
    s = f"{set_name.upper()}   {have} / {of}"
    tw = d.textlength(s, font=f2)
    d.rounded_rectangle((x, y2, x + tw + 44, y2 + 46), 23, fill=(18, 20, 26, 190))
    d.text((x + 22, y2 + 9), s, font=f2, fill=(230, 232, 236))
    if upgrades is not None:
        y3 = y2 + 56; f3 = font(22); s3 = f"UPGRADES  {upgrades}"
        tw3 = d.textlength(s3, font=f3)
        d.rounded_rectangle((x, y3, x + tw3 + 40, y3 + 40), 20, fill=(18, 20, 26, 170))
        d.text((x + 20, y3 + 8), s3, font=f3, fill=GOLD)
    return Image.alpha_composite(im, layer)

def draw_stamp(im, card_box, kind, name=None, alpha=1.0, dy=0):
    """Verdict stamp under the card art area (lower part of the card)."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = card_box
    cx = (x0 + x1) // 2
    if kind == "caught": text, col = "CAUGHT", GREEN
    elif kind == "already": text, col = "ALREADY CAUGHT", GREY
    else: text, col = "UPGRADED", GOLD
    f = font(54 if kind != "already" else 44)
    tw = d.textlength(text, font=f); pw = tw + 60; ph = f.size + 28
    px = cx - pw / 2; py = min(y1 - 170, PANEL_Y_UP - 150 - (0 if not name else 60)) + dy
    d.rounded_rectangle((px, py, px + pw, py + ph), ph // 2, fill=col + (int(255 * alpha),))
    d.text((px + 30, py + 12), text, font=f, fill=(255, 255, 255, int(255 * alpha)) if kind != "upgraded" else (30, 24, 10, int(255 * alpha)))
    if name:
        f2 = font(46); tw2 = d.textlength(name, font=f2)
        d.text((cx - tw2 / 2, py + ph + 10), name, font=f2, fill=(255, 255, 255, int(255 * alpha)), stroke_width=5, stroke_fill=(0, 0, 0, int(255 * alpha)))
    return Image.alpha_composite(im, layer)

# ---------- layout C: page panel (recommended) ----------
PANEL_X0, PANEL_X1 = 90, 990
PANEL_H = 262
PANEL_Y_UP = 1300           # resting y when shown
PANEL_Y_DOWN = 1640         # hidden (below safe area)
SLOTS = 6
def slot_centers(py):
    gap = (PANEL_X1 - PANEL_X0 - SLOTS * TILE_W) / (SLOTS + 1)
    cy = py + 70 + TILE_H / 2
    return [(int(PANEL_X0 + gap + i * (TILE_W + gap) + TILE_W / 2), int(cy)) for i in range(SLOTS)]

def draw_panel(im, py, set_name, have, of, tiles, target_idx, flash=0.0, ribbon=None, target_override=None, flip_x=1.0, shimmer=None, pulse=0.0):
    """tiles: list of (PIL tile or None, number). target_idx gets the outline/flash."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.rounded_rectangle((PANEL_X0, py, PANEL_X1, py + PANEL_H), 28, fill=(14, 16, 22, 215), outline=(70, 74, 86, 255), width=2)
    f = font(28)
    d.text((PANEL_X0 + 28, py + 20), set_name.upper(), font=f, fill=(235, 236, 240))
    s = f"{have} / {of}"; tw = d.textlength(s, font=f)
    d.text((PANEL_X1 - 28 - tw, py + 20), s, font=f, fill=YEL)
    im = Image.alpha_composite(im, layer)
    for i, (c, (tile, num)) in enumerate(zip(slot_centers(py), tiles)):
        t = tile if tile is not None else empty_tile(num)
        if i == target_idx and target_override is not None:
            t = target_override
        if i == target_idx and flip_x < 1.0:
            nw = max(2, int(TILE_W * flip_x)); t = t.resize((nw, TILE_H), Image.LANCZOS)
        x = c[0] - t.width // 2; y = c[1] - TILE_H // 2
        im.alpha_composite(t, (x, y))
        if i == target_idx:
            d2 = ImageDraw.Draw(im)
            if pulse > 0:
                a = int(255 * pulse)
                d2.rounded_rectangle((c[0] - TILE_W // 2 - 4, y - 4, c[0] + TILE_W // 2 + 3, y + TILE_H + 3), 13, outline=(255, 203, 5, a), width=4)
            if flash > 0:
                fl = Image.new("RGBA", (TILE_W, TILE_H), (255, 255, 255, int(255 * flash)))
                m = Image.new("L", fl.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, TILE_W - 1, TILE_H - 1), 10, fill=255); fl.putalpha(Image.eval(m, lambda v: int(v * flash)))
                im.alpha_composite(fl, (c[0] - TILE_W // 2, y))
            if shimmer is not None:  # gold diagonal band sweeping across the tile
                sh = Image.new("RGBA", (TILE_W, TILE_H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
                sx = int(-40 + shimmer * (TILE_W + 80))
                sd.polygon([(sx, 0), (sx + 26, 0), (sx - 20, TILE_H), (sx - 46, TILE_H)], fill=(255, 220, 120, 170))
                m = Image.new("L", sh.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, TILE_W - 1, TILE_H - 1), 10, fill=255)
                sh.putalpha(Image.fromarray(__import__("numpy").minimum(__import__("numpy").array(m), __import__("numpy").array(sh.split()[3]))))
                im.alpha_composite(sh, (c[0] - TILE_W // 2, y))
            if ribbon:
                d2 = ImageDraw.Draw(im); fr = font(20)
                col = GOLD if ribbon == "UPGRADED" else YEL
                tw = d2.textlength(ribbon, font=fr)
                rx = c[0] - TILE_W // 2 - 6; ry = y - 14
                d2.rounded_rectangle((rx, ry, rx + tw + 20, ry + 30), 8, fill=col)
                d2.text((rx + 10, ry + 4), ribbon, font=fr, fill=(30, 24, 10))
    return im

def flying_card(im, crop, card_box, target_c, t, rot=-8):
    """Copy of the card travelling from its on-screen position to the tile centre. t in [0,1]."""
    x0, y0, x1, y1 = card_box
    cw, ch = x1 - x0, y1 - y0
    ease = 1 - (1 - t) ** 3
    sc = 1.0 + (TILE_W / cw - 1.0) * ease
    sx, sy = (x0 + x1) / 2, (y0 + y1) / 2
    tx, ty = target_c
    # quadratic bezier with a control point above-right for an arc
    cxp, cyp = (sx + tx) / 2 + 180, min(sy, ty) - 220
    px = (1 - ease) ** 2 * sx + 2 * (1 - ease) * ease * cxp + ease ** 2 * tx
    py = (1 - ease) ** 2 * sy + 2 * (1 - ease) * ease * cyp + ease ** 2 * ty
    w = max(2, int(cw * sc)); h = max(2, int(ch * sc))
    c = crop.resize((w, h), Image.LANCZOS)
    if sc < 0.6:  # rounded corners once it is small
        m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), int(10 * (w / TILE_W)), fill=255); c.putalpha(m)
    c = c.rotate(rot * (1 - ease), expand=True, resample=Image.BICUBIC)
    # soft shadow
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), mask=c.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(12))
    im.alpha_composite(sh, (int(px - c.width / 2) + 10, int(py - c.height / 2) + 18))
    im.alpha_composite(c, (int(px - c.width / 2), int(py - c.height / 2)))
    return im

def lifted_card(im, crop, card_box, t_lift):
    """Already caught: the card copy lifts slightly and drops back. t_lift in [0,1] = amount of lift."""
    x0, y0, x1, y1 = card_box
    cw, ch = x1 - x0, y1 - y0
    sc = 1.0 - 0.05 * t_lift
    w, h = int(cw * sc), int(ch * sc)
    c = crop.resize((w, h), Image.LANCZOS)
    dimmer = Image.new("RGBA", c.size, (0, 0, 0, int(70 * t_lift))); c = Image.alpha_composite(c, dimmer)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 28 * t_lift
    sh = Image.new("RGBA", c.size, (0, 0, 0, int(140 * t_lift))).filter(ImageFilter.GaussianBlur(16))
    if t_lift > 0.02:
        im.alpha_composite(sh, (int(cx - w / 2) + 12, int(cy - h / 2) + 22))
    im.alpha_composite(c, (int(cx - w / 2), int(cy - h / 2)))
    return im

def ease_out(t): return 1 - (1 - t) ** 3
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))

# Dex page contents for the mock-ups: 6 visible slots around the target
PAGE_SET = ("Mega Evolution", 38, 112)
def page_tiles(target_idx, target_tile=None, filled=("fezandipiti", "ursaluna", "technoradar", "veluza")):
    tiles = []; fi = 0
    for i in range(SLOTS):
        if i == target_idx:
            tiles.append((target_tile, 61))
        elif fi < len(filled) and i in (0, 1, 4, 5):
            tiles.append((TILES[filled[fi]], 50 + i)); fi += 1
        else:
            tiles.append((None, 50 + i))
    return tiles

# ---------- animations ----------
def anim_caught(k="golisopod", frames=72):
    base = FRAMES[k]; box = SRC[k][1]; crop = card_crop(k); name = SRC[k][2]
    out = []
    target = 3; tiles = page_tiles(target)
    for f in range(frames):
        im = base.copy()
        # stamp 0-4
        a = clamp(f / 4); im = draw_stamp(im, box, "caught", name.upper(), alpha=a, dy=int(40 * (1 - a)))
        # panel 4-10 up, holds, 58-68 down
        if 4 <= f < 58: py = PANEL_Y_DOWN + (PANEL_Y_UP - PANEL_Y_DOWN) * ease_out(clamp((f - 4) / 6))
        elif f >= 58: py = PANEL_Y_UP + (PANEL_Y_DOWN - PANEL_Y_UP) * ease_out(clamp((f - 58) / 10))
        else: py = None
        landed = f >= 28
        flash = clamp(1 - (f - 28) / 5) if 28 <= f < 33 else 0.0
        pulse = (0.5 + 0.5 * math.sin(f * 0.6)) if 10 <= f < 28 else 0.0
        if py is not None and py < PANEL_Y_DOWN - 2:
            im = draw_panel(im, int(py), *PAGE_SET[:1], PAGE_SET[1] + (1 if landed else 0), PAGE_SET[2], tiles, target,
                            flash=flash, ribbon="NEW" if f >= 30 else None, target_override=TILES[k] if landed else None, pulse=pulse)
        # flight 10-28
        if 10 <= f < 28 and py is not None:
            im = flying_card(im, crop, box, slot_centers(int(py))[target], (f - 10) / 18)
        # chips: tick at 28 with bump
        bump = 1.0 + 0.18 * math.sin(math.pi * clamp((f - 28) / 8)) if 28 <= f < 36 else 1.0
        im = draw_chips(im, 134 if landed else 133, PAGE_SET[0], PAGE_SET[1] + (1 if landed else 0), PAGE_SET[2], bump=bump)
        out.append(im)
    return out

def anim_upgraded(k="veluza", frames=84):
    base = FRAMES[k]; box = SRC[k][1]; crop = card_crop(k); name = SRC[k][2]
    old_tile = make_tile(crop, dim=True)  # stands in for the plain Veluza already in the Dex
    out = []
    target = 3; tiles = page_tiles(target, target_tile=old_tile)
    for f in range(frames):
        im = base.copy()
        a = clamp(f / 4); im = draw_stamp(im, box, "upgraded", f"{name.upper()} EX", alpha=a, dy=int(40 * (1 - a)))
        if 4 <= f < 70: py = PANEL_Y_DOWN + (PANEL_Y_UP - PANEL_Y_DOWN) * ease_out(clamp((f - 4) / 6))
        elif f >= 70: py = PANEL_Y_UP + (PANEL_Y_DOWN - PANEL_Y_UP) * ease_out(clamp((f - 70) / 10))
        else: py = None
        arrived = f >= 28
        # flip 28-40: old tile squashes to 0 (28-34), new tile grows (34-40)
        if 28 <= f < 34: flip = 1 - (f - 28) / 6; override = old_tile
        elif 34 <= f < 40: flip = (f - 34) / 6; override = TILES[k]
        else: flip = 1.0; override = TILES[k] if arrived else None
        shimmer = clamp((f - 40) / 10) if 40 <= f < 50 else None
        pulse = (0.5 + 0.5 * math.sin(f * 0.6)) if 10 <= f < 28 else 0.0
        if py is not None and py < PANEL_Y_DOWN - 2:
            im = draw_panel(im, int(py), PAGE_SET[0], PAGE_SET[1], PAGE_SET[2], tiles, target,
                            ribbon="UPGRADED" if f >= 40 else None, target_override=override, flip_x=flip, shimmer=shimmer, pulse=pulse)
        if 10 <= f < 28 and py is not None:
            im = flying_card(im, crop, box, slot_centers(int(py))[target], (f - 10) / 18)
        bump = 1.0 + 0.15 * math.sin(math.pi * clamp((f - 40) / 8)) if 40 <= f < 48 else 1.0
        im = draw_chips(im, 134, PAGE_SET[0], PAGE_SET[1], PAGE_SET[2], upgrades=(18 if f >= 40 else 17), bump=1.0)
        out.append(im)
    return out

def anim_already(k="technoradar", frames=36):
    base = FRAMES[k]; box = SRC[k][1]; crop = card_crop(k)
    out = []
    for f in range(frames):
        im = base.copy()
        # lift 2-8, drop 8-14 with a tiny overshoot
        if 2 <= f < 8: lift = ease_out((f - 2) / 6)
        elif 8 <= f < 14: lift = 1 - ease_out((f - 8) / 6)
        else: lift = 0.0
        if lift > 0.01: im = lifted_card(im, crop, box, lift)
        a = clamp(f / 4); im = draw_stamp(im, box, "already", None, alpha=a, dy=int(30 * (1 - a)))
        im = draw_chips(im, 134, PAGE_SET[0], PAGE_SET[1], PAGE_SET[2])
        out.append(im)
    return out

def write_video(frames, name, fps=30):
    d = os.path.join(TMP, "frames_" + name); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    for i, im in enumerate(frames):
        im.convert("RGB").save(os.path.join(d, f"{i:04d}.jpg"), quality=92)
    outp = os.path.join(OUT, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", os.path.join(d, "%04d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", outp], check=True)
    return outp

def sheet(frames_idx, frames, labels, name, title):
    """Key frames side by side, scaled to 405x720, with labels."""
    n = len(frames_idx); fw, fh = 405, 720
    s = Image.new("RGB", (n * fw + (n + 1) * 16, fh + 150), (28, 30, 36)); d = ImageDraw.Draw(s)
    d.text((16, 14), title, font=font(34), fill=WHITE)
    for j, (fi, lab) in enumerate(zip(frames_idx, labels)):
        im = frames[fi].convert("RGB").resize((fw, fh), Image.LANCZOS)
        x = 16 + j * (fw + 16); s.paste(im, (x, 70))
        d.text((x, 70 + fh + 12), lab, font=font(22), fill=(220, 222, 228))
    s.save(os.path.join(OUT, name), quality=90)

# ---------- static layout options (A shelf, B column, C panel) on the Golisopod frame ----------
def layout_option(kind):
    k = "golisopod"; im = FRAMES[k].copy(); box = SRC[k][1]; crop = card_crop(k)
    im = draw_stamp(im, box, "caught", "GOLISOPOD")
    filled = ["fezandipiti", "ursaluna", "technoradar", "veluza"]
    if kind == "A":  # shelf under the chips
        y = 200; xs = [90 + i * (TILE_W + 18) for i in range(7)]
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        d.rounded_rectangle((60, y - 18, 1000, y + TILE_H + 18), 22, fill=(14, 16, 22, 200)); im = Image.alpha_composite(im, layer)
        for i, x in enumerate(xs):
            t = TILES[filled[i]] if i < 4 else empty_tile(60 + i)
            im.alpha_composite(t, (x, y))
        target = (xs[4] + TILE_W // 2, y + TILE_H // 2)
        im = flying_card(im, crop, box, target, 0.55)
        im = draw_chips(im, 133, *PAGE_SET)
        im = draw_chips(im, 133, *PAGE_SET)  # chips sit above the shelf; re-drawn on top
        label = "A. Shelf: a row of tiles under the chips; the card flies up."
    elif kind == "B":  # column on the left edge
        x = 24; ys = [330 + i * (TILE_H + 14) for i in range(6)]
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        d.rounded_rectangle((x - 12, ys[0] - 14, x + TILE_W + 12, ys[-1] + TILE_H + 14), 22, fill=(14, 16, 22, 200)); im = Image.alpha_composite(im, layer)
        for i, y in enumerate(ys):
            t = TILES[filled[i]] if i < 4 else empty_tile(60 + i)
            im.alpha_composite(t, (x, y))
        target = (x + TILE_W // 2, ys[4] + TILE_H // 2)
        im = flying_card(im, crop, box, target, 0.55, rot=-14)
        im = draw_chips(im, 133, *PAGE_SET)
        label = "B. Column: tiles down the left edge; the card flies left."
    else:  # C panel
        tiles = page_tiles(3)
        im = draw_panel(im, PANEL_Y_UP, PAGE_SET[0], PAGE_SET[1], PAGE_SET[2], tiles, 3, pulse=1.0)
        im = flying_card(im, crop, box, slot_centers(PANEL_Y_UP)[3], 0.55)
        im = draw_chips(im, 133, *PAGE_SET)
        label = "C. Page panel: the set page slides up from below; the card flies down into its slot."
    return im, label

if __name__ == "__main__":
    which = sys.argv[1:] or ["layouts", "caught", "upgraded", "already", "sheets"]
    store = {}
    if "layouts" in which:
        fw, fh = 540, 960
        s = Image.new("RGB", (3 * fw + 4 * 16, fh + 150), (28, 30, 36)); d = ImageDraw.Draw(s)
        d.text((16, 14), "Where the Dex lives on screen (same Caught moment, mid-flight)", font=font(34), fill=WHITE)
        for j, kind in enumerate("ABC"):
            im, lab = layout_option(kind)
            x = 16 + j * (fw + 16); s.paste(im.convert("RGB").resize((fw, fh), Image.LANCZOS), (x, 70))
            d.text((x, 70 + fh + 12), lab, font=font(20), fill=(220, 222, 228))
            im.convert("RGB").save(os.path.join(OUT, f"layout_{kind}.jpg"), quality=90)
        s.save(os.path.join(OUT, "layouts_ABC.jpg"), quality=90)
        print("layouts ok")
    if "caught" in which:
        store["caught"] = anim_caught(); print(write_video(store["caught"], "anim_caught"))
    if "upgraded" in which:
        store["upgraded"] = anim_upgraded(); print(write_video(store["upgraded"], "anim_upgraded"))
    if "already" in which:
        store["already"] = anim_already(); print(write_video(store["already"], "anim_already"))
    if "sheets" in which:
        if "caught" in store:
            sheet([3, 9, 20, 32], store["caught"], ["0.1 s  stamp + ding", "0.3 s  page slides up, slot pulses", "0.7 s  card flies to its slot", "1.1 s  slot flashes, NEW, DEX 133 -> 134"], "storyboard_caught.jpg", "CAUGHT  (Golisopod, first time in the run)")
        if "upgraded" in store:
            sheet([3, 20, 31, 46], store["upgraded"], ["0.1 s  gold stamp", "0.7 s  flies to the slot holding Veluza", "1.0 s  old tile flips away", "1.5 s  new tile, shimmer, UPGRADES 17 -> 18"], "storyboard_upgraded.jpg", "UPGRADED  (Veluza ex replaces the plain Veluza tile)")
        if "already" in store:
            sheet([3, 7, 11, 20], store["already"], ["0.1 s  grey stamp, soft tick", "0.25 s  card lifts a little...", "0.4 s  ...and drops back", "0.7 s  nothing else happens"], "storyboard_already.jpg", "ALREADY CAUGHT  (Techno Radar, seen before)")
        print("sheets ok")
