"""Tiny software rasteriser (stdlib only) producing 8-bit RGB PNGs."""

import struct
import zlib


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = int(w)
        self.h = int(h)
        self.buf = bytearray(bg * (self.w * self.h))

    # -- primitives ---------------------------------------------------------

    def _set(self, x, y, color):
        x = int(x)
        y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = color[0]
            self.buf[i + 1] = color[1]
            self.buf[i + 2] = color[2]

    def px(self, x, y, color):
        self._set(x, y, color)

    def rect(self, x, y, w, h, color):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x + w))
        y1 = min(self.h, int(y + h))
        r, g, b = color
        for yy in range(y0, y1):
            row = yy * self.w
            for xx in range(x0, x1):
                i = (row + xx) * 3
                self.buf[i] = r
                self.buf[i + 1] = g
                self.buf[i + 2] = b

    def rect_outline(self, x, y, w, h, color, t=1):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def vgrad(self, x, y, w, h, top, bottom):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x + w))
        y1 = min(self.h, int(y + h))
        span = max(1, y1 - y0 - 1)
        for yy in range(y0, y1):
            t = (yy - y0) / span
            c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            self.rect(x0, yy, x1 - x0, 1, c)

    def hgrad(self, x, y, w, h, left, right):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x + w))
        y1 = min(self.h, int(y + h))
        span = max(1, x1 - x0 - 1)
        for xx in range(x0, x1):
            t = (xx - x0) / span
            c = tuple(int(left[i] + (right[i] - left[i]) * t) for i in range(3))
            self.rect(xx, y0, 1, y1 - y0, c)

    def disc(self, cx, cy, r, color):
        r2 = r * r
        x0 = max(0, int(cx - r) - 1)
        x1 = min(self.w, int(cx + r) + 2)
        y0 = max(0, int(cy - r) - 1)
        y1 = min(self.h, int(cy + r) + 2)
        for yy in range(y0, y1):
            dy = yy - cy
            for xx in range(x0, x1):
                dx = xx - cx
                if dx * dx + dy * dy <= r2:
                    self._set(xx, yy, color)

    def line(self, x0, y0, x1, y1, color, w=1):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            self.disc(x0, y0, w / 2.0, color)
            return
        rad = w / 2.0
        for i in range(int(steps) + 1):
            t = i / steps
            self.disc(x0 + dx * t, y0 + dy * t, rad, color)

    def ring(self, cx, cy, r, color, t=1):
        r_out = r + t / 2.0
        r_in = max(0.0, r - t / 2.0)
        r_out2 = r_out * r_out
        r_in2 = r_in * r_in
        x0 = max(0, int(cx - r_out) - 1)
        x1 = min(self.w, int(cx + r_out) + 2)
        y0 = max(0, int(cy - r_out) - 1)
        y1 = min(self.h, int(cy + r_out) + 2)
        for yy in range(y0, y1):
            dy = yy - cy
            for xx in range(x0, x1):
                dx = xx - cx
                d2 = dx * dx + dy * dy
                if r_in2 <= d2 <= r_out2:
                    self._set(xx, yy, color)

    def poly(self, points, color):
        n = len(points)
        if n < 3:
            return
        ymin = min(int(p[1]) for p in points)
        ymax = max(int(p[1]) for p in points)
        y0 = max(0, ymin)
        y1 = min(self.h, ymax + 1)
        edges = []
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if y1 == y2:
                continue
            edges.append((float(x1), float(y1), float(x2), float(y2)))
        for yy in range(y0, y1):
            yc = yy + 0.5
            xs = []
            for x1, y1, x2, y2 in edges:
                lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
                if lo <= yc < hi:
                    xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                xa = int(xs[i] + 0.5)
                xb = int(xs[i + 1] + 0.5)
                xa = max(xa, 0)
                xb = min(xb, self.w)
                for xx in range(xa, xb):
                    self._set(xx, yy, color)

    # -- output -------------------------------------------------------------

    def save(self, path):
        def chunk(tag, data):
            return (struct.pack(">I", len(data)) + tag + data +
                    struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

        raw = bytearray()
        row = bytearray(self.w * 3)
        base = 0
        for _ in range(self.h):
            raw.append(0)  # filter: none
            raw += self.buf[base:base + self.w * 3]
            base += self.w * 3
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        png = (b"\x89PNG\r\n\x1a\n" +
               chunk(b"IHDR", ihdr) +
               chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
               chunk(b"IEND", b""))
        with open(path, "wb") as f:
            f.write(png)


if __name__ == "__main__":
    c = Canvas(64, 64, bg=(250, 250, 250))
    c.vgrad(0, 0, 64, 64, (30, 60, 120), (200, 220, 255))
    c.rect_outline(4, 4, 56, 56, (0, 0, 0), t=2)
    c.disc(32, 32, 12, (220, 40, 40))
    c.ring(32, 32, 12, (0, 0, 0), t=1)
    c.line(8, 56, 56, 8, (0, 100, 0), w=3)
    c.poly([(20, 50), (44, 50), (32, 20)], (250, 200, 0))
    c.hgrad(10, 60, 44, 2, (0, 0, 0), (255, 255, 255))
    # clipping smoke tests (must not raise)
    c.rect(-10, -10, 20, 20, (255, 0, 0))
    c.disc(200, 200, 30, (0, 255, 0))
    c.line(-50, 32, 100, 32, (0, 0, 255), w=2)
    c.poly([(0, 0), (-5, 100), (70, 64)], (128, 128, 128))
    c.save("/tmp/draw_test.png")
    print("wrote /tmp/draw_test.png")
