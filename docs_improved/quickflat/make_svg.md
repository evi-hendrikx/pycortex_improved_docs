# cortex.quickflat.make_svg

## Current signature (from source)
```python
def make_svg(
    fname,
    braindata,
    with_labels=False,
    with_curvature=True,
    layers=['rois'],
    height=1024,
    overlay_file=None,
    with_dropout=False,
    **kwargs,
):
```
Note: no type hints here (unlike `make_figure`/`make_png` in the same file); all types below
were inferred from usage in the body.

## Where this is documented today
- Source docstring: [cortex/quickflat/view.py:308-339](cortex/quickflat/view.py#L308-L339)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.quickflat.make_svg.html
  (autodoc-generated from this docstring; flat listing truncates to
  `make_svg(fname, braindata[, with_labels, ...])`).

## Issues with current documentation
- **Mutable default argument.** `layers=['rois']` is a mutable list default — a Python
  anti-pattern (shared across calls if ever mutated in place). Not currently mutated inside
  `make_svg`, so it's not an active bug, but it's worth flagging as a maintainer note since
  it's easy to accidentally break in a future edit. Not something to fix here (source is
  out of scope), but noted in `_notes.md`.
- **`**kwargs` undocumented.** `make_svg` forwards `**kwargs` to
  `quickflat.utils.make_flatmap_image(braindata, height=height, **kwargs)`. The only
  keywords `make_flatmap_image` itself accepts beyond `braindata`/`height` are `recache`
  (bool) and `nanmean` (bool) as named parameters, plus a *further* `**kwargs` that is
  forwarded again to `get_flatcache(subject, xfmname, height=..., recache=..., **kwargs)`,
  whose accepted keywords are `pixelwise`, `thick`, `sampler`, `depth`. None of this chain
  is mentioned in `make_svg`'s docstring — a user cannot tell from the docs that
  `make_svg(fname, vol, pixelwise=False, sampler='trilinear')` is valid.
  `make_svg` does **not**, however, forward to `make_figure` — this is a materially
  different (much smaller) kwargs surface than `make_png`, and the docstring doesn't clarify
  that distinction (a reader familiar with `make_png` might reasonably assume `make_svg`
  also accepts things like `with_rois`, `linewidth`, `roifill`, etc. — it does not; ROI
  styling instead comes from `layers`/the overlay SVG's own defaults, not from kwargs).
- **No Returns section** — returns `None`; writes a file as a side effect via
  `roipack.get_svg(fname, ...)`.
- **No Raises section.**
- **No Examples section.**
- **`layers` parameter under-documented.** Docstring says "List of layer names to show" with
  no indication of what named layers actually exist (`'rois'`, `'sulci'`, `'cutouts'`, and
  any custom layers present in the subject's `overlays.svg`), nor that only ROI-vector data
  is truly vector — everything else (`with_curvature`, `with_dropout`, and the data itself)
  is rendered as one or more flattened *raster* PNGs embedded inside the SVG, not real SVG
  paths (stated in the function's own comment "Ideally, this function would layer different
  images... but that has been left to implement" but not carried into the parameter docs).
- **`with_dropout` docstring says "or a `cortex.Dataview` object"** but the actual dropout
  branch (`if with_dropout: ... hatch_data = with_dropout if isinstance(with_dropout,
  dataset.Dataview) else utils.get_dropout(...)`) only special-cases `True`/`Dataview` — a
  numeric "power" value (as `make_figure`'s `with_dropout` accepts) is **not** supported
  here: any truthy non-`Dataview` value falls through to
  `utils.get_dropout(dataview.subject, dataview.xfmname)` using the *default* power (`20`),
  silently ignoring the passed-in number. This is a real behavioral difference from
  `make_figure`'s `with_dropout` that isn't documented and could surprise a user coming from
  `make_figure`/`make_png`.
- **`overlay_file` type not given** — it's a file path (str) to an alternate SVG overlay
  file, same convention as `make_figure`'s `overlay_file`, but this cross-reference isn't
  made.

## Fixed documentation

### Summary
Renders `braindata` as a flattened cortical image and embeds it (as one or more base64 PNG
raster layers: data, optionally curvature, optionally dropout hatching) inside a copy of the
subject's overlay SVG file, keeping the requested vector `layers` (e.g. ROI outlines) as
real, editable SVG paths on top. Useful for producing publication figures where ROI outlines
need to remain vector graphics (editable in Inkscape/Illustrator) while the underlying data
map is a raster image.

### Parameters
- **fname** : str
    File path to save the resulting `.svg` file to.
- **braindata** : `cortex.dataset.Dataview`
    The data to render as the raster data layer. See `make_figure.md` for accepted types.
- **with_labels** : bool, default `False`
    Whether to show text labels on the vector layers listed in `layers` (e.g. ROI names).
- **with_curvature** : bool, default `True`
    Whether to render a grayscale curvature image and embed it as a background raster layer
    beneath the data. Uses fixed 2-level shading (0.25/0.5) rather than a continuous
    colormap — there are no tunable brightness/contrast parameters here (unlike
    `make_figure`'s `curvature_brightness`/`curvature_contrast`).
- **layers** : list of str, default `['rois']`
    Which named vector layer(s) from the overlay SVG to keep as real (editable) SVG
    paths in the output — typically `'rois'` and/or `'sulci'`, or any custom layer name
    present in the subject's `overlays.svg`.
- **height** : int, default `1024`
    Height, in pixels, of the embedded raster PNG layer(s).
- **overlay_file** : str, optional
    Path to an alternate overlay SVG file to use instead of the subject's default
    `overlays.svg` in the pycortex database.
- **with_dropout** : bool or `cortex.Dataview`, default `False`
    Whether/how to overlay dropout hatching as an additional raster layer.
    - `False` (default): no dropout layer.
    - `True`: auto-compute dropout via `cortex.utils.get_dropout(subject, xfmname)` (fixed
      `power=20` — unlike `make_figure`, a custom numeric power is **not** supported here;
      any other truthy non-`Dataview` value is treated the same as `True` and still uses the
      default power).
    - a `cortex.Dataview`: use this view's values directly as the dropout map.
- **\*\*kwargs** : forwarded to `cortex.quickflat.utils.make_flatmap_image`
    Recognized keywords (traced through `make_flatmap_image` → `get_flatcache`):
    - `recache` : bool, default `False` — force regeneration of cached flatmap geometry.
    - `nanmean` : bool, default `False` — ignore NaNs when averaging samples per pixel.
    - `pixelwise` : bool, default `True`
    - `thick` : int, default `32`
    - `sampler` : {'nearest', 'trilinear', 'gaussian', 'lanczos'}, default `'nearest'`
    - `depth` : float, default `0.5`

    Unlike `make_png`, keywords specific to `make_figure` (`with_rois`, `linewidth`,
    `roifill`, `cutout`, `fig`, etc.) are **not** accepted here and will raise `TypeError`
    if passed, since they're not consumed anywhere in this call chain.

### Returns
`None`. The SVG file is written to `fname` as a side effect.

### Raises
- `TypeError` — if an unrecognized keyword is passed via `**kwargs` (it will eventually
  reach a function that doesn't accept it — e.g. `get_flatcache`).
- Any exception raised by `cortex.database.Database.get_overlay` (e.g. missing/corrupt
  overlay file) or `RoiPack.get_svg` (e.g. unwritable `fname` path).

### Notes
- Same disk-cache side effects as `make_figure`/`make_png` (flatmap geometry cache files
  under the subject's pycortex cache directory).
- `with_curvature=True` triggers an additional call to `db.get_surfinfo(braindata.subject)`
  (curvature must already exist for the subject — see `cortex.surfinfo.curvature`).
- No FreeSurfer/FSL/GUI dependency for this function itself.
- The produced SVG embeds raster PNGs as base64 data URIs; file sizes can get large at high
  `height`.

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
volume_shape = cortex.db.get_xfm(subject, xfm).shape
data = np.random.randn(*volume_shape)
vol = cortex.Volume(data, subject, xfm, vmin=-2, vmax=2, cmap='RdBu_r')

cortex.quickflat.make_svg(
    "example_flatmap.svg",
    vol,
    with_labels=True,
    with_curvature=True,
    layers=['rois', 'sulci'],
    height=512,
)
```

## Confidence / open questions
- The claim that a numeric `with_dropout` power is silently ignored (falls back to the
  default `power=20`) is based on static reading of `view.py:372-379`
  (`hatch_data = with_dropout if isinstance(with_dropout, dataset.Dataview) else
  utils.get_dropout(dataview.subject, dataview.xfmname)` — no `power=` forwarded at all) —
  confirmed by source inspection, not execution.
- Could not verify from source/tests what the intended distinction is between `background`
  and `name` parameters of the underlying `RoiPack.get_texture` (marked `idkwtf` in that
  function's own docstring) — this is upstream of `make_svg` (not one of its own parameters)
  so it doesn't affect `make_svg`'s own docs, but is flagged in `_notes.md` since it hints at
  a broader in-source documentation gap in `cortex/svgoverlay.py`.
- **Recommendation for maintainers:** clarify in the docstring that `make_svg`'s kwargs
  surface is materially smaller than `make_png`'s (it does not go through `make_figure`);
  either support a numeric dropout power (for consistency with `make_figure`/`make_png`) or
  explicitly document that it's unsupported; avoid the mutable default `layers=['rois']`.
