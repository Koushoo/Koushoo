# Profile artwork

The header is one borderless space scene. The name and introduction sit in the same black star field as the astronaut, with no window controls, inset frame or panel borders. A moon, ringed planet, satellite and occasional meteor complement the captured calendar, notebook, envelope and checkmark.

## Source credit

The scene was captured from the local `F:/friday-3d-website` project. Its README identifies the underlying astronaut, Earth, textures and rendering code as a reconstruction of [Lusion](https://lusion.co/). The Friday adaptation adds a calendar, notebook, envelope and checkmark. These third-party scene assets are not claimed as original profile artwork. The source website files were not modified.

The README delivers a full-colour animated WebP, with GIF as a fallback, rather than running WebGL or JavaScript. The WebP avoids palette banding in Earth’s atmosphere. A static PNG is selected by the README when reduced motion is requested. The 160-frame, 14.4-second loop uses a cosine timeline with motion-compensated source frames; motion eases to a stop before reversing. Added objects follow periodic paths that meet at the loop boundary. The GIF fallback uses one shared palette to keep the text and star field stable.

## Rebuilding

Capture PNG frames from the locally running scene into a separate directory, with three-digit numeric filenames. Then run:

```powershell
python scripts/build_astronaut_banner.py path/to/frames --fonts C:/Windows/Fonts
```

The compositor requires Pillow, NumPy, OpenCV and the Segoe UI font files. Bidirectional optical flow follows moving edges before blending intermediate frames, reducing doubled outlines on the suit and hands. It crops the scene, adds stationary profile text and orbiting objects, uses one shared palette, and writes WebP/GIF/PNG assets. It does not modify the source website or contact a service. Source captures stay local; the repository contains the final rendered banners. The earlier SVG artwork and v1 space banner are retained. The v1 release is preserved in commit `98cf1f0`; a separate local ZIP and full-history bundle were verified before the update.
