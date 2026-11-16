"""Project cards, section headers, divider and footer."""
import math
import textwrap
from common import *

CARDS = [
    ("reel-studio", "Reel Studio", "Brief in, finished 9:16 explainer reel out — researched, scripted, voiced and hand-drawn in SVG.",
     ["Claude Code plugin", "GSAP", "three.js", "MIT"], PINK, "▶", "open source · v0.1"),
    ("multimodal_crag", "Multimodal CRAG", "Full-stack multimodal Corrective RAG pipeline that reasons over PDFs, images and text.",
     ["Corrective RAG", "Multimodal", "Python"], CYAN, "◫", "rag"),
    ("multi_agentic_chatbot_cRAG", "Multi-agent cRAG Chatbot", "LangGraph-orchestrated multi-agent assistant with corrective retrieval-augmented generation.",
     ["LangGraph", "Agents", "CRAG"], VIOLET, "⬡", "agents"),
    ("Leadership-Insight-Agent", "Leadership Insight Agent", "RAG-powered conversational agent for analysing Apple's corporate strategy.",
     ["RAG", "LLM", "Strategy"], AMBER, "▲", "rag"),
    ("medguardian", "MedGuardian", "Real-time emergency response platform and safety ecosystem for physicians in India.",
     ["HealthTech", "Real-time", "India"], GREEN, "✚", "health"),
    ("shikshak-Sahayak", "Shikshak Sahayak", "Digital ecosystem and educational app for Bihar Board educators.",
     ["EdTech", "Bharat", "App"], "#60A5FA", "✎", "edtech"),
]


