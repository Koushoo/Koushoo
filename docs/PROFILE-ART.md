# Profile artwork

The banner combines a small macOS-style window with an original pixel-art desk scene. The cat, monitor, plant, mug, window, hills and project icons are drawn with SVG rectangles and paths. No sprites, fonts or artwork were copied from another profile.

I looked at [pixel-profile](https://github.com/TheMysteriousGhost/pixel-profile) and [RyMe.md](https://github.com/ryanpolasky/ryme.md) for the idea of keeping lightweight animated artwork inside the repository. Those references informed the approach, rather than providing code or assets.

Run `python scripts/build_profile_art.py` to regenerate the light and dark banners and project icons. It uses only the Python standard library and does not contact any service.

The banner tells a small looping story. Over 24 seconds, the cat hops off the desk, walks underneath, pauses, returns and jumps back up. A nested sprite flips its direction independently from the jump path. The window has a slower 48-second daylight-to-moonlight cycle, with stars and an occasional shooting star. Code lines appear on the monitor, while the mug steams and the cursor blinks. The project icons have their own small animations.

The cat follows a fluttering butterfly through the room. Birds cross the window, coloured string lights gently brighten and fade, and a sunbeam fades as evening arrives. Both themes use a warm mix of lavender, peach, mint and gold. A striped rug, bookshelf, tiny framed heart, speaker, flower, slippers and sticky note fill out the room. The caption “the cat has other plans” refers to the little scene rather than a claim about the profile owner.

CSS animations run inside the SVG; there is no JavaScript. `prefers-reduced-motion` stops all movement and leaves a complete daylight scene. The README provides alternative text and uses a `picture` element to choose a light or dark banner from the browser's color-scheme preference. Neither the text nor the layout moves during playback.

The original header is retained as `assets/header.svg`. The daily statistics runner owns only its existing snapshot and stats-card paths, so it does not regenerate or overwrite this artwork.
