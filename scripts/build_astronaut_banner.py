"""Compose captured Friday scene frames into GitHub-compatible profile banners.

Usage: python scripts/build_astronaut_banner.py path/to/frames --fonts C:/Windows/Fonts
Requires Pillow. Captures are inputs; this script does not run or modify the website.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def build(frames_dir, fonts):
    captures = sorted(frames_dir.glob("[0-9][0-9][0-9].png"))
    if len(captures) < 2:
        raise ValueError("At least two captured PNG frames are required")
    font = lambda size, bold=False: ImageFont.truetype(str(fonts / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)
    for theme in ("dark", "light"):
        bg, edge, ink, muted, accent = ("#1c192e", "#3b3455", "#f3eafb", "#b4a6c6", "#d2a6eb") if theme == "dark" else ("#fff8f2", "#e6d3dc", "#392d46", "#7b697d", "#9364b3")
        base = Image.new("RGB", (1000, 430), bg)
        d = ImageDraw.Draw(base)
        d.rounded_rectangle((1, 1, 998, 428), radius=19, outline=edge, width=2)
        d.line((1, 51, 998, 51), fill=edge)
        for x, c in ((29, "#ff6058"), (48, "#febc2e"), (67, "#29c840")):
            d.ellipse((x-5, 22, x+5, 32), fill=c)
        d.text((500, 25), "Koushoo’s desk", font=font(13), fill=muted, anchor="mm")
        d.text((53, 111), "HELLO THERE", font=font(13), fill=accent)
        d.text((50, 147), "I’m Koushoo.", font=font(44, True), fill=ink)
        d.text((53, 212), "A student, building small things.", font=font(19), fill=muted)
        d.rounded_rectangle((53, 263, 88, 266), radius=1, fill=accent)
        d.text((53, 289), "learning as I go.", font=font(13), fill=muted)
        d.text((53, 367), "Python · Linux · small tools", font=font(13), fill=muted)
        mask = Image.new("L", (448, 310))
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, 447, 309), radius=12, fill=255)
        frames=[]
        for path in captures:
            with Image.open(path) as shot:
                scene=shot.convert("RGB").crop((155, 125, 900, 640)).resize((448, 310), Image.Resampling.LANCZOS)
            frame=base.copy()
            frame.paste(scene, (495, 82), mask)
            frames.append(frame)
        # One shared palette keeps the stationary lettering and background stable.
        sample=Image.new("RGB", (500, 215*len(frames)))
        for i, frame in enumerate(frames):
            sample.paste(frame.resize((500,215)), (0, i*215))
        palette=sample.quantize(colors=240)
        reserved=[bg, edge, ink, muted, accent, "#ff6058", "#febc2e", "#29c840", "#000000"]
        values=palette.getpalette()[:720]
        for color in reserved:
            values.extend(bytes.fromhex(color.lstrip("#")))
        values.extend([0] * (768-len(values)))
        palette.putpalette(values)
        indexed=[f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
        loop=indexed+indexed[-2:0:-1]
        target=ROOT / "assets" / f"astronaut-{theme}.gif"
        loop[0].save(target, save_all=True, append_images=loop[1:], duration=110, loop=0, optimize=True, disposal=1)
        frames[0].save(ROOT / "assets" / f"astronaut-{theme}-still.png")
        print(theme, len(loop), "frames", target.stat().st_size, "bytes")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frames", type=Path)
    parser.add_argument("--fonts", type=Path, required=True)
    args=parser.parse_args()
    build(args.frames, args.fonts)
