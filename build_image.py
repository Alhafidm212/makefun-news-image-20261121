#!/usr/bin/env python3
"""Draw the news-image-20261121 front page (1024x1024 PNG) with Pillow.

The page is a newspaper front page for Saturday 21 November 2026:
masthead, lead story on the ICJ genocide ruling against Myanmar, a
Peace Palace banner illustration, and six more stories of the day in a
two-column grid. Fully deterministic: no network, no randomness, no
clock. Run:  python3 build_image.py [output-path]

Default output is entry.png next to this script.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
MARGIN = 40
CONTENT_W = WIDTH - 2 * MARGIN

CREAM = (246, 240, 220)
INK = (22, 22, 22)
RED = (176, 32, 48)
NAVY = (17, 23, 47)
GOLD = (214, 176, 58)
PALE_BLUE = (148, 158, 190)
MID_BLUE = (110, 122, 158)
GREY = (96, 96, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    """Load a DejaVu font by file name, falling back to the default font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_BOLD = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: load_font("DejaVuSerif.ttf", s)
SANS_BOLD = lambda s: load_font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: load_font("DejaVuSans.ttf", s)


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width, breaking on word bounds."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_rule(draw, y, height=3, color=INK, x0=None, x1=None):
    draw.rectangle(
        [x0 if x0 is not None else MARGIN, y,
         x1 if x1 is not None else WIDTH - MARGIN, y + height - 1],
        fill=color,
    )


def draw_badge(draw, cx, cy, number, radius=17):
    """Red circled story number with a white digit."""
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius], fill=RED
    )
    font = SANS_BOLD(22)
    label = str(number)
    w = draw.textlength(label, font=font)
    h = font.size
    draw.text((cx - w / 2, cy - h / 2 - 2), label, font=font, fill=(255, 255, 255))


def draw_palace_banner(draw, y0, y1):
    """Night banner: starry navy sky with the Peace Palace and scales."""
    draw.rectangle([MARGIN, y0, WIDTH - MARGIN, y1], fill=NAVY)
    # Fixed stars, hand-placed so the sky is identical every run.
    stars = [
        (70, 522, 2), (150, 514, 1), (235, 528, 2), (330, 516, 1),
        (420, 524, 2), (700, 518, 1), (790, 526, 2), (880, 514, 1),
        (950, 528, 2), (120, 606, 1), (900, 606, 1), (640, 611, 1),
        (290, 614, 1), (520, 514, 1), (760, 611, 2),
    ]
    for x, y, r in stars:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(235, 235, 240))

    cx = WIDTH // 2
    base = y1
    # Steps.
    draw.rectangle([cx - 150, base - 12, cx + 150, base], fill=MID_BLUE)
    draw.rectangle([cx - 125, base - 24, cx + 125, base - 12], fill=PALE_BLUE)
    draw.rectangle([cx - 100, base - 36, cx + 100, base - 24], fill=MID_BLUE)
    floor = base - 36
    # Columns.
    for off in (-78, -26, 26, 78):
        draw.rectangle([cx + off - 11, floor - 62, cx + off + 11, floor],
                       fill=PALE_BLUE)
    # Entablature and golden pediment.
    draw.rectangle([cx - 118, floor - 76, cx + 118, floor - 62], fill=PALE_BLUE)
    draw.polygon(
        [(cx - 118, floor - 76), (cx + 118, floor - 76), (cx, floor - 108)],
        fill=GOLD,
    )
    # Scales of justice, centred on the palace front.
    post_x = cx
    post_top = floor - 58
    draw.line([post_x, post_top, post_x, floor - 8], fill=GOLD, width=4)
    beam_y = post_top + 8
    draw.line([post_x - 62, beam_y, post_x + 62, beam_y], fill=GOLD, width=4)
    draw.ellipse([post_x - 6, post_top - 6, post_x + 6, post_top + 6], fill=GOLD)
    for end in (-62, 62):
        pan_x = post_x + end
        pan_y = beam_y + 30
        draw.line([pan_x, beam_y, pan_x, pan_y], fill=GOLD, width=2)
        draw.pieslice(
            [pan_x - 20, pan_y - 4, pan_x + 20, pan_y + 20],
            start=0, end=180, fill=GOLD,
        )
        draw.line([pan_x - 20, pan_y, pan_x + 20, pan_y], fill=GOLD, width=2)


