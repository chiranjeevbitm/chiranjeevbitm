"""Animated isometric agentic-RAG pipeline: packets flow block to block, blocks light up, corrective loop."""
from common import *

W, H = 1200, 440

STAGES = [
    ("01", "Ingest", "PDF · image · text"),
    ("02", "Embed + Index", "Azure AI Search"),
    ("03", "Retrieve", "hybrid + rerank"),
    ("04", "Orchestrate", "LangGraph agents"),
    ("05", "Act", "tools via MCP"),
    ("06", "Answer", "grounded + evals"),
]


def build():
    defs, bg = panel_bg(W, H, gid="q")
    defs += (f'<filter id="pg" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/>'
             f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
             f'<linearGradient id="flow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    out = [svg_open(W, H, "How I build agentic RAG systems: ingest, index, retrieve, orchestrate, act via MCP, answer — animated pipeline", defs), bg]
    out.append(f'<text x="48" y="54" font-family="{MONO}" font-size="15" fill="{CYAN}">// how i ship</text>')
    out.append(f'<text x="48" y="88" font-family="{SANS}" font-size="30" font-weight="800" fill="{TEXT}">Agentic RAG, end to end — in production</text>')

    n = len(STAGES)
    x0, dx = 130, 188
    yb = 250
    CYC = 6.0
    xs = [x0 + i * dx for i in range(n)]
    # floor track
    out.append(f'<path d="M{xs[0]-60},{yb+46} L{xs[-1]+60},{yb+46}" stroke="{STROKE}" stroke-width="10" stroke-linecap="round"/>')
    out.append(f'<path d="M{xs[0]-60},{yb+46} L{xs[-1]+60},{yb+46}" stroke="url(#flow)" stroke-width="2" stroke-dasharray="6 10" opacity=".8">'
               f'<animate attributeName="stroke-dashoffset" values="32;0" dur="1s" repeatCount="indefinite"/></path>')

    # corrective loop arc 06 -> 03 (drawn first, behind)
    ax1, ax2 = xs[5], xs[2]
    arc = f"M{ax1},{yb-58} C{ax1-40},{yb-150} {ax2+40},{yb-150} {ax2},{yb-58}"
    out.append(f'<path id="loop" d="{arc}" fill="none" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="5 7" opacity=".75">'
               f'<animate attributeName="stroke-dashoffset" values="0;-24" dur="1s" repeatCount="indefinite"/></path>')
    mx = (ax1 + ax2) / 2
    out.append(f'<circle r="4" fill="{AMBER}" filter="url(#pg)"><animateMotion dur="3s" repeatCount="indefinite" begin="1.5s"><mpath href="#loop" xlink:href="#loop"/></animateMotion>'
               f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="3s" begin="1.5s" repeatCount="indefinite"/></circle>')
    out.append(f'<g transform="translate({mx},{yb-128})"><rect x="-176" y="-16" width="352" height="30" rx="15" fill="{PANEL2}" stroke="{AMBER}" stroke-opacity=".6"/>'
               f'<text x="0" y="4.5" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{AMBER}">↺ corrective loop (CRAG) if ungrounded</text></g>')

    for i, (num, name, sub) in enumerate(STAGES):
        x = xs[i]
        t_hit = i / n
        # glow pulse when packet arrives
        kt = f"0;{f(max(0,t_hit-0.001),4)};{f(t_hit+0.02,4)};{f(min(1,t_hit+0.16),4)};1" if i else "0;0.02;0.16;1"
        vals_op = "0;0;1;0;0" if i else "1;1;0;0"
        if i == 0:
            kt = "0;0.02;0.16;1"
        bob = f"0 0;0 -6;0 0"
        top = PANEL2
        out.append(f'<g><animateTransform attributeName="transform" type="translate" values="{bob}" dur="{3 + (i%3)*0.4}s" repeatCount="indefinite"/>')
        # shadow
        out.append(f'<ellipse cx="{x}" cy="{yb+46}" rx="46" ry="12" fill="#000" opacity=".35"/>')
        out.append(iso_cube(x, yb - 40, 50, 46, "#13213A", "#0C1628", "#101C33", stroke=STROKE))
        # lit top overlay
        hs = 25
        tp = f"M{x},{yb-40-hs} L{x+50},{yb-40} L{x},{yb-40+hs} L{x-50},{yb-40}Z"
        col = [CYAN, CYAN, TEAL, VIOLET, PINK, GREEN][i]
        out.append(f'<path d="{tp}" fill="{col}" opacity=".18"/>')
        out.append(f'<path d="{tp}" fill="{col}" opacity="0" filter="url(#pg)"><animate attributeName="opacity" values="{vals_op}" keyTimes="{kt}" dur="{CYC}s" repeatCount="indefinite"/></path>')
        out.append(f'<text x="{x}" y="{yb-35}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}">{num}</text>')
        out.append("</g>")
        out.append(f'<text x="{x}" y="{yb+90}" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">{esc(name)}</text>')
        out.append(f'<text x="{x}" y="{yb+116}" text-anchor="middle" font-family="{MONO}" font-size="14.5" fill="{MUTED}">{esc(sub)}</text>')

    # packets travelling along the top of the blocks
    path = f"M{xs[0]},{yb-40} " + " ".join(f"L{x},{yb-40}" for x in xs[1:])
    out.append(f'<path id="track" d="{path}" fill="none"/>')
    for k, col in enumerate([CYAN, VIOLET, AMBER]):
        b = f"{k * CYC / 3:.1f}s"
        out.append(f'<g><animateMotion dur="{CYC}s" begin="{b}" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath href="#track" xlink:href="#track"/></animateMotion>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.92;1" dur="{CYC}s" begin="{b}" repeatCount="indefinite"/>'
                   f'<circle r="5" fill="{col}" filter="url(#pg)"/><circle r="11" fill="none" stroke="{col}" stroke-opacity=".5"/></g>')
    out.append(f'<text x="{W-36}" y="{H-22}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}">the pattern behind multimodal_crag · multi_agentic_chatbot_cRAG · client work</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
