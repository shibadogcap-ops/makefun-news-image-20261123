"""Stroke (vector) font renderer on top of draw.Canvas. Stdlib only.

Glyphs live in a 10x14 unit cell: x runs 0..10 left to right,
y runs 0 (cap height) .. 14 (baseline), y down. Each glyph is a
list of strokes; each stroke is a list of (x, y) points.
"""

import math

from draw import Canvas


# -- stroke builders ---------------------------------------------------------

def ln(a, b):
    """Two-point stroke from a to b."""
    return [tuple(a), tuple(b)]


def arc(cx, cy, rx, ry, a0, a1, n=12):
    """Points along an elliptical arc. Angles in radians, y down."""
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts


def bez(p0, p1, p2, p3, n=12):
    """Points along a cubic Bezier curve."""
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = (u ** 3 * p0[0] + 3 * u * u * t * p1[0] +
             3 * u * t * t * p2[0] + t ** 3 * p3[0])
        y = (u ** 3 * p0[1] + 3 * u * u * t * p1[1] +
             3 * u * t * t * p2[1] + t ** 3 * p3[1])
        pts.append((x, y))
    return pts


def _dot(cx, cy, r=0.9):
    """Small circle used for ., ,, :, ;, !"""
    return [arc(cx, cy, r, r, 0, 2 * math.pi, n=10)]


# Strokes of the uppercase S, reused to build the lowercase s.
_S_STROKES = [
    arc(5, 3.5, 4, 3.5, -math.pi / 4, -3 * math.pi / 2, n=22),
    ln((5, 7), (6.7, 7.33)),
    arc(5, 10.5, 4, 3.5, 5.15, 8.3, n=22),
]


def _xheight(strokes):
    """Fit a cap-height glyph (y 0..14) into the x-height body (y 5..14)."""
    return [[(1.5 + (x - 1) * 0.875, 5 + y * 9 / 14)
             for x, y in stroke] for stroke in strokes]


# -- glyphs ------------------------------------------------------------------
# y: 0 = cap height, 14 = baseline. All coordinates in the 10x14 cell.

