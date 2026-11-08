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
    gap = 22
    while True:
        f = font(sz)
        widths = [d.textlength(w, font=f) for w in words]
        total = sum(widths) + gap * (len(words) - 1)
        if total <= W - 80 or sz <= 40:
            break
        sz -= 4
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



def wall_panel(t, words, active, note):
    """Mock of a 4K crop on the wall of numbered packs (top of the frame)."""
    img = Image.open(F + "f_9.5.jpg").convert("RGBA").resize((W, H))
    region = img.crop((250, 0, 830, 1030)).resize((W, H))
    band = region.crop((0, 140, W, 470)).filter(ImageFilter.GaussianBlur(40))
    region.paste(band, (0, 140))
    d = ImageDraw.Draw(region, "RGBA")
    d.rectangle([0, 140, W, 470], fill=(0, 0, 0, 120))
    header(d)
    caption(d, words, active)
    chip(d, W - 360, 1480, "4K crop of the wall", bg=(0, 0, 0), sz=32)
    d.rectangle([0, H - 220, W, H], fill=(0, 0, 0, 215))
    d.text((W / 2, H - 165), t, font=font(50), fill=YEL, anchor="mm")
    d.text((W / 2, H - 85), note, font=font(38), fill=(255, 255, 255), anchor="mm")
    return region

rows = [
    ("1. THE WALL", "Stakes shown: a wall of numbered packs, and the drum picks one. Nobody else has this frame.", [
        wall_panel("0.0s", ["Fifty", "packs."], "Fifty", "wide on the wall of numbered packs"),
        panel("f_29.4.jpg", "1.0s", ["The", "drum", "picked", "twenty."], "twenty.", ball=20, note="cut to the drum, ball 20 drops"),
        panel("f_32.0.jpg", "2.0s", ["Twenty", "had", "a", "Special", "Illustration", "Rare."], "Rare.", ball=20, note="pack 20 tearing, card not shown"),
        panel("f_28.6.jpg", "2.9s", ["But", "first,", "forty."], "forty.", ball=20, note="cut to the drum, ball A"),
    ]),
    ("2. THE RECORD", "Superlative claim, the #1 hook type in the research (most expensive, most iconic, rarest). Ours is true from our own tables, no price.", [
        panel("f_42.6.jpg", "0.0s", ["The", "rarest", "card"], "rarest", note="hit landing, slow-mo (our proven shot)", slowmo=True),
        panel("f_44.0.jpg", "1.0s", ["this", "drum", "has", "picked"], "picked", note="card settles, push-in", slowmo=True),
        panel("f_44.0.jpg", "2.0s", ["in", "twenty-eight", "packs."], "packs.", note="no tag, no name"),
        panel("f_29.4.jpg", "2.7s", ["Ball", "twenty."], "twenty.", ball=20, note="cut to the drum: this pack's ball"),
    ]),
    ("3. THE STREAK", "Story hook, PokeRev type (22.6M): narration over the moment. Only a serial channel can tell it.", [
        panel("d4_20.4.jpg", "0.0s", ["Eleven", "packs,"], "Eleven", note="previous dud rare slots, 0.3s each"),
        panel("d4_77.3.jpg", "0.6s", ["no", "hit."], "hit.", note="...flashing past"),
        panel("f_29.4.jpg", "1.3s", ["Then", "the", "drum", "picked", "twenty."], "twenty.", ball=20, note="cut to the drum, ball 20 drops"),
        panel("f_28.6.jpg", "2.7s", ["But", "first,", "forty."], "forty.", ball=20, note="cut to ball A (or straight to pack 20)"),
    ]),
    ("4. THE CHASE", "Conditional stakes, Purplecliffe type (15M, 'If I pulled Zekrom...'). The set's chase card is the target, the pack beat it.", [
        panel("f_9.5.jpg", "0.0s", ["Destined", "Rivals,"], "Destined", note="pack 40 in hand, set readable"),
        panel("f_9.5.jpg", "0.8s", ["the", "Mewtwo", "set."], "Mewtwo", note="hold on the pack"),
        panel("f_11.5.jpg", "1.6s", ["Forty", "had", "a", "Special", "Illustration", "Rare."], "Rare.", ball=40, note="tearing, card not shown"),
        panel("f_29.4.jpg", "2.7s", ["But", "first,", "twenty."], "twenty.", ball=40, note="cut to the drum, ball A"),
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
out = D + "/options2-storyboard.png"
sheet.save(out)
print("wrote", out, sheet.size)
