# Profile artwork

The header is one borderless space scene. The name and introduction sit in the same black star field as the astronaut, with no window controls, inset frame or panel borders. A moon, ringed planet, satellite and occasional meteor complement the captured calendar, notebook, envelope and checkmark.

## Source credit

The scene was captured from the local `F:/friday-3d-website` project. Its README identifies the underlying astronaut, Earth, textures and rendering code as a reconstruction of [Lusion](https://lusion.co/). The Friday adaptation adds a calendar, notebook, envelope and checkmark. These third-party scene assets are not claimed as original profile artwork. The source website files were not modified.

GitHub displays the scene as a GIF, rather than running WebGL or JavaScript. A static PNG is selected by the README when reduced motion is requested. The 120-frame loop uses a cosine timeline with blended source frames; motion eases to a stop before reversing. Added objects follow periodic paths that meet at the loop boundary. One shared palette keeps the text and star field stable.

## Rebuilding

Capture PNG frames from the locally running scene into a separate directory, with three-digit numeric filenames. Then run:

```powershell
python scripts/build_astronaut_banner.py path/to/frames --fonts C:/Windows/Fonts
```

The compositor requires Pillow and the Segoe UI font files. It crops the scene, adds stationary profile text and orbiting objects, uses one shared palette, and writes GIF/PNG assets. It does not modify the source website or contact a service. Source captures stay local; the repository contains the final rendered banners. The earlier SVG artwork is retained.
