# Profile artwork

The header is one borderless space scene. The name and introduction sit in the same black star field as the astronaut, with no window controls, inset frame or panel borders. A moon, ringed planet, satellite and steady star field complement the captured calendar, notebook, envelope and checkmark.

## Source credit

The scene was captured from the local `F:/friday-3d-website` project. Its README identifies the underlying astronaut, Earth, textures and rendering code as a reconstruction of [Lusion](https://lusion.co/). The Friday adaptation adds a calendar, notebook, envelope and checkmark. These third-party scene assets are not claimed as original profile artwork. The source website files were not modified.

The README delivers a full-colour animated WebP with lossless endpoints, with GIF as a fallback, rather than running WebGL or JavaScript. The WebP avoids palette banding in Earth’s atmosphere. A static PNG is selected by the README when reduced motion is requested. The 160-frame, 14.4-second loop uses a cosine timeline with motion-compensated source frames; motion eases to a stop before reversing. The final rendered frame is explicitly copied from the first. WebP endpoints reuse the same lossless bitstream; intermediate frames update only the moving right-hand area, preserving the text and left-hand stars unchanged. The decoded WebP and GIF endpoints are checked for exact equality. Planets and star brightness stay fixed; the satellite only drifts gently. The GIF fallback uses one shared palette to keep the text and star field stable.

## Rebuilding

Capture PNG frames from the locally running scene into a separate directory, with three-digit numeric filenames. Then run:

```powershell
python scripts/build_astronaut_banner.py path/to/frames --fonts C:/Windows/Fonts
```

The compositor requires Pillow, NumPy, OpenCV and the Segoe UI font files. Bidirectional optical flow follows moving edges before blending intermediate frames, reducing doubled outlines on the suit and hands. It crops the scene, adds stationary profile text and orbiting objects, uses one shared palette, and writes WebP/GIF/PNG assets. It does not modify the source website or contact a service. Source captures stay local; the repository contains the final rendered banners. The earlier SVG artwork is retained; older raster exports are removed from the current tree but preserved in Git history and local backups. The v1 release is preserved in commit `98cf1f0`; a separate local ZIP and full-history bundle were verified before the update.

## Copying and attribution

This is public artwork, so it is downloadable. Public GitHub repositories can be viewed, cloned and forked; browsers can also save images or take screenshots. Disabling right-click, obfuscating JavaScript or hiding a URL would not prevent those routes. GitHub README artwork cannot enforce an access-control policy on a visitor’s device.

This version burns `@Koushoo` into the astronaut area and includes a profile URL in the image. These marks discourage casual reuse and identify this profile adaptation; they can still be cropped, retouched or removed. `assets/space-orbit-v3-provenance.json` records file hashes so exact copies can be compared. Hashes are provenance evidence, not DRM or proof of ownership of the underlying model.

The source captures and full-colour intermediate frames stay in the ignored local `work/` directory. Obsolete unbranded exports were removed from the current file tree; earlier published files and code remain accessible through Git history and cannot be recalled from other people’s copies. The upstream MIT license is retained, and these changes do not revoke any rights already granted. The astronaut, textures and source scene retain their third-party credits; the username mark is not a claim to have created those assets.

References: [GitHub repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility), [GitHub licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [Firefox screenshots](https://support.mozilla.org/en-US/kb/take-screenshots-firefox).

The WebP frame container follows [RFC 9649](https://www.rfc-editor.org/rfc/rfc9649.html). Lossless full-canvas endpoints reuse the same encoded image data; compressed intermediate frames replace only the moving area, so the name and introduction never need to be re-encoded.
