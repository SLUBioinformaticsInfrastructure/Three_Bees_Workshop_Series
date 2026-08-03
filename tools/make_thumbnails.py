#!/usr/bin/env python3
"""Regenerate the per-session bee thumbnails (sessions/*/thumbnail.svg).

Each session gets the same logo-styled honeybee (elongated black-and-amber
striped body, large veined wings, dark fuzzy head) in a different pose, with a
topic-coloured background and a topic emblem pinned to the lower-right corner.

To add a session: create its sessions/sessionNN-slug/ folder, give it an entry
in EMBLEM below, then run `python3 tools/make_thumbnails.py` from the repo root.
"""
import os, re, glob, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# session number -> topic emblem key
EMBLEM = {
    1:"R", 2:"term", 3:"stats", 4:"doc", 5:"chart", 6:"func", 7:"py", 8:"nodes",
    9:"chart", 10:"hpc", 11:"git", 12:"git", 13:"folder", 14:"chart", 15:"term",
    16:"hpc", 17:"R", 18:"stats", 19:"py", 20:"doc", 21:"doc", 22:"stats",
    23:"db", 24:"chart", 25:"hpc", 26:"box", 27:"R", 28:"code", 29:"term",
}
# emblem key -> (background tint, accent colour)
STYLE = {
    "R":("#eceaf7","#6457c4"), "py":("#e7eef7","#3a6ea5"), "term":("#eceef0","#4a5568"),
    "chart":("#eaf4e6","#4c956c"), "stats":("#e6f0ea","#2f8f6b"), "doc":("#e7f3f1","#2a9d8f"),
    "func":("#f0eaf7","#7a4fc0"), "nodes":("#f7eaf1","#b04a7a"), "hpc":("#e8edf5","#3f5e8c"),
    "git":("#f7efe2","#c47e2a"), "folder":("#f4eee3","#9a7b4f"), "box":("#e7eef7","#3a6ea5"),
    "code":("#e9edf6","#3f6fb0"), "db":("#e3f0f3","#2f7d92"),
}
# a distinct pose per session (rot, mirror, tx, ty, scale) spread across zones:
# centre / from-left / from-top (head-down) / upper-left / upper-right / lower-left
POSE_BY_N = {
    1:(26,True,150,110,0.93),  2:(-52,True,168,90,0.88),  3:(48,False,106,98,0.86),
    4:(-20,False,126,118,0.94),5:(150,True,144,76,0.84),  6:(10,True,96,136,0.87),
    7:(-10,True,136,112,0.95), 8:(86,False,102,96,0.85),  9:(-48,False,124,92,0.92),
    10:(34,False,148,106,0.9), 11:(-70,False,170,94,0.88),12:(160,False,134,72,0.84),
    13:(64,True,102,100,0.85), 14:(20,False,142,112,0.93),15:(-46,True,170,92,0.86),
    16:(6,False,140,108,0.95), 17:(-40,True,128,88,0.93), 18:(58,True,108,100,0.86),
    19:(40,True,150,104,0.9),  20:(-16,True,130,116,0.94),21:(14,False,138,104,0.95),
    22:(30,True,150,108,0.92), 23:(-64,False,164,96,0.89),24:(74,False,98,92,0.86),
    25:(176,True,148,74,0.83), 26:(168,False,140,72,0.84),27:(-30,True,120,92,0.95),
    28:(16,False,92,140,0.86), 29:(-62,True,176,86,0.88),
}

ABDOMEN, BAND, THORAX, HEAD, OUTLINE = "#e6a019", "#241c12", "#2e2417", "#241c12", "#6e4f1a"
WING, WING_EDGE, WING_VEIN = "#f5f8fc", "#6f6149", "#9b8e76"


def hexagon(cx, cy, r, fill, op):
    pts = [f"{cx+r*math.cos(math.radians(60*i-30)):.1f},{cy+r*math.sin(math.radians(60*i-30)):.1f}" for i in range(6)]
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" fill-opacity="{op}"/>'