def draw_story(draw, x, y, number, headline, body, col_w):
    """One numbered grid story: badge, bold headline, wrapped body."""
    draw_badge(draw, x + 17, y + 14, number)
    head_font = SANS_BOLD(25)
    draw.text((x + 44, y), headline, font=head_font, fill=INK)
    body_font = SANS(19)
    lines = wrap_text(draw, body, body_font, col_w - 44)
    ly = y + 33
    for line in lines[:4]:
        draw.text((x + 44, ly), line, font=body_font, fill=INK)
        ly += 24
    return ly


def build(path):
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(img)

    # Dateline row.
    date_font = SANS_BOLD(21)
    draw.text((MARGIN, 26), "SATURDAY, 21 NOVEMBER 2026", font=date_font, fill=INK)
    tag = "WORLD NEWS - IN ONE IMAGE"
    tag_w = draw.textlength(tag, font=date_font)
    draw.text((WIDTH - MARGIN - tag_w, 26), tag, font=date_font, fill=RED)
    draw_rule(draw, 56, height=4)

    # Masthead.
    mast_font = SERIF_BOLD(118)
    mast = "THE WORLD"
    mw = draw.textlength(mast, font=mast_font)
    draw.text(((WIDTH - mw) / 2, 66), mast, font=mast_font, fill=INK)
    draw_rule(draw, 196, height=2)
    sub_font = SERIF(24)
    sub = "One day of world news, summed up in a single picture"
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((WIDTH - sw) / 2, 206), sub, font=sub_font, fill=GREY)

    # Lead story kicker + headline + deck.
    kick_font = SANS_BOLD(23)
    draw.text((MARGIN, 244), "THE HAGUE  -  LEAD STORY", font=kick_font, fill=RED)
    head_font = SERIF_BOLD(60)
    for i, line in enumerate(["COURT RULES MYANMAR", "COMMITTED GENOCIDE"]):
        draw.text((MARGIN, 272 + i * 64), line, font=head_font, fill=INK)
    deck_font = SERIF(26)
    deck = (
        "The International Court of Justice rules 9-6 that Myanmar committed "
        "genocide against the Rohingya in 2017, ordering an investigation and "
        "compensation for survivors."
    )
    dy = 404
    for line in wrap_text(draw, deck, deck_font, CONTENT_W):
        draw.text((MARGIN, dy), line, font=deck_font, fill=INK)
        dy += 33

    # Palace banner + caption.
    draw_palace_banner(draw, 506, 622)
    cap_font = SERIF(19)
    draw.text(
        (MARGIN, 630),
        "The Peace Palace, The Hague, where the court gave its ruling. Illustration.",
        font=cap_font, fill=GREY,
    )

    # Six stories, two columns x three rows.
    stories = [
        (1, "MARKETS PLUNGE",
         "AI-led selloff: S&P 500 falls 3.7% into correction, Nasdaq -5.28%; "
         "SEC probes Nvidia, shares -13.8%."),
        (2, "COP31 DEADLOCK",
         "Climate summit in Antalya misses its deadline; the draft text drops "
         "any mention of fossil fuels."),
        (3, "TANKER ON FIRE",
         "A tanker is hit by a projectile off Khasab, Oman, and catches fire "
         "in the Strait of Hormuz; no casualties."),
        (4, "YEMEN STRIKES",
         "Saudi-led strikes hit Hodeidah port; Houthis say 41 dead, and the "
         "coalition downs missiles aimed at Riyadh."),
        (5, "UK-EU DEAL",
         "Brussels deal scraps most food checks, links carbon markets and "
         "opens youth mobility for up to 100,000 a side."),
        (6, "OBITUARY",
         "Phumzile Mlambo-Ngcuka, South Africa's first female deputy "
         "president and ex-UN Women chief, dies aged 71."),
    ]
    col_w = (CONTENT_W - 40) // 2
    row_y = [668, 780, 892]
    for idx, (number, headline, body) in enumerate(stories):
        col = idx % 2
        row = idx // 2
        x = MARGIN + col * (col_w + 40)
        draw_story(draw, x, row_y[row], number, headline, body, col_w)

    # Footer.
    draw_rule(draw, 972, height=2)
    foot_font = SANS(17)
    draw.text(
        (MARGIN, 982),
        "Compiled from Reuters and other wires - 21 Nov 2026 - make.fun news-image-20261121",
        font=foot_font, fill=GREY,
    )

    img.save(path, format="PNG")
    size = os.path.getsize(path)
    if size > 1 << 20:
        raise SystemExit("error: saved image is %d bytes, over the 1 MiB limit" % size)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")
    build(out)
    print("wrote", out)
