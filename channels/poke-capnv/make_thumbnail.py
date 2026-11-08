"""Thumbnails/covers from a real footage frame (no AI imagery): bold headline + neon highlight circle.
Usage: python scripts/make_thumbnail.py <frame.png> <out.png> "<HEADLINE>" <circle_x> <circle_y> [radius] [subline] [crop "x0,y0,x1,y1"]
Coordinates are in the SOURCE frame's pixels. Output 1080x1920 (TikTok cover / Shorts thumbnail)."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out, head, cx, cy = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
r = float(sys.argv[6]) if len(sys.argv) > 6 else 170
sub = (sys.argv[7] or None) if len(sys.argv) > 7 else None
crop = [float(v) for v in sys.argv[8].split(",")] if len(sys.argv) > 8 else None
W, H = 1080, 1920
im = Image.open(src).convert("RGB")
if crop:  # zoom: crop a region of the source first (coordinates stay in source pixels)
    im = im.crop(tuple(round(v) for v in crop)); cx -= crop[0]; cy -= crop[1]
s = max(W / im.width, H / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
ox, oy = (im.width - W) // 2, (im.height - H) // 2
im = im.crop((ox, oy, ox + W, oy + H))
cx, cy, r = cx * s - ox, cy * s - oy, r * s
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
NEON = (222, 255, 40)
# neon circle: blurred glow layers + crisp ring
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
for wdt, a in [(48, 90), (30, 140)]:
    g.ellipse((cx - r, cy - r, cx + r, cy + r), outline=NEON + (a,), width=wdt)
glow = glow.filter(ImageFilter.GaussianBlur(14))
ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((cx - r, cy - r, cx + r, cy + r), outline=NEON + (255,), width=12)
im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), glow), ring)
d = ImageDraw.Draw(im)
def text(t, y, size, fill=(255, 255, 255)):
    f = ImageFont.truetype(FONT, size)
    while d.textlength(t, font=f) > W - 120: size -= 4; f = ImageFont.truetype(FONT, size)
    x = (W - d.textlength(t, font=f)) / 2
    d.text((x + 6, y + 8), t, font=f, fill=(0, 0, 0, 150))                     # drop shadow
    d.text((x, y), t, font=f, fill=fill, stroke_width=max(6, size // 11), stroke_fill=(0, 0, 0))
text(head, 210, 118)
if sub: text(sub, 345, 64, fill=(255, 203, 5))
im.convert("RGB").save(out, quality=95)
print("wrote", out)
