# cortex.quickflat.make_figure

## Current signature (from source)
```python
def make_figure(
    braindata: dataset.Dataview,
    recache: bool = False,
    pixelwise: bool = True,
    thick: int = 32,
    sampler: str = 'nearest',
    height: int = 1024,
    dpi: int = 100,
    depth: float = 0.5,
    with_rois: bool = True,
    with_sulci: bool = False,
    with_labels: bool = True,
    with_colorbar: bool = True,
    with_borders: bool = False,
    with_dropout: Union[bool, float] = False,
    with_curvature: bool = False,
    extra_disp: Optional[tuple[str, str]] = None,
    with_connected_vertices: bool = False,
    overlay_file: Optional[str] = None,
    linewidth: Optional[int] = None,
    linecolor: Optional[ColorType] = None,
    roifill: Optional[ColorType] = None,
    shadow: Optional[int] = None,
    labelsize: Optional[str] = None,
    labelcolor: Optional[ColorType] = None,
    cutout: Optional[str] = None,
    curvature_brightness: Optional[float] = None,
    curvature_contrast: Optional[float] = None,
    curvature_threshold: Optional[bool] = None,
    fig: Optional[Union[Figure, Axes]] = None,
    extra_hatch: Optional[tuple[dataset.Dataview, tuple[float, float, float]]] = None,
    colorbar_ticks: Optional[npt.ArrayLike] = None,
    colorbar_location: Union[tuple[float, float, float, float], str] = 'center',
    roi_list: Optional[list[str]] = None,
    sulci_list: Optional[list[str]] = None,
    nanmean: bool = False,
) -> Figure:
```
This is the true, current signature — `cortex/quickflat/view.py` uses PEP 484 type hints
directly in the function definition, so (unlike many other pycortex functions) there is no
drift between the signature and a separate docstring type description here. The docstring
below it, however, is missing several of these parameters (see "Issues" below).

