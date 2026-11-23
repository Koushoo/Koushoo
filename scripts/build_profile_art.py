"""Draw the profile's original SVG artwork. No network or dependencies."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "light": dict(bg="#f8f8fb", border="#dddde7", ink="#252734", muted="#737787", accent="#7274b8",
                  wall="#eeedf5", sky="#deddf2", cloud="#f8f4fa", mountain="#b5b3d8", hill="#8d9cb6",
                  floor="#d7d5e5", desk="#b69b8e", shadow="#c9c4d5", leaf="#709987"),
    "dark": dict(bg="#171b26", border="#303749", ink="#ebeaf4", muted="#9bA4b7", accent="#b2a9e6",
                 wall="#242939", sky="#333654", cloud="#555775", mountain="#4b506e", hill="#636684",
                 floor="#303448", desk="#8b777d", shadow="#252b3b", leaf="#7aab97"),
}


def rect(x, y, w, h, color, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'


def scene(p):
    art = [rect(0, 0, 96, 62, p["wall"]), rect(0, 51, 96, 11, p["floor"]),
           rect(8, 4, 80, 33, p["shadow"]), rect(10, 6, 76, 29, p["sky"]),
           '<g clip-path="url(#view)">', rect(69, 9, 8, 8, "#e5bfaa"),
           '<g class="cloud">', rect(15, 11, 15, 3, p["cloud"]), rect(18, 9, 8, 2, p["cloud"]),
           rect(51, 19, 18, 3, p["cloud"]), rect(55, 17, 9, 2, p["cloud"]), '</g>',
           f'<path d="M10 35V29H18V26H24V23H32V26H39V29H47V27H53V24H60V27H67V30H77V28H86V35Z" fill="{p["mountain"]}"/>',
           f'<path d="M10 35V32H23V30H35V32H48V31H61V33H74V31H86V35Z" fill="{p["hill"]}"/>',
           '</g>', rect(47, 6, 2, 29, p["shadow"]), rect(10, 21, 76, 2, p["shadow"]),
           rect(6, 37, 84, 2, p["shadow"]),
           # Desk, keyboard and monitor.
           rect(5, 48, 87, 3, p["shadow"]), rect(3, 46, 90, 3, p["desk"]),
           rect(9, 49, 3, 11, p["desk"]), rect(84, 49, 3, 11, p["desk"]),
           rect(15, 27, 28, 17, "#50586c"), rect(17, 29, 24, 12, "#273748"),
           rect(27, 44, 4, 2, "#747888"), rect(23, 45, 12, 1, "#747888"),
           rect(20, 32, 8, 1, "#abc6c0"), rect(20, 35, 14, 1, "#c4b7de"),
           rect(20, 38, 6, 1, "#e3c5ad"), rect(28, 38, 2, 1, "#e3c5ad", 'class="cursor"'),
           rect(17, 45, 22, 1, "#a5a6b7"), rect(44, 41, 5, 5, "#d8b9ab"),
           rect(49, 42, 2, 3, "#d8b9ab"), rect(49, 43, 1, 1, p["wall"]),
           '<g class="steam" opacity=".5">', rect(45, 35, 1, 3, p["muted"]),
           rect(47, 33, 1, 3, p["muted"]), '</g>',
           # Original cat sprite.
           '<g class="cat">', rect(59, 40, 14, 6, "#bd9e91"), rect(57, 41, 2, 4, "#bd9e91"),
           rect(62, 38, 8, 2, "#bd9e91"), rect(68, 37, 7, 8, "#d7b6a2"),
           rect(68, 35, 2, 3, "#d7b6a2"), rect(73, 35, 2, 3, "#d7b6a2"),
           rect(69, 36, 1, 2, "#bd9e91"), rect(73, 36, 1, 2, "#bd9e91"),
           rect(70, 43, 3, 2, "#ead2bd"), rect(69, 40, 1, 1, "#4c4350", 'class="eye"'),
           rect(73, 40, 1, 1, "#4c4350", 'class="eye"'), rect(71, 42, 1, 1, "#94787b"),
           '<g class="tail">', rect(55, 39, 3, 6, "#bd9e91"), rect(53, 37, 4, 3, "#bd9e91"),
           rect(53, 35, 2, 3, "#bd9e91"), '</g>', '</g>',
           # A small plant and books.
           rect(80, 40, 8, 6, "#b9abc4"), rect(79, 39, 10, 2, "#c8bbd1"),
           rect(83, 31, 2, 9, p["leaf"]), rect(79, 33, 4, 3, p["leaf"]),
           rect(77, 30, 3, 4, p["leaf"]), rect(85, 34, 4, 3, p["leaf"]),
           rect(88, 31, 3, 4, p["leaf"]), rect(83, 28, 2, 3, p["leaf"]),
           rect(4, 43, 9, 3, "#9298b6"), rect(5, 40, 7, 3, "#c7afbc")]
    return ''.join(art)


def header(theme):
    p = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="366" viewBox="0 0 1000 366" role="img" aria-labelledby="title desc">
<title id="title">Koushoo — a little workspace</title>
<desc id="desc">A macOS-inspired window with a pixel-art desk, a blinking cat, a monitor, a mug and a plant by the window. Student. Building small things, learning as I go.</desc>
<defs><clipPath id="view"><rect x="10" y="6" width="76" height="29"/></clipPath>
<clipPath id="scene"><rect width="96" height="62" rx="3"/></clipPath></defs>
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.cloud{{animation:drift 16s ease-in-out infinite alternate}}
.cursor{{animation:blink 1.3s steps(1,end) infinite}}
.eye{{animation:cat-blink 7s steps(1,end) infinite}}
.tail{{transform-origin:58px 44px;animation:tail 7s steps(3,end) infinite}}
.steam{{animation:steam 3s ease-in-out infinite}}
@keyframes drift{{to{{transform:translateX(7px)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes cat-blink{{0%,44%,49%,100%{{opacity:1}}45%,48%{{opacity:0}}}}
@keyframes tail{{0%,65%,100%{{transform:rotate(0deg)}}75%,85%{{transform:rotate(12deg)}}}}
@keyframes steam{{0%,100%{{transform:translateY(0);opacity:.3}}50%{{transform:translateY(-2px);opacity:.65}}}}
@media(prefers-reduced-motion:reduce){{.cloud,.cursor,.eye,.tail,.steam{{animation:none}}}}
</style>
<rect x="1" y="1" width="998" height="364" rx="19" fill="{p['bg']}" stroke="{p['border']}"/>
<path d="M1 51H999" stroke="{p['border']}"/>
<circle cx="29" cy="27" r="5.5" fill="#ff6058"/><circle cx="48" cy="27" r="5.5" fill="#febc2e"/><circle cx="67" cy="27" r="5.5" fill="#29c840"/>
<text x="500" y="32" font-size="13" text-anchor="middle" fill="{p['muted']}">koushoo / a little workspace</text>
<text x="53" y="127" font-size="13" letter-spacing="2" fill="{p['accent']}">HELLO THERE</text>
<text x="50" y="188" font-size="48" font-weight="600" letter-spacing="-1.8" fill="{p['ink']}">I’m Koushoo.</text>
<text x="53" y="228" font-size="19" fill="{p['muted']}">A student, building small things.</text>
<rect x="53" y="263" width="28" height="3" rx="1.5" fill="{p['accent']}"/>
<text x="53" y="304" font-size="13" fill="{p['muted']}">learning as I go.</text>
<g transform="translate(558 80) scale(4)" shape-rendering="crispEdges" clip-path="url(#scene)">{scene(p)}</g>
</svg>\n'''


def icon(kind):
    ink, accent = "#8c8bbd", "#8bb1a4"
    if kind == "watch":
        drawing = rect(4, 6, 24, 20, ink) + rect(6, 8, 20, 16, "#252c3b")
        drawing += f'<path d="M8 17H12V13H15V21H18V16H24" fill="none" stroke="{accent}" stroke-width="2"/>'
        drawing += rect(10, 27, 12, 2, ink)
    else:
        drawing = rect(5, 4, 15, 20, ink) + rect(11, 9, 15, 20, accent)
        drawing += rect(14, 14, 9, 2, "#dbe4dc") + rect(14, 19, 7, 2, "#dbe4dc")
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" shape-rendering="crispEdges">{drawing}</svg>\n'


def main():
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for theme in PALETTES:
        (assets / f"workspace-{theme}.svg").write_text(header(theme), encoding="utf-8", newline="\n")
    for kind in ("watch", "files"):
        (assets / f"pixel-{kind}.svg").write_text(icon(kind), encoding="utf-8", newline="\n")
    print("Built two themed banners and two project icons.")


if __name__ == "__main__":
    main()
