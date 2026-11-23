#!/usr/bin/env python3
"""Render the news-image-20261122 broadsheet front page (1024x1024 PNG).

Deterministic: no timestamps, no randomness, no network. Run twice and the
bytes are identical. Every headline/detail is measured before drawing; any
overflow aborts loudly instead of truncating.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
REPO = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(REPO, "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (18, 33, 61)
RED = (178, 34, 34)
ACCENT = (27, 94, 124)
GOLD = (176, 124, 20)
GREY = (90, 92, 96)
LIGHT = (233, 228, 216)
RULE = (150, 145, 130)

def F(path, size):
    return ImageFont.truetype(path, size)

# ---------------------------------------------------------------- stories
# head: bold one line. detail: one line. icon: pictogram kind.
# map: (lat, lon) plus badge offset (dx, dy) in px for the world map strip.
STORIES = [
    # lead (drawn large, not in the grid)
    dict(n=1, head="CLIMATE TALKS COLLAPSE",
         detail="COP31 ends with no deal after the longest UN climate summit ever",
         detail2="EU and island states reject a pact that never mentions fossil fuels",
         detail3="194 nations split; US absent after its pull-out from climate action",
         icon="globe", region="Global",
         map=(36.9, 30.7), moff=(-26, -14)),
    # secondary leads (drawn as wide cards, not in the grid)
    dict(n=2, head="Russian warship sunk off Libya",
         detail="Corvette Merkury capsizes in Benghazi",
         detail2="Sea drones hit; 6 sent, 4 stopped, 2 struck",
         icon="ship", region="Africa",
         map=(32.1, 20.1), moff=(-26, 12)),
    dict(n=3, head="Democrats take 258 House seats",
         detail="Biggest House majority since 1992",
         detail2="North Carolina recount by 330 votes over Foxx",
         icon="capitol", region="N. America",
         map=(38.9, -77.0), moff=(14, 12)),
    # grid stories 4..32
    dict(n=4, head="Strike hits Kyiv flats",
         detail="3 killed, 4 hurt; 11 feared trapped",
         icon="flame", region="Europe", map=(50.8, 30.4), moff=(26, -6)),
    dict(n=5, head="Cargo ship towed from Baltic",
         detail="Sparta II hit by drones, still burning",
         icon="ship", region="Europe", map=(59.9, 26.5), moff=(-24, -16)),
    dict(n=6, head="165 missiles in a week",
         detail="Kyiv urges US to release Patriots",
         icon="bolt", region="Europe", map=None, moff=None),
    dict(n=7, head="Bridge strikes fair response",
         detail="Cites 109 Russian hits on bridges",
         icon="shield", region="Europe", map=None, moff=None),
    dict(n=8, head="Lavrov: Kyiv is Russian land",
         detail='Calls Kyiv "ancestral Russian lands"',
         icon="flag", region="Europe", map=None, moff=None),
    dict(n=9, head="Settler arson condemned",
         detail="Eisenkot condemns West Bank attacks",
         icon="flame", region="Middle East", map=(31.9, 35.2), moff=(24, 14)),
    dict(n=10, head="Putin 'not America's friend'",
         detail="Intel chief Clayton breaks with Trump",
         icon="shield", region="N. America", map=None, moff=None),
    dict(n=11, head="Nvidia quizzed over China",
         detail="Bessent seeks answers on chips",
         icon="chip", region="N. America", map=None, moff=None),
    dict(n=12, head="Trump hosts meme-coin gala",
         detail="185 wallets qualify as coin slides",
         icon="coin", region="N. America", map=None, moff=None),
    dict(n=13, head="Schumer leadership fight",
         detail="Van Hollen runs; vote set for 1 Dec",
         icon="vote", region="N. America", map=None, moff=None),
    dict(n=14, head="Iowa blast to go ahead",
         detail="68 barrels of lead azide due by Tue",
         icon="alert", region="N. America", map=(41.9, -93.1), moff=(-20, -12)),
    dict(n=15, head="FBI probes database hack",
         detail="Apparent NCIC breach; scope unclear",
         icon="shield", region="N. America", map=None, moff=None),
    dict(n=16, head="Arrests at Seattle airport",
         detail="Travellers held; flight delayed",
         icon="plane", region="N. America", map=(47.6, -122.3), moff=(-16, -14)),
    dict(n=17, head="Biggest waves in years",
         detail="Coastal towns on alert for huge surf",
         icon="wave", region="N. America", map=(36.0, -121.0), moff=(-18, 12)),
    dict(n=18, head="El Chapo Isidro captured",
         detail="11 killed in Sinaloa raid; $5m reward",
         icon="star", region="Latin Am.", map=(25.6, -108.5), moff=(10, 14)),
    dict(n=19, head="Factory fire kills at least 3",
         detail="Dozens missing after Jakarta blaze",
         icon="factory", region="Asia-Pacific", map=(-6.1, 106.2), moff=(16, 12)),
    dict(n=20, head="Minister quits in exam row",
         detail="AI-cheating chaos at college test",
         icon="school", region="Asia-Pacific", map=(37.5, 127.0), moff=(16, -12)),
    dict(n=21, head="UK set for 2035 Women's Cup",
         detail="First UK World Cup since 1966 looms",
         icon="ball", region="Europe", map=(51.5, -0.1), moff=(-26, -14)),
    dict(n=22, head="Alcaraz wins first ATP Finals",
         detail="Beats No. 1 Zverev 6-2, 7-6 in Turin",
         icon="trophy", region="Europe", map=(45.1, 7.7), moff=(14, 14)),
    dict(n=23, head="Liverpool thrash Man Utd 4-0",
         detail="Debut ends in Anfield rout",
         icon="ball", region="Europe", map=(53.4, -3.0), moff=(-24, 14)),
    dict(n=24, head="Verstappen wins Las Vegas GP",
         detail="Vegas win; Norris 2nd, Piastri 3rd",
         icon="car", region="N. America", map=(36.2, -115.1), moff=(24, -6)),
    dict(n=25, head="Haugan wins Gurgl slalom",
         detail="Norway takes top two in Gurgl",
         icon="ski", region="Europe", map=(46.9, 11.0), moff=(18, -14)),
    dict(n=26, head="Miley Cyrus confirms wedding",
         detail="Weds Maxx Morando in Palm Springs",
         icon="rings", region="N. America", map=None, moff=None),
    dict(n=27, head="Paolo Bulgari dies aged 89",
         detail="Led the family firm for decades",
         icon="star", region="Europe", map=None, moff=None),
    dict(n=28, head="May 'aghast' at EU plans",
         detail="May: Brexit done; Tories to scrap it",
         icon="flag", region="Europe", map=None, moff=None),
    dict(n=29, head="Spitting Image creator dies",
         detail="Co-created the satirical puppet show",
         icon="mic", region="Europe", map=None, moff=None),
    dict(n=30, head="More tech outages ahead",
         detail="Upgrades will keep breaking systems",
         icon="bolt", region="N. America", map=None, moff=None),
    dict(n=31, head="Lebanon to hold all arms",
         detail="Aoun: era of outside weapons is over",
         icon="shield", region="Middle East", map=None, moff=None),
    dict(n=32, head="Weather foils intercept",
         detail="Gripen pilot cannot fire over Poland",
         icon="plane", region="Europe", map=None, moff=None),
]

MARKETS = [
    ("Dow", "48,147", "-1.9%"), ("S&P", "6,910", "-3.7%"),
    ("Nasdaq", "22,618", "-5.3%"), ("FTSE", "10,346", "-1.0%"),
    ("Brent", "$92.57", "+0.6%"), ("Gold", "$3,515", "-4.6%"),
]

# ---------------------------------------------------------------- icons
def icon(draw, kind, cx, cy, s, color):
    """Small vector pictogram centred on (cx, cy), box size s."""
    h = s / 2.0
    x0, y0, x1, y1 = cx - h, cy - h, cx + h, cy + h
    w = max(1, int(s / 9))
    if kind == "globe":
        draw.ellipse([x0, y0, x1, y1], outline=color, width=w)
        draw.ellipse([cx - h * 0.45, y0, cx + h * 0.45, y1], outline=color, width=max(1, w - 1))
        draw.line([x0, cy, x1, cy], fill=color, width=max(1, w - 1))
        draw.arc([x0, y0 + h * 0.5, x1, y1 - h * 0.5], 200, 340, fill=color, width=max(1, w - 1))
    elif kind == "ship":
        draw.polygon([(x0, cy + h * 0.2), (x1, cy + h * 0.2), (x1 - h * 0.3, y1),
                      (x0 + h * 0.3, y1)], fill=color)
        draw.line([cx, y0 + h * 0.2, cx, cy + h * 0.2], fill=color, width=w)
        draw.polygon([(cx, y0), (cx + h * 0.7, cy - h * 0.1), (cx, cy - h * 0.1)], fill=color)
        draw.line([x0, y1 + 1, x1, y1 + 1], fill=color, width=max(1, w - 1))
    elif kind == "capitol":
        draw.arc([cx - h * 0.7, y0, cx + h * 0.7, cy + h * 0.2], 180, 360, fill=color, width=w)
        draw.line([cx, y0 - 2, cx, y0 + 2], fill=color, width=w)
        for dx in (-0.55, -0.18, 0.18, 0.55):
            draw.line([cx + dx * h, cy, cx + dx * h, y1], fill=color, width=max(1, w - 1))
        draw.line([x0, y1, x1, y1], fill=color, width=w)
    elif kind == "flame":
        draw.polygon([(cx, y0), (cx + h * 0.7, cy), (cx + h * 0.4, cy + h * 0.3),
                      (cx + h * 0.75, y1), (cx - h * 0.75, y1), (cx - h * 0.4, cy + h * 0.3),
                      (cx - h * 0.7, cy)], fill=color)
    elif kind == "bolt":
        draw.polygon([(cx + h * 0.2, y0), (cx - h * 0.5, cy + h * 0.2), (cx - h * 0.05, cy + h * 0.2),
                      (cx - h * 0.2, y1), (cx + h * 0.5, cy - h * 0.1), (cx + h * 0.05, cy - h * 0.1)],
                     fill=color)
    elif kind == "chip":
        draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], outline=color, width=w)
        draw.rectangle([cx - h * 0.35, cy - h * 0.35, cx + h * 0.35, cy + h * 0.35],
                       outline=color, width=max(1, w - 1))
        for dx in (-0.5, 0, 0.5):
            draw.line([cx + dx * h, y0, cx + dx * h, y0 + 3], fill=color, width=max(1, w - 1))
            draw.line([cx + dx * h, y1 - 3, cx + dx * h, y1], fill=color, width=max(1, w - 1))
    elif kind == "coin":
        draw.ellipse([x0, y0, x1, y1], outline=color, width=w)
        draw.text((cx, cy), "$", font=F(SANS_B, int(s * 0.62)), fill=color, anchor="mm")
    elif kind == "vote":
        draw.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], outline=color, width=w)
        draw.line([x0 + h * 0.25, cy, cx - h * 0.1, y1 - h * 0.25], fill=color, width=w)
        draw.line([cx - h * 0.1, y1 - h * 0.25, x1 - h * 0.2, y0 + h * 0.3], fill=color, width=w)
    elif kind == "alert":
        draw.polygon([(cx, y0), (x1, y1), (x0, y1)], outline=color, width=w)
        draw.line([cx, cy - h * 0.4, cx, cy + h * 0.3], fill=color, width=w)
        draw.point((cx, y1 - h * 0.2), fill=color)
    elif kind == "factory":
        draw.rectangle([x0, cy, x1 - h * 0.4, y1], outline=color, width=max(1, w - 1))
        draw.rectangle([x1 - h * 0.5, y0 + h * 0.3, x1 - h * 0.1, y1], fill=color)
        draw.line([x0, y1, x1, y1], fill=color, width=w)
    elif kind == "school":
        draw.polygon([(x0, cy), (cx, y0), (x1, cy), (cx, cy + h * 0.5)], outline=color, width=w)
        draw.line([cx + h * 0.6, cy, cx + h * 0.6, y1], fill=color, width=max(1, w - 1))
        draw.line([x0 + h * 0.2, y1, x1 - h * 0.2, y1], fill=color, width=max(1, w - 1))
    elif kind == "trophy":
        draw.arc([x0 + h * 0.2, y0, x1 - h * 0.2, cy + h * 0.6], 0, 180, fill=color, width=w)
        draw.line([cx - h * 0.3, cy + h * 0.5, cx + h * 0.3, cy + h * 0.5], fill=color, width=w)
        draw.line([cx, cy + h * 0.5, cx, y1], fill=color, width=w)
        draw.line([cx - h * 0.4, y1, cx + h * 0.4, y1], fill=color, width=w)
    elif kind == "ball":
        draw.ellipse([x0, y0, x1, y1], outline=color, width=w)
        draw.polygon([(cx, cy - h * 0.35), (cx + h * 0.35, cy - h * 0.1), (cx + h * 0.2, cy + h * 0.35),
                      (cx - h * 0.2, cy + h * 0.35), (cx - h * 0.35, cy - h * 0.1)], fill=color)
    elif kind == "car":
        draw.polygon([(x0 + h * 0.1, cy), (cx - h * 0.3, y0 + h * 0.4), (cx + h * 0.3, y0 + h * 0.4),
                      (x1 - h * 0.1, cy), (x1, y1 - h * 0.2), (x0, y1 - h * 0.2)], fill=color)
        draw.ellipse([x0 + h * 0.2, y1 - h * 0.5, x0 + h * 0.7, y1], fill=INK)
        draw.ellipse([x1 - h * 0.7, y1 - h * 0.5, x1 - h * 0.2, y1], fill=INK)
    elif kind == "ski":
        draw.polygon([(cx, y1), (cx + h * 0.7, cy), (x1, cy), (cx, y0)], fill=color)
        draw.line([x0, y1, x1, y1 - h * 0.3], fill=color, width=w)
    elif kind == "rings":
        draw.ellipse([x0, y0, cx + h * 0.2, cy + h * 0.2], outline=color, width=w)
        draw.ellipse([cx - h * 0.2, cy - h * 0.2, x1, y1], outline=color, width=w)
    elif kind == "star":
        pts = []
        import math
        for i in range(10):
            r = h if i % 2 == 0 else h * 0.45
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, fill=color)
    elif kind == "flag":
        draw.line([cx - h * 0.5, y0, cx - h * 0.5, y1], fill=color, width=w)
        draw.polygon([(cx - h * 0.5, y0), (x1, y0 + h * 0.35), (cx - h * 0.5, y0 + h * 0.7)], fill=color)
    elif kind == "wave":
        for k, yy in enumerate((cy - h * 0.45, cy, cy + h * 0.45)):
            draw.arc([x0, yy - h * 0.4, cx, yy + h * 0.4], 270, 90, fill=color, width=max(1, w - 1))
            draw.arc([cx, yy - h * 0.4, x1, yy + h * 0.4], 90, 270, fill=color, width=max(1, w - 1))
    elif kind == "plane":
        draw.polygon([(x0, cy), (x1, cy - h * 0.5), (cx + h * 0.2, cy), (x1, cy + h * 0.5)], fill=color)
        draw.line([cx, cy - h * 0.7, cx + h * 0.3, cy], fill=color, width=max(1, w - 1))
    elif kind == "mic":
        draw.ellipse([cx - h * 0.45, y0, cx + h * 0.45, cy + h * 0.3], outline=color, width=w)
        draw.line([cx, cy + h * 0.3, cx, y1], fill=color, width=w)
        draw.line([cx - h * 0.4, y1, cx + h * 0.4, y1], fill=color, width=max(1, w - 1))
    elif kind == "shield":
        draw.polygon([(cx - h * 0.7, y0), (cx + h * 0.7, y0), (cx + h * 0.7, cy),
                      (cx, y1), (cx - h * 0.7, cy)], outline=color, width=w)
        draw.line([cx - h * 0.3, cy, cx, cy + h * 0.3], fill=color, width=max(1, w - 1))
        draw.line([cx, cy + h * 0.3, cx + h * 0.35, cy - h * 0.35], fill=color, width=max(1, w - 1))
    else:
        draw.ellipse([x0, y0, x1, y1], outline=color, width=w)

# ---------------------------------------------------------------- map
CONTINENTS = [
    # North America (rough)
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-92, 15), (-97, 16), (-105, 20),
     (-112, 28), (-120, 34), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-168, 66)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -25), (-77, -12), (-80, 10)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12),
     (51, 11), (40, -5), (35, -18), (32, -28), (20, -35), (12, -18), (9, -1), (-8, 4), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 49), (0, 51), (5, 58), (10, 59), (18, 56), (21, 55),
     (28, 60), (30, 70), (45, 68), (60, 69), (80, 73), (100, 76), (130, 72), (160, 70),
     (178, 65), (162, 60), (142, 50), (140, 40), (127, 35), (120, 30), (108, 20),
     (100, 8), (95, 16), (90, 22), (80, 20), (72, 20), (66, 25), (57, 26), (52, 28),
     (48, 30), (44, 29), (36, 36), (30, 36), (26, 38), (22, 37), (19, 42), (12, 44),
     (8, 44), (3, 43), (-2, 37), (-9, 37), (-10, 36)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19), (150, -23), (153, -27),
     (150, -37), (140, -38), (132, -32), (124, -33), (115, -35), (114, -22)],
]

def project(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (75.0 - lat) / 130.0 * mh
    return x, y

# ---------------------------------------------------------------- fit check
def fit_check():
    """Measure every line; abort on any overflow. Returns a report list."""
    report = []
    f_head = F(SANS_B, 15)
    f_det = F(SANS, 15)
    grid_w = 312  # column width
    text_w = grid_w - 22  # icon + gap
    worst = 0.0
    for s in STORIES[3:]:
        num = "%02d " % s["n"]
        hw = F(SANS_B, 15).getlength(num + s["head"])
        dw = f_det.getlength(s["detail"])
        worst = max(worst, hw / text_w, dw / text_w)
        if hw > text_w:
            raise SystemExit("FIT FAIL headline #%d too wide: %.0f > %.0f : %s"
                             % (s["n"], hw, text_w, s["head"]))
        if dw > text_w:
            raise SystemExit("FIT FAIL detail #%d too wide: %.0f > %.0f : %s"
                             % (s["n"], dw, text_w, s["detail"]))
    # lead
    f_lead = F(SANS_B, 30)
    if f_lead.getlength(STORIES[0]["head"]) > 640:
        raise SystemExit("FIT FAIL lead headline too wide")
    for k in ("detail", "detail2", "detail3"):
        if F(SANS, 16).getlength(STORIES[0][k]) > 640:
            raise SystemExit("FIT FAIL lead %s too wide" % k)
    # secondary cards
    for s in STORIES[1:3]:
        if F(SANS_B, 17).getlength(s["head"]) > 380:
            raise SystemExit("FIT FAIL secondary headline #%d" % s["n"])
        for k in ("detail", "detail2"):
            if F(SANS, 15).getlength(s[k]) > 380:
                raise SystemExit("FIT FAIL secondary %s #%d" % (k, s["n"]))
    report.append("fit: 29 grid stories, 0 truncated; worst width ratio %.2f" % worst)
    return report

# ---------------------------------------------------------------- drawing
def draw_lead_art(d, x, y, w, h):
    """Cracked globe for the COP31 lead."""
    cx, cy, r = x + w // 2, y + h // 2 + 4, min(w, h) // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(173, 216, 230), outline=NAVY, width=3)
    # land blobs
    d.ellipse([cx - r * 0.75, cy - r * 0.55, cx - r * 0.1, cy + r * 0.1], fill=(74, 140, 74))
    d.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.7, cy + r * 0.6], fill=(74, 140, 74))
    d.ellipse([cx - r * 0.2, cy - r * 0.85, cx + r * 0.45, cy - r * 0.35], fill=(96, 160, 96))
    # latitude lines
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=NAVY, width=1)
    d.arc([cx - r, cy + r * 0.1, cx + r, cy + r * 0.75], 180, 360, fill=NAVY, width=1)
    d.ellipse([cx - r * 0.35, cy - r, cx + r * 0.35, cy + r], outline=NAVY, width=1)
    # jagged crack
    crack = [(cx - r * 0.15, cy - r), (cx + r * 0.1, cy - r * 0.5), (cx - r * 0.2, cy - r * 0.1),
             (cx + r * 0.15, cy + r * 0.25), (cx - r * 0.1, cy + r * 0.6), (cx + r * 0.05, cy + r)]
    d.line(crack, fill=RED, width=4, joint="curve")
    # NO DEAL ribbon
    d.rectangle([x, y + h - 30, x + w, y + h - 4], fill=RED)
    d.text((x + w / 2, y + h - 17), "NO DEAL", font=F(SANS_B, 17), fill=(255, 255, 255), anchor="mm")

def draw_secondary_art(d, kind, x, y, w, h):
    if kind == "ship":
        d.polygon([(x + 6, y + h * 0.62), (x + w - 6, y + h * 0.62), (x + w - 16, y + h - 8),
                   (x + 16, y + h - 8)], fill=NAVY)
        d.rectangle([x + w * 0.42, y + 8, x + w * 0.58, y + h * 0.62], fill=NAVY)
        d.polygon([(x + w * 0.58, y + 10), (x + w * 0.86, y + h * 0.3), (x + w * 0.58, y + h * 0.3)],
                  fill=RED)
        for i in range(3):
            yy = y + h - 4 + i * 3
            d.line([x, yy, x + w, yy], fill=ACCENT, width=1)
        d.text((x + w / 2, y + h * 0.78), "MERKURY", font=F(SANS_B, 10), fill=(255, 255, 255),
               anchor="mm")
    else:  # capitol dome
        d.arc([x + w * 0.2, y + 4, x + w * 0.8, y + h * 0.55], 180, 360, fill=NAVY, width=3)
        d.line([x + w * 0.5, y + 2, x + w * 0.5, y + 8], fill=NAVY, width=2)
        for i, dx in enumerate((-0.36, -0.12, 0.12, 0.36)):
            d.line([x + w * (0.5 + dx), y + h * 0.5, x + w * (0.5 + dx), y + h - 8],
                   fill=NAVY, width=3)
        d.line([x + 4, y + h - 6, x + w - 4, y + h - 6], fill=NAVY, width=3)
        d.text((x + w / 2, y + h * 0.32), "258", font=F(SANS_B, 20), fill=RED, anchor="mm")

def render():
    report = fit_check()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((MARGIN, 14), "THE WORLD IN ONE DAY", font=F(SERIF_B, 40), fill=(247, 243, 234))
    d.text((W - MARGIN, 22), "No. 22  \u00b7  $100 bounty", font=F(SANS, 14), fill=(200, 205, 215),
           anchor="ra")
    d.line([MARGIN, 66, W - MARGIN, 66], fill=(120, 130, 150), width=1)
    d.text((MARGIN, 76), "SUNDAY 22 NOVEMBER 2026", font=F(SANS_B, 46), fill=(255, 214, 90))
    d.text((MARGIN, 128), "32 dated stories  \u00b7  7 regions  \u00b7  Every figure checked against two sources",
           font=F(SANS, 14), fill=(200, 205, 215))
    d.text((W - MARGIN, 128), "Events of 22 Nov, or first reported that day",
           font=F(SANS, 13), fill=(170, 175, 190), anchor="ra")

    # ---- lead
    lead = STORIES[0]
    d.rectangle([MARGIN, 158, W - MARGIN, 330], fill=(255, 255, 255), outline=RULE, width=1)
    d.text((MARGIN + 14, 168), "1  LEAD", font=F(SANS_B, 13), fill=RED)
    d.text((MARGIN + 14, 188), lead["head"], font=F(SANS_B, 30), fill=INK)
    yy = 232
    for k in ("detail", "detail2", "detail3"):
        d.text((MARGIN + 14, yy), lead[k], font=F(SANS, 16), fill=(40, 44, 54))
        yy += 24
    d.text((MARGIN + 14, 306), "Antalya, Turkey \u2014 the Antalya Pact never reached consensus",
           font=F(SANS, 13), fill=GREY)
    draw_lead_art(d, 700, 166, 280, 156)

    # ---- secondary cards
    sy, sh = 340, 88
    card_w = (W - 2 * MARGIN - 16) // 2
    for i, s in enumerate(STORIES[1:3]):
        x = MARGIN + i * (card_w + 16)
        d.rectangle([x, sy, x + card_w, sy + sh], fill=(255, 255, 255), outline=RULE, width=1)
        d.text((x + 12, sy + 8), "%d" % s["n"], font=F(SANS_B, 15), fill=RED)
        d.text((x + 34, sy + 8), s["head"], font=F(SANS_B, 17), fill=INK)
        d.text((x + 12, sy + 34), s["detail"], font=F(SANS, 15), fill=(40, 44, 54))
        d.text((x + 12, sy + 56), s["detail2"], font=F(SANS, 15), fill=(40, 44, 54))
        draw_secondary_art(d, s["icon"], x + card_w - 92, sy + 8, 80, sh - 16)

    # ---- grid of stories 4..32
    grid = STORIES[3:]
    gy0, gy1 = 438, 818
    cols = 3
    col_w = (W - 2 * MARGIN - (cols - 1) * 16) // cols
    per_col = [10, 10, 9]
    idx = 0
    f_num = F(SANS_B, 15)
    f_head = F(SANS_B, 15)
    f_det = F(SANS, 15)
    row_h = (gy1 - gy0) / 10
    for c in range(cols):
        x = MARGIN + c * (col_w + 16)
        for r in range(per_col[c]):
            s = grid[idx]
            idx += 1
            y = gy0 + r * row_h
            icon(d, s["icon"], x + 9, y + 11, 18, ACCENT)
            tx = x + 22
            d.text((tx, y + 1), "%02d " % s["n"], font=f_num, fill=RED)
            nw = f_num.getlength("%02d " % s["n"])
            d.text((tx + nw, y + 1), s["head"], font=f_head, fill=INK)
            d.text((tx, y + 20), s["detail"], font=f_det, fill=(52, 56, 66))
            if r < per_col[c] - 1:
                d.line([x, y + row_h - 2, x + col_w, y + row_h - 2], fill=(220, 215, 200), width=1)
    d.line([MARGIN, gy1 + 4, W - MARGIN, gy1 + 4], fill=RULE, width=1)

    # ---- world map strip (correct-aspect inset + side panels)
    d.text((MARGIN, 830), "WHERE IT HAPPENED \u2014 numbers match the stories above",
           font=F(SANS_B, 13), fill=NAVY)
    d.text((MARGIN, 850), "BY REGION", font=F(SANS_B, 13), fill=RED)
    regions = [("N. America", 12), ("Europe", 13), ("Middle East", 2),
               ("Asia-Pacific", 2), ("Latin Am.", 1), ("Africa", 1), ("Global", 1)]
    for i, (name, cnt) in enumerate(regions):
        col = i // 4
        row = i % 4
        x = MARGIN + col * 150
        y = 870 + row * 17
        d.text((x, y), "%s  %d" % (name, cnt), font=F(SANS, 13), fill=(52, 56, 66))
    d.text((684, 850), "THE DAY IN NUMBERS", font=F(SANS_B, 13), fill=RED)
    numbers = ["258  House seats for Democrats",
               "165  missiles fired at Ukraine in a week",
               "6  sea drones at the Merkury; 2 hit",
               "68  barrels of lead azide in Iowa"]
    for i, line in enumerate(numbers):
        d.text((684, 870 + i * 17), line, font=F(SANS, 13), fill=(52, 56, 66))
    mx, my, mw, mh = 354, 846, 316, 114
    d.rectangle([mx - 4, my - 4, mx + mw + 4, my + mh + 4], fill=(235, 231, 220),
                outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(196, 205, 190), outline=(120, 128, 118))
    f_map = F(SANS_B, 10)
    for s in STORIES:
        if s["map"] is None:
            continue
        lat, lon = s["map"]
        px, py = project(lon, lat, mx, my, mw, mh)
        dx, dy = s["moff"]
        bx, by = px + dx, py + dy
        d.line([px, py, bx, by], fill=GREY, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=NAVY, outline=(255, 255, 255), width=1)
        d.text((bx, by), str(s["n"]), font=f_map, fill=(255, 255, 255), anchor="mm")

    # ---- markets strip
    my2 = 968
    d.rectangle([MARGIN, my2, W - MARGIN, my2 + 32], fill=NAVY)
    f_mk = F(SANS_B, 11)
    d.text((MARGIN + 10, my2 + 10), "MARKETS \u2014 FRI 20 NOV:",
           font=f_mk, fill=(255, 214, 90))
    x = MARGIN + 178
    for name, val, chg in MARKETS:
        col = (255, 120, 120) if chg.startswith("-") else (120, 220, 140)
        base = "%s %s " % (name, val)
        d.text((x, my2 + 10), base, font=f_mk, fill=(247, 243, 234))
        d.text((x + f_mk.getlength(base), my2 + 10), chg, font=f_mk, fill=col)
        x += f_mk.getlength(base + chg) + 10

    # ---- footer
    d.text((MARGIN, 1006), "Sources: Reuters, BBC, AP, CNN, WSJ, Kyiv Independent \u00b7 Figures as reported on 22 Nov 2026 \u00b7 Markets: Fri 20 Nov close (last trading day)",
           font=F(SANS, 12), fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    report.append("rendered %s (%d bytes)" % (OUT, size))
    if size > 1048576:
        raise SystemExit("SIZE FAIL: %d bytes over hard limit" % size)
    return report

if __name__ == "__main__":
    for line in render():
        print(line)