GLYPHS = {
    # -- uppercase ---------------------------------------------------------
    'A': [
        ln((1, 14), (5, 0)),
        ln((5, 0), (9, 14)),
        ln((3, 10), (7, 10)),
    ],
    'B': [
        ln((1, 0), (1, 14)),
        bez((1, 0), (9, 0), (9, 7), (1, 7)),
        bez((1, 7), (9, 7), (9, 14), (1, 14)),
    ],
    'C': [
        arc(5.5, 7, 4.5, 7, math.pi / 2 + 0.35, 3 * math.pi / 2 - 0.35, n=20),
    ],
    'D': [
        ln((1, 0), (1, 14)),
        arc(1, 7, 9, 7, -math.pi / 2, math.pi / 2, n=20),
    ],
    'E': [
        ln((1, 0), (1, 14)),
        ln((1, 0), (8, 0)),
        ln((1, 7), (6.5, 7)),
        ln((1, 14), (8, 14)),
    ],
    'F': [
        ln((1, 0), (1, 14)),
        ln((1, 0), (8, 0)),
        ln((1, 7), (6.5, 7)),
    ],
    'G': [
        arc(5.5, 7, 4.5, 7, math.radians(40), math.radians(320), n=24),
        ln((4.5, 8.5), (9.5, 8.5)),
        ln((9.5, 8.5), (9.5, 12.5)),
    ],
    'H': [
        ln((1, 0), (1, 14)),
        ln((9, 0), (9, 14)),
        ln((1, 7), (9, 7)),
    ],
    'I': [
        ln((5, 0), (5, 14)),
        ln((3, 0), (7, 0)),
        ln((3, 14), (7, 14)),
    ],
    'J': [
        ln((6, 0), (8, 0)),
        ln((8, 0), (8, 9)),
        bez((8, 9), (8, 14), (5, 14.5), (3, 14)),
    ],
    'K': [
        ln((1, 0), (1, 14)),
        ln((1, 7), (9, 0)),
        ln((2, 8), (9, 14)),
    ],
    'L': [
        ln((1, 0), (1, 14)),
        ln((1, 14), (9, 14)),
    ],
    'M': [
        ln((1, 0), (1, 14)),
        ln((9, 0), (9, 14)),
        ln((1, 0), (5, 7)),
        ln((5, 7), (9, 0)),
    ],
    'N': [
        ln((1, 0), (1, 14)),
        ln((9, 0), (9, 14)),
        ln((1, 0), (9, 14)),
    ],
    'O': [
        arc(5, 7, 4.5, 7, 0, 2 * math.pi, n=24),
    ],
    'P': [
        ln((1, 0), (1, 14)),
        arc(1, 3.5, 7, 3.5, -math.pi / 2, math.pi / 2, n=18),
    ],
    'Q': [
        arc(5, 7, 4.5, 7, 0, 2 * math.pi, n=24),
        bez((7, 10.5), (9.5, 12), (9.8, 14.2), (7.5, 14.5)),
    ],
    'R': [
        ln((1, 0), (1, 14)),
        arc(1, 3.5, 7, 3.5, -math.pi / 2, math.pi / 2, n=18),
        ln((4.8, 7), (9, 14)),
    ],
    'S': _S_STROKES,
    'T': [
        ln((1, 0), (9, 0)),
        ln((5, 0), (5, 14)),
    ],
    'U': [
        ln((2, 0), (2, 10)),
        ln((8, 0), (8, 10)),
        arc(5, 10, 3, 4, math.pi, 0, n=16),
    ],
    'V': [
        ln((1, 0), (5, 14)),
        ln((9, 0), (5, 14)),
    ],
    'W': [
        ln((1, 0), (3, 13)),
        ln((3, 13), (5, 1.5)),
        ln((5, 1.5), (7, 13)),
        ln((7, 13), (9, 0)),
    ],
    'X': [
        ln((1, 0), (9, 14)),
        ln((9, 0), (1, 14)),
    ],
    'Y': [
        ln((1, 0), (5, 7)),
        ln((9, 0), (5, 7)),
        ln((5, 7), (5, 14)),
    ],
    'Z': [
        ln((1, 0), (9, 0)),
        ln((9, 0), (1, 14)),
        ln((1, 14), (9, 14)),
    ],

    # -- lowercase ---------------------------------------------------------
    # x-height body spans y 5..14; ascenders reach y 0..2, descenders y 18.
    'a': [
        arc(3.9, 9.5, 2.9, 4.5, 0, 2 * math.pi, n=20),
        ln((6.8, 5), (6.8, 14)),
        bez((6.8, 5), (6.4, 4.4), (5.5, 4.5), (4.8, 5.8)),
    ],
    'b': [
        ln((1.4, 0), (1.4, 14)),
        arc(5, 9.5, 3.5, 4.5, 0, 2 * math.pi, n=22),
    ],
    'c': [
        arc(5, 9.5, 3.5, 4.5, math.pi / 2 + 0.3,
            3 * math.pi / 2 - 0.3, n=20),
    ],
    'd': [
        arc(5, 9.5, 3.5, 4.5, 0, 2 * math.pi, n=22),
        ln((8.6, 0), (8.6, 14)),
    ],
    'e': [
        arc(5, 9.5, 3.5, 4.5, math.pi, 2 * math.pi, n=16),
        arc(5, 9.5, 3.5, 4.5, 0, math.pi, n=16),
        ln((1.6, 9.5), (9, 9.5)),
    ],
    'f': [
        bez((5, 1), (5.3, 4), (5.2, 8), (4.6, 12.5)),
        bez((5, 1), (6.1, 0.7), (6.7, 1.8), (6.6, 3.6)),
        ln((2, 8), (8, 8)),
    ],
    'g': [
        arc(5, 9.5, 3.5, 4.5, 0, 2 * math.pi, n=22),
        ln((8.6, 7), (8.6, 17)),
        bez((8.6, 17), (8.3, 18.2), (7.3, 18), (6.8, 17.2)),
    ],
    'h': [
        ln((1.5, 0), (1.5, 14)),
        arc(5, 5, 3.5, 2.5, math.pi, 2 * math.pi, n=16),
        ln((8.5, 5), (8.5, 14)),
    ],
    'i': [
        ln((5, 6), (5, 14)),
    ] + _dot(5, 3),
    'j': [
        ln((5.5, 6), (5.5, 17)),
        bez((5.5, 17), (5.3, 18), (4.5, 18.2), (4, 17.3)),
    ] + _dot(5.5, 3),
    'k': [
        ln((1.5, 1), (1.5, 14)),
        ln((2, 9.5), (8.5, 4.5)),
        ln((2, 9.5), (8.5, 13.8)),
    ],
    'l': [
        ln((1.5, 0), (1.5, 13.5)),
        bez((1.5, 13.5), (2, 14.4), (3.5, 14.5), (4.2, 13.9)),
    ],
    'm': [
        ln((1.5, 5), (1.5, 14)),
        arc(3.5, 5, 2, 2.6, math.pi, 2 * math.pi, n=14),
        ln((5.5, 5), (5.5, 14)),
        arc(7.25, 5, 1.75, 2.6, math.pi, 2 * math.pi, n=14),
        ln((9, 5), (9, 14)),
    ],
    'n': [
        ln((1.5, 5), (1.5, 14)),
        arc(5, 5, 3.5, 2.5, math.pi, 2 * math.pi, n=16),
        ln((8.5, 5), (8.5, 14)),
    ],
    'o': [
        arc(5, 9.5, 3.5, 4.5, 0, 2 * math.pi, n=24),
    ],
    'p': [
        arc(5, 9.5, 3.5, 4.5, 0, 2 * math.pi, n=22),
        ln((1.4, 5), (1.4, 18)),
    ],
    'q': [
        arc(5, 9.5, 3.5, 4.5, 0, 2 * math.pi, n=22),
        ln((8.6, 5), (8.6, 17)),
        bez((8.6, 17), (8.4, 18), (7.5, 18.2), (7, 17.5)),
    ],
    'r': [
        ln((1.5, 5), (1.5, 14)),
        bez((1.5, 5.5), (4, 4), (6, 5.2), (7.6, 7.8)),
    ],
    's': _xheight(_S_STROKES),
    't': [
        ln((5, 2), (5, 12.5)),
        ln((2, 8), (8, 8)),
        bez((5, 12.5), (5, 14), (4.5, 14.3), (3.8, 14)),
    ],
    'u': [
        ln((2, 5), (2, 10)),
        ln((8, 5), (8, 10)),
        arc(5, 10, 3, 4, math.pi, 0, n=16),
    ],
    'v': [
        ln((2, 5), (5, 14)),
        ln((8, 5), (5, 14)),
    ],
    'w': [
        ln((1, 5), (2.5, 14)),
        ln((2.5, 14), (4.5, 6)),
        ln((4.5, 6), (6.5, 14)),
        ln((6.5, 14), (9, 5)),
    ],
    'x': [
        ln((2, 5), (8, 14)),
        ln((8, 5), (2, 14)),
    ],
    'y': [
        ln((2, 5), (5, 14)),
        bez((8, 5), (6.5, 11), (5.3, 15), (4.3, 18)),
    ],
    'z': [
        ln((2, 5), (8, 5)),
        ln((8, 5), (2, 14)),
        ln((2, 14), (8, 14)),
    ],

    # -- digits ------------------------------------------------------------
    '0': [
        arc(5, 7, 4, 7, 0, 2 * math.pi, n=24),
    ],
    '1': [
        ln((2.5, 2.5), (5, 0)),
        ln((5, 0), (5, 14)),
        ln((3, 14), (7, 14)),
    ],
    '2': [
        arc(5, 4, 4, 4, math.pi, 2 * math.pi, n=16),
        ln((9.2, 4.6), (1, 13)),
        ln((1, 13), (9, 13)),
    ],
    '3': [
        bez((2.5, 0.5), (10, 0.8), (10, 6.2), (5.0, 7.0)),
        bez((5.0, 7.0), (10, 8.0), (10, 12.5), (2.5, 13.5)),
    ],
    '4': [
        ln((9, 0), (4.5, 9)),
        ln((8, 0), (8, 14)),
        ln((2, 9), (8, 9)),
    ],
    '5': [
        ln((1, 0), (8, 0)),
        ln((1, 0), (1, 4)),
        arc(1, 9, 8, 5, -math.pi / 2, math.pi / 2, n=20),
    ],
    '6': [
        bez((8, 0), (3, 0), (0, 4), (1.5, 10)),
        bez((1.5, 10), (1, 12.5), (2.5, 14), (4.5, 13.6)),
        arc(5, 10, 3.5, 3.5, 0, 2 * math.pi, n=24),
    ],
    '7': [
        ln((1.5, 1.5), (9, 1.5)),
        bez((9, 1.5), (6, 5), (3, 10), (1, 13)),
    ],
    '8': [
        arc(5, 4.5, 3, 4, 0, 2 * math.pi, n=18),
        arc(5, 9.5, 3, 4, 0, 2 * math.pi, n=18),
    ],
    '9': [
        arc(5, 5, 3.5, 4.5, 0, 2 * math.pi, n=20),
        bez((7, 7.5), (9.5, 9), (9.5, 12), (7, 14)),
    ],

    # -- punctuation --------------------------------------------------------
    ' ': [],
    '.': _dot(5, 12.5),
    ',': _dot(5, 11.5) + [bez((5, 12.5), (5.5, 14), (4, 15.5), (2.5, 15))],
    ':': _dot(5, 4.5) + _dot(5, 10.5),
    ';': _dot(5, 4.5) + _dot(5, 11.5) +
        [bez((5, 12.5), (5.5, 14), (4, 15.5), (2.5, 15))],
    "'": [bez((6, 0), (4.5, 3), (4, 5), (4.5, 7))],
    '!': [ln((5, 0), (5, 10))] + _dot(5, 12.5),
    '?': [
        arc(5, 3.5, 3, 3.5, math.pi, 2 * math.pi, n=14),
        bez((8, 3.5), (8, 6), (6, 7), (5, 7.5)),
        ln((5, 7.5), (5, 10)),
    ] + _dot(5, 12.5),
    '-': [ln((2, 7), (8, 7))],
    '%': [
        arc(3, 4, 2, 3, 0, 2 * math.pi, n=14),
        arc(7, 10, 2, 3, 0, 2 * math.pi, n=14),
        ln((8.2, 1.2), (1.8, 12.8)),
    ],
    '$': [
        bez((7, 0), (4, 0), (2.5, 2), (3.5, 4)),
        bez((3.5, 4), (5, 6), (6, 8), (4.5, 10)),
        bez((4.5, 10), (3, 12), (4, 14), (7, 14)),
        ln((4.2, 0), (4.2, 14)),
    ],
    '(': [arc(6, 7, 5.5, 7, math.pi / 2 + 0.15, 3 * math.pi / 2 - 0.15, n=18)],
    ')': [arc(4, 7, 5.5, 7, -math.pi / 2 + 0.15, math.pi / 2 - 0.15, n=18)],
    '/': [ln((8, 0), (2, 14))],
    '+': [ln((5, 4), (5, 10)), ln((2, 7), (8, 7))],
    '&': [
        bez((6, 0), (8, 1), (8, 3), (6, 4)),
        bez((6, 4), (4, 5), (3, 7), (4.5, 8)),
        bez((4.5, 8), (6, 9), (6, 10), (4.5, 11)),
        bez((4.5, 11), (3, 12), (3.5, 14), (5.5, 14)),
        bez((5.5, 14), (7.5, 14), (8, 12.5), (7, 11.5)),
        bez((7, 11.5), (6, 10.5), (5.5, 10), (4.8, 9.5)),
        bez((4.8, 9.5), (4.5, 8.5), (5, 7.5), (6.5, 7)),
        bez((6.5, 7), (8, 6.5), (8, 5), (7, 4)),
        bez((7, 4), (6, 3.5), (6, 2), (6, 0)),
    ],
    '@': [
        arc(5, 7, 4, 5, 0, 2 * math.pi, n=22),
        arc(5, 7, 2, 2.6, 0.4, 5.9, n=14),
        bez((7.6, 8.8), (9.2, 9.6), (9, 11.5), (7.2, 12)),
    ],
    '#': [
        ln((3.5, 0), (3.5, 14)),
        ln((6.5, 0), (6.5, 14)),
        ln((1, 4.5), (9, 4.5)),
        ln((1, 9.5), (9, 9.5)),
    ],
    '\u00b7': _dot(5, 7, r=1.1),  # middle dot
}