## Where this is documented today
- Source docstring: [cortex/quickflat/view.py:36-126](cortex/quickflat/view.py#L36-L126)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.quickflat.make_figure.html
  (Sphinx-autodoc page generated directly from this docstring — content matches source
  exactly, including the gaps below). The flat listing at
  https://gallantlab.org/pycortex/api_reference_flat.html truncates the signature to
  `make_figure(braindata[, recache, pixelwise, ...])`.

## Issues with current documentation
- **Parameters missing from the docstring entirely** despite being in the signature:
  `with_borders`, `with_connected_vertices`, `roi_list`. `with_borders` in particular is
  accepted by the signature but — see Notes below — is not read anywhere in the function
  body, so documenting it is actively misleading without a caveat.
- **`with_rois, with_labels, with_colorbar, with_borders, with_dropout, with_curvature, etc : bool, optional`**
  is a single collapsed docstring entry covering 6+ parameters with one description
  ("Display the rois, labels, colorbar, ..."). This hides that `with_dropout` is not
  actually `bool` — it accepts `bool`, `float` (a dropout "power"), or a `cortex.Dataview`
  (see Parameters below) — and it hides that `with_borders` does nothing.
- **No Returns section.** The function returns a `matplotlib.figure.Figure`; this is only
  visible from the `-> Figure` type annotation on the signature, not from any docstring text.
- **No Raises section.** The function raises `TypeError` if `braindata` is not a `Dataview`
  (e.g. if a `Dataset` is passed), and raises `ValueError` from `_check_colorbar_location`
  if `colorbar_location` is a string not in `{'left', 'center', 'right'}`. Neither is documented.
- **No Examples section.**
- **`sampler` doesn't enumerate real options accurately.** The docstring says `'trilinear'`,
  `'nearest'`, `'lanczos'`; the actual available samplers (from
  `cortex/mapper/samplers.py`) are `nearest`, `trilinear`, `gaussian`, `lanczos` — `gaussian`
  is missing from the docs.
- **`shadow` is documented as functional but is dead code.** The docstring says: "Standard
  deviation of the gaussian shadow. Set to 0 if you want no shadow." In the current source,
  `shadow` is threaded through to `composite.add_rois`, `composite.add_sulci`, and
  `composite.add_custom`, all of which forward it into `**kwargs` → `_convert_svg_kwargs`.
  That helper's `svg_style_key_mapping` dict (in `cortex/quickflat/utils.py`) has **no
  `"shadow"` key**. Because the dict comprehension in `_convert_svg_kwargs` does
  `svg_style_key_mapping[k]` for every kwarg whose value is not `None`, passing **any
  non-`None` value** for `shadow` (e.g. `make_figure(vol, shadow=2)`) raises
  `KeyError: 'shadow'` at runtime. This is a real behavioral bug (see `_notes.md`), and the
  current docs give no hint that the documented feature will crash if used.
- **Undocumented forwarding chains ("Other Parameters" is incomplete).** `make_figure`
  itself has no `**kwargs`, so it's not a *forwarding* problem the way `make_png`/`make_svg`
  are, but several of its own parameters are themselves opaque wrappers around further
  functions whose real parameter sets are not cross-referenced:
  - `pixelwise, thick, sampler, height, depth, recache, nanmean` → `composite.add_data` →
    `quickflat.utils.make_flatmap_image` → `get_flatcache`/`get_flatmask` (disk-caching
    behavior, e.g. writing `.npz` cache files under `<filestore>/<subject>/cache/`, is not
    mentioned anywhere here).
  - `with_dropout` (when not a `Dataview`) → `cortex.utils.get_dropout(subject, xfmname,
    power=...)`, which itself requires the `xfmname` transform's reference EPI image to be
    loadable from the database. This dependency is invisible from `make_figure`'s docs.
  - `linewidth, linecolor, roifill, shadow, labelsize, labelcolor, overlay_file, roi_list` →
    `composite.add_rois` → `svgobject.get_texture(...)` (in `cortex/svgoverlay.py`). The
    actual accepted *values* for `linecolor`/`labelcolor`/`roifill` are "anything
    `matplotlib.colors.ColorConverter.to_rgba` accepts" (documented nowhere) because they
    pass through `_color2hex`.
  - `sulci_list` → `composite.add_sulci` (same `get_texture` machinery).
  - `extra_disp` → `composite.add_custom`, which additionally requires a full,
    correctly-structured external SVG file (same structure as `overlays.svg`) — a
    significant undocumented precondition.
  - `extra_hatch` and `with_dropout` both → `composite.add_hatch` /
    `composite._make_hatch_image`, which has its own `hatch_space`/`hatch_color` knobs that
    are hard-coded when called from `make_figure` (not exposed as `make_figure` kwargs at
    all) — worth noting so users don't go looking for a `hatch_color=` kwarg on
    `make_figure` that doesn't exist.
- **`cutout` is under-explained.** The docstring says it should be "the name of a sub-layer
  of the 'cutouts' layer in `<filestore>/<subject>/overlays.svg`" — this assumes the reader
  already knows what "`<filestore>`" means and how to open/edit `overlays.svg` (e.g. via
  `cortex.add_roi`/`cortex.utils` GUI helpers); no pointer is given.
- **No mention of side effects**: `make_flatmap_image`/`get_flatcache`/`get_flatmask` write
  `.npz` cache files to disk under the subject's pycortex database cache directory the first
  time a given `(subject, xfmname, height, sampler, thick/depth)` combination is rendered
  (and whenever `recache=True`). This is a meaningful side effect (disk I/O, first-call
  latency) that is not mentioned.
- **`fig` behavior is under-specified.** Passing an existing `Figure` vs. `Axes` behaves
  differently (a `Figure` causes `plt.figure(fig.number)` + a brand new full-figure `Axes`
  to be added on top of it, rather than reusing the figure's existing axes; an `Axes` is used
  directly). This distinction — that passing a `Figure` will *add a new overlapping axes*
  rather than draw into the figure's existing axes — is easy to get wrong and isn't
  explained.

## Fixed documentation

### Summary
Show a Volume or Vertex on a flatmap with matplotlib.

### Parameters
- **braindata** : Dataview (e.g. `cortex.Volume`, `cortex.Vertex`, ...)
    The data to plot. Must be a `Dataview`, not a `Dataset` (raises `TypeError`).
- **recache** : bool, default `False`
    Force recreation of cached intermediate flatmap files. Slower, but can fix stale-cache
    issues after changing an alignment.
- **pixelwise** : bool, default `True`
    Use pixel-wise mapping instead of nearest-vertex mapping.
- **thick** : int, default `32`
    Number of samples through cortical thickness per pixel. Only used if `pixelwise=True`.
- **sampler** : {'nearest', 'trilinear', 'gaussian', 'lanczos'}, default `'nearest'`
    Resampling kernel for pulling values from volumetric data (see `cortex.mapper.samplers`).
- **height** : int, default `1024`
    Height in pixels of the output image; width follows the flatmap's aspect ratio.
- **dpi** : int, default `100`
    DPI used only for sizing the matplotlib figure in inches, not pixel resolution.
- **depth** : float, default `0.5`
    Cortical depth to sample (0=white matter, 1=pial). Used only when `thick <= 1`.
- **with_rois**, **with_sulci**, **with_labels**, **with_colorbar** : bool
    Whether to draw ROI outlines, sulcus outlines, layer labels, and a colorbar.
    Defaults `True`, `False`, `True`, `True`.
- **with_borders** : bool, default `False`
    Currently has no effect — accepted but unused in this version of pycortex.
- **with_dropout** : bool, float, or Dataview, default `False`
    Overlay hatching for low-signal regions. `True` auto-computes dropout (power=20);
    a float uses that as the power; a `Dataview` supplies the dropout map directly.
- **with_curvature** : bool, default `False`
    Show curvature as a grayscale background layer.
- **extra_disp** : (str, str), optional
    `(filename, layer)` — an extra SVG layer to display, from a file structured like
    `overlays.svg`.
- **with_connected_vertices** : bool, default `False`
    Draw lines between distant vertices sharing a voxel. Volumetric data only
    (raises `ValueError` for vertex data).
- **overlay_file** : str, optional
    Alternate overlay SVG file to use instead of the subject's default.
- **linewidth**, **linecolor**, **roifill**, **shadow**, **labelsize**, **labelcolor** :
  optional
    Line/fill/label styling for ROIs and sulci. `None` uses `options.cfg` defaults.
    `shadow` is currently non-functional — any non-`None` value raises `KeyError` (see
    Issues).
- **cutout** : str, optional
    Name of a shape in the overlay's `"cutouts"` layer to crop the figure to.
- **curvature_brightness**, **curvature_contrast**, **curvature_threshold** : optional
    Curvature display tuning; `None` uses `options.cfg` defaults.
- **fig** : Figure or Axes, optional
    Where to draw. `None` creates a new figure. A `Figure` gets a new axes added on top
    (existing axes aren't reused); an `Axes` is drawn into directly.
- **extra_hatch** : (Dataview, (float, float, float)), optional
    Extra cross-hatch layer, analogous to dropout hatching, driven by any `Dataview`.
- **colorbar_ticks** : array-like, optional
    Tick locations for the colorbar. `None` uses evenly-spaced values between vmin/vmax.
- **colorbar_location** : {'left', 'center', 'right'} or 4-tuple, default `'center'`
    Colorbar position; a preset name or `(left, bottom, width, height)` in figure fraction.
- **roi_list**, **sulci_list** : list of str, optional
    Restrict which ROIs/sulci are drawn. `None` draws all.
- **nanmean** : bool, default `False`
    Ignore NaNs when averaging multiple samples per pixel.

### Returns
- **fig** : `matplotlib.figure.Figure`
    The figure the flatmap (and any enabled overlay layers) was drawn into — either the
    newly-created figure, or the one derived from the `fig` argument.

### Raises
- `TypeError` — if `braindata` does not resolve to a `cortex.dataset.Dataview` (e.g. a
  `cortex.Dataset` was passed instead of a single view).
- `ValueError` — if `colorbar_location` is a string not in `{'left', 'center', 'right'}`.
- `ValueError` — if `with_connected_vertices=True` but `braindata` has no `xfmname`
  (i.e. is vertex, not volume, data).
- `KeyError: 'shadow'` — if `shadow` is given any non-`None` value while `with_rois`,
  `with_sulci`, or `extra_disp` is enabled (dead/broken parameter, see Issues above).
- `Exception` — from `composite.add_cutout`, if `cutout` names a shape with zero pixels.

### Notes
- **Disk cache side effects.** The first call for a given
  `(subject, height, xfmname, pixelwise, thick/depth, sampler)` combination writes cache
  files (flatmap mask + pixel/vertex mapping matrix) to
  `<filestore>/<subject>/cache/` (pycortex's per-subject database directory — see
  `cortex.database.Database`). Subsequent calls reuse these unless `recache=True`.
- **No FreeSurfer/FSL/GUI dependency** for this function itself, but it does require the
  subject to already exist in the pycortex database with flat surfaces generated
  (`cortex.freesurfer.flatten` or equivalent) and, for volumetric data, a transform
  registered via `cortex.align`.
- `with_dropout=True` additionally requires the transform's reference EPI image to be
  loadable (`cortex.database.Database.get_xfm(...).reference`).
- Performance: `pixelwise=True` with large `thick` and `height` can be slow the first time
  (before caching); `with_connected_vertices=True` is noted in the source as
  computationally expensive for high-resolution flatmaps.

### Example
```python
import matplotlib.pyplot as plt
import numpy as np
import cortex

# pycortex ships a small example subject ("S1") together with its own test/demo data,
# used throughout the pycortex documentation and gallery.
subject = "S1"
xfm = "fullhead"

# Random data matching S1's fullhead functional volume shape, for a runnable example.
volume_shape = cortex.db.get_xfm(subject, xfm).shape
data = np.random.randn(*volume_shape)
vol = cortex.Volume(data, subject, xfm, vmin=-2, vmax=2, cmap='RdBu_r')

fig = cortex.quickflat.make_figure(
    vol,
    with_curvature=True,
    with_rois=True,
    with_labels=True,
    with_colorbar=True,
)
fig.savefig("example_flatmap.png", dpi=100)
plt.close(fig)
```

## Confidence / open questions
- Confirmed by direct inspection of `cortex/quickflat/view.py`, `composite.py`, and
  `utils.py` that `with_borders` is unused in the function body and that `shadow` triggers a
  `KeyError` when non-`None`. These are code behaviors, not docstring interpretation, but I
  did not execute the code to confirm the `KeyError` at runtime (no pycortex install with a
  built extension + example subject was available in this pass) — this is inferred from
  static reading of `_convert_svg_kwargs` in `cortex/quickflat/utils.py:221-255` and should
  be double-checked by actually running `cortex.quickflat.make_figure(vol, shadow=2)`.
- I could not verify against a live pycortex installation that subject `"S1"` /
  transform `"fullhead"` are present by default in a fresh pycortex database — these names
  are the standard example subject/transform used throughout pycortex's own docs and
  examples gallery, but a first-time user must run the pycortex example-data download step
  (`cortex.utils.download_subject`-style setup, per pycortex's install docs) before this
  example will run. This is called out generically for all examples in `_notes.md`.
- **Recommendation for maintainers:** either implement `with_borders` or remove it from the
  signature; fix (or remove) the `shadow` parameter's broken kwarg-forwarding; add a
  `Returns` section to the real docstring; add at least one runnable example.
