"""Render assets/og.png (1200x630) for Meringo Listen, in the house style.

The title page as a card: the velvet plate, flat with hard edges; the gold
thread along the top; the H1 in Cormorant; the app's own question as the
epigraph, beside a 2 px gold rule; Inter for the small lines. No glow, no
shadow, no frame. Run from the repo root:

    python tools/og/make_og.py

Needs Pillow, fontTools and brotli. Pillow can't read woff2, so the site's
own fonts are converted to TTF in a temporary folder first.
"""
import os
import tempfile

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "assets", "og.png")

W, H = 1200, 630
PLATE = (0x2D, 0x1C, 0x47)    # VelvetElevated, the plate
IVORY = (0xF4, 0xE8, 0xD0)    # Parchment
IVORY_2 = (0xB8, 0xA8, 0x8A)  # ParchmentDim
GOLD = (0xED, 0xA0, 0x40)     # CandlelightGold

TMP = tempfile.mkdtemp(prefix="og-fonts-")


def font(woff2, size, weight):
    ttf = os.path.join(TMP, os.path.basename(woff2).replace(".woff2", ".ttf"))
    if not os.path.exists(ttf):
        f = TTFont(os.path.join(FONTS, woff2))
        f.flavor = None
        f.save(ttf)
    face = ImageFont.truetype(ttf, size)
    face.set_variation_by_axes([weight])
    return face


f_word = font("cormorant-normal-latin.woff2", 40, 500)
f_desc = font("inter-latin.woff2", 22, 400)
f_h1 = font("cormorant-normal-latin.woff2", 92, 500)
f_quote = font("cormorant-italic-latin.woff2", 34, 500)
f_small = font("inter-latin.woff2", 24, 400)

img = Image.new("RGB", (W, H), PLATE)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 5], fill=GOLD)                       # the thread

x = 80
d.text((x, 52), "Meringo Listen", font=f_word, fill=IVORY)
d.text((x, 102), "an audiobook player for Android", font=f_desc, fill=IVORY_2)

d.text((x, 168), "Your books.", font=f_h1, fill=IVORY)
d.text((x, 264), "Exactly as narrated.", font=f_h1, fill=IVORY)

qx, qy, lh = 560, 410, 46
lines = ["“Last time you listened to Eleanor Voss.", "You used the Late Night preset. Restore it", "for this book?”"]
d.rectangle([qx, qy + 6, qx + 1, qy + 2 * lh + 40], fill=GOLD)  # the 2 px rule beside said words
for i, line in enumerate(lines):
    d.text((qx + (18 if i == 0 else 30), qy + i * lh), line, font=f_quote, fill=IVORY)  # the opening quote hangs

d.text((x, 540), "meringolisten.app", font=f_small, fill=IVORY)
d.text((x, 574), "$14.99 once, after a 14-day free trial", font=f_small, fill=IVORY_2)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