# Narrow glyphs get a smaller advance width.
NARROW = set("il1j.,:;'!?-+%$()/&@#\u00b7")


# -- metrics -----------------------------------------------------------------

def char_width(ch, size):
    if ch == ' ':
        return size * 0.45
    if ch in NARROW:
        return size * 0.4
    return size * 0.74


def text_width(s, size):
    return sum(char_width(ch, size) for ch in s)


# -- drawing -----------------------------------------------------------------

def draw_text(cv, x, y, s, size, color, weight=1, align='left'):
    """Draw s with its cap-height top at y. x is left/center/right
    anchor depending on align."""
    if align == 'center':
        x -= text_width(s, size) / 2.0
    elif align == 'right':
        x -= text_width(s, size)
    scale = size / 14.0
    cx = x
    for ch in s:
        strokes = GLYPHS.get(ch)
        if strokes is None:
            strokes = GLYPHS.get(ch.upper())
        if strokes:
            for stroke in strokes:
                for i in range(len(stroke) - 1):
                    x0, y0 = stroke[i]
                    x1, y1 = stroke[i + 1]
                    cv.line(cx + x0 * scale, y + y0 * scale,
                            cx + x1 * scale, y + y1 * scale,
                            color, weight)
                if len(stroke) == 1:
                    p = stroke[0]
                    cv.line(cx + p[0] * scale, y + p[1] * scale,
                            cx + p[0] * scale, y + p[1] * scale,
                            color, weight)
        cx += char_width(ch, size)


