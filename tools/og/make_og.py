"""Render assets/og.png (1200x630) for Meringo Listen.

Deep Velvet card: chapter-tick logo + wordmark + tagline on the left,
the Now Listening screenshot framed on the right. Run from the repo root:

    python tools/og/make_og.py

Requires Pillow and the Windows core fonts (Georgia / Segoe UI).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREENS = os.path.join(ROOT, "assets", "screens")
OUT = os.path.join(ROOT, "assets", "og.png")
FONTS = r"C:\Windows\Fonts"

W, H = 1200, 630
VELVET   = (26, 14, 46)
SURFACE  = (38, 24, 64)
PARCH    = (244, 232, 208)
PARCH_DIM= (184, 168, 138)
GOLD     = (232, 181, 96)
GOLD_HI  = (244, 208, 128)
VIOLET   = (155, 127, 212)

def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS, name), size)
    except OSError:
        return ImageFont.load_default()

f_word   = font("georgiab.ttf", 78)
f_tag    = font("georgiai.ttf", 40)
f_sub    = font("segoeui.ttf", 27)
f_url    = font("segoeui.ttf", 23)

img = Image.new("RGB", (W, H), VELVET)

# --- soft glows ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([720, 60, 1240, 580], fill=(232, 181, 96, 60))      # gold behind device
gd.ellipse([-160, -160, 360, 360], fill=(155, 127, 212, 55))   # violet top-left
glow = glow.filter(ImageFilter.GaussianBlur(130))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img)

# subtle top border rule
draw.line([(0, 0), (W, 0)], fill=GOLD, width=3)

# --- chapter-tick logo mark (top-left) ---
ox, oy = 80, 132
draw.rounded_rectangle([ox, oy, ox + 64, oy + 64], radius=15, fill=SURFACE)
# open-book curve
draw.arc([ox + 12, oy + 30, ox + 52, oy + 54], start=200, end=340, fill=VIOLET, width=2)
# chapter ticks
ticks = [(10, 32), (16, 26), (22, 22), (28, 25), (34, 30), (40, 34)]
for i, (tx, ty) in enumerate(ticks):
    h = oy + 40 - ty
    draw.rounded_rectangle([ox + tx, oy + ty, ox + tx + 3, oy + 40], radius=1, fill=GOLD_HI)
draw.ellipse([ox + 20, oy + 17, ox + 25, oy + 22], fill=GOLD)

# --- wordmark: "Meringo " (parchment) + "Listen" (gold) ---
wx, wy = 80, 220
draw.text((wx, wy), "Meringo ", font=f_word, fill=PARCH)
w_meringo = draw.textlength("Meringo ", font=f_word)
draw.text((wx + w_meringo, wy), "Listen", font=f_word, fill=GOLD)

# --- tagline ---
draw.text((82, 322), "Your books, exactly as narrated.", font=f_tag, fill=GOLD_HI)

# --- sub line ---
draw.text((84, 392), "Audiobookshelf + your files   ·   A real voice EQ", font=f_sub, fill=PARCH_DIM)

# --- gold rule + url ---
draw.line([(86, 470), (470, 470)], fill=(158, 122, 62), width=1)
draw.text((86, 486), "meringolisten.app", font=f_url, fill=GOLD)
draw.text((300, 486), "$14.99 once · no subscription · no ads", font=f_url, fill=PARCH_DIM)

# --- device screenshot on the right ---
shot = Image.open(os.path.join(SCREENS, "now_listening.png")).convert("RGBA")
target_h = 558
target_w = round(shot.width * target_h / shot.height)
shot = shot.resize((target_w, target_h), Image.LANCZOS)
# rounded corners
mask = Image.new("L", shot.size, 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width, shot.height], radius=34, fill=255)
shot.putalpha(mask)
dx = W - target_w - 80
dy = (H - target_h) // 2
# drop shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([dx + 8, dy + 22, dx + target_w + 8, dy + target_h + 22], radius=34, fill=(0, 0, 0, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
img = Image.alpha_composite(img.convert("RGBA"), shadow)
img.alpha_composite(shot, (dx, dy))
# thin gold frame on the device
ImageDraw.Draw(img).rounded_rectangle([dx, dy, dx + target_w, dy + target_h], radius=34, outline=(232, 181, 96, 90), width=1)

img.convert("RGB").save(OUT, "PNG")
print("wrote", OUT, img.size)
