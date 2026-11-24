"""Tiện ích nhỏ để vẽ sơ đồ SVG (BPMN / ArchiMate) — không cần cài thêm thư viện."""
from html import escape

FONT = "Inter, 'DejaVu Sans', Arial, sans-serif"


def wrap(text, max_chars):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            if len(line) + len(w) + (1 if line else 0) <= max_chars:
                line = (line + " " + w).strip()
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


class Svg:
    def __init__(self, w, h, bg="#ffffff"):
        self.w, self.h = w, h
        self.parts = []
        self.defs = []
        self.bg = bg

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, txt, size=13, weight="400", fill="#1f2937", anchor="middle",
             max_chars=None, lh=None, italic=False, valign="middle"):
        lines = wrap(txt, max_chars) if max_chars else txt.split("\n")
        lh = lh or size * 1.25
        total = lh * (len(lines) - 1)
        if valign == "middle":
            y0 = y - total / 2
        elif valign == "top":
            y0 = y + size * 0.9
        else:
            y0 = y - total
        st = ' font-style="italic"' if italic else ""
        for i, ln in enumerate(lines):
            self.add(
                f'<text x="{x}" y="{y0 + i * lh:.1f}" font-family="{FONT}" font-size="{size}" '
                f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
                f'dominant-baseline="central"{st}>{escape(ln)}</text>')

    def rect(self, x, y, w, h, fill="#fff", stroke="#333", sw=1.5, rx=0, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>')

    def line(self, pts, stroke="#333", sw=1.6, dash=None, marker=None, mstart=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        ms = f' marker-start="url(#{mstart})"' if mstart else ""
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.add(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d}{m}{ms} '
                 f'stroke-linejoin="round"/>')

    def save(self, path):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}"><defs>{"".join(self.defs)}</defs>'
                f'<rect width="100%" height="100%" fill="{self.bg}"/>')
        open(path, "w", encoding="utf-8").write(head + "".join(self.parts) + "</svg>")
