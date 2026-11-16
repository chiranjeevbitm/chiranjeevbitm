"""Hero banner: name + typed roles on the left, rotating 3D agent-network sphere on the right."""
import math
import random
from common import *

W, H = 1200, 440
DUR = 24  # seconds per full rotation
FR = 48   # keyframes per rotation
SCX, SCY, R = 900, 205, 132
TILT = math.radians(-18)


def fib_sphere(n):
    pts = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - y * y)
        th = ga * i
        pts.append((math.cos(th) * r, y, math.sin(th) * r))
    return pts


def build():
    random.seed(7)
    pts = fib_sphere(58)
    # edges: 3 nearest neighbours
    edges = set()
    for i, p in enumerate(pts):
        d = sorted(range(len(pts)), key=lambda j: sum((p[k] - pts[j][k]) ** 2 for k in range(3)))
        for j in d[1:4]:
            edges.add(tuple(sorted((i, j))))
    edges = sorted(edges)

    angles = [2 * math.pi * k / FR for k in range(FR + 1)]
    proj = []  # proj[frame][i] = (x, y, z, k)
    for a in angles:
        row = []
        for p in pts:
            q = rot(p, TILT, a)
            x, y, k = project(q, SCX, SCY, R, cam=4.2)
            row.append((x, y, q[2], k))
        proj.append(row)

    defs, bg = panel_bg(W, H, gid="h")
    defs += (
        f'<linearGradient id="nameg" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">'
        f'<stop offset="0" stop-color="{TEXT}"/><stop offset=".42" stop-color="{TEXT}"/>'
        f'<stop offset=".5" stop-color="{CYAN}"/><stop offset=".58" stop-color="{TEXT}"/><stop offset="1" stop-color="{TEXT}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;.35;1" dur="7s" repeatCount="indefinite"/>'
        f'</linearGradient>'
        f'<radialGradient id="core" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/>'
        f'<stop offset=".6" stop-color="{VIOLET}" stop-opacity=".10"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset=".35" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
        f'<linearGradient id="floorx" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/>'
        f'<stop offset=".45" stop-color="#000"/><stop offset=".7" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient>'
        f'<mask id="floormask"><rect width="{W}" height="{H}" fill="url(#floorfade)"/></mask>'
        f'<mask id="floormask2"><rect width="{W}" height="{H}" fill="url(#floorx)"/></mask>'
    )
    out = [svg_open(W, H, "Chiranjeev Kumar — GenAI Engineer. Animated banner with a rotating 3D agent network.", defs), bg]

    # ---------- perspective floor grid (right side) ----------
    hz = 330
    vx = SCX
    g = ['<g mask="url(#floormask2)"><g mask="url(#floormask)" stroke="' + TEAL + '" stroke-width="1" fill="none" opacity=".45">']
    for i in range(-14, 15):
        xb = vx + i * 70
        g.append(f'<line x1="{vx + i*7}" y1="{hz}" x2="{xb}" y2="{H}"/>')
    n_lines = 7
    for i in range(n_lines):
        ys = []
        ops = []
        for k in range(25):
            s = ((i + k / 24) / n_lines)
            y = hz + (H - hz) * s * s
            ys.append(y)
            ops.append(min(1, s * 2.2))
        g.append(f'<line x1="0" x2="{W}" y1="{f(ys[0])}" y2="{f(ys[0])}">'
                 f'<animate attributeName="y1" values="{vals(ys)}" dur="3s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y2" values="{vals(ys)}" dur="3s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="{vals(ops,2)}" dur="3s" repeatCount="indefinite"/></line>')
    g.append(f'<line x1="0" x2="{W}" y1="{hz}" y2="{hz}" stroke="{CYAN}" opacity=".7"/>')
    g.append("</g></g>")
    out.append("".join(g))

    # ---------- sphere halo ----------
    out.append(f'<circle cx="{SCX}" cy="{SCY}" r="{R*1.55}" fill="url(#core)"/>')

    # ---------- orbit ring behind (back half) ----------
    ring_r = 1.62
    ring_tilt = math.radians(17)
    ring_pts = []
    for k in range(121):
        t = 2 * math.pi * k / 120
        q = rot((ring_r * math.cos(t), 0, ring_r * math.sin(t)), ring_tilt, 0, math.radians(-11))
        x, y, kk = project(q, SCX, SCY, R, cam=4.2)
        ring_pts.append((x, y, q[2]))

    def ring_path(front):
        segs, cur = [], []
        for x, y, z in ring_pts:
            if (z >= 0) == front:
                cur.append(f"{f(x)},{f(y)}")
            elif cur:
                segs.append(cur); cur = []
        if cur:
            segs.append(cur)
        return " ".join("M" + " L".join(s) for s in segs if len(s) > 1)

    out.append(f'<path d="{ring_path(False)}" fill="none" stroke="{VIOLET}" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="3 6"/>')
    BACK_CHIPS_IDX = len(out)

    dur = f'dur="{DUR}s" repeatCount="indefinite"'

    # ---------- edges ----------
    eg = [f'<g stroke="{CYAN}" stroke-width="1" stroke-linecap="round">']
    for (i, j) in edges:
        xs1 = [proj[k][i][0] for k in range(FR + 1)]
        ys1 = [proj[k][i][1] for k in range(FR + 1)]
        xs2 = [proj[k][j][0] for k in range(FR + 1)]
        ys2 = [proj[k][j][1] for k in range(FR + 1)]
        op = [max(0.05, 0.12 + 0.5 * ((proj[k][i][2] + proj[k][j][2]) / 2 + 1) / 2) for k in range(FR + 1)]
        eg.append(
            f'<line x1="{f(xs1[0])}" y1="{f(ys1[0])}" x2="{f(xs2[0])}" y2="{f(ys2[0])}" opacity="{f(op[0],2)}">'
            f'<animate attributeName="x1" values="{vals(xs1,0)}" {dur}/>'
            f'<animate attributeName="y1" values="{vals(ys1,0)}" {dur}/>'
            f'<animate attributeName="x2" values="{vals(xs2,0)}" {dur}/>'
            f'<animate attributeName="y2" values="{vals(ys2,0)}" {dur}/>'
            f'<animate attributeName="opacity" values="{vals(op,2)}" {dur}/></line>')
    eg.append("</g>")
    out.append("".join(eg))

    # ---------- nodes ----------
    ng = ['<g>']
    hubs = set(random.sample(range(len(pts)), 7))
    for i in range(len(pts)):
        xs = [proj[k][i][0] for k in range(FR + 1)]
        ys = [proj[k][i][1] for k in range(FR + 1)]
        zs = [proj[k][i][2] for k in range(FR + 1)]
        base = 3.4 if i in hubs else 2.2
        rs = [base * (0.65 + 0.45 * (z + 1) / 2) for z in zs]
        op = [0.25 + 0.75 * (z + 1) / 2 for z in zs]
        col = AMBER if i in hubs else (CYAN if i % 3 else "#A5F3FC")
        ng.append(
            f'<circle cx="{f(xs[0])}" cy="{f(ys[0])}" r="{f(rs[0])}" fill="{col}" opacity="{f(op[0],2)}"'
            + (' filter="url(#glow)"' if i in hubs else "") + ">"
            f'<animate attributeName="cx" values="{vals(xs)}" {dur}/>'
            f'<animate attributeName="cy" values="{vals(ys)}" {dur}/>'
            f'<animate attributeName="r" values="{vals(rs)}" {dur}/>'
            f'<animate attributeName="opacity" values="{vals(op,2)}" {dur}/></circle>')
    ng.append("</g>")
    out.append("".join(ng))

    # ---------- message pulses hopping along edges ----------
    adj = {i: [] for i in range(len(pts))}
    for i, j in edges:
        adj[i].append(j); adj[j].append(i)
    HOP = 4  # frames per hop
    for pi, col in enumerate([AMBER, PINK, CYAN, GREEN]):
        cur = random.choice(list(hubs))
        walk = [cur]
        while len(walk) * HOP < FR + 1:
            cur = random.choice(adj[cur]); walk.append(cur)
        walk.append(random.choice(adj[cur]))
        xs, ys, ops = [], [], []
        for k in range(FR + 1):
            h = k // HOP
            t = (k % HOP) / HOP
            a, b = walk[h], walk[h + 1]
            pa, pb = proj[k][a], proj[k][b]
            xs.append(pa[0] + (pb[0] - pa[0]) * t)
            ys.append(pa[1] + (pb[1] - pa[1]) * t)
            ops.append(0.35 + 0.65 * ((pa[2] + pb[2]) / 2 + 1) / 2)
        # loop closure: ensure last == first to avoid jump
        xs[-1], ys[-1], ops[-1] = xs[0], ys[0], ops[0]
        out.append(
            f'<circle r="3.6" fill="{col}" filter="url(#glow)" cx="{f(xs[0])}" cy="{f(ys[0])}">'
            f'<animate attributeName="cx" values="{vals(xs)}" {dur}/>'
            f'<animate attributeName="cy" values="{vals(ys)}" {dur}/>'
            f'<animate attributeName="opacity" values="{vals(ops,2)}" {dur}/></circle>')

    # ---------- orbit ring front half + orbiting chips ----------
    out.append(f'<path d="{ring_path(True)}" fill="none" stroke="{VIOLET}" stroke-opacity=".8" stroke-width="1.4"/>')
    chips = ["RAG", "MCP", "Agents", "LangGraph", "LLMOps"]
    ODUR = 20
    OF = 60

    def chip_layer(front):
        res = []
        for ci, label in enumerate(chips):
            xs, ys, sc, op = [], [], [], []
            for k in range(OF + 1):
                t = 2 * math.pi * (k / OF + ci / len(chips))
                q = rot((ring_r * math.cos(t), 0, ring_r * math.sin(t)), ring_tilt, 0, math.radians(-11))
                x, y, kk = project(q, SCX, SCY, R, cam=4.2)
                xs.append(x); ys.append(y)
                d = (q[2] / ring_r + 1) / 2
                sc.append(0.72 + 0.38 * d)
                o = 0.35 + 0.65 * d
                vis = (q[2] >= 0) == front
                op.append(o if vis else 0)
            w = 18 + 9 * len(label)
            tr = ";".join(f"{f(x)} {f(y)}" for x, y in zip(xs, ys))
            res.append(
                f'<g><animateTransform attributeName="transform" type="translate" values="{tr}" dur="{ODUR}s" repeatCount="indefinite"/>'
                f'<g opacity="{f(op[0],2)}"><animate attributeName="opacity" values="{vals(op,2)}" dur="{ODUR}s" repeatCount="indefinite"/>'
                f'<g><animateTransform attributeName="transform" type="scale" values="{vals(sc,2)}" dur="{ODUR}s" repeatCount="indefinite"/>'
                f'<rect x="{f(-w/2)}" y="-13" width="{f(w)}" height="26" rx="13" fill="{PANEL2}" stroke="{VIOLET}" stroke-width="1.2"/>'
                f'<text x="0" y="4.5" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="600" fill="{TEXT}">{label}</text>'
                f'</g></g></g>')
        return "".join(res)

    out.append(chip_layer(True))
    out.insert(BACK_CHIPS_IDX, chip_layer(False))

    # ---------- left: text block ----------
    LX = 64
    out.append(
        f'<g font-family="{MONO}" font-size="16" fill="{MUTED}">'
        f'<text x="{LX}" y="92"><tspan fill="{GREEN}">➜</tspan> <tspan fill="{CYAN}">~/bengaluru</tspan> whoami</text></g>')
    out.append(
        f'<text x="{LX-3}" y="160" font-family="{SANS}" font-size="62" font-weight="800" letter-spacing="-1.5" fill="url(#nameg)">Chiranjeev Kumar</text>')
    out.append(
        f'<text x="{LX}" y="198" font-family="{SANS}" font-size="20" font-weight="500" fill="{MUTED}">'
        f'GenAI Engineer <tspan fill="{DIM}">·</tspan> Data Science Consultant @ <tspan fill="{TEXT}" font-weight="700">Deloitte</tspan></text>')

    # typed rotating lines
    lines = [
        "Leading a GenAI Centre of Excellence",
        "Shipping agentic systems to production",
        "RAG · multi-agent · MCP · LLMOps",
        "Building AI tools for Bharat 🇮🇳",
    ]
    lines[3] = "Building AI tools for Bharat"
    CH = 11.4  # forced glyph advance via textLength
    slot = 4.0
    total = slot * len(lines)
    ty = 252
    out.append(f'<rect x="{LX-12}" y="{ty-26}" width="520" height="40" rx="10" fill="{BG}" stroke="{STROKE}"/>')
    out.append(f'<text x="{LX}" y="{ty}" font-family="{MONO}" font-size="17" fill="{GREEN}">$</text>')
    tx = LX + 22
    for li, s in enumerate(lines):
        wpx = CH * len(s)
        t0 = li * slot / total
        t_typed = (li * slot + 1.3) / total
        t_hold = (li * slot + 3.2) / total
        t_end = (li * slot + 3.7) / total
        kt = [0, t0, t_typed, t_hold, t_end, 1]
        ws = [0, 0, wpx, wpx, 0, 0]
        # dedupe keyTimes at 0
        if t0 == 0:
            kt = [0, t_typed, t_hold, t_end, 1]; ws = [0, wpx, wpx, 0, 0]
        ktv = ";".join(f(k, 4) for k in kt)
        cid = f"tc{li}"
        out.append(
            f'<clipPath id="{cid}"><rect x="{tx}" y="{ty-22}" height="32" width="0">'
            f'<animate attributeName="width" values="{vals(ws)}" keyTimes="{ktv}" dur="{total}s" repeatCount="indefinite"/></rect></clipPath>'
            f'<text clip-path="url(#{cid})" x="{tx}" y="{ty}" font-family="{MONO}" font-size="17" fill="{TEXT}" '
            f'textLength="{f(wpx)}" lengthAdjust="spacingAndGlyphs">{esc(s)}</text>')
        # caret follows
        cx = [tx + w for w in ws]
        out.append(
            f'<rect x="{tx}" y="{ty-16}" width="9" height="20" fill="{CYAN}" opacity="0">'
            f'<animate attributeName="x" values="{vals(cx)}" keyTimes="{ktv}" dur="{total}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{f(t0+0.0001,4)};{f(t_end,4)};{f(t_end+0.0001,4)};1" dur="{total}s" repeatCount="indefinite" calcMode="discrete"/>'
            f'</rect>')
    # caret blink overlay (cheap): a blinking mask over caret area not needed; add subtle blink on the whole caret layer
    # meta chips
    chips2 = [("📍", "Bengaluru, India"), ("◆", "GenAI CoE Lead"), ("⚡", "Kaggle Notebooks Expert")]
    cx0 = LX
    for icon, label in chips2:
        w = 38 + 9.2 * len(label)
        out.append(
            f'<g transform="translate({f(cx0)},300)"><rect width="{f(w)}" height="30" rx="15" fill="{PANEL2}" stroke="{STROKE}"/>'
            f'<text x="14" y="20" font-family="{SANS}" font-size="14" fill="{CYAN}">{icon}</text>'
            f'<text x="34" y="20.5" font-family="{SANS}" font-size="15" fill="{TEXT}">{esc(label)}</text></g>')
        cx0 += w + 10
    # status dot
    out.append(
        f'<g transform="translate({LX},366)"><circle cx="6" cy="0" r="5" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>'
        f'<circle cx="6" cy="0" r="5" fill="none" stroke="{GREEN}"><animate attributeName="r" values="5;13" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>'
        f'<text x="22" y="5" font-family="{MONO}" font-size="15" fill="{MUTED}">now building <tspan fill="{TEXT}">Reel Studio</tspan> '
        f'<tspan fill="{DIM}">—</tspan> brief → finished reel</text></g>')

    # corner label
    out.append(f'<text x="{W-24}" y="{H-18}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}">agent-network.svg · 58 nodes · rendered in pure SVG</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
