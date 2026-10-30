"""Write the five README diagrams into docs/assets/ (run: python docs/assets/src/make_diagrams.py docs/assets). Sizes are set for GitHub's ~830 px README column (scale ~0.67)."""
import sys, pathlib
OUT = pathlib.Path(sys.argv[1])
GOLD, RULE, INK, CAP, DIM = '#d2ab68', '#a8834f', '#efe9dc', '#b3ab9a', '#8c8476'
HOLDS, PARTLY, FAILS = '#d8b26e', '#8f7d55', '#c4553f'
STYLE = f'''  <style>
    svg {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }}
    .mono {{ font-family: "SF Mono", ui-monospace, Menlo, Consolas, monospace; }}
    .bg {{ fill: #1b1a17; }}
    .panel {{ fill: #24221e; stroke: #ffffff; stroke-opacity: 0.09; stroke-width: 1.5; }}
    .hi {{ fill: #2b2721; stroke: {RULE}; stroke-opacity: 0.75; stroke-width: 1.6; }}
    .well {{ fill: #141311; stroke: #ffffff; stroke-opacity: 0.08; stroke-width: 1; }}
    .h1 {{ fill: {INK}; font-size: 34px; font-weight: 700; letter-spacing: -0.5px; }}
    .h2 {{ fill: {INK}; font-size: 23px; font-weight: 700; letter-spacing: -0.3px; }}
    .cap {{ fill: {CAP}; font-size: 18.5px; }}
    .lab {{ fill: {DIM}; font-size: 13.5px; letter-spacing: 0.7px; }}
    .m {{ fill: #d4ccbb; font-size: 15.5px; }}
    .dim {{ fill: {DIM}; }}
    .gold {{ fill: {GOLD}; }}
    .ink {{ fill: {INK}; }}
    .seal {{ fill: none; stroke: {RULE}; stroke-width: 2.4; }}
    .tick {{ fill: none; stroke: {GOLD}; stroke-width: 2.8; stroke-linecap: round; stroke-linejoin: round; }}
    .arrow {{ fill: none; stroke: {RULE}; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }}
    .chip {{ fill: none; stroke: {INK}; stroke-opacity: 0.24; stroke-width: 1.4; }}
  </style>'''

def svg(name, w, h, title, desc, body):
    head = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{name}-t {name}-d">
  <title id="{name}-t">{title}</title>
  <desc id="{name}-d">{desc}</desc>
{STYLE}
  <rect class="bg" x="0" y="0" width="{w}" height="{h}" rx="24"/>
  <!-- The seal (a square with a tick) heads every celsus diagram. -->
  <rect class="seal" x="44" y="36" width="38" height="38" rx="8"/>
  <path class="tick" d="M53 55 L61 63 L74 47"/>
  <text class="h1" x="100" y="68">{title}</text>
