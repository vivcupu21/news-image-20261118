#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a one-page newspaper front page
summing up the world news of Wednesday 18 November 2026.

Everything is drawn with Pillow from scratch (flat vector-style shapes and
text); no network, no external images, no randomness, no timestamps.
Output: entry.png, 1024x1024, well under 1 MiB.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

CREAM = (248, 244, 236)
PAPER = (255, 255, 255)
INK = (20, 20, 20)
NAVY = (14, 34, 64)
NAVY2 = (22, 48, 88)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
TEAL = (31, 111, 139)
SLATE = (74, 85, 104)
BURNT = (124, 45, 18)
SKY = (220, 233, 245)
MUTED = (90, 90, 90)
RULE = (200, 192, 175)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text; return y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    """Five-point star centred at (cx, cy)."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_us(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(178, 34, 52))
    draw.rectangle([x, y, x + w * 0.42, y + stripe * 4], fill=(30, 58, 120))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 9, y + 3 + r * 7,
                          x + 7 + c * 9, y + 6 + r * 7], fill=(255, 255, 255))


def flag_india(draw, x, y, w, h):
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=(255, 153, 51))
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(255, 255, 255))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(19, 136, 8))
    cx, cy, r = x + w / 2, y + h / 2, third * 0.42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 0, 128), width=2)


def flag_japan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.ellipse([x + w / 2 - h * 0.3, y + h * 0.2,
                  x + w / 2 + h * 0.3, y + h * 0.8], fill=(188, 0, 45))


def flag_australia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    draw.rectangle([x, y, x + w * 0.45, y + h * 0.5], fill=(200, 16, 46))
    draw.line([x, y, x + w * 0.45, y + h * 0.5], fill=(255, 255, 255), width=2)
    draw.line([x + w * 0.45, y, x, y + h * 0.5], fill=(255, 255, 255), width=2)
    for sx, sy in [(0.72, 0.28), (0.85, 0.55), (0.68, 0.72), (0.88, 0.8)]:
        draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                      x + w * sx + 2, y + h * sy + 2], fill=(255, 255, 255))


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.22, y + h * 0.28, h * 0.22, (255, 222, 0))
    for sx, sy in [(0.48, 0.15), (0.58, 0.28), (0.55, 0.48), (0.42, 0.55)]:
        draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                      x + w * sx + 2, y + h * sy + 2], fill=(255, 222, 0))


def flag_russia(draw, x, y, w, h):
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=(255, 255, 255))
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 0, 50))


def skyline(draw, x, y, w, h):
    """Shenzhen skyline at dusk: sun, towers, lit windows, water."""
    draw.rectangle([x, y, x + w, y + h], fill=(176, 208, 232))
    draw.ellipse([x + w - 78, y + 8, x + w - 18, y + 68], fill=(214, 69, 65))
    buildings = [(0, 96, 46), (48, 70, 44), (94, 112, 40),
                 (136, 58, 48), (186, 88, 42), (230, 66, 46),
                 (278, 104, 38)]
    for bx, top, bw in buildings:
        draw.rectangle([x + bx, y + top, x + bx + bw, y + h - 22], fill=NAVY)
        # windows
        for wy in range(y + top + 10, y + h - 30, 14):
            for wx in range(x + bx + 7, x + bx + bw - 6, 12):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=GOLD)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(38, 90, 130))
    for wx in range(x + 8, x + w - 8, 26):
        draw.line([wx, y + h - 11, wx + 14, y + h - 11], fill=(255, 255, 255),
                  width=2)


def bridge_scene(draw, x, y, w, h):
    """Crimean Bridge: deck, towers, middle span collapsed into waves."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    # sea
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(56, 120, 178))
    for wx in range(x + 4, x + w - 4, 22):
        draw.arc([wx, y + h - 24, wx + 18, y + h - 12], 180, 360,
                 fill=(255, 255, 255), width=2)
    # towers
    for tx in (x + 70, x + w - 92):
        draw.rectangle([tx, y + 8, tx + 8, y + h - 26], fill=SLATE)
        draw.rectangle([tx - 16, y + 8, tx + 24, y + 14], fill=SLATE)
    # deck: left part intact, middle collapsed, right part intact
    draw.rectangle([x, y + 34, x + w * 0.38, y + 42], fill=(40, 40, 40))
    draw.rectangle([x + w * 0.62, y + 34, x + w, y + 42], fill=(40, 40, 40))
    # collapsed span plunging into the strait
    draw.polygon([(x + w * 0.38, y + 38), (x + w * 0.50, y + h - 24),
                  (x + w * 0.54, y + h - 24), (x + w * 0.44, y + 38)],
                 fill=(40, 40, 40))
    # explosion burst at the break
    star(draw, x + w * 0.40, y + 30, 16, (245, 158, 11))
    star(draw, x + w * 0.40, y + 30, 8, (220, 38, 38))


