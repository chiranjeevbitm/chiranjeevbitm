"""Tech stack as a 3D orbital system: an isometric GenAI core with three tilted rings of tool chips.
Each chip is drawn twice (behind and in front of the core) so occlusion stays correct as it orbits."""
import math
from common import *

W, H = 1200, 540
CX, CY = 600, 285
SCALE = 150

RINGS = [
    # (radius, tilt_x deg, tilt_z deg, period s, colour, label, items)
    (1.5, -21, -7, 30, CYAN, "GenAI", ["LangChain", "LangGraph", "Azure OpenAI", "Claude", "MCP", "NVIDIA DGX", "RAG"]),
    (2.5, -24, 5, 44, VIOLET, "Data + ML", ["Python", "PySpark", "Databricks", "SQL", "Pandas", "MLflow", "Dataiku", "Azure AI Search"]),
    (3.45, -19, -3, 58, AMBER, "Ship", ["Docker", "Kubernetes", "GitHub Actions", "React", "TypeScript", "Vercel", "Playwright"]),
]
FR = 72


def ring_point(r, t, tx, tz):
    p = (r * math.cos(t), 0, r * math.sin(t))
    return rot(p, math.radians(tx), 0, math.radians(tz))


def build():
    defs, bg = panel_bg(W, H, gid="o")
    defs += (f'<filter id="og" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>'
             f'<radialGradient id="ocore" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".45"/>'
             f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>')
    out = [svg_open(W, H, "Tech stack orbit: GenAI (LangChain, LangGraph, Azure OpenAI, Claude, MCP, NVIDIA DGX, RAG), Data and ML (Python, PySpark, Databricks, SQL, Pandas, MLflow, Dataiku, Azure AI Search), Ship (Docker, Kubernetes, GitHub Actions, React, TypeScript, Vercel, Playwright)", defs), bg]
    out.append(f'<text x="48" y="54" font-family="{MONO}" font-size="15" fill="{CYAN}">// stack</text>')
    out.append(f'<text x="48" y="88" font-family="{SANS}" font-size="30" font-weight="800" fill="{TEXT}">The orbit I work in</text>')
    # legend
    lx = W - 48
    for r, tx, tz, per, col, label, items in reversed(RINGS):
        w = 32 + 9 * len(label)
        lx -= w
        out.append(f'<g transform="translate({lx},62)"><circle cx="8" cy="0" r="5" fill="{col}"/>'
                   f'<text x="20" y="4.5" font-family="{MONO}" font-size="15" fill="{MUTED}">{label}</text></g>')
        lx -= 14

    def ring_path(r, tx, tz, front):
        segs, cur = [], []
        for k in range(181):
            t = 2 * math.pi * k / 180
            q = ring_point(r, t, tx, tz)
            x, y = CX + q[0] * SCALE * 1.0, CY + q[1] * SCALE
            if (q[2] >= 0) == front:
                cur.append(f"{f(x)},{f(y)}")
            elif cur:
                segs.append(cur); cur = []
        if cur:
            segs.append(cur)
        return " ".join("M" + " L".join(s) for s in segs if len(s) > 1)

    def chips(front):
        res = []
        for r, tx, tz, per, col, label, items in RINGS:
            n = len(items)
            for ci, name in enumerate(items):
                xs, ys, sc, op = [], [], [], []
                for k in range(FR + 1):
                    t = 2 * math.pi * (k / FR + ci / n)
                    q = ring_point(r, t, tx, tz)
                    xs.append(CX + q[0] * SCALE); ys.append(CY + q[1] * SCALE)
                    d = (q[2] / r + 1) / 2
                    sc.append(0.74 + 0.36 * d)
                    vis = (q[2] >= 0) == front
                    op.append((0.4 + 0.6 * d) if vis else 0)
                w = 36 + 8.6 * len(name)
                tr = ";".join(f"{f(x)} {f(y)}" for x, y in zip(xs, ys))
                du = f'dur="{per}s" repeatCount="indefinite"'
                res.append(
                    f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" {du}/>'
                    f'<g opacity="{f(op[0],2)}"><animate attributeName="opacity" values="{vals(op,2)}" {du}/>'
                    f'<g><animateTransform attributeName="transform" type="scale" values="{vals(sc,2)}" {du}/>'
                    f'<rect x="{f(-w/2)}" y="-15" width="{f(w)}" height="30" rx="15" fill="{PANEL2}" stroke="{col}" stroke-width="1.3"/>'
                    f'<circle cx="{f(-w/2+13)}" cy="0" r="4" fill="{col}"/>'
                    f'<text x="{f(-w/2+24)}" y="5.4" text-anchor="start" font-family="{SANS}" font-size="15.5" font-weight="600" fill="{TEXT}">{esc(name)}</text>'
                    f'</g></g></g>')
        return "".join(res)

    # back halves of rings + back chips
    for r, tx, tz, per, col, label, items in RINGS:
        out.append(f'<path d="{ring_path(r, tx, tz, False)}" fill="none" stroke="{col}" stroke-opacity=".28" stroke-width="1.2" stroke-dasharray="3 6"/>')
    out.append(chips(False))

    # core: glowing isometric chip
    out.append(f'<circle cx="{CX}" cy="{CY}" r="120" fill="url(#ocore)"/>')
    out.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="4s" repeatCount="indefinite"/>')
    s = 62
    out.append(iso_cube(CX, CY - 12, s, 22, "#123048", "#0B1A2C", "#0E2238", stroke=CYAN))
    inner = iso_cube(CX, CY - 22, s * 0.62, 10, "#1B4A66", "#103048", "#143A57", stroke=CYAN)
    out.append(inner)
    out.append(f'<text x="{CX}" y="{CY - 22}" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="800" fill="{TEXT}" transform="rotate(0)">GenAI</text>')
    out.append(f'<circle cx="{CX}" cy="{CY-24}" r="44" fill="none" stroke="{CYAN}" stroke-opacity=".5"><animate attributeName="r" values="30;80" dur="3s" repeatCount="indefinite"/>'
               f'<animate attributeName="stroke-opacity" values=".6;0" dur="3s" repeatCount="indefinite"/></circle>')
    out.append("</g>")

    for r, tx, tz, per, col, label, items in RINGS:
        out.append(f'<path d="{ring_path(r, tx, tz, True)}" fill="none" stroke="{col}" stroke-opacity=".75" stroke-width="1.4"/>')
    out.append(chips(True))
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
