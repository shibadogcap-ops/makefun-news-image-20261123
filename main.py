import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.environ.get("MAKEFUN_BOT_DIR", ".")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import math

from draw import Canvas
from font import draw_text, draw_wrapped, text_width

PAPER = (250, 247, 238)
INK = (22, 22, 22)
RED = (178, 34, 34)
GREY = (110, 105, 95)
BLUE = (70, 110, 150)
PALE = (225, 232, 238)


def build() -> Canvas:
    cv = Canvas(1024, 1024, bg=PAPER)

    # -- masthead ---------------------------------------------------------
    cv.rect(36, 22, 988 - 36, 2, INK)
    cv.rect(36, 106, 988 - 36, 1, INK)
    draw_text(cv, 512, 34, "THE WORLD GAZETTE", 56, INK, weight=3, align='center')

    # -- date band --------------------------------------------------------
    cv.rect(36, 114, 988 - 36, 40, INK)
    draw_text(cv, 512, 120, "MONDAY 23 NOVEMBER 2026", 29, PAPER, weight=2, align='center')
    draw_text(cv, 48, 128, "VOL. I - NO. 23", 13, PAPER, align='left')
    draw_text(cv, 976, 128, "ONE IMAGE - ALL THE NEWS", 13, PAPER, align='right')

    # -- lead story: COP31 -------------------------------------------------
    draw_text(cv, 36, 170, "CLIMATE - ANTALYA, TURKIYE", 17, RED, weight=2)
    draw_text(cv, 36, 196, "COP31 CLIMATE SUMMIT", 50, INK, weight=3)
    draw_text(cv, 36, 196 + 62, "COLLAPSES, NO DEAL", 50, INK, weight=3)
    draw_wrapped(cv, 36, 330,
                 "The longest climate summit in history ends in Antalya "
                 "without a deal, as the EU and its allies reject a final "
                 "pact that never mentions fossil fuels - the first "
                 "breakdown since Copenhagen in 2009.",
                 19, INK, 560, weight=2, line_gap=1.3)

    # globe visual
    cx, cy, r = 796, 356, 92
    cv.disc(cx, cy, r, PALE)
    cv.ring(cx, cy, r, INK, t=2)
    for f in (-0.66, -0.33, 0, 0.33, 0.66):
        rx = r * abs(f)
        pts = []
        for i in range(49):
            t = 2 * math.pi * i / 48
            pts.append((cx + rx * math.cos(t), cy + r * math.sin(t)))
        for i in range(len(pts) - 1):
            cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], BLUE, 1)
    for dy in (-46, 0, 46):
        rx = math.sqrt(max(0.0, r * r - dy * dy))
        ry = 18.0
        pts = []
        for i in range(49):
            t = 2 * math.pi * i / 48
            pts.append((cx + rx * math.cos(t), cy + dy + ry * math.sin(t)))
        for i in range(len(pts) - 1):
            cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], BLUE, 1)
    crack = [(748, 282), (786, 322), (770, 356), (806, 392), (792, 428)]
    for i in range(len(crack) - 1):
        cv.line(crack[i][0], crack[i][1], crack[i + 1][0], crack[i + 1][1], RED, 3)
    draw_text(cv, 796, 458, "THE ANTALYA TALKS", 13, GREY, align='center')

    # -- row 2 ------------------------------------------------------------
    cv.rect(512, 486, 1, 650 - 486, INK)

    draw_text(cv, 36, 486, "UKRAINE", 15, RED, weight=2)
    draw_wrapped(cv, 36, 510, "RUSSIAN STRIKES KILL 11 IN KYIV REGION",
                 27, INK, 452, weight=2, line_gap=1.15)
    draw_wrapped(cv, 36, 596,
                 "Ukraine says Russian strikes on the Kyiv region killed "
                 "11 people. The village of Dymer, north of the capital, "
                 "was among the places hit.",
                 15.5, INK, 452, weight=2, line_gap=1.3)

    draw_text(cv, 536, 486, "MARKETS", 15, RED, weight=2)
    draw_wrapped(cv, 536, 510, "AI SELL-OFF RATTLES WORLD MARKETS",
                 27, INK, 452, weight=2, line_gap=1.15)
    draw_wrapped(cv, 536, 596,
                 "The S&P 500 falls 3.7% and Tokyo's Nikkei 5.06% as "
                 "investors dump AI shares. Gold jumps 2.72%; Brent "
                 "crude holds near 90 dollars a barrel.",
                 15.5, INK, 452, weight=2, line_gap=1.3)

    # --- bottom half ---
    # Row 3 rules
    cv.rect(36, 690, 988 - 36, 1, INK)
    cv.rect(512, 700, 1, 876 - 700, INK)

    # Row 3 - Sudan
    draw_text(cv, 36, 700, "SUDAN", 15, RED, weight=2)
    draw_wrapped(cv, 36, 724, "DRONES HIT HOMES, U.N. BUILDING IN KHARTOUM",
                 24, INK, 452, weight=2, line_gap=1.15)
    draw_wrapped(cv, 36, 796,
                 "Drone strikes hit homes and a U.N. building in the "
                 "capital; five children were killed in attacks in "
                 "Khartoum and Omdurman.",
                 15.5, INK, 452, weight=2, line_gap=1.3)

    # Row 3 - United States
    draw_text(cv, 536, 700, "UNITED STATES", 15, RED, weight=2)
    draw_wrapped(cv, 536, 724,
                 "DEMOCRATS WIN BIGGEST HOUSE MAJORITY SINCE 1992",
                 24, INK, 452, weight=2, line_gap=1.15)
    draw_wrapped(cv, 536, 796,
                 "Democrats secure at least 258 seats in the House of "
                 "Representatives - the party's largest majority since "
                 "1992 - reshaping Washington's balance of power.",
                 15.5, INK, 452, weight=2, line_gap=1.3)

    # Row 4 rules
    cv.rect(36, 890, 988 - 36, 1, INK)
    cv.rect(348, 898, 1, 978 - 898, INK)
    cv.rect(668, 898, 1, 978 - 898, INK)

    # Row 4 - compact items
    draw_text(cv, 36, 898, "LIBYA", 13, RED, weight=2)
    draw_wrapped(cv, 36, 918,
                 "BLAST ROCKS BENGHAZI NAVAL BASE; U.N. SEEKS PROBE "
                 "OF SHIP ATTACK",
                 16.5, INK, 300, weight=2, line_gap=1.2)

    draw_text(cv, 356, 898, "INDONESIA", 13, RED, weight=2)
    draw_wrapped(cv, 356, 918,
                 "34 MISSING AFTER FIRE GUTS INDONESIA CANDY FACTORY",
                 16.5, INK, 300, weight=2, line_gap=1.2)

    draw_text(cv, 676, 898, "SOUTH SUDAN", 13, RED, weight=2)
    draw_wrapped(cv, 676, 918,
                 "PARAMILITARY ATTACK KILLS 24 CIVILIANS",
                 16.5, INK, 308, weight=2, line_gap=1.2)

    # Footer
    cv.rect(36, 986, 988 - 36, 1, INK)
    draw_text(cv, 512, 990,
              "IN BRIEF - ALCARAZ BEATS ZVEREV FOR FIRST ATP FINALS "
              "TITLE - THANKSGIVING AIR TEAM ON GUARD",
              12.5, GREY, weight=2, align='center')
    draw_text(cv, 512, 1005,
              "MARQUEZ TAKES EIGHTH MOTOGP CROWN - FIGHTING DISRUPTS "
              "EBOLA RESPONSE IN DR CONGO",
              12.5, GREY, weight=2, align='center')

    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.png")
    build().save(path)


if __name__ == "__main__":
    main()
