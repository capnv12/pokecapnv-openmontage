"""Four clean hook options, four frames each, minimal graphics. Frames from the Draw #7 render."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = sys.argv[1]
F = D + "/frames/"
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
W, H = 1080, 1920
YEL = (255, 203, 5)


def font(sz):
    return ImageFont.truetype(FONT, sz)


def caption(d, words, active, y=560, sz=72):
    f = font(sz)
    widths = [d.textlength(w, font=f) for w in words]
    gap = 22
    total = sum(widths) + gap * (len(words) - 1)
    x = (W - total) / 2
    for w, wd in zip(words, widths):
        col = YEL if w == active else (255, 255, 255)
        d.text((x, y), w, font=f, fill=col, stroke_width=9, stroke_fill=(0, 0, 0), anchor="lm")
        x += wd + gap


def chip(d, x, y, s, bg=(20, 24, 40), fg=(255, 255, 255), sz=38, pad=22, h=72):
    f = font(sz)
    w = d.textlength(s, font=f) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + pad, y + h / 2), s, font=f, fill=fg, anchor="lm")
    return x + w


def header(d, ball=None):
    x = chip(d, 40, 165, "Draw #8") + 16
    for i in range(2):
        cx = x + 40 + i * 92
        if i == 0 and ball:
            d.ellipse([cx - 36, 165, cx + 36, 237], fill=(255, 140, 0), outline=(0, 0, 0), width=4)
            d.text((cx, 201), str(ball), font=font(34), fill=(0, 0, 0), anchor="mm")
        else:
            d.ellipse([cx - 36, 165, cx + 36, 237], fill=(60, 60, 70), outline=(0, 0, 0), width=4)


def panel(src, t, words, active, ball=None, note="", slowmo=False):
    img = Image.open(F + src).convert("RGBA").resize((W, H))
    band = img.crop((0, 140, W, 430)).filter(ImageFilter.GaussianBlur(40))
    img.paste(band, (0, 140))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 140, W, 430], fill=(0, 0, 0, 120))
    header(d, ball)
    if words:
        caption(d, words, active)
    if slowmo:
        chip(d, W - 300, 1480, "0.5x slow-mo", bg=(0, 0, 0), sz=32)
    d.rectangle([0, H - 220, W, H], fill=(0, 0, 0, 215))
    d.text((W / 2, H - 165), t, font=font(50), fill=YEL, anchor="mm")
    d.text((W / 2, H - 85), note, font=font(38), fill=(255, 255, 255), anchor="mm")
    return img


L = ["Drum", "picked", "twenty."]
R = ["Twenty", "had", "a", "Special", "Illustration", "Rare."]

rows = [
    ("1. PACK IN HAND", "Tear at frame one. Voice names the result. Cut to the drum.", [
        panel("f_31.0.jpg", "0.0s", L[:2], "Drum", note="pack 20 in hand, foil starting"),
        panel("f_32.0.jpg", "0.8s", L, "twenty.", ball=20, note="tearing, ball 20 docks"),
        panel("f_32.0.jpg", "2.4s", R[3:], "Rare.", ball=20, note="still tearing, card not shown"),
        panel("f_29.4.jpg", "2.7s", ["But", "first,", "forty."], "forty.", ball=20, note="cut to the real drum, ball A"),
    ]),
    ("2. DRUM FIRST", "Real drum at frame one, then the pack. Cut back to the drum.", [
        panel("f_29.4.jpg", "0.0s", L, "Drum", note="ball 20 drops out of the drum"),
        panel("f_31.0.jpg", "1.0s", R[:3], "a", ball=20, note="cut to pack 20 in hand"),
        panel("f_32.0.jpg", "2.4s", R[3:], "Rare.", ball=20, note="tearing, card not shown"),
        panel("f_28.6.jpg", "2.7s", ["But", "first,", "forty."], "forty.", ball=20, note="cut to the drum, ball A"),
    ]),
    ("3. PACK, THEN CARD", "Tear, then the card in slow-mo. Our #1/#2/#6 hooks, with the pack in front.", [
        panel("f_31.0.jpg", "0.0s", L, "Drum", note="pack 20 in hand"),
        panel("f_32.0.jpg", "1.0s", ["This", "came"], "came", ball=20, note="tearing"),
        panel("f_42.6.jpg", "1.6s", ["This", "came", "out", "of", "it."], "it.", ball=20, note="the hit landing, slow-mo", slowmo=True),
        panel("f_29.4.jpg", "2.7s", ["But", "first,", "forty."], "forty.", ball=20, note="cut to the drum, ball A"),
    ]),
    ("4. TWO TEARS", "Pack A tear, then pack B tear. The two-pack format on screen.", [
        panel("f_9.5.jpg", "0.0s", ["Two", "packs."], "Two", note="pack 40 in hand"),
        panel("f_11.5.jpg", "0.9s", ["The", "second", "one"], "second", note="pack 40 tearing"),
        panel("f_32.0.jpg", "1.5s", ["had", "a", "Special", "Illustration", "Rare."], "Rare.", ball=20, note="cut to pack 20 tearing"),
        panel("f_29.4.jpg", "2.7s", ["But", "first,", "forty."], "forty.", ball=20, note="cut to the drum, ball A"),
    ]),
]

pw, ph = 360, 640
gap = 16
label_w = 420
sheet = Image.new("RGB", (label_w + 4 * (pw + gap) + gap, len(rows) * (ph + gap) + gap), (18, 18, 22))
sd = ImageDraw.Draw(sheet)
for r, (title, sub, panels) in enumerate(rows):
    y = gap + r * (ph + gap)
    sd.text((24, y + 40), title, font=font(38), fill=YEL)
    # wrap subtitle
    words, line, lines = sub.split(), "", []
    for w in words:
        if sd.textlength(line + " " + w, font=font(28)) > label_w - 48:
            lines.append(line.strip()); line = w
        else:
            line += " " + w
    lines.append(line.strip())
    for i, ln in enumerate(lines):
        sd.text((24, y + 120 + i * 38), ln, font=font(28), fill=(230, 230, 230))
    for c, p in enumerate(panels):
        sheet.paste(p.convert("RGB").resize((pw, ph)), (label_w + gap + c * (pw + gap), y))
out = D + "/options-storyboard.png"
sheet.save(out)
print("wrote", out, sheet.size)
