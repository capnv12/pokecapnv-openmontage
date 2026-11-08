"""Dex mock-ups v4: two new design directions, no persistent HUD.
A = Take-over: the footage dims, the card lifts to centre, big type, the Pokédex row appears edge to edge, the card drops into its slot, everything fades back.
B = Inline: footage untouched, type-only verdict under the card, an edge-to-edge tile row (no box) at the bottom, the card flies into its slot.
Reuses frames/helpers from make_mockups_v3.py."""
import math, os, sys, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_mockups_v3 as L  # fonts, frames, aa helpers, flying_card, rounded_mask, shadow

OUT = f"{L.ROOT}/channels/poke-capnv/dex/mockups/v4"; TMP = L.TMP.replace("/v3", "/v4")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
W, H = L.W, L.H
YEL, GREEN, GOLD, GREY, WHITE, INK = L.YEL, (72, 220, 140), (255, 200, 70), (165, 170, 182), L.WHITE, L.INK
font, clamp, ease_out, ease_in_out, bezier = L.font, L.clamp, L.ease_out, L.ease_in_out, L.bezier
SAFE_BOTTOM = 1570

def tracked(d, xy, text, f, fill, tracking=0.0, stroke=0, sfill=(0, 0, 0, 255), anchor="l"):
    """Letter-spaced text. tracking in px. anchor l/c."""
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor == "c": x -= total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill); x += w + tracking
    return total