'''
    (OUT / f'{name}.svg').write_text(head + '\n'.join('  ' + b for b in body) + '\n</svg>\n')

def text(x, y, s, cls='cap', **kw):
    # A class's CSS beats a font-size attribute, so a size given here goes in style, which beats the class.
    size = kw.pop('font_size', None)
    extra = ''.join(f' {k.replace("_", "-")}="{v}"' for k, v in kw.items())
    if size is not None:
        extra += f' style="font-size:{size}px"'
    return f'<text class="{cls}" x="{x}" y="{y}"{extra}>{s}</text>'
def arrow_r(x0, x1, y):
    return f'<path class="arrow" d="M{x0} {y} H{x1} M{x1-6} {y-6} L{x1} {y} L{x1-6} {y+6}"/>'
def arrow_d(x, y0, y1):
    return f'<path class="arrow" d="M{x} {y0} V{y1} M{x-6} {y1-6} L{x} {y1} L{x+6} {y1-6}"/>'
def tick(x, y, s=1.0, w=2.8):
    return f'<path class="tick" stroke-width="{w}" d="M{x} {y} L{x+7*s:.1f} {y+7*s:.1f} L{x+20*s:.1f} {y-10*s:.1f}"/>'
def dot(cx, cy, kind, r=6.5):
    if kind == 'holds': return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{HOLDS}"/>'
    if kind == 'partly': return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PARTLY}"/>'
    if kind == 'fails': return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FAILS}"/>'
    if kind == 'cnc': return f'<circle cx="{cx}" cy="{cy}" r="{r-0.8}" fill="none" stroke="{CAP}" stroke-width="1.7"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{r-0.8}" fill="none" stroke="{DIM}" stroke-width="1.7" stroke-dasharray="2.6 2.6"/>'
def paper(x, y, op=0.92, lines=True):
    b = [f'<path d="M{x} {y} H{x+44} L{x+58} {y+14} V{y+74} H{x} Z" fill="{INK}" fill-opacity="{op}"/>',
         f'<path d="M{x+44} {y} V{y+14} H{x+58}" fill="#c9c1b0" fill-opacity="{op}"/>']
    if lines:
        for k, (ln, yy) in enumerate([(40, 24), (34, 33), (18, 42), (40, 51), (28, 60)]):
            b.append(f'<line x1="{x+8}" y1="{y+yy}" x2="{x+8+ln}" y2="{y+yy}" stroke="#1b1a17" stroke-opacity="0.45" stroke-width="3"/>')
        b.append(f'<rect x="{x+29}" y="{y+39}" width="19" height="6" rx="1" fill="{RULE}"/>')
    return b

# ---------- 1. check-flow: the hero ----------
b = []
PW, GAP, X0, PY, PH = 210, 26, 44, 112, 210
xs = [X0 + i * (PW + GAP) for i in range(5)]
b.append(f'<path d="M{xs[3]+PW/2} {PY-2} C{xs[3]+PW/2} {PY-28} {xs[2]+PW/2} {PY-28} {xs[2]+PW/2} {PY-6}" fill="none" stroke="{RULE}" stroke-width="1.8" stroke-dasharray="4 5" stroke-linecap="round"/>')
b.append(f'<path class="arrow" d="M{xs[2]+PW/2-6} {PY-12} L{xs[2]+PW/2} {PY-5} L{xs[2]+PW/2+6} {PY-12}"/>')
b.append(text((xs[2] + xs[3]) / 2 + PW / 2, PY - 30, 'a finding sends it back', 'mono lab', text_anchor='middle'))
steps = [('Reads the paper', ['The arXiv LaTeX,', 'every file inlined']),
         ('Typed spec', ['Every number,', 'copied as printed']),
         ('Rebuilds it', ['On public data,', 'in a sandbox']),
         ('Two reviews', ['Either one can', 'send it back']),
         ('Code judges', ['By published', 'replication rules'])]
for i, (x, (t, cap)) in enumerate(zip(xs, steps)):
    b.append(f'<rect class="panel" x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="16"/>')
    ix, iy = x + 20, PY + 20
    if i == 0:
        b += paper(ix, iy - 2)
        b.append(text(ix + 74, iy + 70, 'arXiv', 'mono lab'))
    elif i == 1:
        b.append(f'<rect class="well" x="{ix}" y="{iy}" width="{PW-40}" height="76" rx="9"/>')
        for k, w in enumerate(['hypothesis', 'sample', 'method']):
            b.append(text(ix + 14, iy + 19 + k * 16, w, 'mono m', font_size=14))
        b.append(text(ix + 14, iy + 67, 'numbers', 'mono gold', font_size=14))
    elif i == 2:
        b.append(f'<rect class="well" x="{ix}" y="{iy}" width="{PW-40}" height="76" rx="9"/>')
        for k in range(3):
            b.append(f'<circle cx="{ix+13+k*11}" cy="{iy+12}" r="3.5" fill="{INK}" fill-opacity="0.25"/>')
        b.append(f'<text class="mono m" x="{ix+12}" y="{iy+42}"><tspan class="gold">$</tspan> python</text>')
        b.append(text(ix + 12, iy + 62, '  replicate.py', 'mono m'))
        b.append(f'<rect x="{ix+136}" y="{iy+50}" width="9" height="15" fill="{GOLD}"/>')
    elif i == 3:
        for k, cx in enumerate([ix + 38, ix + 122]):
            b.append(f'<circle cx="{cx}" cy="{iy+34}" r="30" fill="none" stroke="{INK}" stroke-opacity="0.5" stroke-width="2"/>')
            b.append(tick(cx - 12, iy + 34, 1.15))
    else:
        b.append(f'<rect class="well" x="{ix}" y="{iy}" width="{PW-40}" height="76" rx="9"/>')
        b.append(text(ix + 12, iy + 22, 'paper', 'mono dim', font_size=15))
        b.append(text(ix + PW - 52, iy + 22, '0.4531', 'mono m', text_anchor='end'))
        b.append(text(ix + 12, iy + 44, 'here', 'mono dim', font_size=15))
        b.append(text(ix + PW - 52, iy + 44, '0.4482', 'mono m', text_anchor='end'))
        b.append(tick(ix + 12, iy + 62, 0.62, 2.4))
        b.append(text(ix + 32, iy + 67, 'consistent', 'mono gold', font_size=15))
    b.append(text(x + 20, PY + 136, t, 'h2'))
    b.append(text(x + 20, PY + 164, cap[0]))
    b.append(text(x + 20, PY + 188, cap[1]))
    if i < 4:
        b.append(arrow_r(x + PW + 4, x + PW + GAP - 4, PY + PH / 2))
b.append(arrow_d(xs[4] + PW / 2, PY + PH + 4, PY + PH + 26))
VY = PY + PH + 30
b.append(f'<rect class="well" x="44" y="{VY}" width="1152" height="96" rx="14"/>')
b.append(f'<text class="mono" x="68" y="{VY+38}" font-size="17"><tspan class="gold">→ </tspan><tspan class="ink">The paper’s numbers hold up: 84 of 84 checked results match within their uncertainty.</tspan></text>')
lx = 74
for kind, label in [('holds', 'holds up'), ('partly', 'partly holds up'), ('fails', 'does not hold up'), ('cnc', 'could not check: the checker’s own failure, never the paper’s')]:
    b.append(dot(lx, VY + 70, kind, 6.5))
    b.append(text(lx + 14, VY + 76, label, font_size=17))
    lx += {'holds': 104, 'partly': 160, 'fails': 172}.get(kind, 0)
svg('check-flow', 1240, VY + 96 + 36, 'One paper in, one verdict out',
    'Five steps. Reads the paper: the arXiv LaTeX, with every file inlined. Typed spec: Muse copies every reported number as printed, and code checks each one is in the LaTeX. Rebuilds it: Muse writes and runs the script on public data in a sandbox, and only a fresh re-run counts. Two reviews: independent, and a finding from either sends the script back to be rebuilt. Code judges: each number, by rules from published replication practice, for example 0.4531 in the paper against 0.4482 here, consistent. The verdict comes out in plain words: the paper’s numbers hold up, 84 of 84 checked results match within their uncertainty. The verdicts are holds up, partly holds up, does not hold up, and could not check, which is the checker’s own failure and never counts against the paper.', b)

# ---------- 2. vision ----------
b = []
b.append(text(44, 128, 'SOFTWARE', 'mono lab'))
cx = 152
for k, w in enumerate(['commit', 'tests pass', 'merge']):
    cw = len(w) * 9.4 + 34
    b.append(f'<rect class="chip" x="{cx}" y="{106}" width="{cw:.0f}" height="32" rx="16"/>')
    b.append(text(cx + cw / 2, 128, w, 'mono m', text_anchor='middle', font_size=15))
    cx += cw
    if k < 2:
        b.append(f'<path d="M{cx+8:.0f} 122 H{cx+28:.0f} M{cx+22:.0f} 116 L{cx+28:.0f} 122 L{cx+22:.0f} 128" fill="none" stroke="{DIM}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        cx += 36
b.append(text(44, 182, 'PAPERS', 'mono lab'))
PY, PH, PW, G = 196, 166, 222, 26
px = [44 + i * (PW + G) for i in range(3)]
cards = [('Every new', 'paper', ['Empirical, on', 'public data']),
         ('Checked', 'by celsus', ['Script, numbers', 'and verdict: open']),
         ('A public', 'library', ['For anyone who', 'relies on a result'])]
for i, (x, (t1, t2, cap)) in enumerate(zip(px, cards)):
    b.append(f'<rect class="{"hi" if i == 1 else "panel"}" x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="16"/>')
    ix, iy = x + 20, PY + 20
    if i == 0:
        b += paper(ix + 16, iy - 6, 0.3, False) + paper(ix + 8, iy, 0.55, False) + paper(ix, iy + 6, 0.92)[:2]
        for k, (ln, yy) in enumerate([(36, 30), (28, 40), (36, 50)]):
            b.append(f'<line x1="{ix+8}" y1="{iy+6+yy}" x2="{ix+8+ln}" y2="{iy+6+yy}" stroke="#1b1a17" stroke-opacity="0.45" stroke-width="3"/>')
    elif i == 1:
        b.append(f'<rect class="seal" x="{ix}" y="{iy+8}" width="56" height="56" rx="11"/>')
        b.append(tick(ix + 13, iy + 37, 1.45, 3.2))
    else:
        heights = [52, 62, 48, 58, 50, 64]
        kinds = ['holds', 'partly', 'partly', 'fails', 'holds', 'partly']
        sx = ix
        for k, (hh, kind) in enumerate(zip(heights, kinds)):
            b.append(f'<rect x="{sx}" y="{iy+74-hh}" width="9.5" height="{hh}" fill="{INK}" fill-opacity="{0.5 + 0.06 * (k % 4)}"/>')
            b.append(dot(sx + 5, iy + 74 - hh + 9, kind, 3))
            sx += 12
        b.append(f'<line x1="{ix-4}" y1="{iy+75}" x2="{sx+2}" y2="{iy+75}" stroke="{RULE}" stroke-width="2.6"/>')
    b.append(text(x + 100, PY + 46, t1, 'h2'))
    b.append(text(x + 100, PY + 72, t2, 'h2'))
    b.append(text(x + 20, PY + 124, cap[0]))
    b.append(text(x + 20, PY + 148, cap[1]))
    if i < 2:
        b.append(arrow_r(x + PW + 4, x + PW + G - 4, PY + PH / 2))
RX = 44 + 3 * PW + 2 * G + 30
b.append(f'<rect class="panel" x="{RX}" y="106" width="{1196-RX}" height="{PY+PH-106}" rx="16"/>')
b.append(text(RX + 24, 138, 'THE WHOLE POOL, ON MUSE SPARK OPEN', 'mono lab'))
b.append(text(RX + 22, 204, '$8,500', 'gold', font_size=68, font_weight=700, letter_spacing=-2))
b.append(text(RX + 24, 238, 'One run on each of the 6,552 arXiv'))
b.append(text(RX + 24, 262, 'papers the held-out set was drawn'))
b.append(text(RX + 24, 286, 'from, at the mean of $1.30 a run.'))
b.append(f'<line x1="{RX+24}" y1="302" x2="{1172}" y2="302" stroke="#ffffff" stroke-opacity="0.09" stroke-width="1.5"/>')
b.append(text(RX + 24, 334, '35 min', 'ink', font_size=24, font_weight=700))
b.append(text(RX + 24, 354, 'median run', font_size=15.5))
b.append(text(RX + 140, 334, '$1.34', 'ink', font_size=24, font_weight=700))
b.append(text(RX + 140, 354, 'median, at list prices', font_size=15.5))
FY = PY + PH + 46
b.append(text(44, FY + 4, 'FIELDS', 'mono lab'))
cx = 128
for k, w in enumerate(['finance, economics · first', 'social science', 'climate', 'machine learning']):
    cw = len(w) * 9.4 + 34
    if k == 0:
        b.append(f'<rect x="{cx}" y="{FY-18}" width="{cw:.0f}" height="32" rx="16" fill="{RULE}" fill-opacity="0.22" stroke="{RULE}" stroke-width="1.4"/>')
        b.append(text(cx + cw / 2, FY + 4, w, 'mono', fill='#e6c78f', font_size=15.5, text_anchor='middle'))
    else:
        b.append(f'<rect class="chip" x="{cx}" y="{FY-18}" width="{cw:.0f}" height="32" rx="16"/>')
        b.append(text(cx + cw / 2, FY + 4, w, 'mono m', text_anchor='middle'))
    cx += cw + 12
b.append(text(cx + 8, FY + 4, 'any field with public data', font_size=17))
svg('vision', 1240, FY + 46, 'Continuous integration, for papers',
    'Software checks every change before it merges: commit, tests pass, merge. celsus does the same for research: every new empirical paper on public data is checked, with the script, the numbers and the verdict open, and the checked papers build into a public library for anyone who relies on a result. One run on each of the 6,552 arXiv papers the held-out set was drawn from would cost about $8,500, at the mean of $1.30 a run; a run takes a median of 35 minutes and $1.34 at list prices on Muse Spark Open. Finance and economics came first; social science, climate and machine learning, and any field with public data, have the same shape.', b)

# ---------- 3. held-out ----------
b = []
LW = 470
rows = [(112, 78, '6,552', ['arXiv hits the draw', 'started from']),
        (222, 128, '32', ['papers, by a rule fixed before', 'any run. None seen in', 'development; 12 dropped for', 'a glimpsed result.']),
        (382, 78, '63', ['runs: each paper twice on', 'Muse Spark Open, $2 stop'])]
for k, (y, h, n, cap) in enumerate(rows):
    b.append(f'<rect class="panel" x="44" y="{y}" width="{LW}" height="{h}" rx="16"/>')
    b.append(text(66, y + 50 if h < 100 else y + 54, n, 'ink', font_size=36, font_weight=700, letter_spacing=-0.8))
    for j, line in enumerate(cap):
        b.append(text(176, y + 32 + j * 24, line))
    if k < 2:
        b.append(arrow_d(44 + LW / 2, y + h + 4, rows[k + 1][0] - 4))
RX, RY, RH = 44 + LW + 26, 112, 348
b.append(f'<rect class="panel" x="{RX}" y="{RY}" width="{1196-RX}" height="{RH}" rx="16"/>')
b.append(text(RX + 24, RY + 32, 'VERDICTS, AS RUN · ONE DOT PER RUN', 'mono lab'))
groups = [(['holds', 'up'], 1, 1, 'holds', HOLDS, 92),
          (['partly', 'holds up'], 26, 6, 'partly', '#b7a173', 144),
          (['does not', 'hold up'], 3, 1, 'fails', '#d06a55', 104),
          (['could not', 'check'], 28, 6, 'cnc', '#d4ccbb', 144),
          (['budget', 'stop'], 5, 2, 'budget', CAP, 70)]
gx = RX + 24
for labels, n, cols, kind, colour, slot in groups:
    b.append(text(gx, RY + 84, n, font_size=36, font_weight=700, fill=colour, letter_spacing=-0.8))
    for i in range(n):
        c, r = i % cols, i // cols
        b.append(dot(gx + 8 + c * 20, RY + 112 + r * 20, kind, 7))
    for j, line in enumerate(labels):
        b.append(text(gx, RY + 236 + j * 22, line, font_size=17.5))
    gx += slot
b.append(f'<line x1="{RX+24}" y1="{RY+276}" x2="{1172}" y2="{RY+276}" stroke="#ffffff" stroke-opacity="0.09" stroke-width="1.5"/>')
b.append(text(RX + 24, RY + 306, 'Could not check is the checker’s own failure, given'))
b.append(text(RX + 24, RY + 330, 'with its reason. It never counts against the paper.'))
svg('held-out', 1240, RY + RH + 36, 'A held-out set nobody had looked at',
    'From 6,552 arXiv hits, 32 finance and economics papers were drawn by a rule written down before any run: public data a script can fetch, LaTeX source, about 30 minutes of compute, and no paper seen during development; 12 were dropped because someone had glimpsed a result. Each paper ran twice on Muse Spark Open at effort xhigh with a $2 budget stop, and 63 runs finished. Verdicts as run, one dot per run: holds up 1, partly holds up 26, does not hold up 3, could not check 28, could not check at the $2 budget stop 5. Could not check is the checker’s own failure, given with its reason, and never counts against the paper.', b)

# ---------- 4. battery ----------
b = []
LW = 400
b.append(f'<rect class="panel" x="44" y="112" width="{LW}" height="246" rx="16"/>')
b.append(text(68, 144, 'PLANTED IN CLEAN RUNS', 'mono lab'))
items = [['Results typed in', 'from the paper'], ['Samples cut or padded', 'to the paper’s count'], ['Synthetic data'], ['Altered paper numbers']]
y = 182
for it in items:
    b.append(f'<path d="M70 {y-12} L81 {y-1} M81 {y-12} L70 {y-1}" stroke="{FAILS}" stroke-width="2.4" stroke-linecap="round"/>')
    b.append(text(98, y, it[0], 'ink', font_size=18.5))
    if len(it) > 1:
        b.append(text(98 + len(it[0]) * 8.9 + 6, y, it[1], font_size=18.5)) if False else None
    y += 38
# two-part items on one line where they fit, dim tail
b = [l for l in b if l is not None]
b = b[:3]
y = 182
for it in items:
    b.append(f'<path d="M70 {y-12} L81 {y-1} M81 {y-12} L70 {y-1}" stroke="{FAILS}" stroke-width="2.4" stroke-linecap="round"/>')
    b.append(text(98, y, it[0], 'ink', font_size=18.5))
    if len(it) > 1:
        y += 24
        b.append(text(98, y, it[1], font_size=17))
    y += 36
b.append(arrow_r(44 + LW + 4, 44 + LW + 22, 230))
RX = 44 + LW + 26
b.append(f'<rect class="panel" x="{RX}" y="112" width="{1196-RX}" height="246" rx="16"/>')
b.append(text(RX + 24, 144, 'CAUGHT, OF 116 PLANTS', 'mono lab'))
X0, X1, N = RX + 24, 1172, 116
step = (X1 - X0) / N
for k, (label, caught, pct) in enumerate([('Coded checks alone', 94, ''), ('With one review', 106, '91.4%'), ('With both reviews', 108, '93.1%')]):
    y = 180 + k * 56
    b.append(text(X0, y, label, 'ink', font_size=19, font_weight=700))
    tail = f'<tspan fill="{CAP}" font-size="16" font-weight="400">{pct}  </tspan>' if pct else ''
    b.append(f'<text x="{X1}" y="{y}" font-size="21" font-weight="700" text-anchor="end">{tail}<tspan class="gold">{caught}</tspan></text>')
    cells = ''.join(f'<rect x="{X0 + i * step:.2f}" y="{y + 10}" width="{step - 1.4:.2f}" height="17" rx="1" fill="{GOLD if i < caught else INK}"{"" if i < caught else " fill-opacity=\"0.13\""}/>' for i in range(N))
    b.append(cells)
b.append(text(X0, 340, 'No false alarm in 12 reviews of untouched scripts.', font_size=17))
BY = 382
b.append(f'<rect class="panel" x="44" y="{BY}" width="1152" height="118" rx="16"/>')
b.append(text(68, BY + 32, 'HELD-OUT SET · 46 FINDINGS FROM ONLY ONE REVIEW, EACH READ BY HAND', 'mono lab'))
for i in range(46):
    x = 68 + i * 19
    if i < 43: b.append(f'<rect x="{x}" y="{BY+50}" width="14" height="14" rx="2.5" fill="{GOLD}"/>')
    elif i < 45: b.append(f'<rect x="{x}" y="{BY+50}" width="14" height="14" rx="2.5" fill="{PARTLY}"/>')
    else: b.append(f'<rect x="{x+1}" y="{BY+51}" width="12" height="12" rx="2.5" fill="none" stroke="{FAILS}" stroke-width="1.8"/>')
b.append(f'<text class="cap" x="68" y="{BY+96}"><tspan class="gold" font-weight="700">43</tspan> true · <tspan fill="#b7a173" font-weight="700">2</tspan> borderline · <tspan fill="#d06a55" font-weight="700">1</tspan> false. No false or borderline finding decided a verdict.</text>')
svg('battery', 1240, BY + 118 + 36, 'Planted faults, and what catches them',
    'The sabotage battery plants faults into clean runs: results typed in from the paper, samples cut or padded to the paper’s count, synthetic data, and altered paper numbers. Of 116 viable plants, the coded checks alone catch 94; with one review, 106 (91.4%); with both reviews, 108 (93.1%). The reviews raised no false alarm in 12 reviews of untouched scripts. In the held-out set, 46 findings came from only one of the two reviews; each was read against the script by hand: 43 true, 2 borderline, 1 false, and no false or borderline finding decided a verdict.', b)

# ---------- 5. matching ----------
def diamond(cx, cy, r=8):
    return f'<path d="M{cx} {cy-r} L{cx+r} {cy} L{cx} {cy+r} L{cx-r} {cy} Z" fill="{GOLD}"/>'
def here(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="{INK}"/>'
AX = f'stroke="{INK}" stroke-opacity="0.45" stroke-width="2" stroke-linecap="round"'
b = [f'<g transform="translate(846 56)">{diamond(0, 0, 7)}{text(14, 6, "the paper", font_size=17)}{here(124, 0)}{text(138, 6, "the reproduction", font_size=17)}</g>']
PW, G, Y = 270, 24, 190
panels = [('Estimate with an SE', ['The paper’s value lies', 'inside the reproduction’s', '95% interval.']),
          ('No sampling error', ['It rounds to the value as', 'printed, or else lies', 'within 10% of it.']),
          ('Test statistic', ['Same conclusion at 5%, on', 'the side the paper tested.', 'p-values: same side of 0.05.']),
          ('Sample total', ['Within 15% of the paper’s.', 'Subgroups: 15%, or else', 'within 1.96 √n.'])]
for i, (title, cap) in enumerate(panels):
    x = 44 + i * (PW + G)
    a, c = x + 24, x + PW - 24
    m = (a + c) / 2
    b.append(f'<rect class="panel" x="{x}" y="112" width="{PW}" height="270" rx="16"/>')
    b.append(f'<line x1="{a}" y1="{Y}" x2="{c}" y2="{Y}" {AX}/>')
    lab = lambda xx, yy, s: text(xx, yy, s, 'mono lab', text_anchor='middle', font_size=14)
    if i == 0:
        b.append(f'<rect x="{m-70}" y="{Y-13}" width="140" height="26" rx="5" fill="{GOLD}" fill-opacity="0.16" stroke="{GOLD}" stroke-opacity="0.7" stroke-width="1.5"/>')
        b += [here(m - 8, Y), diamond(m + 26, Y), lab(m, Y + 40, 'reproduction, 95% CI')]
    elif i == 1:
        b.append(f'<rect x="{m-54}" y="{Y-13}" width="108" height="26" rx="5" fill="{GOLD}" fill-opacity="0.10"/>')
        b.append(f'<rect x="{m-10}" y="{Y-13}" width="20" height="26" rx="3" fill="{GOLD}" fill-opacity="0.30"/>')
        b += [diamond(m, Y), here(m + 4, Y - 26), lab(m, Y + 40, '±10%'), lab(m + 64, Y - 22, 'rounds')]
    elif i == 2:
        u = 26
        b.append(f'<rect x="{a}" y="{Y-13}" width="{m-1.96*u-a:.1f}" height="26" fill="{GOLD}" fill-opacity="0.07"/>')
        b.append(f'<rect x="{m+1.96*u:.1f}" y="{Y-13}" width="{c-(m+1.96*u):.1f}" height="26" fill="{GOLD}" fill-opacity="0.24"/>')
        for t, s in ((-1.96, '−1.96'), (0, '0'), (1.96, '1.96')):
            b.append(f'<line x1="{m+t*u:.1f}" y1="{Y-6}" x2="{m+t*u:.1f}" y2="{Y+6}" {AX}/>')
            b.append(lab(round(m + t * u, 1), Y + 36, s))
        b += [diamond(m + 3.05 * u, Y), here(m + 2.35 * u, Y - 26)]
    else:
        b.append(f'<rect x="{m-62}" y="{Y-13}" width="124" height="26" rx="5" fill="{GOLD}" fill-opacity="0.16" stroke="{GOLD}" stroke-opacity="0.7" stroke-width="1.5"/>')
        b += [diamond(m, Y), here(m + 34, Y - 26), lab(m, Y + 40, '±15%')]
    b.append(text(x + 24, 280, title, 'h2', font_size=22))
    for j, line in enumerate(cap):
        b.append(text(x + 24, 310 + j * 23, line, font_size=17.5))
b.append(text(44, 414, 'Code, not a model, applies these rules. Each one’s source is in the table below.', font_size=17))
svg('matching', 1240, 446, 'When a number matches',
    'Four rules, each drawn on a number line. An estimate with a standard error is consistent when the paper’s value lies inside the reproduction’s 95% interval. A number with no sampling error, such as a return over a fixed period or a ratio, is consistent when it rounds to the value as printed, or else lies within 10% of it. A test statistic must reach the same conclusion at 5% on the side the paper tested, and a p-value must fall on the same side of 0.05. A sample total must be within 15% of the paper’s; a subgroup count within 15%, or else within 1.96 times the square root of n. Code, not a model, applies the rules.', b)
print('ok')
