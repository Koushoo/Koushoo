"""Draw the profile's original SVG artwork. No network or dependencies."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEMES = ("light", "dark")


def rect(x, y, w, h, color, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'


def header(theme):
    dark = theme == "dark"
    bg, edge, ink, muted = ("#17191c", "#34383e", "#e5e7eb", "#9299a3") if dark else ("#fafafa", "#d9dde2", "#25292f", "#646d78")
    accent = "#8eaf98" if dark else "#426e51"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="270" viewBox="0 0 1000 270" role="img" aria-labelledby="title desc">
<title id="title">Koushoo</title>
<desc id="desc">Koushoo. Student. Python, Linux and small tools. A quiet terminal window with a little cat beside the prompt.</desc>
<style>
text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.cursor{{animation:blink 1.8s steps(1,end) infinite}}
@keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:0}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect x="1" y="1" width="998" height="268" rx="9" fill="{bg}" stroke="{edge}"/>
<path d="M1 39H999" stroke="{edge}"/>
<g fill="{muted}" opacity=".65"><circle cx="22" cy="20" r="4"/><circle cx="38" cy="20" r="4"/><circle cx="54" cy="20" r="4"/></g>
<text x="500" y="24" font-size="12" text-anchor="middle" fill="{muted}">koushoo — ~</text>
<text x="36" y="88" font-size="14" fill="{accent}">~ / home</text>
<text x="34" y="136" font-size="33" font-weight="600" letter-spacing="-1" fill="{ink}">Koushoo</text>
<text x="36" y="171" font-size="15" fill="{muted}">Student. Working with Python and Linux.</text>
<text x="36" y="226" font-size="14" fill="{accent}">$</text>
<rect class="cursor" x="54" y="213" width="8" height="15" fill="{accent}"/>
<path d="M650 71V235" stroke="{edge}"/>
<g font-size="13" fill="{muted}">
<text x="685" y="94">~/projects</text>
<text x="685" y="126">├── quietwatch/</text>
<text x="685" y="153">└── file-tidy/</text>
</g>
<g fill="{muted}" shape-rendering="crispEdges" transform="translate(865 195) scale(2)">
<path d="M0 9h3V3h2v2h6V3h2v6h2v8H3v-2H0zm5-2v2h2V7zm5 0v2h2V7z" fill-rule="evenodd"/>
<path d="M15 13h5v-5h2v7h-7z"/>
</g>
</svg>\n'''


def icon(kind):
    ink, accent = "#9299a3", "#8eaf98"
    if kind == "watch":
        drawing = rect(4, 6, 24, 20, ink) + rect(6, 8, 20, 16, "#252c3b")
        drawing += f'<path class="trace" d="M8 17H12V13H15V21H18V16H24" fill="none" stroke="{accent}" stroke-width="2"/>'
        drawing += rect(10, 27, 12, 2, ink)
    else:
        drawing = rect(5, 4, 15, 20, ink) + '<g class="sheet">' + rect(11, 9, 15, 20, accent)
        drawing += rect(14, 14, 9, 2, "#dbe4dc") + rect(14, 19, 7, 2, "#dbe4dc")
        drawing += '</g>'
    motion = ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" shape-rendering="crispEdges">{motion}{drawing}</svg>\n'


def main():
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for theme in THEMES:
        (assets / f"workspace-{theme}.svg").write_text(header(theme), encoding="utf-8", newline="\n")
    for kind in ("watch", "files"):
        (assets / f"pixel-{kind}.svg").write_text(icon(kind), encoding="utf-8", newline="\n")
    print("Built two themed banners and two project icons.")


if __name__ == "__main__":
    main()