def dim_frame(im, amount, blur):
    """Darken and blur the footage for a take-over moment."""
    if amount <= 0: return im.copy()
    out = im.filter(ImageFilter.GaussianBlur(blur * amount)) if blur * amount > 0.3 else im.copy()
    out = ImageEnhance.Brightness(out).enhance(1 - 0.72 * amount)
    # vignette
    v = Image.new("L", (W // 8, H // 8), 0); dv = ImageDraw.Draw(v)
    dv.ellipse((-W // 16, -H // 32, W // 8 + W // 16, H // 8 + H // 32), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(28)).resize((W, H), Image.BILINEAR)
    dark = Image.new("RGBA", (W, H), (0, 0, 0, int(140 * amount))); dark.putalpha(Image.eval(v, lambda p: int((255 - p) * 0.55 * amount)))
    return Image.alpha_composite(out, dark)

def card_at(im, crop, cx, cy, w, rot=0.0, alpha=1.0, radius_frac=0.045):
    """Place a card crop centred at (cx, cy) with width w, rounded corners and a soft shadow."""
    cw, ch = crop.size; h = int(w * ch / cw); w = int(w)
    c = crop.resize((w, h), Image.LANCZOS); c.putalpha(L.rounded_mask(c.size, int(w * radius_frac)))
    if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1: c.putalpha(Image.eval(c.split()[3], lambda p: int(p * alpha)))
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(170 * alpha)), mask=c.split()[3]); sh = sh.filter(ImageFilter.GaussianBlur(max(6, w // 18)))
    im.alpha_composite(sh, (int(cx - c.width / 2) + w // 22, int(cy - c.height / 2) + w // 10))
    im.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))
    return (w, h)

# ---------- the Pokédex row (shared by A and B; no box, edge-to-edge, faded ends) ----------
def dex_row(im, y_center, numbers, filled, target_idx, tile_w, alpha=1.0, target_tile=None, frame_pulse=0.0, flash=0.0, flip_x=1.0,
            shimmer=None, bounce=1.0, ring=None, ring_col=YEL, ribbon=None, labels=True, header=None, header_right=None, shift=0.0, header_size=26, scrim_a=0.62):
    tile_h = int(tile_w * 1.4); gap = int(tile_w * 0.14)
    n = len(numbers); total = n * tile_w + (n - 1) * gap
    x_start = (W - total) / 2 + shift
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    if header:
        f = font(header_size, "SemiBold"); tracked(d, (W / 2 - total / 2 + 2, y_center - tile_h / 2 - header_size * 2.1), header, f, (232, 235, 240, 255), tracking=3)
    if header_right:
        f = font(header_size + 6, "Bold"); tw = d.textlength(header_right, font=f); d.text((W / 2 + total / 2 - tw, y_center - tile_h / 2 - header_size * 2.25), header_right, font=f, fill=YEL + (255,))
    for i, num in enumerate(numbers):
        cx = x_start + i * (tile_w + gap) + tile_w / 2; cy = y_center
        is_t = i == target_idx
        sc = bounce if is_t else 1.0
        tw_ = max(2, int(tile_w * sc * (flip_x if is_t else 1.0))); th_ = int(tile_h * sc)
        x = int(cx - tw_ / 2); y = int(cy - th_ / 2)
        tile = filled.get(i) if not is_t else target_tile
        if tile is not None:
            t = tile.resize((tw_, th_), Image.LANCZOS); t.putalpha(L.rounded_mask(t.size, int(tile_w * 0.1)))
            sh = L.shadow((tw_, th_), int(tile_w * 0.1), alpha=120, blur=10); layer.alpha_composite(sh, (x - 20, y - 10))
            layer.alpha_composite(t, (x, y))
            L.aa_rounded_rect(layer, (x, y, x + tw_ - 1, y + th_ - 1), int(tile_w * 0.1), outline=(255, 255, 255, 70), width=1)
        else:
            L.aa_rounded_rect(layer, (x, y, x + tw_ - 1, y + th_ - 1), int(tile_w * 0.1), fill=(255, 255, 255, 26 if not is_t else 40))
            f1 = font(int(tile_w * 0.15), "SemiBold"); f2 = font(int(tile_w * 0.24), "Bold")
            L.text_center(d, cx, cy - tile_w * 0.26, "No.", f1, (200, 204, 214, 190))
            L.text_center(d, cx, cy - tile_w * 0.08, f"{num:04d}", f2, (225, 228, 236, 230))
        if is_t:
            if frame_pulse > 0: L.aa_rounded_rect(layer, (x - 4, y - 4, x + tw_ + 3, y + th_ + 3), int(tile_w * 0.1) + 4, outline=YEL + (int(255 * frame_pulse),), width=2)
            if flash > 0:
                fl = Image.new("RGBA", (tw_, th_), WHITE + (int(220 * flash),)); fl.putalpha(Image.eval(L.rounded_mask(fl.size, int(tile_w * 0.1)), lambda p: int(p * flash))); layer.alpha_composite(fl, (x, y))
            if shimmer is not None:
                sh = Image.new("RGBA", (tw_, th_), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); sx = int(-60 + shimmer * (tw_ + 120))
                sd.polygon([(sx, 0), (sx + 34, 0), (sx - 30, th_), (sx - 64, th_)], fill=(255, 236, 170, 200)); sd.polygon([(sx + 46, 0), (sx + 54, 0), (sx - 10, th_), (sx - 18, th_)], fill=(255, 255, 255, 140))
                sh.putalpha(Image.fromarray(np.minimum(np.array(L.rounded_mask(sh.size, int(tile_w * 0.1))), np.array(sh.split()[3])))); layer.alpha_composite(sh, (x, y))
            if ring is not None:
                rr = int(ring * 60); a = int(170 * (1 - ring) ** 1.5)
                L.aa_rounded_rect(layer, (x - rr, y - rr, x + tw_ + rr, y + th_ + rr), int(tile_w * 0.1) + rr, outline=ring_col + (a,), width=2)
            if ribbon:
                fr = font(int(tile_w * 0.13), "Bold"); tw = d.textlength(ribbon, font=fr); rx = x + 8; ry = y + 8
                L.aa_rounded_rect(layer, (rx, ry, rx + tw + 18, ry + int(tile_w * 0.2)), 7, fill=(GOLD if ribbon == "UPGRADED" else YEL) + (255,))
                d.text((rx + 9, ry + 3), ribbon, font=fr, fill=INK)
        if labels and (is_t or tile is not None):
            fl_ = font(int(tile_w * 0.14), "Bold" if is_t else "SemiBold")
            L.text_center(d, cx, cy + tile_h / 2 + 12, f"No. {num:04d}", fl_, WHITE + (255,) if is_t else (190, 194, 204, 255))
    # a soft dark scrim behind the row so type stays readable over a busy frame (no box)
    scrim = Image.new("RGBA", im.size, (0, 0, 0, 0)); sa = np.zeros((H, W), dtype=np.float32)
    top = int(y_center - tile_h / 2 - header_size * 2.1 - 70); bot = min(H, int(y_center + tile_h / 2 + 150))
    if bot > top:
        n_ = bot - top; up = min(90, n_ // 3); down = min(110, n_ // 3)
        ramp = np.concatenate([np.linspace(0, 1, up), np.ones(max(0, n_ - up - down)), np.linspace(1, 0, down)])
        sa[top:bot, :] = (ramp * scrim_a * alpha)[:, None]
    scrim.putalpha(Image.fromarray((sa * 255).astype(np.uint8)))
    im = Image.alpha_composite(im, scrim)
    # fade the row's ends into the frame
    m = np.ones((H, W), dtype=np.float32); fade = 150
    ramp = np.linspace(0, 1, fade, dtype=np.float32); m[:, :fade] *= ramp; m[:, W - fade:] *= ramp[::-1]
    a = np.array(layer.split()[3], dtype=np.float32) * m * alpha; layer.putalpha(Image.fromarray(a.astype(np.uint8)))
    return Image.alpha_composite(im, layer), [(x_start + i * (tile_w + gap) + tile_w / 2, y_center) for i in range(n)], tile_h

# ---------- type-only verdict ----------
def verdict_type(im, cx, y, kind, name=None, sub=None, alpha=1.0, big=True):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    col = {"caught": GREEN, "already": GREY, "upgraded": GOLD}[kind]
    word = {"caught": "CAUGHT", "already": "ALREADY CAUGHT", "upgraded": "UPGRADED"}[kind]
    a = int(255 * alpha)
    if big:
        f = font(96 if kind != "already" else 64, "Bold")
        tracked(d, (cx, y), word, f, col + (a,), tracking=6, stroke=7, sfill=(0, 0, 0, int(200 * alpha)), anchor="c")
        yy = y + f.size + 6
        if name:
            f2 = font(54, "Bold"); tracked(d, (cx, yy), name, f2, WHITE + (a,), tracking=2, stroke=6, sfill=(0, 0, 0, int(200 * alpha)), anchor="c"); yy += 64
        if sub:
            f3 = font(30, "SemiBold"); tracked(d, (cx, yy + 4), sub, f3, (240, 230, 200, a), tracking=3, stroke=4, sfill=(0, 0, 0, int(180 * alpha)), anchor="c")
    else:
        f = font(68 if kind != "already" else 50, "Bold")
        tracked(d, (cx, y), word, f, col + (a,), tracking=4, stroke=7, sfill=(0, 0, 0, int(210 * alpha)), anchor="c")
        if name:
            f2 = font(50, "Bold"); tracked(d, (cx, y + f.size + 4), name, f2, WHITE + (a,), tracking=1, stroke=6, sfill=(0, 0, 0, int(210 * alpha)), anchor="c")
    return Image.alpha_composite(im, layer)

def dex_total(im, cx, y, old, new, t, alpha=1.0, label="POKÉDEX"):
    """'POKÉDEX   134 / 1025' as one typographic line; the number rolls."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    fl = font(26, "SemiBold"); fn = font(64, "Bold"); fs = font(26, "SemiBold")
    wl = d.textlength(label, font=fl) + 3 * (len(label) - 1); wn = max(d.textlength(str(old), font=fn), d.textlength(str(new), font=fn)); ws = d.textlength("/ 1025", font=fs)
    total = wl + 26 + wn + 14 + ws; x = cx - total / 2; a = int(255 * alpha)
    tracked(d, (x, y + 30), label, fl, (215, 219, 228, a), tracking=3); x += wl + 26
    L.roll_number(d, x, y, str(old), str(new), t, fn, YEL + (a,)); x += wn + 14
    d.text((x, y + 32), "/ 1025", font=fs, fill=(190, 194, 204, a))
    return Image.alpha_composite(im, layer)

# =====================================================================
# Direction A: take-over
# =====================================================================
def A_caught(k="golisopod", frames=84):
    base = L.FRAMES[k]; box = L.SRC[k][1]; crop = L.card_crop(k); name, num, region = L.SRC[k][2], L.SRC[k][3], L.SRC[k][4]
    numbers = [num - 2, num - 1, num, num + 1, num + 2]; target = 2
    sx, sy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; sw = box[2] - box[0]
    out = []
    ROW_Y = 1390; TILE_W = 150; CARD_Y = 640; CARD_W = 470
    for f in range(frames):
        # phases: 0-10 dim + card to centre; 10-22 type in + row in; 22-40 card to slot, type out; 40-46 land; 46-70 hold; 70-84 fade all
        t_in = clamp(f / 10); t_type = clamp((f - 10) / 10); t_fly = clamp((f - 22) / 18); t_out = clamp((f - 70) / 14)
        dim = ease_out(t_in) * (1 - ease_out(t_out))
        im = dim_frame(base, dim, 10)
        row_a = ease_out(t_type) * (1 - ease_out(t_out))
        landed = f >= 40
        pulse = (0.6 + 0.4 * math.sin(f * 0.5)) if 22 <= f < 40 else 0.0
        flash = clamp(1 - (f - 40) / 6) if 40 <= f < 46 else 0.0
        bounce = 1 + 0.12 * math.sin(math.pi * clamp((f - 40) / 8)) if 40 <= f < 48 else 1.0
        ring = clamp((f - 40) / 14) if 40 <= f < 54 else None
        centers = None
        if row_a > 0:
            # header left: the Pokédex total (rolls on landing); header right: region count
            roll = clamp((f - 41) / 5)
            total_txt = "134" if roll >= 1 else ("133" if roll <= 0 else "134")
            im, centers, th = dex_row(im, ROW_Y + 40 * (1 - ease_out(t_type)), numbers, {}, target, TILE_W, alpha=row_a, target_tile=L.TILES[k] if landed else None,
                                      frame_pulse=pulse, flash=flash, bounce=bounce, ring=ring, ribbon="NEW" if f >= 43 else None,
                                      header=f"POKÉDEX  {total_txt} / 1025", header_right=f"{region.upper()}  {12 + (1 if landed else 0)} / 88")
        if not landed:
            if f < 22:
                e = ease_in_out(t_in); cx = sx + (W / 2 - sx) * e; cy = sy + (CARD_Y - sy) * e; w = sw + (CARD_W - sw) * e; rot = -4 * (1 - e)
            else:
                e = ease_in_out(t_fly); tx, ty = centers[target] if centers else (W / 2, ROW_Y)
                cx, cy = bezier(W / 2, CARD_Y, tx, ty, e, lift=100); w = CARD_W + (TILE_W - CARD_W) * e; rot = 0
            card_at(im, crop, cx, cy, w, rot=rot, radius_frac=0.045)
        ta = ease_out(t_type) * (1 - ease_out(clamp((f - 22) / 10)))
        if ta > 0:
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer); a = int(255 * ta)
            tracked(d, (W / 2, 250), f"No. {num:04d}   ·   {region.upper()}", font(34, "SemiBold"), (215, 219, 228, a), tracking=4, anchor="c")
            tracked(d, (W / 2, 1035), name.upper(), font(88, "Bold"), WHITE + (a,), tracking=4, anchor="c")
            tracked(d, (W / 2, 1140), "CAUGHT", font(42, "Bold"), GREEN + (a,), tracking=10, anchor="c")
            im = Image.alpha_composite(im, layer)
        out.append(im)
    return out

def A_upgraded(k="veluza", frames=96):
    base = L.FRAMES[k]; box = L.SRC[k][1]; crop = L.card_crop(k); name, num, region = L.SRC[k][2], L.SRC[k][3], L.SRC[k][4]
    numbers = [num - 2, num - 1, num, num + 1, num + 2]; target = 2
    old_tile = L.make_tile(crop, dim=True)
    sx, sy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; sw = box[2] - box[0]
    out = []; ROW_Y = 1390; TILE_W = 150; CARD_Y = 640; CARD_W = 470
    for f in range(frames):
        t_in = clamp(f / 10); t_type = clamp((f - 10) / 10); t_fly = clamp((f - 22) / 18); t_out = clamp((f - 82) / 14)
        dim = ease_out(t_in) * (1 - ease_out(t_out)); im = dim_frame(base, dim, 10)
        row_a = ease_out(t_type) * (1 - ease_out(t_out))
        arrived = f >= 40
        if 40 <= f < 46: flip = 1 - (f - 40) / 6; tile = old_tile
        elif 46 <= f < 52: flip = (f - 46) / 6; tile = L.TILES[k]
        else: flip = 1.0; tile = L.TILES[k] if f >= 52 else old_tile
        shimmer = clamp((f - 52) / 12) if 52 <= f < 64 else None
        bounce = 1 + 0.12 * math.sin(math.pi * clamp((f - 52) / 8)) if 52 <= f < 60 else 1.0
        ring = clamp((f - 52) / 14) if 52 <= f < 66 else None
        pulse = (0.6 + 0.4 * math.sin(f * 0.5)) if 22 <= f < 40 else 0.0
        centers = None
        if row_a > 0:
            ups = "18" if f >= 56 else "17"
            im, centers, th = dex_row(im, ROW_Y + 40 * (1 - ease_out(t_type)), numbers, {}, target, TILE_W, alpha=row_a, target_tile=tile, flip_x=flip,
                                      frame_pulse=pulse, shimmer=shimmer, bounce=bounce, ring=ring, ring_col=GOLD, ribbon="UPGRADED" if f >= 54 else None,
                                      header=f"POKÉDEX  134 / 1025", header_right=f"UPGRADES  {ups}")
        if not arrived:
            if f < 22:
                e = ease_in_out(t_in); cx = sx + (W / 2 - sx) * e; cy = sy + (CARD_Y - sy) * e; w = sw + (CARD_W - sw) * e; rot = -4 * (1 - e)
            else:
                e = ease_in_out(t_fly); tx, ty = centers[target] if centers else (W / 2, ROW_Y)
                cx, cy = bezier(W / 2, CARD_Y, tx, ty, e, lift=100); w = CARD_W + (TILE_W - CARD_W) * e; rot = 0
            card_at(im, crop, cx, cy, w, rot=rot)
        ta = ease_out(t_type) * (1 - ease_out(clamp((f - 22) / 10)))
        if ta > 0:
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer); a = int(255 * ta)
            tracked(d, (W / 2, 250), f"No. {num:04d}   ·   {region.upper()}", font(34, "SemiBold"), (215, 219, 228, a), tracking=4, anchor="c")
            tracked(d, (W / 2, 1035), f"{name.upper()} EX", font(88, "Bold"), WHITE + (a,), tracking=4, anchor="c")
            tracked(d, (W / 2, 1140), "UPGRADED  ·  DOUBLE RARE", font(38, "Bold"), GOLD + (a,), tracking=8, anchor="c")
            im = Image.alpha_composite(im, layer)
        out.append(im)
    return out

def A_already(k="technoradar", frames=40):
    """No take-over for a dud: type only, a quick desaturation pulse on the footage."""
    base = L.FRAMES[k]; box = L.SRC[k][1]; name = L.SRC[k][2]
    out = []
    for f in range(frames):
        pulse = math.sin(math.pi * clamp(f / 14)) if f < 14 else 0.0
        im = base.copy()
        if pulse > 0:
            g = ImageEnhance.Color(im).enhance(1 - 0.6 * pulse); im = Image.blend(im, g, 1.0)
        a = clamp(f / 5)
        im = verdict_type(im, W / 2, box[3] - 150 + 24 * (1 - a), "already", alpha=a, big=False)
        out.append(im)
    return out

# =====================================================================
# Direction B: inline, type-only verdict, row at the bottom, footage untouched
# =====================================================================
def B_caught(k="golisopod", frames=76):
    base = L.FRAMES[k]; box = L.SRC[k][1]; crop = L.card_crop(k); name, num, region = L.SRC[k][2], L.SRC[k][3], L.SRC[k][4]
    numbers = [num - 2, num - 1, num, num + 1, num + 2]; target = 2
    ROW_Y = 1400; TILE_W = 162
    out = []
    for f in range(frames):
        im = base.copy()
        a = clamp(f / 5)
        row_a = ease_out(clamp((f - 4) / 8)) * (1 - ease_out(clamp((f - 64) / 10)))
        landed = f >= 32
        pulse = (0.6 + 0.4 * math.sin(f * 0.5)) if 12 <= f < 32 else 0.0
        flash = clamp(1 - (f - 32) / 6) if 32 <= f < 38 else 0.0
        bounce = 1 + 0.14 * math.sin(math.pi * clamp((f - 32) / 8)) if 32 <= f < 40 else 1.0
        ring = clamp((f - 32) / 14) if 32 <= f < 46 else None
        centers = None
        if row_a > 0:
            im, centers, th = dex_row(im, ROW_Y + 30 * (1 - row_a), numbers, {}, target, TILE_W, alpha=row_a, target_tile=L.TILES[k] if landed else None,
                                      frame_pulse=pulse, flash=flash, bounce=bounce, ring=ring, ribbon="NEW" if f >= 35 else None, header=f"POKÉDEX  {133 + (1 if f >= 36 else 0)} / 1025", header_right=f"{region.upper()}  {12 + (1 if landed else 0)} / 88", header_size=34, scrim_a=0.74)
        if 12 <= f < 32 and centers:
            im = L.flying_card(im, crop, box, centers[target], (f - 12) / 20)
        im = verdict_type(im, W / 2, box[3] - 345 + 26 * (1 - a), "caught", name.upper(), f"No. {num:04d}  ·  {region.upper()}", alpha=a * (1 - ease_out(clamp((f - 64) / 10))), big=False)
        out.append(im)
    return out

def B_upgraded(k="veluza", frames=88):
    base = L.FRAMES[k]; box = L.SRC[k][1]; crop = L.card_crop(k); name, num, region = L.SRC[k][2], L.SRC[k][3], L.SRC[k][4]
    numbers = [num - 2, num - 1, num, num + 1, num + 2]; target = 2
    old_tile = L.make_tile(crop, dim=True); ROW_Y = 1400; TILE_W = 162
    out = []
    for f in range(frames):
        im = base.copy(); a = clamp(f / 5)
        row_a = ease_out(clamp((f - 4) / 8)) * (1 - ease_out(clamp((f - 76) / 10)))
        if 32 <= f < 38: flip = 1 - (f - 32) / 6; tile = old_tile
        elif 38 <= f < 44: flip = (f - 38) / 6; tile = L.TILES[k]
        else: flip = 1.0; tile = L.TILES[k] if f >= 44 else old_tile
        shimmer = clamp((f - 44) / 12) if 44 <= f < 56 else None
        bounce = 1 + 0.12 * math.sin(math.pi * clamp((f - 44) / 8)) if 44 <= f < 52 else 1.0
        ring = clamp((f - 44) / 14) if 44 <= f < 58 else None
        pulse = (0.6 + 0.4 * math.sin(f * 0.5)) if 12 <= f < 32 else 0.0
        centers = None
        if row_a > 0:
            im, centers, th = dex_row(im, ROW_Y + 30 * (1 - row_a), numbers, {}, target, TILE_W, alpha=row_a, target_tile=tile, flip_x=flip, frame_pulse=pulse,
                                      shimmer=shimmer, bounce=bounce, ring=ring, ring_col=GOLD, ribbon="UPGRADED" if f >= 46 else None, header="POKÉDEX  134 / 1025", header_right=f"UPGRADES  {18 if f >= 48 else 17}", header_size=34, scrim_a=0.74)
        if 12 <= f < 32 and centers:
            im = L.flying_card(im, crop, box, centers[target], (f - 12) / 20)
        im = verdict_type(im, W / 2, box[3] - 345 + 26 * (1 - a), "upgraded", f"{name.upper()} EX", "DOUBLE RARE REPLACES COMMON", alpha=a * (1 - ease_out(clamp((f - 76) / 10))), big=False)
        out.append(im)
    return out

def B_already(k="technoradar", frames=40):
    base = L.FRAMES[k]; box = L.SRC[k][1]
    out = []
    for f in range(frames):
        im = base.copy(); a = clamp(f / 5)
        im = verdict_type(im, W / 2, box[3] - 150 + 24 * (1 - a), "already", alpha=a, big=False)
        out.append(im)
    return out

# ---------- output ----------
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

def concat(names, outname):
    lst = os.path.join(TMP, f"{outname}.txt")
    with open(lst, "w") as fh_: fh_.write("".join(f"file '{OUT}/{n}.mp4'\n" for n in names))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{OUT}/{outname}.mp4"], check=True)

if __name__ == "__main__":
    which = sys.argv[1:] or ["A", "B"]
    if "A" in which:
        ac = A_caught(); write_video(ac, "A_caught")
        sheet([8, 18, 30, 44], ac, ["0.25 s  footage dims, card lifts to centre", "0.6 s  number above, name + CAUGHT below, row appears", "1.0 s  card drops into its slot", "1.45 s  NEW, POKÉDEX 133 -> 134, then all fades back"], "A_storyboard_caught.jpg", "A  ·  TAKE-OVER  ·  Caught")
        au = A_upgraded(); write_video(au, "A_upgraded")
        sheet([8, 18, 42, 58], au, ["0.25 s  card lifts to centre", "0.6 s  UPGRADED · DOUBLE RARE", "1.4 s  old tile flips out", "1.9 s  new tile, gold sweep, UPGRADES 17 -> 18"], "A_storyboard_upgraded.jpg", "A  ·  TAKE-OVER  ·  Upgraded")
        aa = A_already(); write_video(aa, "A_already")
        sheet([3, 8, 20], aa, ["0.1 s  type only, colour drains for a beat", "0.25 s  ...and comes back", "0.7 s  nothing else; next card"], "A_storyboard_already.jpg", "A  ·  Already caught (no take-over for a dud)")
        concat(["A_caught", "A_upgraded", "A_already"], "A_preview"); print("A ok")
    if "B" in which:
        bc = B_caught(); write_video(bc, "B_caught")
        sheet([5, 14, 26, 40], bc, ["0.15 s  CAUGHT in type, no pill", "0.45 s  row fades in at the bottom, slot pulses", "0.85 s  card flies in", "1.3 s  NEW, 12 -> 13; row fades after"], "B_storyboard_caught.jpg", "B  ·  INLINE  ·  Caught")
        bu = B_upgraded(); write_video(bu, "B_upgraded")
        sheet([5, 26, 36, 50], bu, ["0.15 s  UPGRADED in type", "0.85 s  flies to the slot holding Veluza", "1.2 s  old tile flips out", "1.65 s  new tile, gold sweep"], "B_storyboard_upgraded.jpg", "B  ·  INLINE  ·  Upgraded")
        ba = B_already(); write_video(ba, "B_already")
        sheet([3, 12, 30], ba, ["0.1 s  ALREADY CAUGHT, grey type", "0.4 s  holds", "1.0 s  next card"], "B_storyboard_already.jpg", "B  ·  INLINE  ·  Already caught")
        concat(["B_caught", "B_upgraded", "B_already"], "B_preview"); print("B ok")
    # side-by-side comparison at the landing moment
    try:
        a = Image.open(os.path.join(TMP, "frames_A_caught", "0044.jpg")); b = Image.open(os.path.join(TMP, "frames_B_caught", "0040.jpg"))
        s = Image.new("RGB", (2 * 540 + 48, 960 + 130), (24, 26, 32)); d = ImageDraw.Draw(s)
        d.text((16, 14), "Caught, landing moment:  A take-over (left)  vs  B inline (right)", font=font(30, "Bold"), fill=WHITE)
        s.paste(a.resize((540, 960), Image.LANCZOS), (16, 70)); s.paste(b.resize((540, 960), Image.LANCZOS), (572, 70))
        s.save(os.path.join(OUT, "compare_A_vs_B.jpg"), quality=90); print("compare ok")
    except Exception as e: print("compare skipped", e)
