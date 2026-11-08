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


def macro_panel(t, words, active, zoom, note):
    """Zoom-out from the SIR texture: crop the centre of the held card by factor zoom."""
    img = Image.open(F + "f_43.3.jpg").convert("RGBA").resize((W, H))
    cx, cy = 560, 1000
    hw, hh = int(W / 2 / zoom), int(H / 2 / zoom)
    region = img.crop((cx - hw, cy - hh, cx + hw, cy + hh)).resize((W, H))
    d = ImageDraw.Draw(region, "RGBA")
    header(d)
    caption(d, words, active)
    chip(d, W - 300, 1480, f"{zoom:.1f}x zoom", bg=(0, 0, 0), sz=32)
    d.rectangle([0, H - 220, W, H], fill=(0, 0, 0, 215))
    d.text((W / 2, H - 165), t, font=font(50), fill=YEL, anchor="mm")
    d.text((W / 2, H - 85), note, font=font(38), fill=(255, 255, 255), anchor="mm")
    return region

rows = [
    ("1. THE SLIDE", "The real reveal at 0.5x: card nine slides off and the hit appears. Starts hidden, ends shown, inside 2.8s. No cut-off.", [
        panel("f_41.6.jpg", "0.0s", ["Pack", "twenty,"], "Pack", note="card nine on top, 0.5x", slowmo=True),
        panel("f_42.3.jpg", "0.9s", ["card", "ten."], "ten.", note="it starts to slide", slowmo=True),
        panel("f_42.6.jpg", "1.6s", ["Special", "Illustration"], "Illustration", note="the hit coming through", slowmo=True),
        panel("f_43.3.jpg", "2.4s", ["Rare."], "Rare.", note="revealed, push-in, cut to drum at 2.8", slowmo=True),
    ]),
    ("2. THE TEXTURE", "Macro on the SIR art, zooming out to the card. On screen from frame one but unreadable until 2s.", [
        macro_panel("0.0s", ["The", "drum"], "drum", 4.0, "etched texture, not readable"),
        macro_panel("0.8s", ["picked", "twenty."], "twenty.", 2.6, "art emerging"),
        macro_panel("1.6s", ["Twenty", "had"], "had", 1.6, "the card appears"),
        panel("f_43.3.jpg", "2.4s", ["this."], "this.", note="full card, cut to drum at 2.8"),
    ]),
    ("3. THE GASP", "Reaction first: the first sound is the gasp, not a sentence. Temukau (15.9M) opens on 'No no no no', RealBreakingNate on 'No way'.", [
        panel("f_42.6.jpg", "0.0s", ["No", "way."], "No", note="[gasps] over the blur of the reveal", slowmo=True),
        panel("f_42.9.jpg", "0.7s", ["No", "way."], "way.", note="card landing", slowmo=True),
        panel("f_43.3.jpg", "1.2s", ["Pack", "twenty."], "twenty.", note="held, push-in"),
        panel("f_43.3.jpg", "2.0s", ["Special", "Illustration", "Rare."], "Rare.", note="cut to the drum at 2.8"),
    ]),
    ("4. THE TRAILER", "The whole short in 2s: five shots, then the card. Promise named over it.", [
        panel("f_29.4.jpg", "0.0s", ["Two", "packs."], "Two", note="drum, 0.4s"),
        panel("f_32.0.jpg", "0.4s", ["Two", "packs."], "packs.", note="tear, 0.4s"),
        panel("f_42.6.jpg", "1.2s", ["One", "Special"], "Special", note="cards blur, reveal, 0.4s each"),
        panel("f_43.3.jpg", "2.0s", ["Illustration", "Rare."], "Rare.", note="the card, hold to 2.8, cut to drum"),
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
out = D + "/options3-storyboard.png"
sheet.save(out)
print("wrote", out, sheet.size)
