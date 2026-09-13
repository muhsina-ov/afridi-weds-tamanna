import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

sys.stdout.reconfigure(encoding='utf-8')

width = 1200
height = 630

# Base canvas with soft royal ivory gradient
base = Image.new('RGBA', (width, height), (252, 248, 240, 255))
draw = ImageDraw.Draw(base)

for y in range(height):
    ratio = y / height
    r = int(254 * (1 - ratio) + 246 * ratio)
    g = int(250 * (1 - ratio) + 238 * ratio)
    b = int(242 * (1 - ratio) + 224 * ratio)
    draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

# Palette
gold_deep = (166, 125, 43, 255)
gold_light = (212, 178, 108, 255)
gold_glow = (235, 210, 155, 255)
burgundy = (90, 15, 27, 255)
burgundy_deep = (70, 10, 20, 255)
text_dark = (50, 35, 25, 255)
text_muted = (115, 90, 70, 255)

# Outer and Inner Ornate Borders
draw.rounded_rectangle([18, 18, width - 18, height - 18], radius=14, outline=gold_deep, width=2)
draw.rounded_rectangle([25, 25, width - 25, height - 25], radius=10, outline=gold_light, width=1)

# Corner ornamental dots
for cx, cy in [(35, 35), (width - 35, 35), (35, height - 35), (width - 35, height - 35)]:
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=gold_deep)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=gold_glow)

# --- LEFT ARCH ARTWORK ---
fw, fh = 380, 490
fx, fy = 65, 70
r = fw // 2

# Background inside arch: warm luxury champagne blush
arch_bg = Image.new('RGBA', (fw, fh), (245, 237, 225, 255))
arch_draw = ImageDraw.Draw(arch_bg)
for ay in range(fh):
    aratio = ay / fh
    ar = int(247 * (1 - aratio) + 236 * aratio)
    ag = int(239 * (1 - aratio) + 224 * aratio)
    ab = int(226 * (1 - aratio) + 208 * aratio)
    arch_draw.line([(0, ay), (fw, ay)], fill=(ar, ag, ab, 255))

# Flowers
fl_left_path = 'images/cdn/noroot_3.png'
fl_right_path = 'images/cdn/noroot_2.png'

if os.path.exists(fl_left_path):
    fl1 = Image.open(fl_left_path).convert('RGBA')
    fl1_w = int(fw * 0.72)
    fl1_h = int(fl1.height * (fl1_w / fl1.width))
    fl1_res = fl1.resize((fl1_w, fl1_h), Image.Resampling.LANCZOS)
    arch_bg.paste(fl1_res, (-20, fh - fl1_h + 30), fl1_res)

if os.path.exists(fl_right_path):
    fl2 = Image.open(fl_right_path).convert('RGBA')
    fl2_w = int(fw * 0.72)
    fl2_h = int(fl2.height * (fl2_w / fl2.width))
    fl2_res = fl2.resize((fl2_w, fl2_h), Image.Resampling.LANCZOS)
    arch_bg.paste(fl2_res, (fw - fl2_w + 20, fh - fl2_h + 10), fl2_res)

# Custom Royal Wax Seal in Arch (Deep Burgundy & Gold with Couple Monogram A & T)
seal_size = 146
seal_img = Image.new('RGBA', (seal_size, seal_size), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(seal_img)

# Multi-layered seal shadow and body
scx, scy = seal_size // 2, seal_size // 2
sr = 66
# Outer wax scallop / lip
s_draw.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(110, 18, 32, 255), outline=(75, 12, 22, 255), width=3)
# Inner bevel rim
s_draw.ellipse([scx - sr + 7, scy - sr + 7, scx + sr - 7, scy + sr - 7], fill=(130, 24, 40, 255), outline=gold_deep, width=2)
# Center stamp bed
s_draw.ellipse([scx - sr + 14, scy - sr + 14, scx + sr - 14, scy + sr - 14], fill=(95, 14, 25, 255))
s_draw.ellipse([scx - sr + 17, scy - sr + 17, scx + sr - 17, scy + sr - 17], outline=gold_light, width=1)

