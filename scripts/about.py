"""neofetch-style terminal card with lines revealing in sequence, plus an isometric monogram."""
import math
from common import *

W, H = 1200, 520


def build():
    defs, bg = panel_bg(W, H, gid="a")
    defs += (f'<filter id="ag" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
             f'<linearGradient id="mono" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    out = [svg_open(W, H, "About Chiranjeev — neofetch-style terminal card", defs), bg]
    # title bar
    out.append(f'<path d="M1 19 a18 18 0 0 1 18 -18 H{W-19} a18 18 0 0 1 18 18 V44 H1Z" fill="{PANEL2}"/>')
    out.append(f'<line x1="1" y1="44" x2="{W-1}" y2="44" stroke="{STROKE}"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        out.append(f'<circle cx="{28 + i*20}" cy="23" r="6" fill="{c}"/>')
    out.append(f'<text x="{W/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTED}">chiranjeev@bengaluru — zsh — 120×32</text>')

    # ---- isometric monogram tower (left) ----
    cx, base = 200, 320
    s = 40
    layers = 6
    cols = [(CYAN, "#1B6F80", "#24A3BA"), (VIOLET, "#4C2F99", "#6D45D6")]
    out.append(f'<ellipse cx="{cx}" cy="{base+40}" rx="120" ry="34" fill="{CYAN}" opacity=".12" filter="url(#ag)"/>')
    # grid plate
    out.append(iso_cube(cx, base + 18, 110, 10, "#0F1B30", "#0A1222", "#0C1628", stroke=STROKE))
    blocks = []
    for gx in range(-1, 2):
        for gy in range(-1, 2):
            hgt = [3, 5, 2, 4, 6, 3, 2, 4, 3][(gx + 1) * 3 + (gy + 1)]
            blocks.append((gx, gy, hgt))
    blocks.sort(key=lambda b: (b[0] + b[1]))
    for bi, (gx, gy, hgt) in enumerate(blocks):
        x = cx + (gx - gy) * s * 0.98
        y = base + (gx + gy) * s * 0.49
        top, left, right = cols[(gx + gy) % 2]
        hpx = hgt * 16
        y0 = y - hpx
        # bars grow/shrink like an equaliser (translate + scale of height via path animate is heavy; use transform)
        amp = [0, -18, 6, -10, 0]
        vv = ";".join(f"0 {a * ((bi % 3) + 1) / 3:.1f}" for a in amp)
        out.append(
            f'<g><animateTransform attributeName="transform" type="translate" values="{vv}" dur="{5 + bi % 4}s" repeatCount="indefinite"/>'
            + iso_cube(x, y0, s * 0.82, hpx, top, left, right, stroke="#0A1120") + "</g>")
    out.append(f'<text x="{cx}" y="{base+86}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{DIM}">commits → skyline</text>')

    # ---- info lines (right) ----
    X = 400
    Y0 = 92
    LH = 30
    lines = [
        [("chiranjeev", CYAN, True), ("@", MUTED, False), ("bengaluru", CYAN, True)],
        [("─" * 40, DIM, False)],
        [("role     ", AMBER, True), ("Data Science Consultant · AI/ML Engineer", TEXT, False)],
        [("org      ", AMBER, True), ("Deloitte — leads a GenAI Centre of Excellence", TEXT, False)],
        [("focus    ", AMBER, True), ("production GenAI · RAG · agentic systems · MCP", TEXT, False)],
        [("before   ", AMBER, True), ("Tredence · Soroco · TCS", TEXT, False)],
        [("edu      ", AMBER, True), ("CSE, BIT Mesra · MSc ML & AI, LJMU · IIIT Bangalore", TEXT, False)],
        [("certs    ", AMBER, True), ("NVIDIA Agentic AI · Azure AI Engineer · Claude Certified", TEXT, False)],
        [("kaggle   ", AMBER, True), ("Notebooks Expert — top 0.5%", TEXT, False)],
        [("paper    ", AMBER, True), ("TLCoV — automated COVID-19 screening (Elsevier, 2021)", TEXT, False)],
        [("founder  ", AMBER, True), ("co-founder, Arogya Sahayak — health-tech for Bihar", TEXT, False)],
    ]
    CYCLE = 16.0
    out.append(f'<text x="{X}" y="{Y0 - 30}" font-family="{MONO}" font-size="17" fill="{MUTED}">'
               f'<tspan fill="{GREEN}">➜</tspan> <tspan fill="{CYAN}">~</tspan> neofetch --profile</text>')
    for i, segs in enumerate(lines):
        y = Y0 + 8 + i * LH
        t_on = (0.6 + i * 0.32) / CYCLE
        t_off = (CYCLE - 1.2) / CYCLE
        kt = f"0;{f(t_on,4)};{f(t_on+0.02,4)};{f(t_off,4)};{f(t_off+0.03,4)};1"
        tsp = []
        for txt, col, bold in segs:
            tsp.append(f'<tspan fill="{col}"' + (' font-weight="700"' if bold else "") + f'>{esc(txt)}</tspan>')
        out.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="-8 0;-8 0;0 0;0 0;0 0;0 0" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>'
            f'<text x="{X}" y="{y}" font-family="{MONO}" font-size="17" xml:space="preserve">{"".join(tsp)}</text></g>')
    # colour blocks
    yb = Y0 + 8 + len(lines) * LH + 4
    palette = ["#0E1729", "#F87171", GREEN, AMBER, "#60A5FA", VIOLET, CYAN, TEXT]
    t_on = (0.6 + len(lines) * 0.32) / CYCLE
    t_off = (CYCLE - 1.2) / CYCLE
    kt = f"0;{f(t_on,4)};{f(t_on+0.02,4)};{f(t_off,4)};{f(t_off+0.03,4)};1"
    out.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>')
    for i, c in enumerate(palette):
        out.append(f'<rect x="{X + i*30}" y="{yb}" width="26" height="14" rx="2" fill="{c}"/>')
    out.append("</g>")
    # blinking prompt at bottom
    out.append(f'<text x="{X}" y="{H-24}" font-family="{MONO}" font-size="15" fill="{MUTED}"><tspan fill="{GREEN}">➜</tspan> <tspan fill="{CYAN}">~</tspan></text>'
               f'<rect x="{X+40}" y="{H-38}" width="9" height="18" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
