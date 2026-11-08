"""Storyboard mockup for the 'rarity ladder' hook (Draw #8 plan). Frames from the Draw #7 render."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = sys.argv[1]  # hook-mockup dir
F = D + "/frames/"
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FONT2 = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1080, 1920
YEL = (255, 203, 5)
GOLD = (255, 215, 80)

STEPS = ["SIR", "IR", "EX", "POKÉ BALL", "HOLO"]  # top to bottom
STEP_COL = {"SIR": (255, 200, 40), "IR": (120, 200, 255), "EX": (200, 120, 255),
            "POKÉ BALL": (255, 110, 110), "HOLO": (190, 190, 190)}


def font(sz, bold=False):
    return ImageFont.truetype(FONT2 if bold else FONT, sz)


def text_stroked(d, xy, s, sz, fill=(255, 255, 255), stroke=10, anchor="mm", bold=False):
    d.text(xy, s, font=font(sz, bold), fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0), anchor=anchor)


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


def header(d, ball=None, rarity=None):
    # cover the old chip row
    d.rectangle([0, 150, W, 250], fill=None)
    x = chip(d, 40, 165, "Draw #8")
    x += 16
    # two ball slots
    for i in range(2):
        cx = x + 40 + i * 92
        if i == 0 and ball:
            d.ellipse([cx - 36, 165, cx + 36, 237], fill=(255, 140, 0), outline=(0, 0, 0), width=4)
            d.text((cx, 201), str(ball), font=font(34), fill=(0, 0, 0), anchor="mm")
        else:
            d.ellipse([cx - 36, 165, cx + 36, 237], fill=(60, 60, 70), outline=(0, 0, 0), width=4)
    if rarity:
        chip(d, x + 220, 165, rarity, bg=(255, 200, 40), fg=(0, 0, 0))


def ladder(img, lit_upto=None, lock=False, climbing=False):
    """lit_upto: index into STEPS from the bottom (0=HOLO ... 4=SIR); None = all dim."""
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0 = 760, 700
    bw, bh, gap = 150, 92, 14
    n = len(STEPS)
    for i, name in enumerate(STEPS):  # i=0 is top (SIR)
        level = n - 1 - i  # 0=HOLO bottom .. 4=SIR top
        y = y0 + i * (bh + gap)
        on = lit_upto is not None and level <= lit_upto
        if lock:
            on = level == n - 1
        col = STEP_COL[name]
        if on:
            fill = col + (240,)
            d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=18, fill=fill, outline=(0, 0, 0, 255), width=4)
            d.text((x0 + bw / 2, y + bh / 2), name, font=font(30 if len(name) > 3 else 40), fill=(0, 0, 0), anchor="mm")
        else:
            d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=18, fill=(15, 15, 25, 150), outline=(255, 255, 255, 60), width=3)
            d.text((x0 + bw / 2, y + bh / 2), name, font=font(28 if len(name) > 3 else 36), fill=(255, 255, 255, 110), anchor="mm")
    if lock:
        # gold glow around the SIR step
        glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        g.rounded_rectangle([x0 - 24, y0 - 24, x0 + bw + 24, y0 + bh + 24], radius=30, fill=GOLD + (200,))
        glow = glow.filter(ImageFilter.GaussianBlur(28))
        img.alpha_composite(glow)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=18, fill=STEP_COL["SIR"] + (255,), outline=(0, 0, 0, 255), width=5)
        d.text((x0 + bw / 2, y0 + bh / 2), "SIR", font=font(44), fill=(0, 0, 0), anchor="mm")


def panel(src, title, words, active, ball=None, rarity=None, lit=None, lock=False, note="", covers=()):
    img = Image.open(F + src).convert("RGBA").resize((W, H))
    # cover old captions/chips with a soft darken band at top
    d = ImageDraw.Draw(img, "RGBA")
    # cover Draw #7's burned-in chip row and caption line
    band = img.crop((0, 140, W, 430)).filter(ImageFilter.GaussianBlur(40))
    img.paste(band, (0, 140))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 140, W, 430], fill=(0, 0, 0, 120))
    for r in covers:
        c = img.crop(r).filter(ImageFilter.GaussianBlur(30))
        img.paste(c, (r[0], r[1]))
    d = ImageDraw.Draw(img, "RGBA")
    header(d, ball, rarity)
    if words:
        caption(d, words, active)
    ladder(img, lit, lock)
    d = ImageDraw.Draw(img, "RGBA")
    # bottom title band
    d.rectangle([0, H - 300, W, H], fill=(0, 0, 0, 215))
    d.text((W / 2, H - 230), title, font=font(54), fill=YEL, anchor="mm")
    y = H - 160
    for line in note.split("\n"):
        d.text((W / 2, y), line, font=font(38), fill=(255, 255, 255), anchor="mm")
        y += 50
    return img


panels = [
    panel("f_31.0.jpg", "0.0s", ["Drum", "picked"], "Drum", note="Frame one: pack 20 in hand.\nVoice starts. Ladder on the right, all dark."),
    panel("f_32.0.jpg", "0.8s", ["Drum", "picked", "twenty."], "twenty.", ball=20, note="Ball 20 docks top-left on the word.\nFoil tearing."),
    panel("f_32.0.jpg", "1.6s", ["Twenty", "had", "a"], "a", ball=20, lit=2, note="Ladder climbs: HOLO, POKÉ BALL, EX...\ntick-tick-tick with the riser."),
    panel("f_32.0.jpg", "2.4s", ["Special", "Illustration", "Rare."], "Rare.", ball=20, rarity="SIR", lit=4, lock=True, note="Locks on SIR, gold flash.\nThe card is NOT shown."),
    panel("f_29.0.jpg", "2.7s", ["But", "first,", "forty."], "forty.", ball=20, note="Cut to the real drum, ball A.\nLadder gone. Beat 2 starts."),
    panel("f_42.6.jpg", "42s  reveal", ["No", "way."], "way.", ball=20, lit=3, note="Same ladder climbs again\nas card ten lands..."),
    panel("f_44.0.jpg", "43s  payoff", ["Palafin", "EX!"], "EX!", ball=20, rarity="SIR", lit=4, lock=True, note="...and locks on SIR with the card.\nThe hook's promise, paid."),
]

sw, sh = 450, 800
sheet = Image.new("RGB", (sw * len(panels) + 20 * (len(panels) + 1), sh + 40), (18, 18, 22))
for i, p in enumerate(panels):
    sheet.paste(p.convert("RGB").resize((sw, sh)), (20 + i * (sw + 20), 20))
sheet.save(D + "/ladder-storyboard.png")
print("wrote", D + "/ladder-storyboard.png", sheet.size)
