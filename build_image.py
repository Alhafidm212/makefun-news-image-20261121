#!/usr/bin/env python3
"""Build the 21 Nov 2026 world-news front page, 1024x1024 PNG.
Deterministic: fixed text, fixed geometry, no timestamps.

Stories (all first reported Saturday 21 Nov 2026, Reuters and wires):
- Lead: the International Court of Justice rules 9-6 that Myanmar
  committed genocide against the Rohingya in 2017, and orders an
  investigation and compensation for survivors.
- AI-led market selloff: the S&P 500 falls 3.7% into correction and
  the Nasdaq 5.28%; the SEC examines Nvidia's accounting and its
  shares fall 13.8%; Nikkei and Kospi drop more than 5%.
- COP31 climate summit in Antalya misses its deadline; the draft
  text drops any mention of fossil fuels.
- A tanker is hit by a projectile off Khasab, Oman, and catches
  fire in the Strait of Hormuz; no casualties.
- Saudi-led strikes hit Hodeidah port in Yemen; Houthis say 41
  dead, while the coalition says it downed three missiles aimed
  at Riyadh.
- UK and EU seal a Brussels deal scrapping most food and farm
  checks, linking carbon markets, and opening youth mobility for
  up to 100,000 under-30s on each side.
- Phumzile Mlambo-Ngcuka, South Africa's first female deputy
  president and former UN Women chief, dies aged 71.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (166, 25, 46)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
NIGHT = (16, 24, 46)
GOLD = (212, 168, 60)
STONE = (58, 72, 104)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_MAST = font("DejaVuSerif-Bold.ttf", 108)
F_HEAD = font("DejaVuSerif-Bold.ttf", 54)
F_KICK = font("DejaVuSans-Bold.ttf", 24)
F_SUB = font("DejaVuSerif.ttf", 24)
F_CELL_H = font("DejaVuSans-Bold.ttf", 25)
F_CELL_B = font("DejaVuSans.ttf", 20)
F_DATE = font("DejaVuSans-Bold.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 18)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 40

def wrap(text, fnt, width_px):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width_px:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def rule(y, w=3):
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=w)

# dateline bar
y = 28
d.text((MX, y), "SATURDAY, 21 NOVEMBER 2026", font=F_DATE, fill=INK)
r = "WORLD NEWS - IN ONE IMAGE"
d.text((W - MX - d.textlength(r, font=F_DATE), y), r, font=F_DATE, fill=RED)
y = 64
rule(y, 4)
# masthead
y = 74
t = "THE WORLD"
d.text(((W - d.textlength(t, font=F_MAST)) / 2, y), t, font=F_MAST, fill=INK)
y = 188
rule(y, 2)
y = 198
sub = "One day of world news, summed up in a single picture"
d.text(((W - d.textlength(sub, font=F_SUB)) / 2, y), sub, font=F_SUB, fill=GREY)

# lead story
y = 232
d.text((MX, y), "THE HAGUE  -  LEAD STORY", font=F_KICK, fill=RED)
y = 264
d.text((MX, y), "COURT RULES MYANMAR", font=F_HEAD, fill=INK)
y = 328
d.text((MX, y), "COMMITTED GENOCIDE", font=F_HEAD, fill=INK)
y = 392
lead = ("The International Court of Justice rules 9-6 that Myanmar committed "
        "genocide against the Rohingya in 2017, ordering an investigation and "
        "compensation for survivors.")
for ln in wrap(lead, F_SUB, W - 2 * MX):
    d.text((MX, y), ln, font=F_SUB, fill=INK)
    y += 29

# illustration band: the Peace Palace at The Hague, scales of justice
by0, by1 = 486, 590
d.rectangle([MX, by0, W - MX, by1], fill=NIGHT)
# stars
for sx, sy in ((90, 500), (180, 512), (300, 498), (420, 516), (560, 502),
               (700, 514), (830, 500), (920, 520), (250, 530), (640, 530)):
    d.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 225, 240))
# courthouse: steps, columns, pediment
d.rectangle([380, 578, 644, by1], fill=STONE)          # base step
d.rectangle([396, 570, 628, 578], fill=STONE)          # step
for cx in (408, 452, 496, 540, 584):
    d.rectangle([cx, 528, cx + 20, 570], fill=(120, 134, 168))  # columns
d.rectangle([396, 520, 628, 528], fill=(120, 134, 168))         # architrave
d.polygon([(388, 520), (512, 492), (636, 520)], fill=GOLD)       # pediment
d.ellipse([504, 496, 520, 512], fill=GOLD)                       # pediment disc
# scales of justice, gold, centre of the band
d.line([(512, 540), (512, 566)], fill=GOLD, width=4)             # pole
d.line([(452, 544), (572, 544)], fill=GOLD, width=4)             # beam
d.ellipse([508, 534, 516, 542], fill=GOLD)                       # finial
for px in (452, 572):
    d.line([(px, 544), (px - 14, 566)], fill=GOLD, width=2)
    d.line([(px, 544), (px + 14, 566)], fill=GOLD, width=2)
    d.chord([px - 16, 556, px + 16, 576], 0, 180, fill=GOLD)
d.text((MX, by1 + 6), "The Peace Palace, The Hague, where the court gave its ruling. Illustration.",
       font=F_FOOT, fill=GREY)

# 2x3 grid of secondary stories (bodies kept to <=3 lines)
cells = [
    ("1", "MARKETS PLUNGE",
     "AI-led selloff: S&P 500 falls 3.7% into correction, Nasdaq -5.28%; SEC probes Nvidia, shares -13.8%."),
    ("2", "COP31 DEADLOCK",
     "Climate summit in Antalya misses its deadline; the draft text drops any mention of fossil fuels."),
    ("3", "TANKER ON FIRE",
     "A tanker is hit by a projectile off Khasab, Oman, and catches fire in the Strait of Hormuz; no casualties."),
    ("4", "YEMEN STRIKES",
     "Saudi-led strikes hit Hodeidah port; Houthis say 41 dead, and the coalition downs missiles aimed at Riyadh."),
    ("5", "UK-EU DEAL",
     "Brussels deal scraps most food checks, links carbon markets and opens youth mobility for up to 100,000 a side."),
    ("6", "OBITUARY",
     "Phumzile Mlambo-Ngcuka, South Africa's first female deputy president and ex-UN Women chief, dies aged 71."),
]
gy = 626
cw = (W - 2 * MX - 24) // 2
ch = 110
for i, (num, head, body) in enumerate(cells):
    cx = MX + (i % 2) * (cw + 24)
    cy = gy + (i // 2) * ch
    d.ellipse([cx, cy + 2, cx + 34, cy + 36], fill=RED)
    tw = d.textlength(num, font=F_CELL_H)
    d.text((cx + (34 - tw) / 2, cy + 5), num, font=F_CELL_H, fill=(255, 255, 255))
    d.text((cx + 44, cy + 4), head, font=F_CELL_H, fill=INK)
    by = cy + 36
    for ln in wrap(body, F_CELL_B, cw - 44):
        d.text((cx + 44, by), ln, font=F_CELL_B, fill=(40, 40, 40))
        by += 24

# footer
fy = 626 + 3 * ch + 4
rule(fy, 2)
d.text((MX, fy + 8), "Compiled from Reuters and other wires - 21 Nov 2026 - make.fun news-image-20261121",
       font=F_FOOT, fill=GREY)

out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
img.save(out, "PNG", optimize=True)
print("saved", out)
