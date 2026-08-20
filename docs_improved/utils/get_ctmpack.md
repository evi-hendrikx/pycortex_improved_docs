# cortex.utils.get_ctmpack

## Current signature (from source)
```python
def get_ctmpack(subject, types=("inflated",), method="raw", level=0, recache=False,
                decimate=False, external_svg=None,
                overlays_available=None):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:74-110](cortex/utils.py#L74-L110)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_ctmpack.html

## Issues with current documentation
- **`Returns` section is present but incomplete**: `"ctmfile :"` has no type/description —
  should state it's the `str` path to the generated/cached `.json` mesh-pack file (the
  companion `.ctm`/`.svg` files sit alongside it, sharing the same base name).
- **No Raises section.**
- **`method`'s docstring is terse ("one of ['mg2','raw']")** without explaining what the
  two methods actually mean for the end user (`mg2`: compressed mesh format requiring a
  vertex remapping — see `get_ctmmap`; `raw`: uncompressed, no remapping needed).
- **This is a key hidden dependency of `cortex.webgl.show`/`make_static`** (both call
  `get_ctmpack` internally with `method="mg2"` hard-coded) — not cross-referenced here.

## Fixed documentation

### Summary
Creates ctm file for the specified input arguments. This is a cached file that specifies
(1) the surfaces between which to interpolate (`types` argument), (2) the `method` to
interpolate between surfaces.

### Parameters
- **subject** : str
    Name of subject in pycortex store
- **types** : tuple
    Surfaces between which to interpolate.
- **method** : str
    string specifying method of how inverse transforms for labels are computed
    (determines how labels are displayed on 3D viewer) one of ['mg2','raw']. `'mg2'` is a
    compressed mesh format (used by `cortex.webgl`) that requires a vertex remapping to
    recover freesurfer-space vertex correspondence (see `get_ctmmap`); `'raw'` is
    uncompressed and needs no remapping.
- **recache** : bool
    Whether to re-generate .ctm files. Can resolve some errors but takes more time to
    re-generate cached files.
- **decimate** : bool
    whether to decimate the mesh geometry of the hemispheres to reduce file size
- **external_svg** : str or None
    file string for .svg file containing alternative overlays for brain viewer. If None,
    the `overlays.svg` file for this subject (in the pycortex_store folder for the
    subject) is used.
- **overlays_available** : tuple or None
    Which overlays in the svg file to include in the viewer. If None, all layers in the
    relevant svg file are included.

### Returns
- **ctmfile** : str
    Path to the generated (or cached) `.json` mesh-pack manifest file. Companion `.ctm`
    (compressed mesh) and `.svg` (overlay) files are written alongside it, sharing the
    same base filename.

### Raises
Propagates errors from `cortex.brainctm.make_pack` (e.g. missing surface types for
`subject`).

### Notes
- **Disk cache side effect**: writes `.json`/`.ctm`/`.svg` files under the subject's
  pycortex cache directory, keyed by subject, `types`, `method`, and `level`/`decimate`.
- Used internally by `cortex.webgl.show`/`cortex.webgl.make_static` (both call this with
  `method="mg2"`).
- No FreeSurfer/FSL/GUI dependency, but requires the requested surface `types` (plus
  fiducial/flat) to already exist in the pycortex database.

### Example
```python
import cortex

ctmfile = cortex.utils.get_ctmpack("S1", types=("inflated", "flat"), method="raw")
```

## Confidence / open questions
- **Recommendation for maintainers:** complete the `Returns` section's description;
  cross-reference `cortex.webgl`'s usage.