# Monogram "A & T" on the wax seal
f_seal_mono = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 30)
f_seal_sub = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 10)

sb = s_draw.textbbox((0, 0), "A & T", font=f_seal_mono)
# Embossed effect (shadow + highlight)
s_draw.text((scx - (sb[2] - sb[0]) // 2 + 1, scy - (sb[3] - sb[1]) // 2 - 2), "A & T", font=f_seal_mono, fill=(50, 8, 14, 255))
s_draw.text((scx - (sb[2] - sb[0]) // 2, scy - (sb[3] - sb[1]) // 2 - 3), "A & T", font=f_seal_mono, fill=gold_glow)

# Flanking decorative laurels
s_draw.line([(scx - 30, scy + 22), (scx + 30, scy + 22)], fill=gold_light, width=1)
s_draw.polygon([(scx, scy + 19), (scx + 3, scy + 22), (scx, scy + 25), (scx - 3, scy + 22)], fill=gold_glow)

# Crown motif above
s_draw.polygon([(scx - 12, scy - 25), (scx - 6, scy - 29), (scx, scy - 24), (scx + 6, scy - 29), (scx + 12, scy - 25), (scx, scy - 20)], fill=gold_glow)

# Paste seal into arch
sx = (fw - seal_size) // 2
sy = (fh - seal_size) // 2 - 35
arch_bg.paste(seal_img, (sx, sy), seal_img)

# Create arch mask
arch_mask = Image.new('L', (fw, fh), 0)
am_draw = ImageDraw.Draw(arch_mask)
am_draw.pieslice([0, 0, fw, fw], 180, 360, fill=255)
am_draw.rectangle([0, r, fw, fh], fill=255)

arch_composite = Image.new('RGBA', (fw, fh), (0, 0, 0, 0))
arch_composite.paste(arch_bg, (0, 0), arch_mask)

# Soft shadow behind arch
shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow)
sdraw.pieslice([fx - 4, fy, fx + fw + 4, fy + fw + 8], 180, 360, fill=(45, 25, 15, 60))
sdraw.rectangle([fx - 4, fy + r, fx + fw + 4, fy + fh + 8], fill=(45, 25, 15, 60))
shadow = shadow.filter(ImageFilter.GaussianBlur(14))
base = Image.alpha_composite(base, shadow)

# Paste arch onto base
base.paste(arch_composite, (fx, fy), arch_composite)

# Draw gold borders over arch
overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
odraw = ImageDraw.Draw(overlay)

odraw.arc([fx, fy, fx + fw, fy + fw], 180, 360, fill=gold_deep, width=3)
odraw.line([(fx, fy + r), (fx, fy + fh)], fill=gold_deep, width=3)
odraw.line([(fx + fw, fy + r), (fx + fw, fy + fh)], fill=gold_deep, width=3)
odraw.line([(fx, fy + fh), (fx + fw, fy + fh)], fill=gold_deep, width=3)

inset = 5
odraw.arc([fx + inset, fy + inset, fx + fw - inset, fy + fw - inset], 180, 360, fill=gold_light, width=1)
odraw.line([(fx + inset, fy + r), (fx + inset, fy + fh - inset)], fill=gold_light, width=1)
odraw.line([(fx + fw - inset, fy + r), (fx + fw - inset, fy + fh - inset)], fill=gold_light, width=1)
odraw.line([(fx + inset, fy + fh - inset), (fx + fw - inset, fy + fh - inset)], fill=gold_light, width=1)

base = Image.alpha_composite(base, overlay)

# --- RIGHT TYPOGRAPHY COLUMN ---
draw = ImageDraw.Draw(base)
rx = 480
rw = 670
cx = rx + rw // 2

# Fonts
f_bismillah = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 13)
f_sub = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 13)
f_host = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 17)
f_invite = ImageFont.truetype('C:/Windows/Fonts/timesi.ttf', 16)
f_name = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 44)
f_date = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 18)
f_events = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 15)
f_venues = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 14)
f_badge = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 12)
f_mono = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 16)

y = 65

