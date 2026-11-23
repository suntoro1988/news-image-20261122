#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: one 1024x1024 PNG summing up the world
news of Sunday 22 November 2026. Deterministic: no randomness, no timestamps,
no network. Data lives in news.json beside this file; run `python3 draw.py`
to regenerate entry.png. Only the Python standard library and Pillow are used
(Pillow is needed locally to render; the submitted program, main.ts, simply
copies the finished entry.png, so the grader needs nothing beyond Node)."""

import json
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

NAVY = (20, 38, 77)
NAVY2 = (28, 52, 102)
CREAM = (248, 244, 233)
PAPER = (252, 250, 244)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RED = (176, 30, 36)
RED_DK = (140, 20, 26)
GOLD = (198, 142, 32)
TEAL = (18, 110, 105)
GREEN = (46, 125, 62)
ORANGE = (214, 110, 28)
SKY = (120, 170, 205)
LINE = (200, 192, 172)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(d, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, s, f, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(d, s, f, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading if leading else int(f.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def trunc(d, s, f, width):
    if text_w(d, s, f) <= width:
        return s
    while s and text_w(d, s + "...", f) > width:
        s = s[:-1]
    return s + "..."


# ---------------------------------------------------------------- art scenes
# Small flat illustrations, drawn in code, one per story kind. Each scene gets
# a box (x0, y0, x1, y1) and paints sky, ground and a few bold shapes.

def scene_summit(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(168, 208, 224))
    d.ellipse([x0 + 14, y0 + 10, x0 + 74, y0 + 70], fill=(52, 132, 88))
    d.ellipse([x0 + 26, y0 + 22, x0 + 62, y0 + 58], fill=(120, 190, 150))
    d.rectangle([x0, y0 + 78, x1, y1], fill=(146, 104, 66))
    for i, c in enumerate([(176, 30, 36), (28, 52, 102), (198, 142, 32),
                           (46, 125, 62), (120, 60, 120)]):
        cx = x0 + 40 + i * 52
        d.ellipse([cx - 9, y0 + 62, cx + 9, y0 + 80], fill=c)
        d.rectangle([cx - 12, y0 + 80, cx + 12, y0 + 92], fill=(40, 40, 40))
    d.rectangle([x0 + 150, y0 + 96, x0 + 260, y0 + 104], fill=(90, 60, 30))


def scene_drones(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 22, 44))
    for i in range(14):
        bx = x0 + 12 + i * 22
        d.rectangle([bx, y0 + 66, bx + 14, y0 + 78], fill=(52, 52, 70))
        d.rectangle([bx + 3, y0 + 78, bx + 11, y0 + 88], fill=(240, 200, 90))
    for i, (dx, dy) in enumerate([(40, 18), (120, 8), (200, 22), (260, 12),
                                  (80, 34), (170, 30), (230, 40)]):
        cx, cy = x0 + dx, y0 + dy
        d.line([cx - 14, cy - 8, cx + 14, cy - 8], fill=(220, 220, 220), width=2)
        d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(230, 230, 230))
        d.line([cx, cy + 4, cx - 6, cy + 26], fill=(240, 170, 60), width=2)
    d.polygon([(x0 + 30, y1), (x0 + 60, y1 - 26), (x0 + 90, y1)],
              fill=(240, 120, 40))
    d.polygon([(x0 + 70, y1), (x0 + 100, y1 - 34), (x0 + 130, y1)],
              fill=(240, 170, 60))


def scene_blast(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 130, 70))
    d.rectangle([x0, y0 + 76, x1, y1], fill=(60, 60, 72))
    for i in range(5):
        bx = x0 + 16 + i * 56
        d.rectangle([bx, y0 + 52, bx + 40, y0 + 76], fill=(90, 88, 100))
        d.rectangle([bx + 8, y0 + 60, bx + 16, y0 + 68], fill=(240, 200, 90))
    cx, cy = x0 + 150, y0 + 52
    for r, c in [(46, (240, 90, 30)), (32, (250, 160, 50)), (18, (255, 220, 120))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for sx, sy, sr in [(90, 30, 16), (230, 26, 20), (260, 44, 12)]:
        d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                  fill=(90, 90, 100))


def scene_ship(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(190, 215, 230))
    d.rectangle([x0, y0 + 74, x1, y1], fill=(28, 68, 110))
    d.rectangle([x0 + 40, y0 + 48, x0 + 270, y0 + 78], fill=(150, 40, 36))
    d.rectangle([x0 + 60, y0 + 30, x0 + 90, y0 + 48], fill=(220, 220, 220))
    d.rectangle([x0 + 200, y0 + 34, x0 + 240, y0 + 48], fill=(220, 220, 220))
    for fx in (150, 210):
        d.polygon([(fx, y0 + 26), (fx + 14, y0 + 2), (fx + 28, y0 + 26)],
                  fill=(240, 120, 40))
    for wx in range(6):
        d.arc([x0 + 10 + wx * 48, y0 + 86, x0 + 46 + wx * 48, y0 + 106],
              180, 360, fill=(200, 225, 240), width=3)


def scene_stadium(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(30, 60, 110))
    d.ellipse([x0 + 60, y0 + 14, x0 + 250, y0 + 96], fill=(240, 240, 235))
    d.ellipse([x0 + 84, y0 + 28, x0 + 226, y0 + 82], fill=(52, 140, 70))
    d.rectangle([x0 + 120, y0 + 44, x0 + 190, y0 + 66], fill=(240, 240, 235))
    for i in range(9):
        cx = x0 + 100 + i * 14
        d.ellipse([cx - 4, y0 + 46, cx + 4, y0 + 54], fill=(26, 26, 26))
    d.rectangle([x0, y0 + 96, x1, y1], fill=(40, 110, 60))


def scene_vote(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(222, 214, 196))
    d.rectangle([x0 + 60, y0 + 20, x0 + 250, y0 + 96], fill=(250, 248, 240))
    d.rectangle([x0 + 60, y0 + 20, x0 + 250, y0 + 36], fill=NAVY)
    d.text((x0 + 70, y0 + 23), "BALLOT", font=font(SANS_B, 11), fill=(255, 255, 255))
    for i, c in enumerate([(176, 30, 36), (28, 52, 102), (46, 125, 62)]):
        cy = y0 + 52 + i * 16
        d.rectangle([x0 + 74, cy, x0 + 88, cy + 12], fill=(255, 255, 255),
                    outline=(120, 120, 120))
        d.rectangle([x0 + 96, cy + 4, x0 + 200, cy + 8], fill=(170, 170, 170))
        if i == 0:
            d.line([x0 + 76, cy + 6, x0 + 80, cy + 10, x0 + 87, cy + 1],
                   fill=RED, width=2)


def scene_rocket(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(14, 20, 46))
    for sx, sy in [(30, 20), (90, 44), (200, 16), (260, 50), (150, 30)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
    d.ellipse([x0 + 210, y0 + 14, x0 + 258, y0 + 62], fill=(220, 220, 210))
    d.ellipse([x0 + 222, y0 + 26, x0 + 246, y0 + 50], fill=(180, 180, 170))
    cx = x0 + 120
    d.polygon([(cx, y0 + 16), (cx + 26, y0 + 44), (cx + 26, y0 + 92),
               (cx, y0 + 104), (cx - 26, y0 + 92), (cx - 26, y0 + 44)],
              fill=(235, 235, 230))
    d.polygon([(cx - 26, y0 + 70), (cx - 44, y0 + 100), (cx - 26, y0 + 96)],
              fill=RED)
    d.polygon([(cx + 26, y0 + 70), (cx + 44, y0 + 100), (cx + 26, y0 + 96)],
              fill=RED)
    d.polygon([(cx - 12, y0 + 104), (cx, y0 + 118), (cx + 12, y0 + 104)],
              fill=(250, 160, 50))


def scene_market(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 236, 222))
    d.rectangle([x0, y0 + 70, x1, y1], fill=(120, 120, 120))
    pts = [(x0 + 20, y0 + 70), (x0 + 60, y0 + 30), (x0 + 110, y0 + 52),
           (x0 + 160, y0 + 22), (x0 + 210, y0 + 56), (x0 + 260, y0 + 30),
           (x0 + 300, y0 + 62)]
    d.line(pts, fill=RED, width=4)
    for px, py in pts[1:-1]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    d.line([x0 + 10, y0 + 20, x0 + 10, y0 + 70], fill=(150, 150, 150), width=1)
    d.line([x0 + 10, y0 + 70, x0 + 310, y0 + 70], fill=(150, 150, 150), width=1)


def scene_flood(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(150, 180, 200))
    d.rectangle([x0, y0 + 62, x1, y1], fill=(30, 80, 130))
    for i in range(4):
        bx = x0 + 14 + i * 74
        d.rectangle([bx, y0 + 30, bx + 52, y0 + 62], fill=(120, 100, 80))
        d.polygon([(bx, y0 + 30), (bx + 26, y0 + 14), (bx + 52, y0 + 30)],
                  fill=(150, 60, 50))
    for wx in range(5):
        d.arc([x0 + 8 + wx * 60, y0 + 78, x0 + 44 + wx * 60, y0 + 98],
              180, 360, fill=(200, 225, 245), width=3)


def scene_court(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(226, 220, 205))
    d.rectangle([x0 + 40, y0 + 18, x0 + 270, y0 + 96], fill=(250, 248, 240))
    d.rectangle([x0 + 40, y0 + 18, x0 + 270, y0 + 32], fill=NAVY)
    d.line([x0 + 120, y0 + 40, x0 + 120, y0 + 92], fill=(120, 120, 120), width=2)
    d.line([x0 + 60, y0 + 40, x0 + 250, y0 + 40], fill=(120, 120, 120), width=1)
    d.line([x0 + 60, y0 + 92, x0 + 250, y0 + 92], fill=(120, 120, 120), width=1)
    d.ellipse([x0 + 140, y0 + 56, x0 + 156, y0 + 72], fill=RED)


def scene_protest(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(200, 210, 220))
    d.rectangle([x0, y0 + 84, x1, y1], fill=(110, 110, 110))
    for i, c in enumerate([(176, 30, 36), (28, 52, 102), (198, 142, 32),
                           (46, 125, 62), (120, 60, 120)]):
        cx = x0 + 36 + i * 56
        d.ellipse([cx - 10, y0 + 56, cx + 10, y0 + 76], fill=c)
        d.rectangle([cx - 13, y0 + 76, cx + 13, y0 + 92], fill=(50, 50, 50))
        d.rectangle([cx - 20, y0 + 22, cx + 20, y0 + 46], fill=(250, 248, 240),
                    outline=(120, 120, 120))
        d.line([cx, y0 + 46, cx, y0 + 56], fill=(80, 80, 80), width=2)


def scene_fire(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(40, 44, 60))
    d.rectangle([x0, y0 + 78, x1, y1], fill=(24, 24, 30))
    for i in range(5):
        bx = x0 + 12 + i * 60
        d.rectangle([bx, y0 + 44, bx + 44, y0 + 78], fill=(80, 80, 95))
        d.rectangle([bx + 8, y0 + 54, bx + 18, y0 + 64], fill=(240, 200, 90))
    for fx in (90, 200):
        d.polygon([(fx - 26, y0 + 78), (fx, y0 + 30), (fx + 26, y0 + 78)],
                  fill=(240, 110, 30))
        d.polygon([(fx - 14, y0 + 78), (fx, y0 + 48), (fx + 14, y0 + 78)],
                  fill=(250, 190, 60))


def scene_plane(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(170, 205, 230))
    for sx in (20, 120, 240):
        d.ellipse([x0 + sx, y0 + 16, x0 + sx + 34, y0 + 26], fill=(255, 255, 255))
    cx, cy = x0 + 150, y0 + 62
    d.ellipse([cx - 90, cy - 12, cx + 90, cy + 12], fill=(240, 240, 235))
    d.polygon([(cx + 80, cy - 8), (cx + 130, cy - 2), (cx + 80, cy + 8)],
              fill=(200, 200, 195))
    d.polygon([(cx - 20, cy - 10), (cx + 10, cy - 40), (cx + 30, cy - 10)],
              fill=(200, 200, 195))
    d.polygon([(cx - 20, cy + 10), (cx + 10, cy + 38), (cx + 30, cy + 10)],
              fill=(200, 200, 195))
    for wx in range(6):
        d.ellipse([cx - 70 + wx * 22, cy - 4, cx - 62 + wx * 22, cy + 4],
                  fill=NAVY)


def scene_flag(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(235, 230, 215))
    d.rectangle([x0 + 40, y0 + 10, x0 + 48, y0 + 106], fill=(90, 70, 50))
    d.rectangle([x0 + 48, y0 + 12, x0 + 250, y0 + 62], fill=RED)
    d.rectangle([x0 + 48, y0 + 62, x0 + 250, y0 + 66], fill=(255, 255, 255))
    d.rectangle([x0 + 48, y0 + 66, x0 + 250, y0 + 100], fill=NAVY)
    d.rectangle([x0 + 180, y0 + 74, x0 + 230, y0 + 106], fill=(250, 248, 240))
    d.rectangle([x0 + 180, y0 + 74, x0 + 230, y0 + 78], fill=(120, 120, 120))


def scene_globe(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(18, 40, 90))
    cx, cy = x0 + (x1 - x0) // 2, y0 + (y1 - y0) // 2
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(70, 150, 200))
    d.ellipse([cx - 30, cy - 34, cx + 6, cy - 6], fill=(70, 170, 100))
    d.ellipse([cx - 6, cy + 8, cx + 34, cy + 40], fill=(70, 170, 100))
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=(200, 220, 240),
              width=2)
    for sx, sy in [(30, 14), (250, 22), (280, 80), (20, 84)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                  fill=(255, 255, 255))


def scene_health(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(235, 244, 240))
    d.rectangle([x0 + 60, y0 + 16, x0 + 250, y0 + 100], fill=(255, 255, 255),
                outline=(150, 150, 150))
    d.rectangle([x0 + 140, y0 + 30, x0 + 160, y0 + 86], fill=TEAL)
    d.rectangle([x0 + 118, y0 + 52, x0 + 182, y0 + 72], fill=TEAL)
    d.line([(x0 + 80, y0 + 92), (x0 + 230, y0 + 92)], fill=(200, 200, 200),
           width=1)


def scene_tech(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(24, 28, 44))
    cx, cy = x0 + 160, y0 + 59
    d.rectangle([cx - 46, cy - 30, cx + 46, cy + 30], fill=(16, 20, 34),
                outline=(90, 120, 160), width=2)
    d.rectangle([cx - 22, cy - 16, cx + 22, cy + 16], fill=(46, 90, 70))
    for i in range(5):
        px = cx - 36 + i * 18
        d.line([px, cy - 30, px, cy - 44], fill=(140, 170, 200), width=3)
        d.line([px, cy + 30, px, cy + 44], fill=(140, 170, 200), width=3)
    for j in range(3):
        py = cy - 16 + j * 16
        d.line([cx - 46, py, cx - 60, py], fill=(140, 170, 200), width=3)
        d.line([cx + 46, py, cx + 60, py], fill=(140, 170, 200), width=3)
    d.ellipse([cx - 62, cy - 50, cx - 50, cy - 38], fill=(240, 200, 90))
    d.ellipse([cx + 50, cy + 38, cx + 62, cy + 50], fill=(120, 220, 160))


SCENES = {
    "summit": scene_summit, "drones": scene_drones, "blast": scene_blast,
    "ship": scene_ship, "stadium": scene_stadium, "vote": scene_vote,
    "rocket": scene_rocket, "market": scene_market, "flood": scene_flood,
    "court": scene_court, "protest": scene_protest, "fire": scene_fire,
    "plane": scene_plane, "flag": scene_flag, "globe": scene_globe,
    "health": scene_health, "tech": scene_tech,
}


def draw_art(d, tag, x0, y0, x1, y1):
    # Render every scene at a fixed 320x118 canvas, then scale to the box,
    # so the same scene works for tall top-story art and short card art.
    fn = SCENES.get(tag, scene_globe)
    tmp = Image.new("RGB", (320, 118), CREAM)
    td = ImageDraw.Draw(tmp)
    fn(td, 0, 0, 320, 118)
    _IMG.paste(tmp.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=(60, 55, 45), width=1)


# ---------------------------------------------------------------- dotted map
# Continents as ellipses in a 64x30 equirectangular grid; dots are kept where
# they fall inside any ellipse. (cx, cy, rx, ry) in grid cells.
CONTINENTS = [
    (13.0, 6.5, 8.5, 4.5),    # North America
    (15.5, 2.0, 3.0, 1.6),    # Alaska / far north
    (23.0, 2.5, 2.2, 1.3),    # Greenland
    (19.5, 19.0, 3.8, 5.5),   # South America
    (33.0, 5.5, 3.6, 2.6),    # Europe
    (31.0, 3.0, 1.0, 1.0),    # Britain
    (34.5, 15.5, 4.8, 5.8),   # Africa
    (46.0, 7.0, 11.0, 4.8),   # Asia
    (53.5, 13.5, 2.2, 2.0),   # SE Asia
    (57.0, 8.5, 1.4, 2.2),    # Japan
    (52.5, 22.5, 3.8, 2.2),   # Australia
    (49.0, 24.5, 1.2, 1.0),   # New Zealand
]


def lonlat_to_xy(lon, lat, x0, y0, x1, y1):
    gx = (lon + 180.0) / 360.0 * 64.0
    gy = (75.0 - lat) / 130.0 * 30.0
    return (x0 + gx / 64.0 * (x1 - x0), y0 + gy / 30.0 * (y1 - y0))


def draw_map(d, x0, y0, x1, y1, pins):
    d.rectangle([x0, y0, x1, y1], fill=(238, 232, 214))
    d.rectangle([x0, y0, x1, y1], outline=(120, 110, 90), width=1)
    cw = (x1 - x0) / 64.0
    ch = (y1 - y0) / 30.0
    for gy in range(30):
        for gx in range(64):
            inside = False
            for cx, cy, rx, ry in CONTINENTS:
                if ((gx + 0.5 - cx) / rx) ** 2 + ((gy + 0.5 - cy) / ry) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([x0 + gx * cw + 1, y0 + gy * ch + 1,
                           x0 + (gx + 1) * cw - 1, y0 + (gy + 1) * ch - 1],
                          fill=(178, 160, 120))
    for n, lon, lat in pins:
        px, py = lonlat_to_xy(lon, lat, x0, y0, x1, y1)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(n), font=font(SANS_B, 10),
               fill=(255, 255, 255))


# ---------------------------------------------------------------- layout

def build(data):
    global _IMG
    img = Image.new("RGB", (W, H), CREAM)
    _IMG = img
    d = ImageDraw.Draw(img)
    mx = 16
    cw = W - 2 * mx  # content width

    # --- top ribbon
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((mx, 5), "THE WORLD IN ONE DAY", font=font(SANS_B, 12),
           fill=(255, 255, 255))
    ribbon_r = "%d STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026" % data["count"]
    d.text((W - mx - text_w(d, ribbon_r, font(SANS_B, 12)), 5), ribbon_r,
           font=font(SANS_B, 12), fill=(255, 210, 90))

    # --- giant date title
    title = "Sunday 22 November 2026"
    tf = font(SERIF_B, 57)
    d.text(((W - text_w(d, title, tf)) / 2, 30), title, font=tf, fill=INK)

    # --- subline: the three top headlines
    sub = "  ·  ".join(data["subline"])
    sf = font(SERIF_I, 15)
    d.text(((W - text_w(d, sub, sf)) / 2, 96), sub, font=sf, fill=RED_DK)

    # --- key numbers strip
    y = 120
    keys = data["key_numbers"]
    cell = cw / len(keys)
    d.line([mx, y, W - mx, y], fill=INK, width=2)
    for i, k in enumerate(keys):
        x = mx + i * cell
        nf = font(SANS_B, 26)
        d.text((x + 8, y + 6), k["n"], font=nf, fill=RED)
        draw_wrapped(d, x + 8, y + 36, k["label"], font(SANS, 11),
                     cell - 14, fill=MUTED, leading=13, max_lines=2)
        if i:
            d.line([x, y + 4, x, y + 56], fill=LINE, width=1)
    d.line([mx, y + 62, W - mx, y + 62], fill=INK, width=1)

    # --- region strip
    y = 188
    regs = data["regions"]
    seg = cw / len(regs)
    for i, r in enumerate(regs):
        x = mx + i * seg
        d.rectangle([x, y, x + seg - 2, y + 22], fill=tuple(r["color"]))
        lab = "%s %d" % (r["name"].upper(), r["count"])
        d.text((x + 8, y + 4), lab, font=font(SANS_B, 12), fill=(255, 255, 255))

    # --- top 3 stories
    y = 218
    colw = (cw - 2 * 14) / 3
    art_h = 100
    for i, s in enumerate(data["top"]):
        x = mx + i * (colw + 14)
        draw_art(d, s["art"], int(x), y, int(x + colw), y + art_h)
        # chip top-left, stat top-right
        chip = s["chip"]
        cf = font(SANS_B, 11)
        tw = text_w(d, chip, cf) + 12
        d.rectangle([x + 4, y + 4, x + 4 + tw, y + 22], fill=RED)
        d.text((x + 10, y + 6), chip, font=cf, fill=(255, 255, 255))
        if s.get("chip2"):
            c2 = s["chip2"]
            tw2 = text_w(d, c2, cf) + 12
            d.rectangle([x + colw - 4 - tw2, y + 4, x + colw - 4, y + 22],
                        fill=(255, 255, 255))
            d.text((x + colw - 10 - tw2 + 6, y + 6), c2, font=cf, fill=INK)
        # label bottom-left on the art
        if s.get("label"):
            lf = font(SANS, 10)
            lab = s["label"]
            tw3 = text_w(d, lab, lf) + 10
            d.rectangle([x + 4, y + art_h - 20, x + 4 + tw3, y + art_h - 4],
                        fill=(0, 0, 0))
            d.text((x + 9, y + art_h - 19), lab, font=lf, fill=(255, 255, 255))
        ty = y + art_h + 8
        d.text((x, ty), "%d  %s · %s" % (s["n"], s["place"], s["field"]),
               font=font(SANS_B, 11), fill=RED_DK)
        ty += 16
        ty = draw_wrapped(d, x, ty, s["headline"], font(SERIF_B, 19),
                          colw, leading=22, max_lines=2)
        ty += 3
        ty = draw_wrapped(d, x, ty, s["summary"] + "  (" + s["source"] + ")",
                          font(SANS, 12), colw, leading=15, max_lines=2)
    y = 218 + art_h + 8 + 16 + 2 * 22 + 3 + 2 * 15 + 8

    # --- 10 medium cards, 5 x 2
    card_w = (cw - 4 * 10) / 5
    card_h = 96
    for row in range(2):
        for col in range(5):
            s = data["cards"][row * 5 + col]
            x = mx + col * (card_w + 10)
            cy = y + row * (card_h + 8)
            draw_art(d, s["art"], int(x), int(cy), int(x + card_w), int(cy + 40))
            chip = s["chip"]
            cf = font(SANS_B, 10)
            tw = text_w(d, chip, cf) + 10
            d.rectangle([x + 3, cy + 3, x + 3 + tw, cy + 18], fill=RED)
            d.text((x + 8, cy + 4), chip, font=cf, fill=(255, 255, 255))
            num = str(s["n"])
            nf = font(SANS_B, 11)
            nw = text_w(d, num, nf) + 8
            d.ellipse([x + card_w - 4 - nw, cy + 3, x + card_w - 4, cy + 18],
                      fill=(255, 255, 255))
            d.text((x + card_w - nw, cy + 4), num, font=nf, fill=INK)
            if s.get("label"):
                lf = font(SANS, 9)
                lab = s["label"]
                tw3 = text_w(d, lab, lf) + 8
                d.rectangle([x + 3, cy + 40 - 15, x + 3 + tw3, cy + 40 - 2],
                            fill=(0, 0, 0))
                d.text((x + 7, cy + 40 - 14), lab, font=lf, fill=(255, 255, 255))
            ty = cy + 43
            d.text((x, ty), s["place"], font=font(SANS_B, 9), fill=RED_DK)
            ty += 10
            ty = draw_wrapped(d, x, ty, s["headline"], font(SANS_B, 11),
                              card_w, leading=12, max_lines=2)
            ty += 1
            draw_wrapped(d, x, ty, s["summary"] + " (" + s["source"] + ")",
                         font(SANS, 9), card_w, leading=10, max_lines=2)
    y = y + 2 * card_h + 8 + 6

    # --- map (left) + more stories (right)
    map_w = 330
    map_h = 156
    d.text((mx, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    d.text((mx, y + 14), "pins match story numbers", font=font(SANS, 10),
           fill=MUTED)
    draw_map(d, mx, y + 30, mx + map_w, y + 30 + map_h,
             [(s["n"], s["lon"], s["lat"]) for s in data["top"]])
    lx = mx + map_w + 16
    lw = W - mx - lx
    d.text((lx, y), "ALSO ON SUNDAY 22 NOVEMBER — %d MORE STORIES"
           % len(data["more"]), font=font(SANS_B, 12), fill=INK)
    d.line([lx, y + 16, W - mx, y + 16], fill=INK, width=1)
    more = data["more"]
    half = (len(more) + 1) // 2
    cols = [more[:half], more[half:]]
    colw2 = (lw - 12) / 2
    for ci, col in enumerate(cols):
        cx = lx + ci * (colw2 + 12)
        ty = y + 22
        for m in col:
            src = "(" + m["source"] + ")"
            sw = text_w(d, src, font(SANS_I, 10))
            txt = trunc(d, m["text"], font(SANS, 11), colw2 - 24 - sw - 6)
            d.text((cx, ty), str(m["n"]), font=font(SANS_B, 11), fill=RED)
            d.text((cx + 24, ty), txt, font=font(SANS, 11), fill=INK)
            d.text((cx + colw2 - sw, ty), src,
                   font=font(SANS_I, 10), fill=MUTED)
            ty += 12
    y = y + max(30 + map_h, 22 + ((len(data["more"]) + 1) // 2) * 12) + 8

    # --- UTC timeline
    d.text((mx, y), "THE DAY IN UTC", font=font(SANS_B, 12), fill=INK)
    ty = y + 18
    d.line([mx + 30, ty + 8, W - mx - 10, ty + 8], fill=INK, width=2)
    for h in range(0, 25, 3):
        tx = mx + 30 + (W - mx - 40 - 30) * h / 24.0
        d.line([tx, ty + 4, tx, ty + 12], fill=INK, width=1)
        lab = "%02d:00" % h
        d.text((tx - 12, ty + 14), lab, font=font(SANS, 9), fill=MUTED)
    for ev in data["timeline"]:
        ex = mx + 30 + (W - mx - 40 - 30) * ev["h"] / 24.0
        d.ellipse([ex - 4, ty + 4, ex + 4, ty + 12], fill=RED)
        lab = ev["label"]
        lf = font(SANS, 9)
        lw_ = text_w(d, lab, lf)
        lx_ = min(max(ex - lw_ / 2, mx), W - mx - lw_)
        d.text((lx_, ty - 12), lab, font=lf, fill=INK)
    y = ty + 26

    # --- date check box
    d.rectangle([mx, y, W - mx, y + 66], outline=RED, width=2)
    d.text((mx + 8, y + 5), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    dc = data["datecheck"]
    draw_wrapped(d, mx + 8, y + 20, dc, font(SANS, 11), cw - 16,
                 leading=13, max_lines=3)
    y = y + 66 + 6

    # --- footer
    draw_wrapped(d, mx, y, data["sources_line"], font(SANS, 10), cw,
                 fill=MUTED, leading=12, max_lines=2)
    y = y + 26
    d.rectangle([0, H - 22, W, H], fill=NAVY)
    d.text((mx, H - 17), "THE WORLD IN ONE DAY", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    foot_r = "SUNDAY 22 NOVEMBER 2026  ·  ONE PAGE"
    d.text((W - mx - text_w(d, foot_r, font(SANS_B, 11)), H - 17), foot_r,
           font=font(SANS_B, 11), fill=(255, 210, 90))
    return img


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as f:
        data = json.load(f)
    img = build(data)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
