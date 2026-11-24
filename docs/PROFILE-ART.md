# Profile artwork

The macOS-style header keeps the earlier profile layout and uses a rendered astronaut scene in place of the pixel room. Text and window controls remain stationary.

## Source credit

The scene was captured from the local `F:/friday-3d-website` project. Its README identifies the underlying astronaut, Earth, textures and rendering code as a reconstruction of [Lusion](https://lusion.co/). The Friday adaptation adds a calendar, notebook, envelope and checkmark. These third-party scene assets are not claimed as original profile artwork. The source website files were not modified.

GitHub displays the scene as a GIF, rather than running WebGL or JavaScript. Light and dark versions are provided, along with static PNGs selected by the README when reduced motion is requested. The rendered sequence plays forwards and backwards to avoid a jump at the loop boundary.

## Rebuilding

Capture PNG frames from the locally running scene into a separate directory, with three-digit numeric filenames. Then run:

```powershell
python scripts/build_astronaut_banner.py path/to/frames --fonts C:/Windows/Fonts
```

The compositor requires Pillow and the Segoe UI font files. It crops the scene, adds the stationary profile text, uses one palette per theme, and writes GIF/PNG assets. It does not modify the source website or contact a service. Source captures stay local; the repository contains the final rendered banners. The earlier SVG artwork is retained.
