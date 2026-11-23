# Profile artwork

The banner combines a small macOS-style window with an original pixel-art desk scene. The cat, monitor, plant, mug, window, hills and project icons are drawn with SVG rectangles and paths. No sprites, fonts or artwork were copied from another profile.

I looked at [pixel-profile](https://github.com/TheMysteriousGhost/pixel-profile) and [RyMe.md](https://github.com/ryanpolasky/ryme.md) for the idea of keeping lightweight animated artwork inside the repository. Those references informed the approach, rather than providing code or assets.

Run `python scripts/build_profile_art.py` to regenerate the light and dark banners and project icons. It uses only the Python standard library and does not contact any service.

The banner has drifting clouds, mug steam, a blinking cursor, occasional cat blinks and a small tail movement. CSS animations run inside the SVG; there is no JavaScript. `prefers-reduced-motion` stops the movement. The README provides alternative text and uses a `picture` element to choose a light or dark banner from the browser's color-scheme preference.

The original header is retained as `assets/header.svg`. The daily statistics runner owns only its existing snapshot and stats-card paths, so it does not regenerate or overwrite this artwork.