# Monogram circle
mono_w = 48
mono_h = 48
draw.ellipse([cx - mono_w // 2, y, cx + mono_w // 2, y + mono_h], fill=(255, 252, 246, 240), outline=gold_deep, width=2)
mb = draw.textbbox((0, 0), "A & T", font=f_mono)
draw.text((cx - (mb[2] - mb[0]) // 2, y + 14), "A & T", font=f_mono, fill=burgundy)
y += mono_h + 12

# Subtitle
sub = "ROYAL WEDDING INVITATION"
bb = draw.textbbox((0, 0), sub, font=f_sub)
draw.text((cx - (bb[2] - bb[0]) // 2, y), sub, font=f_sub, fill=gold_deep)
y += 24

# Inviting Parents
hosts = "Mr. Firoz Khan & Mr. M.D. Ali"
bb = draw.textbbox((0, 0), hosts, font=f_host)
draw.text((cx - (bb[2] - bb[0]) // 2, y), hosts, font=f_host, fill=burgundy)
y += 24

# Cordially invite
inv = "Cordially invite you to celebrate the wedding ceremonies of their children"
bb = draw.textbbox((0, 0), inv, font=f_invite)
draw.text((cx - (bb[2] - bb[0]) // 2, y), inv, font=f_invite, fill=text_muted)
y += 26

# Couple Names
names_line = "AFRIDI  &  TAMANNA"
bb = draw.textbbox((0, 0), names_line, font=f_name)
draw.text((cx - (bb[2] - bb[0]) // 2, y), names_line, font=f_name, fill=burgundy)
y += 56

# Vector Gold Flourish Divider
div_half = 140
draw.line([(cx - div_half, y), (cx - 16, y)], fill=gold_light, width=1)
draw.line([(cx + 16, y), (cx + div_half, y)], fill=gold_light, width=1)
draw.polygon([(cx, y - 6), (cx + 6, y), (cx, y + 6), (cx - 6, y)], fill=gold_deep)
draw.ellipse([cx - 12, y - 2, cx - 8, y + 2], fill=gold_light)
draw.ellipse([cx + 8, y - 2, cx + 12, y + 2], fill=gold_light)
y += 18

# Date Banner Box
date_str = "02ND — 06TH DECEMBER 2026"
bb = draw.textbbox((0, 0), date_str, font=f_date)
bw = bb[2] - bb[0] + 36
bh = 38
draw.rounded_rectangle([cx - bw // 2, y, cx + bw // 2, y + bh], radius=19, fill=(90, 15, 27, 245), outline=gold_light, width=1)
draw.text((cx - (bb[2] - bb[0]) // 2, y + 9), date_str, font=f_date, fill=(255, 245, 230, 255))
y += bh + 16

# Ceremonies
cer_str = "Haldi  ·  Nikah  ·  Grand Reception"
bb = draw.textbbox((0, 0), cer_str, font=f_events)
draw.text((cx - (bb[2] - bb[0]) // 2, y), cer_str, font=f_events, fill=gold_deep)
y += 24

# Venues
ven_str = "Hiland Greens PH-1  ·  Hemachandra Library  ·  Kolkata"
bb = draw.textbbox((0, 0), ven_str, font=f_venues)
draw.text((cx - (bb[2] - bb[0]) // 2, y), ven_str, font=f_venues, fill=text_muted)
y += 28

# Production Link Badge
badge_str = "afridi-weds-tamanna.pages.dev"
bb = draw.textbbox((0, 0), badge_str, font=f_badge)
bw = bb[2] - bb[0] + 28
bh = 26
draw.rounded_rectangle([cx - bw // 2, y, cx + bw // 2, y + bh], radius=13, fill=(255, 252, 246, 230), outline=gold_deep, width=1)
draw.text((cx - (bb[2] - bb[0]) // 2, y + 6), badge_str, font=f_badge, fill=gold_deep)

# Save high-quality PNG and JPG
os.makedirs('images', exist_ok=True)
png_path = 'images/og-image.png'
jpg_path = 'images/og-image.jpg'

base.save(png_path, 'PNG', optimize=True)
rgb = base.convert('RGB')
rgb.save(jpg_path, 'JPEG', quality=95)

print('Generated bespoke monogram OG image:', png_path)