def emblem(key, cx, cy, c):
    if key == "chart":
        return "".join(f'<rect x="{cx-21+i*12}" y="{cy+18-h}" width="8" height="{h}" rx="2" fill="{c}"/>' for i,h in enumerate((16,28,22,34)))
    if key == "doc":
        s=f'<rect x="{cx-16}" y="{cy-20}" width="32" height="40" rx="4" fill="none" stroke="{c}" stroke-width="3"/>'
        return s+"".join(f'<line x1="{cx-9}" y1="{cy-9+i*9}" x2="{cx+9}" y2="{cy-9+i*9}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>' for i in range(3))
    if key == "box":
        return (f'<path d="M{cx-18},{cy-6} L{cx},{cy-17} L{cx+18},{cy-6} L{cx},{cy+5} Z" fill="{c}" fill-opacity=".35" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M{cx-18},{cy-6} L{cx-18},{cy+15} L{cx},{cy+26} L{cx},{cy+5} Z" fill="{c}" fill-opacity=".15" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M{cx+18},{cy-6} L{cx+18},{cy+15} L{cx},{cy+26} L{cx},{cy+5} Z" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>')
    if key == "stats":
        ax=f'<path d="M{cx-16},{cy-16} L{cx-16},{cy+16} L{cx+16},{cy+16}" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        return ax+"".join(f'<circle cx="{cx-8+i*9}" cy="{cy+10-j}" r="2.7" fill="{c}"/>' for i,j in [(0,2),(1,10),(2,7),(3,16)])
    if key == "hpc":
        s=""
        for i in range(3):
            y=cy-16+i*12
            s+=f'<rect x="{cx-17}" y="{y}" width="34" height="9" rx="2.5" fill="none" stroke="{c}" stroke-width="2.6"/><circle cx="{cx-11}" cy="{y+4.5}" r="1.8" fill="{c}"/>'
        return s
    if key == "git":
        return (f'<circle cx="{cx-9}" cy="{cy+11}" r="5" fill="none" stroke="{c}" stroke-width="3"/>'
                f'<circle cx="{cx-9}" cy="{cy-11}" r="5" fill="none" stroke="{c}" stroke-width="3"/>'
                f'<circle cx="{cx+12}" cy="{cy-3}" r="5" fill="none" stroke="{c}" stroke-width="3"/>'
                f'<path d="M{cx-9},{cy+6} L{cx-9},{cy-6}" stroke="{c}" stroke-width="3"/>'
                f'<path d="M{cx-9},{cy-3} q0,-7 21,-3" fill="none" stroke="{c}" stroke-width="3"/>')
    if key == "folder":
        return f'<path d="M{cx-18},{cy-11} h11 l4,5 h17 a3,3 0 0 1 3,3 v14 a3,3 0 0 1 -3,3 h-32 a3,3 0 0 1 -3,-3 v-19 a3,3 0 0 1 3,-3 z" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="2.6" stroke-linejoin="round"/>'
    if key == "nodes":
        n=[(cx-14,cy-12),(cx-14,cy+12),(cx+14,cy)]
        return (f'<path d="M{n[0][0]},{n[0][1]} L{n[2][0]},{n[2][1]} M{n[1][0]},{n[1][1]} L{n[2][0]},{n[2][1]}" stroke="{c}" stroke-width="2"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{c}"/>' for x,y in n))
    if key == "db":
        return (f'<ellipse cx="{cx}" cy="{cy-13}" rx="15" ry="6" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="2.6"/>'
                f'<path d="M{cx-15},{cy-13} v26 a15,6 0 0 0 30,0 v-26" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-width="2.6"/>'
                f'<path d="M{cx-15},{cy} a15,6 0 0 0 30,0" fill="none" stroke="{c}" stroke-width="2.2"/>')
    txt={"R":"R","code":"&lt;/&gt;","term":"&gt;_","py":"Py","func":"f(x)"}[key]
    size=30 if key=="R" else (20 if key=="func" else 24)
    style=' font-style="italic"' if key=="func" else ''
    return f'<text x="{cx}" y="{cy}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="{size}" font-weight="700"{style} fill="{c}" text-anchor="middle" dominant-baseline="central">{txt}</text>'