def card(slug, title, desc, tags, col, glyph, kicker, idx):
    W, H = 590, 262
    gid = f"c{idx}"
    defs = (
        f'<linearGradient id="{gid}b" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{col}" stop-opacity=".9"/><stop offset=".35" stop-color="{STROKE}"/>'
        f'<stop offset=".65" stop-color="{STROKE}"/><stop offset="1" stop-color="{col}" stop-opacity=".5"/>'
        f'<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="8s" repeatCount="indefinite"/></linearGradient>'
        f'<radialGradient id="{gid}g" cx=".15" cy=".5" r=".55"><stop offset="0" stop-color="{col}" stop-opacity=".18"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
        f'<filter id="{gid}f" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )
    out = [svg_open(W, H, f"{title} — {desc}", defs)]
    out.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{PANEL}" stroke="url(#{gid}b)" stroke-width="1.6"/>')
    out.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#{gid}g)"/>')

    # isometric stack icon
    ix, iy = 100, 140
    out.append(f'<ellipse cx="{ix}" cy="{iy+52}" rx="60" ry="16" fill="#000" opacity=".35"/>')
    layer_cols = [("#0F1B30", "#0A1222", "#0C1628"), ("#13233D", "#0C1628", "#101E36"), (None, None, None)]
    for li in range(3):
        y = iy + 30 - li * 26
        amp = (li + 1) * 6
        vv = f"0 0;0 {-amp};0 0"
        if li < 2:
            top, l, r = layer_cols[li]
            cube = iso_cube(ix, y, 56, 12, top, l, r, stroke=STROKE)
        else:
            cube = iso_cube(ix, y, 56, 14, "#16304A", "#0E2036", "#122843", stroke=col)
            hs = 28
            cube += (f'<path d="M{ix},{y-hs} L{ix+56},{y} L{ix},{y+hs} L{ix-56},{y}Z" fill="{col}" opacity=".22">'
                     f'<animate attributeName="opacity" values=".12;.38;.12" dur="2.6s" repeatCount="indefinite"/></path>'
                     f'<text x="{ix}" y="{y+7}" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="{col}" filter="url(#{gid}f)" '
                     f'transform="matrix(1 0 0 .62 0 {f(y*0.38)})">{glyph}</text>')
        out.append(f'<g><animateTransform attributeName="transform" type="translate" values="{vv}" dur="3.2s" repeatCount="indefinite"/>{cube}</g>')
    # sparkles
    for k, (sx, sy) in enumerate([(ix - 62, iy - 52), (ix + 58, iy - 40), (ix + 40, iy + 60)]):
        out.append(f'<circle cx="{sx}" cy="{sy}" r="2" fill="{col}"><animate attributeName="opacity" values="0;1;0" dur="{2 + k*0.7}s" begin="{k*0.5}s" repeatCount="indefinite"/></circle>')

    X = 200
    out.append(f'<text x="{X}" y="44" font-family="{MONO}" font-size="13" fill="{col}">github.com/chiranjeevbitm/</text>')
    out.append(f'<text x="{X}" y="78" font-family="{SANS}" font-size="25" font-weight="800" fill="{TEXT}">{esc(title)}</text>')
    lines = textwrap.wrap(desc, 40)[:3]
    for i, ln in enumerate(lines):
        out.append(f'<text x="{X}" y="{110 + i*23}" font-family="{SANS}" font-size="16.5" fill="{MUTED}">{esc(ln)}</text>')
    tx = X
    ty = 110 + len(lines) * 23 + 14
    for t in tags:
        w = 20 + 7.9 * len(t)
        out.append(f'<rect x="{f(tx)}" y="{ty}" width="{f(w)}" height="27" rx="13.5" fill="{PANEL2}" stroke="{col}" stroke-opacity=".55"/>'
                   f'<text x="{f(tx + w/2)}" y="{ty+18}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{TEXT}">{esc(t)}</text>')
        tx += w + 8
    # arrow cta
    out.append(f'<g transform="translate({W-34},44)"><text x="0" y="0" text-anchor="end" font-family="{MONO}" font-size="13.5" fill="{col}">view repo</text>'
               f'<text x="14" y="0" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{col}">→<animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.4s" repeatCount="indefinite"/></text></g>')
    out.append("</svg>")
    return "\n".join(out)


def header(num, title, sub, col, name, theme="dark"):
    W, H = 1200, 86
    TX, MU, ST = (TEXT, MUTED, STROKE) if theme == "dark" else ("#0F172A", "#57606A", "#D0D7DE")
    out = [svg_open(W, H, f"{title} — {sub}")]
    out.append(f'<text x="4" y="30" font-family="{MONO}" font-size="14" fill="{col}">{num} /</text>')
    out.append(f'<text x="4" y="64" font-family="{SANS}" font-size="30" font-weight="800" fill="{TX}" letter-spacing="-.5">{esc(title)}</text>')
    tw = 17 * len(title) + 30
    out.append(f'<text x="{tw}" y="64" font-family="{MONO}" font-size="16" fill="{MU}">{esc(sub)}</text>')
    out.append(f'<line x1="4" y1="78" x2="{W-4}" y2="78" stroke="{ST}" stroke-width="1.5"/>')
    out.append(f'<rect x="4" y="76.5" width="160" height="3" rx="1.5" fill="{col}"><animate attributeName="x" values="4;{W-164};4" dur="9s" repeatCount="indefinite"/>'
               f'<animate attributeName="width" values="160;60;160" dur="9s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    return "\n".join(out)


def footer(theme="dark"):
    TX, MU = (TEXT, MUTED) if theme == "dark" else ("#0F172A", "#57606A")
    W, H = 1200, 170
    defs = (f'<linearGradient id="fw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    out = [svg_open(W, H, "Thanks for visiting — let's build something agentic", defs)]

    def wave(amp, phase, yb, n=8):
        pts = []
        for k in range(n * 8 + 1):
            x = W * k / (n * 8)
            y = yb + amp * math.sin(2 * math.pi * (k / (n * 8)) * 2 + phase)
            pts.append(f"{f(x)},{f(y)}")
        return f"M0,{H} L" + " L".join(pts) + f" L{W},{H}Z"

    for li, (amp, yb, op, d) in enumerate([(12, 92, .18, 9), (16, 108, .28, 7), (10, 126, .5, 5)]):
        frames = [wave(amp, 2 * math.pi * k / 6 + li, yb) for k in range(7)]
        out.append(f'<path d="{frames[0]}" fill="url(#fw)" opacity="{op}"><animate attributeName="d" values="{";".join(frames)}" dur="{d}s" repeatCount="indefinite"/></path>')
    out.append(f'<text x="{W/2}" y="46" text-anchor="middle" font-family="{SANS}" font-size="25" font-weight="800" fill="{TX}">Thanks for stopping by — let\'s build something agentic.</text>')
    out.append(f'<text x="{W/2}" y="72" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{MU}">every visual on this page is hand-built SVG — no GIFs, no trackers</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import os, sys
    d = sys.argv[1]
    os.makedirs(f"{d}/cards", exist_ok=True)
    for i, c in enumerate(CARDS):
        open(f"{d}/cards/{c[0].lower()}.svg", "w").write(card(*c, i))
    hdrs = [
        ("01", "About", "whoami, but longer", CYAN, "about"),
        ("02", "How I build", "the pattern behind most of my work", TEAL, "build"),
        ("03", "Featured work", "click a card to open the repo", VIOLET, "projects"),
        ("04", "Stack", "tools in orbit", AMBER, "stack"),
        ("05", "Activity", "contributions, in 3D", GREEN, "activity"),
        ("06", "Connect", "say hello", PINK, "connect"),
    ]
    for th in ("dark", "light"):
        for h in hdrs:
            open(f"{d}/h-{h[4]}-{th}.svg", "w").write(header(*h, theme=th))
        open(f"{d}/footer-{th}.svg", "w").write(footer(th))
