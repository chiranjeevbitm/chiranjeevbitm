"""Shared palette, fonts and helpers for the profile SVG generator."""
import math

BG = "#060A13"
PANEL = "#0A1120"
PANEL2 = "#0E1729"
STROKE = "#1C2A42"
CYAN = "#36D7F0"
TEAL = "#2EA1B5"
VIOLET = "#8B5CF6"
PINK = "#E879F9"
AMBER = "#FBBF24"
GREEN = "#34D399"
TEXT = "#E6EDF7"
MUTED = "#8A9BB4"
DIM = "#4A5B76"

SANS = "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"


def f(x, nd=1):
    """Compact number formatting."""
    s = f"{x:.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s


def vals(seq, nd=1):
    return ";".join(f(v, nd) for v in seq)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg_open(w, h, title, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n<defs>{extra_defs}</defs>\n"
    )


def panel_bg(w, h, rx=18, glow=True, gid="p"):
    out = [
        f'<linearGradient id="{gid}bd" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/>'
        f'<stop offset=".5" stop-color="{STROKE}" stop-opacity=".9"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity=".55"/></linearGradient>',
    ]
    defs = "".join(out)
    body = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="{PANEL}" stroke="url(#{gid}bd)" stroke-width="1.5"/>']
    if glow:
        defs += (
            f'<radialGradient id="{gid}g1" cx="0.85" cy="0.15" r="0.6">'
            f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{gid}g2" cx="0.1" cy="0.95" r="0.6">'
            f'<stop offset="0" stop-color="{VIOLET}" stop-opacity=".16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="{gid}clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}"/></clipPath>'
        )
        body.append(f'<g clip-path="url(#{gid}clip)"><rect width="{w}" height="{h}" fill="url(#{gid}g1)"/><rect width="{w}" height="{h}" fill="url(#{gid}g2)"/></g>')
    return defs, "\n".join(body)


def rot(p, ax, ay, az=0.0):
    x, y, z = p
    # rotate about Y
    c, s = math.cos(ay), math.sin(ay)
    x, z = x * c + z * s, -x * s + z * c
    # rotate about X (tilt)
    c, s = math.cos(ax), math.sin(ax)
    y, z = y * c - z * s, y * s + z * c
    if az:
        c, s = math.cos(az), math.sin(az)
        x, y = x * c - y * s, x * s + y * c
    return x, y, z


def project(p, cx, cy, scale, cam=4.0):
    """Perspective projection; z toward viewer is positive."""
    x, y, z = p
    k = cam / (cam - z)
    return cx + x * scale * k, cy + y * scale * k, k


def iso_cube(x, y, s, h, top, left, right, stroke=None, extra=""):
    """Isometric box: (x,y) = top-face centre, s = half-width, h = height."""
    hs = s * 0.5
    t = f"M{f(x)},{f(y-hs)} L{f(x+s)},{f(y)} L{f(x)},{f(y+hs)} L{f(x-s)},{f(y)}Z"
    l = f"M{f(x-s)},{f(y)} L{f(x)},{f(y+hs)} L{f(x)},{f(y+hs+h)} L{f(x-s)},{f(y+h)}Z"
    r = f"M{f(x+s)},{f(y)} L{f(x)},{f(y+hs)} L{f(x)},{f(y+hs+h)} L{f(x+s)},{f(y+h)}Z"
    st = f' stroke="{stroke}" stroke-width="1" stroke-linejoin="round"' if stroke else ""
    return (f'<path d="{l}" fill="{left}"{st}/><path d="{r}" fill="{right}"{st}/>'
            f'<path d="{t}" fill="{top}"{st}{extra}/>')