def draw_wrapped(cv, x, y, s, size, color, max_width, weight=1,
                 line_gap=1.25, max_lines=None, align='left'):
    """Greedy word wrap. Returns the y just below the last drawn line."""
    words = s.split()
    lines = []
    cur = ''
    for w in words:
        cand = w if not cur else cur + ' ' + w
        if cur and text_width(cand, size) > max_width:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    pitch = size * line_gap
    for i, line in enumerate(lines):
        draw_text(cv, x, y + i * pitch, line, size, color,
                  weight=weight, align=align)
    if not lines:
        return y
    return y + (len(lines) - 1) * pitch + size


if __name__ == "__main__":
    cv = Canvas(760, 160, bg=(255, 255, 255))
    draw_text(cv, 20, 20, "ABCDEFGHJKLM", 40, (0, 0, 0), weight=2)
    draw_text(cv, 20, 90, "0123456789 .,!", 40, (0, 0, 0), weight=2)
    cv.save("/tmp/font_test.png")
    print("wrote /tmp/font_test.png")

    cv2 = Canvas(760, 160, bg=(255, 255, 255))
    draw_text(cv2, 20, 20, "NOPQRSTUVWXYZ", 40, (0, 0, 0), weight=2)
    draw_text(cv2, 20, 90, "GSGS 25 NOVEMBER", 40, (0, 0, 0), weight=2)
    cv2.save("/tmp/font_test2.png")
    print("wrote /tmp/font_test2.png")

    cv3 = Canvas(760, 180, bg=(255, 255, 255))
    draw_text(cv3, 20, 30, "the quick brown fox jumps", 40,
              (0, 0, 0), weight=2)
    draw_text(cv3, 20, 110, "sudan khartoum gazette 23", 40,
              (0, 0, 0), weight=2)
    cv3.save("/tmp/font_test3.png")
    print("wrote /tmp/font_test3.png")

    cv4 = Canvas(760, 110, bg=(255, 255, 255))
    draw_text(cv4, 20, 20, "COP31 GAZETTE 23", 60, (0, 0, 0), weight=3)
    cv4.save("/tmp/font_test4.png")
    print("wrote /tmp/font_test4.png")
