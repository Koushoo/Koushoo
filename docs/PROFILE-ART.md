# Profile artwork

The header is rendered offline. The editable generator and publishing tools are kept in a separate private project; this public repository receives only the finished banner files. The animation itself remains visible on the profile.

The 14.4-second loop has identical decoded start and end frames. The name, introduction and background stars stay fixed. A static PNG is used when reduced motion is requested, with GIF as an alternative to WebP.

## Source credit

The astronaut, Earth, textures and original scene come from [Lusion](https://lusion.co/), through the local Friday adaptation. That adaptation adds the calendar, notebook, envelope and checkmark. The Koushoo mark identifies this profile composition; it does not claim authorship of those third-party assets. Existing licenses and credits remain unchanged.

## Publication

The private publishing tool checks file hashes, decoded loop endpoints and the destination repository. It only accepts the three finished images and their provenance manifest. It stops if source files are included, exports were changed after validation, the public checkout has unfinished work, or the destination is not Koushoo/Koushoo. These are publishing safeguards, not DRM.

Earlier versions of the generator were public and may remain in Git history or other people's copies. Moving the current tools to a private repository cannot recall those versions. The published images are still downloadable; visible branding and hashes provide attribution rather than access control.