def radar_scene(draw, x, y, w, h):
    """Radar dish, drone silhouette, Gulf waves."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(56, 120, 178))
    for wx in range(x + 4, x + w - 4, 22):
        draw.arc([wx, y + h - 20, wx + 18, y + h - 8], 180, 360,
                 fill=(255, 255, 255), width=2)
    # radar dish on a mast
    draw.line([x + 52, y + h - 22, x + 52, y + 34], fill=SLATE, width=4)
    draw.arc([x + 22, y + 6, x + 82, y + 52], 200, 340, fill=SLATE, width=5)
    draw.line([x + 52, y + 30, x + 92, y + 8], fill=(185, 28, 28), width=3)
    # drone
    dx, dy = x + w - 92, y + 22
    draw.ellipse([dx - 16, dy - 5, dx + 16, dy + 5], fill=(30, 30, 30))
    draw.line([dx - 26, dy - 8, dx + 26, dy - 8], fill=(30, 30, 30), width=3)
    draw.ellipse([dx - 30, dy - 12, dx - 22, dy - 4], fill=(90, 90, 90))
    draw.ellipse([dx + 22, dy - 12, dx + 30, dy - 4], fill=(90, 90, 90))
    draw.line([dx, dy + 5, dx, dy + 14], fill=(30, 30, 30), width=3)


def cyclone_scene(draw, x, y, w, h):
    """Cyclone spiral over the sea, rain slashes."""
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    for r, start, end, col in [(46, 20, 300, (30, 90, 160)),
                               (36, 110, 390, (56, 130, 200)),
                               (26, 200, 120, (30, 90, 160)),
                               (16, 290, 210, (56, 130, 200))]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=col, width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(185, 28, 28))
    for rx in range(x + 6, x + w - 6, 18):
        draw.line([rx, y + h - 16, rx - 5, y + h - 6], fill=(56, 130, 200),
                  width=2)


def panel(draw, x, y, w, h, bar_color):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER,
                   outline=(180, 172, 155), width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=bar_color)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- outer frame -------------------------------------------------
    d.rectangle([4, 4, W - 5, H - 5], outline=NAVY, width=4)

    # ---- masthead ----------------------------------------------------
    d.rectangle([8, 8, W - 9, 108], fill=NAVY)
    d.text((28, 16), "THE WORLD IN ONE IMAGE",
           font=font(BOLD, 44), fill=(255, 255, 255))
    d.text((28, 66), "WEDNESDAY  \u2022  18 NOVEMBER 2026",
           font=font(BOLD, 27), fill=GOLD)
    d.text((W - 28, 70), "ONE DAY \u2022 ONE PICTURE",
           font=font(BOLD, 17), fill=(255, 255, 255), anchor="ra")
    d.rectangle([8, 108, W - 9, 112], fill=GOLD)

    # ---- lead story: APEC opens in Shenzhen -------------------------
    lx, ly, lw, lh = 16, 122, 992, 244
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PAPER,
                outline=(180, 172, 155), width=2)
    d.rectangle([lx, ly, lx + lw, ly + 6], fill=RED)
    d.text((lx + 18, ly + 18), "LEAD STORY  \u2014  ASIA",
           font=font(BOLD, 17), fill=RED)
    d.text((lx + 18, ly + 44), "APEC OPENS IN SHENZHEN",
           font=font(BOLD, 38), fill=INK)
    draw_text_block(d, lx + 18, ly + 100,
                    "World leaders gather in China as Trump, Xi and Putin "
                    "converge on the summit city.",
                    font(REG, 21), INK, 600, leading=27)
    draw_text_block(d, lx + 18, ly + 158,
                    "Trade, AI and security top the agenda as the "
                    "21-member forum opens.",
                    font(REG, 21), INK, 600, leading=27)
    d.text((lx + 18, ly + 208), "SHENZHEN, CHINA",
           font=font(BOLD, 15), fill=MUTED)
    skyline(d, lx + 648, ly + 20, 326, 204)

    # ---- row 1 -------------------------------------------------------
    ry, rh = 380, 226
    # QUAD in Manila
    px, pw = 16, 478
    panel(d, px, ry, pw, rh, TEAL)
    d.text((px + 16, ry + 18), "DIPLOMACY  \u2014  MANILA",
           font=font(BOLD, 15), fill=RED)
    d.text((px + 16, ry + 42), "QUAD MEETS IN MANILA",
           font=font(BOLD, 28), fill=INK)
    draw_text_block(d, px + 16, ry + 80,
                    "Trump joins Modi, Albanese and Takaichi. Leaders unveil "
                    "a new plan on maritime security, an AI accelerator and "
                    "undersea cables.",
                    font(REG, 19), INK, pw - 32, leading=24)
    flags = [flag_us, flag_india, flag_japan, flag_australia]
    fx = px + 16
    for fl in flags:
        fl(d, fx, ry + rh - 52, 58, 38)
        d.rectangle([fx, ry + rh - 52, fx + 58, ry + rh - 14],
                    outline=(160, 160, 160), width=1)
        fx += 70
    d.text((px + 16 + 4 * 70, ry + rh - 46), "QUAD",
           font=font(BOLD, 20), fill=MUTED)

    # Trilateral summit set
    px = 530
    panel(d, px, ry, pw, rh, RED)
    d.text((px + 16, ry + 18), "HISTORY IN THE MAKING",
           font=font(BOLD, 15), fill=RED)
    d.text((px + 16, ry + 42), "TRUMP-XI-PUTIN SUMMIT SET",
           font=font(BOLD, 27), fill=INK)
    draw_text_block(d, px + 16, ry + 80,
                    "First-ever three-way summit tomorrow, 19 Nov, in "
                    "Shenzhen. Agenda: nuclear arms, Ukraine, Iran, trade "
                    "and AI.",
                    font(REG, 19), INK, pw - 32, leading=24)
    flags = [flag_us, flag_china, flag_russia]
    fx = px + 16
    for fl in flags:
        fl(d, fx, ry + rh - 52, 58, 38)
        d.rectangle([fx, ry + rh - 52, fx + 58, ry + rh - 14],
                    outline=(160, 160, 160), width=1)
        fx += 70
    d.ellipse([px + 16 + 3 * 70, ry + rh - 54, px + 16 + 3 * 70 + 52,
               ry + rh - 2], fill=NAVY)
    d.text((px + 16 + 3 * 70 + 26, ry + rh - 44), "19",
           font=font(BOLD, 20), fill=(255, 255, 255), anchor="ma")
    d.text((px + 16 + 3 * 70 + 26, ry + rh - 22), "NOV",
           font=font(BOLD, 11), fill=(255, 255, 255), anchor="ma")

    # ---- row 2 -------------------------------------------------------
    ry = 620
    # Crimean Bridge
    px, pw = 16, 478
    panel(d, px, ry, pw, rh, SLATE)
    d.text((px + 16, ry + 18), "WAR IN EUROPE",
           font=font(BOLD, 15), fill=RED)
    d.text((px + 16, ry + 42), "UKRAINE HITS",
           font=font(BOLD, 28), fill=INK)
    d.text((px + 16, ry + 74), "CRIMEAN BRIDGE",
           font=font(BOLD, 28), fill=INK)
    draw_text_block(d, px + 16, ry + 112,
                    "Missiles and drones drop a road span into the Kerch "
                    "Strait. Russia answers by striking two bridges in Kyiv.",
                    font(REG, 18), INK, 250, leading=23)
    bridge_scene(d, px + 282, ry + 108, 180, 104)

    # Gulf flashpoint
    px = 530
    panel(d, px, ry, pw, rh, BURNT)
    d.text((px + 16, ry + 18), "MIDDLE EAST",
           font=font(BOLD, 15), fill=RED)
    d.text((px + 16, ry + 42), "GULF FLASHPOINT",
           font=font(BOLD, 28), fill=INK)
    draw_text_block(d, px + 16, ry + 80,
                    "Iranian drones strike a US radar base in Bahrain \u2014 "
                    "the third attack in five days. The US hits an IRGC "
                    "missile base on Qeshm Island.",
                    font(REG, 18), INK, 250, leading=22)
    radar_scene(d, px + 282, ry + 92, 180, 120)

    # ---- bottom strip ------------------------------------------------
    by, bh = 860, 140
    # Cyclone Akvan
    cx0, cw = 16, 404
    d.rectangle([cx0, by, cx0 + cw, by + bh], fill=PAPER,
                outline=(180, 172, 155), width=2)
    d.rectangle([cx0, by, cx0 + cw, by + 6], fill=(30, 90, 160))
    d.text((cx0 + 16, by + 16), "WEATHER  \u2014  BAY OF BENGAL",
           font=font(BOLD, 15), fill=RED)
    d.text((cx0 + 16, by + 40), "CYCLONE AKVAN",
           font=font(BOLD, 24), fill=INK)
    d.text((cx0 + 16, by + 68), "NEARS INDIA",
           font=font(BOLD, 24), fill=INK)
    draw_text_block(d, cx0 + 16, by + 100,
                    "Storm strengthens toward Andhra Pradesh; landfall due "
                    "20 November.",
                    font(REG, 16), INK, 250, leading=19)
    cyclone_scene(d, cx0 + 282, by + 40, 106, 88)

    # Also today
    ax, aw = 436, 572
    d.rectangle([ax, by, ax + aw, by + bh], fill=PAPER,
                outline=(180, 172, 155), width=2)
    d.rectangle([ax, by, ax + aw, by + 6], fill=GOLD)
    d.text((ax + 16, by + 14), "ALSO TODAY",
           font=font(BOLD, 17), fill=RED)
    items = [
        "MS Dhoni retires from the IPL",
        "Eisenkot tapped to form Israel\u2019s next government",
        "Four nations urge Israel to open Gaza aid routes",
        "North Korea fires missile into the Sea of Japan",
        "Cyber-attack hits supermarket freezers in 7 countries",
    ]
    iy = by + 38
    for item in items:
        d.ellipse([ax + 18, iy + 6, ax + 26, iy + 14], fill=NAVY)
        draw_text_block(d, ax + 34, iy, item, font(REG, 17), INK, aw - 52,
                        leading=21)
        iy += 19

    # ---- footer ------------------------------------------------------
    d.text((W // 2, 1000),
           "Reported 18 November 2026  \u2022  Sources: Reuters, NDTV, "
           "Al Jazeera, AP, France 24",
           font=font(REG, 11), fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
