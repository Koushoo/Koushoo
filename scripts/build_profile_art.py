"""Draw the profile's original SVG artwork. No network or dependencies."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "light": dict(bg="#fff8f2", border="#e6d3dc", ink="#392d46", muted="#7b697d", accent="#aa5f8b",
                  wall="#f4dfdf", sky="#8acddd", cloud="#fff4e2", mountain="#ae90d1", hill="#68bba6",
                  floor="#e6cbd7", desk="#cc987c", shadow="#ccb0c8", leaf="#48aa88"),
    "dark": dict(bg="#1c192e", border="#3b3455", ink="#f3eafb", muted="#b4a6c6", accent="#d2a6eb",
                 wall="#36324f", sky="#75b8d3", cloud="#e2def3", mountain="#9380c9", hill="#63afac",
                 floor="#413750", desk="#b98775", shadow="#55445f", leaf="#73d5ac"),
}


def rect(x, y, w, h, color, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'


def scene(p):
    art = [rect(0, 0, 112, 82, p["wall"]), rect(0, 51, 112, 31, p["floor"]),
           # A woven rug, its fringe, and little floorboard marks.
           rect(28, 64, 49, 14, "#b476a1"), rect(30, 66, 45, 10, "#deabbb"),
           rect(33, 68, 39, 6, "#8b87bd"), rect(35, 70, 35, 2, "#b4c8cf"),
           ''.join(rect(x, y, 2, 1, "#dfb1c0") for x in (26, 77) for y in range(65, 78, 3)),
           rect(1, 58, 18, .4, p["shadow"]), rect(90, 69, 20, .4, p["shadow"]),
           rect(5, 79, 16, .4, p["shadow"]),
           rect(8, 4, 80, 33, p["shadow"]), rect(10, 6, 76, 29, p["sky"]),
           '<g clip-path="url(#view)">', rect(10, 6, 76, 29, "#171c38", 'class="night"'),
           '<g class="sun">', rect(68, 8, 10, 10, "#ffce83"),
           rect(70, 7, 6, 1, "#ffe4a6"), rect(69, 9, 2, 2, "#ffe4a6"), '</g>',
           '<g class="moon">', rect(26, 10, 5, 6, "#e2debf"), rect(28, 9, 3, 1, "#e2debf"),
           rect(29, 10, 3, 4, "#171c38"), '</g>',
           '<g class="stars">', rect(17, 9, 1, 1, "#eee6d5"), rect(39, 13, 1, 1, "#eee6d5"),
           rect(58, 9, 1, 1, "#eee6d5"), rect(77, 17, 1, 1, "#eee6d5"),
           rect(66, 15, 1, 1, "#eee6d5"), '</g>',
           '<g class="shooting-star">', rect(72, 10, 2, 1, "#f3e4c7"),
           rect(74, 9, 3, 1, "#afa9b8"), '</g>',
           '<g class="cloud">', rect(15, 11, 15, 3, p["cloud"]), rect(18, 9, 8, 2, p["cloud"]),
           rect(51, 19, 18, 3, p["cloud"]), rect(55, 17, 9, 2, p["cloud"]), '</g>',
           '<g class="birds" fill="none" stroke="#6d638d" stroke-width=".7">',
           '<path d="M91 13l2-1 2 1 2-1 2 1M103 17l1.5-1 1.5 1 1.5-1 1.5 1"/></g>',
           f'<path d="M10 35V29H18V26H24V23H32V26H39V29H47V27H53V24H60V27H67V30H77V28H86V35Z" fill="{p["mountain"]}"/>',
           f'<path d="M10 35V32H23V30H35V32H48V31H61V33H74V31H86V35Z" fill="{p["hill"]}"/>',
           '</g>', rect(47, 6, 2, 29, p["shadow"]), rect(10, 21, 76, 2, p["shadow"]),
           rect(6, 37, 84, 2, p["shadow"]),
           f'<path class="sunbeam" d="M10 23H45L72 63H39Z" fill="#ffe4a1" opacity=".08"/>',
           # Coloured string lights and a shelf in the little side wall.
           '<path d="M1 1Q55 8 111 1" fill="none" stroke="#92799e" stroke-width=".45"/>',
           ''.join(rect(x, y, 1.7, 2, color, f'class="bulb" style="animation-delay:-{i}s"')
                   for i, (x, y, color) in enumerate([(4, 2, "#ffa5a1"), (21, 4, "#ffe19a"),
                       (38, 5, "#8de5c4"), (55, 5, "#c4a8ff"), (72, 4, "#ffa5a1"),
                       (89, 3, "#ffe19a"), (106, 1, "#8de5c4")])),
           rect(94, 32, 15, 1.5, p["desk"]), rect(96, 25, 3, 7, "#82d1c2"),
           rect(99, 27, 3, 5, "#f5a4a8"), rect(102, 24, 3, 8, "#ae9ddd"),
           rect(96.5, 27, 1, 1, "#dff5da"), rect(102.5, 26, 1, 1, "#eed9ae"),
           rect(98, 39, 11, 11, "#a58bbb"), rect(99, 40, 9, 9, "#e6cfb5"),
           '<path d="M101 43h2v1h1v-1h2v3h-1v1h-1v1h-1v-1h-1v-1h-1Z" fill="#e78f9b"/>',
           # Desk, keyboard and monitor.
           rect(5, 48, 87, 3, p["shadow"]), rect(3, 46, 90, 3, p["desk"]),
           rect(9, 49, 3, 11, p["desk"]), rect(84, 49, 3, 11, p["desk"]),
           rect(15, 27, 28, 17, "#8d8ac2"), rect(17, 29, 24, 12, "#29324d"),
           rect(27, 44, 4, 2, "#747888"), rect(23, 45, 12, 1, "#747888"),
           rect(20, 32, 8, 1, "#8aebc8", 'class="line-a"'),
           rect(20, 35, 14, 1, "#e5a7e7", 'class="line-b"'),
           rect(20, 38, 6, 1, "#ffd18b"), rect(28, 38, 2, 1, "#ffd18b", 'class="cursor"'),
           rect(17, 45, 22, 1, "#bdb2dc"), rect(44, 41, 5, 5, "#ef9c98"),
           rect(49, 42, 2, 3, "#ef9c98"), rect(49, 43, 1, 1, p["wall"]),
           rect(44, 41, 5, 1, "#ffd8bf"),
           rect(6, 36, 6, 10, "#746193"), rect(7, 38, 4, 3, "#b5a2d5"),
           rect(8, 43, 2, 1, "#f3baaf"),
           '<g class="steam" opacity=".5">', rect(45, 35, 1, 3, p["muted"]),
           rect(47, 33, 1, 3, p["muted"]), '</g>',
           # Original cat sprite.
           '<g class="cat-motion"><g class="cat-facing">', rect(59, 40, 14, 6, "#e49c71"), rect(57, 41, 2, 4, "#e49c71"),
           rect(62, 38, 8, 2, "#e49c71"), rect(68, 37, 7, 8, "#ffc38d"),
           rect(68, 35, 2, 3, "#ffc38d"), rect(73, 35, 2, 3, "#ffc38d"),
           rect(69, 36, 1, 2, "#e49c71"), rect(73, 36, 1, 2, "#e49c71"),
           rect(62, 40, 1, 3, "#c57962"), rect(65, 39, 1, 4, "#c57962"),
           rect(70, 43, 3, 2, "#ffe5b7"), rect(69, 40, 1, 1, "#4c4350", 'class="eye"'),
           rect(73, 40, 1, 1, "#4c4350", 'class="eye"'), rect(71, 42, 1, 1, "#94787b"),
           '<g class="tail">', rect(55, 39, 3, 6, "#e49c71"), rect(53, 37, 4, 3, "#e49c71"),
           rect(53, 35, 2, 3, "#e49c71"), '</g>',
           '<g class="paws">', rect(60, 44, 3, 2, "#ffe5b7"), rect(69, 44, 3, 2, "#ffe5b7"),
           '</g></g></g>',
           # A small plant and books.
           rect(80, 40, 8, 6, "#b99ae4"), rect(79, 39, 10, 2, "#d4b6f2"),
           rect(83, 31, 2, 9, p["leaf"]), rect(79, 33, 4, 3, p["leaf"]),
           rect(77, 30, 3, 4, p["leaf"]), rect(85, 34, 4, 3, p["leaf"]),
           rect(88, 31, 3, 4, p["leaf"]), rect(83, 28, 2, 3, p["leaf"]),
           rect(83, 27, 2, 2, "#f4a6c7"), rect(82, 28, 4, 1, "#f4a6c7"),
           # Small lived-in details; the note is decorative, not a profile claim.
           rect(94, 8, 15, 18, "#f2d48c"), rect(106, 8, 3, 3, p["wall"]),
           '<g fill="#6e625f" font-family="Georgia,serif" font-size="2.6" font-style="italic">',
           '<text x="96" y="13">one thing</text><text x="96" y="17">at a time.</text>',
           '<path d="M96 20q4-2 9 0" stroke="#9d8c7b" stroke-width=".4" fill="none"/></g>',
           rect(9, 74, 7, 3, "#8bbfb6"), rect(18, 73, 7, 3, "#8bbfb6"),
           rect(99, 75, 10, 2, "#96a8d5"), rect(101, 72, 7, 3, "#efa3b7"),
           '<g class="butterfly"><g class="wings">',
           rect(0, 0, 2, 3, "#ff9cbe"), rect(3, 0, 2, 3, "#ffc978"),
           rect(1, 3, 1, 1, "#d6a5f1"), rect(3, 3, 1, 1, "#d6a5f1"), '</g>',
           rect(2, 1, 1, 3, "#66517e"), '</g>']
    return ''.join(art)


def header(theme):
    p = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="430" viewBox="0 0 1000 430" role="img" aria-labelledby="title desc">
<title id="title">Koushoo — a little workspace</title>
<desc id="desc">Koushoo's little workspace. A pixel cat hops off the desk, explores the floor and jumps back. Outside the window, day turns to night. Student. Building small things, learning as I go.</desc>
<defs><clipPath id="view"><rect x="10" y="6" width="76" height="29"/></clipPath>
<clipPath id="scene"><rect width="112" height="82" rx="3"/></clipPath>
<linearGradient id="name"><stop stop-color="{'#9364b3' if theme == 'light' else '#cfb1ff'}"/><stop offset="1" stop-color="{'#bb667a' if theme == 'light' else '#ffc2a5'}"/></linearGradient></defs>
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
.cloud{{animation:drift 16s ease-in-out infinite alternate}}
.cursor{{animation:blink 1.3s steps(1,end) infinite}}
.eye{{animation:cat-blink 7s steps(1,end) infinite}}
.tail{{transform-origin:58px 44px;animation:tail 7s steps(3,end) infinite}}
.steam{{animation:steam 3s ease-in-out infinite}}
.night{{animation:night 48s ease-in-out infinite;opacity:0}}
.sun{{animation:sunset 48s ease-in-out infinite}}
.moon{{animation:moonrise 48s ease-in-out infinite;opacity:0}}
.stars{{animation:starlight 48s ease-in-out infinite;opacity:0}}
.shooting-star{{animation:shoot 48s linear infinite;opacity:0}}
.cat-motion{{animation:explore 24s cubic-bezier(.4,0,.2,1) infinite}}
.cat-facing{{transform-box:fill-box;transform-origin:center;animation:face 24s steps(1,end) infinite}}
.paws{{animation:pad 0.6s steps(2,end) infinite}}
.line-a,.line-b{{transform-box:fill-box;transform-origin:left;animation:code 7s steps(8,end) infinite}}
.line-b{{animation-delay:1.1s}}
.birds{{animation:birds 22s linear infinite}}
.bulb{{animation:glow 7s ease-in-out infinite alternate}}
.sunbeam{{animation:room-light 48s ease-in-out infinite}}
.butterfly{{transform:translate(83px,24px);animation:butterfly 24s ease-in-out infinite}}
.wings{{transform-origin:2.5px 2px;animation:flutter .8s steps(2,end) infinite}}
@keyframes drift{{to{{transform:translateX(7px)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes cat-blink{{0%,44%,49%,100%{{opacity:1}}45%,48%{{opacity:0}}}}
@keyframes tail{{0%,65%,100%{{transform:rotate(0deg)}}75%,85%{{transform:rotate(12deg)}}}}
@keyframes steam{{0%,100%{{transform:translateY(0);opacity:.3}}50%{{transform:translateY(-2px);opacity:.65}}}}
@keyframes night{{0%,15%,100%{{opacity:0}}42%,76%{{opacity:.95}}}}
@keyframes sunset{{0%,10%,100%{{transform:translateY(0);opacity:1}}35%,78%{{transform:translateY(27px);opacity:0}}}}
@keyframes moonrise{{0%,29%,93%,100%{{opacity:0;transform:translateY(10px)}}43%,75%{{opacity:1;transform:translateY(0)}}}}
@keyframes starlight{{0%,30%,95%,100%{{opacity:0}}45%,75%{{opacity:.85}}}}
@keyframes shoot{{0%,59%,64%,100%{{opacity:0;transform:translate(0,0)}}60%{{opacity:1;transform:translate(0,0)}}63%{{opacity:0;transform:translate(-30px,12px)}}}}
@keyframes explore{{0%,10%,76%,100%{{transform:translate(0,0)}}14%{{transform:translate(8px,-10px)}}20%{{transform:translate(31px,0)}}25%{{transform:translate(31px,22px)}}34%{{transform:translate(-8px,22px)}}40%,47%{{transform:translate(-25px,22px)}}57%,63%{{transform:translate(31px,22px)}}69%{{transform:translate(17px,-10px)}}}}
@keyframes face{{0%,25%,48%,100%{{transform:scaleX(1)}}26%,47%{{transform:scaleX(-1)}}}}
@keyframes pad{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(1px)}}}}
@keyframes code{{0%,10%{{transform:scaleX(.1)}}55%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(.1)}}}}
@keyframes birds{{from{{transform:translateX(0)}}to{{transform:translateX(-110px)}}}}
@keyframes glow{{from{{opacity:.55}}to{{opacity:1}}}}
@keyframes room-light{{0%,15%,100%{{opacity:.1}}42%,76%{{opacity:0}}}}
@keyframes flutter{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(.35)}}}}
@keyframes butterfly{{0%,10%,76%,100%{{transform:translate(83px,24px)}}20%{{transform:translate(100px,29px)}}32%{{transform:translate(53px,52px)}}40%,47%{{transform:translate(30px,56px)}}57%,63%{{transform:translate(100px,53px)}}69%{{transform:translate(91px,20px)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect x="1" y="1" width="998" height="428" rx="19" fill="{p['bg']}" stroke="{p['border']}"/>
<path d="M1 51H999" stroke="{p['border']}"/>
<circle cx="29" cy="27" r="5.5" fill="#ff6058"/><circle cx="48" cy="27" r="5.5" fill="#febc2e"/><circle cx="67" cy="27" r="5.5" fill="#29c840"/>
<text x="500" y="32" font-size="13" text-anchor="middle" fill="{p['muted']}">Koushoo’s desk</text>
<text x="53" y="127" font-size="13" letter-spacing="2" fill="{p['accent']}">HELLO THERE</text>
<text x="50" y="188" font-size="45" font-weight="600" letter-spacing="-1.8" fill="url(#name)">I’m Koushoo.</text>
<text x="53" y="228" font-size="19" fill="{p['muted']}">A student, building small things.</text>
<rect x="53" y="263" width="28" height="3" rx="1.5" fill="{p['accent']}"/>
<rect x="85" y="263" width="13" height="3" rx="1.5" fill="#ef9fae"/>
<rect x="102" y="263" width="9" height="3" rx="1.5" fill="#84cbb8"/>
<rect x="115" y="263" width="5" height="3" rx="1.5" fill="#f1cc8c"/>
<text x="53" y="304" font-size="13" fill="{p['muted']}">learning as I go.</text>
<text x="53" y="375" font-size="16" font-style="italic" fill="{p['accent']}">the cat has other plans.</text>
<g transform="translate(495 76) scale(4)" shape-rendering="crispEdges" clip-path="url(#scene)">{scene(p)}</g>
</svg>\n'''


def icon(kind):
    ink, accent = "#b193e1", "#84ddbd"
    if kind == "watch":
        drawing = rect(4, 6, 24, 20, ink) + rect(6, 8, 20, 16, "#252c3b")
        drawing += f'<path class="trace" d="M8 17H12V13H15V21H18V16H24" fill="none" stroke="{accent}" stroke-width="2"/>'
        drawing += rect(10, 27, 12, 2, ink)
    else:
        drawing = rect(5, 4, 15, 20, ink) + '<g class="sheet">' + rect(11, 9, 15, 20, accent)
        drawing += rect(14, 14, 9, 2, "#dbe4dc") + rect(14, 19, 7, 2, "#dbe4dc")
        drawing += '</g>'
    motion = '<style>.trace{stroke-dasharray:40;animation:trace 3s linear infinite}.sheet{animation:sheet 4s steps(3,end) infinite}@keyframes trace{0%{stroke-dashoffset:40}70%,100%{stroke-dashoffset:0}}@keyframes sheet{0%,100%{transform:translate(0,0)}50%{transform:translate(-2px,-2px)}}@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" shape-rendering="crispEdges">{motion}{drawing}</svg>\n'


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