BEE = f'''    <g fill="{WING}" fill-opacity="0.9" stroke="{WING_EDGE}" stroke-width="1.6" stroke-linejoin="round">
      <path d="M -4,-12 C -36,-22 -84,6 -80,34 C -76,54 -42,40 -6,2 Z"/>
      <path d="M 4,-12 C 36,-22 84,6 80,34 C 76,54 42,40 6,2 Z"/>
    </g>
    <g fill="none" stroke="{WING_VEIN}" stroke-width="1">
      <path d="M -7,-10 C -34,-12 -66,10 -76,32"/><path d="M 7,-10 C 34,-12 66,10 76,32"/>
    </g>
    <g stroke="{HEAD}" stroke-width="2.4" stroke-linecap="round" fill="none">
      <path d="M -11,10 q -22,6 -30,22"/><path d="M -8,30 q -22,8 -27,25"/>
      <path d="M 11,10 q 22,6 30,22"/><path d="M 8,30 q 22,8 27,25"/>
    </g>
    <path d="M -5,86 L 0,104 L 5,86 Z" fill="{HEAD}"/>
    <defs><clipPath id="ab"><ellipse cx="0" cy="44" rx="23" ry="47"/></clipPath></defs>
    <ellipse cx="0" cy="44" rx="23" ry="47" fill="{ABDOMEN}"/>
    <g clip-path="url(#ab)">
      <rect x="-30" y="6" width="60" height="13" fill="{BAND}"/><rect x="-30" y="30" width="60" height="13" fill="{BAND}"/>
      <rect x="-30" y="54" width="60" height="13" fill="{BAND}"/><rect x="-30" y="78" width="60" height="18" fill="{BAND}"/>
    </g>
    <ellipse cx="0" cy="44" rx="23" ry="47" fill="none" stroke="{OUTLINE}" stroke-width="2"/>
    <ellipse cx="0" cy="-2" rx="20" ry="22" fill="{THORAX}"/>
    <circle cx="0" cy="-30" r="13" fill="{HEAD}"/>
    <g stroke="{HEAD}" stroke-width="2.2" stroke-linecap="round" fill="none">
      <path d="M -5,-40 q -7,-12 -15,-15"/><path d="M 5,-40 q 7,-12 15,-15"/>
    </g>
    <circle cx="-20" cy="-55" r="2.6" fill="{HEAD}"/><circle cx="20" cy="-55" r="2.6" fill="{HEAD}"/>'''


def svg_for(n, pose):
    key = EMBLEM[n]; tint, accent = STYLE[key]
    rot, mirror, tx, ty, sc = pose
    sx = -sc if mirror else sc
    return (f'<svg width="320" height="240" viewBox="0 0 320 240" xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f'  <rect width="320" height="240" fill="{tint}"/>\n'
            f'  {hexagon(40,42,26,accent,.10)}\n  {hexagon(74,96,18,accent,.08)}\n  {hexagon(296,58,22,accent,.08)}\n'
            f'  <g transform="translate({tx} {ty}) rotate({rot}) scale({sx} {sc})">\n{BEE}\n  </g>\n'
            f'  <circle cx="244" cy="178" r="31" fill="#fff" stroke="{accent}" stroke-width="3"/>\n'
            f'  {emblem(key,244,178,accent)}\n</svg>\n')


def main():
    for folder in sorted(glob.glob(os.path.join(ROOT, "sessions", "session*-*"))):
        mo = re.search(r"session(\d+)-", os.path.basename(folder))
        if not mo:
            continue
        n = int(mo.group(1))
        if n not in EMBLEM or n not in POSE_BY_N:
            print(f"  skip session {n}: no emblem/pose assigned"); continue
        pose = POSE_BY_N[n]
        with open(os.path.join(folder, "thumbnail.svg"), "w") as f:
            f.write(svg_for(n, pose))
        print(f"  wrote {os.path.basename(folder)}/thumbnail.svg")


if __name__ == "__main__":
    main()
