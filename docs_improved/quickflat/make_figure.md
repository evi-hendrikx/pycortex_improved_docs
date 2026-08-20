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
- **braindata** : Dataview (e.g. instance of cortex.Volume, cortex.Vertex, ...)
    the data you would like to plot on a flatmap
- **recache** : boolean
    Whether or not to recache intermediate files. Takes longer to plot this way, potentially
    resolves some errors. Useful if you've made changes to the alignment
- **pixelwise** : bool
    Use pixel-wise mapping
- **thick** : int
    Number of layers through the cortical sheet to sample. Only applies for pixelwise = True
- **sampler** : str
    Name of sampling function used to sample underlying volume data. Options are 'nearest',
    'trilinear', 'gaussian', 'lanczos' (see `cortex.mapper.samplers`; the shipped docstring
    omits 'gaussian').
- **height** : int
    Height of the image to render. Automatically scales the width for the aspect
    of the subject's flatmap
- **dpi** : int
    DPI of the generated image. Only applies to the scaling of matplotlib elements,
    specifically the colormap
- **depth** : float
    Value between 0 and 1 for how deep to sample the surface for the flatmap (0 = gray/white
    matter boundary, 1 = pial surface)
- **with_rois**, **with_labels**, **with_colorbar**, **with_sulci** : bool, optional
    Display the rois, labels, colorbar, and sulci. Defaults `True`, `True`, `True`, `False`.
- **with_borders** : bool, optional
    Accepted but currently has no effect — unused in this version of pycortex (see Issues).
- **with_dropout** : bool, float, or Dataview, optional
    Display annotated flatmap dropout. `True` auto-computes it (power=20); a float is used
    as the power; a `Dataview` supplies the dropout map directly. Default `False`.
- **with_curvature** : bool, optional
    Display curvature. Default `False`.
- **with_connected_vertices** : bool, optional
    Draw lines between distant vertices sharing a voxel. Volumetric data only (raises
    `ValueError` otherwise). Default `False`.
- **cutout** : str
    Name of flatmap cutout with which to clip the full flatmap. Should be the name
    of a sub-layer of the 'cutouts' layer in <filestore>/<subject>/overlays.svg
- **roi_list** : list, optional
    Restrict which ROIs are drawn (by name). `None` draws all.
- **sulci_list** : list
    List of sulci to include
- **overlay_file** : str, optional
    Custom overlays.svg file to use instead of the subject's default.
- **linewidth** : int, optional
    Width of ROI lines. Defaults to roi options in your local `options.cfg`
- **linecolor** : tuple of float, optional
    (R, G, B, A) specification of line color
- **roifill** : tuple of float, optional
    (R, G, B, A) specification for the fill of each ROI region
- **shadow** : int, optional
    Standard deviation of the gaussian shadow. Set to 0 if you want no shadow. **Currently
    non-functional** — any non-`None` value raises `KeyError` (see Issues).
- **labelsize** : str, optional
    Font size for the label, e.g. "16pt"
- **labelcolor** : tuple of float, optional
    (R, G, B, A) specification for the label color
- **curvature_brightness** : float, optional
    Mean brightness of background. 0 = black, 1 = white. `None` defaults to config file
    value.
- **curvature_contrast** : float, optional
    Contrast of curvature. 1 = maximal contrast (black/white), 0 = no contrast.
- **curvature_threshold** : bool, optional
    Whether to apply a threshold to the curvature values to create a binary curvature
    image. `None` defaults to value specified in the config file
- **fig** : figure or ax
    figure into which to plot flatmap. `None` creates a new one; a `Figure` gets a new
    axes added on top (existing axes aren't reused); an `Axes` is drawn into directly.
- **extra_disp** : tuple, optional
    Optional extra display layer from external .svg file: (filename, layer). External svg
    file should be structured exactly as overlays.svg for the subject.
- **extra_hatch** : tuple, optional
    Optional extra crosshatch-textured layer, given as (DataView, [r, g, b]) tuple.
- **colorbar_ticks** : array-like, optional
    For 1D colormaps indicates the ticks of the colorbar. If None, it defaults to equally
    spaced values between vmin and vmax. Not used for 2D colormaps.
- **colorbar_location** : str or tuple, optional
    Location of the colorbar: one of 'left', 'center', 'right' (default 'center'), or a
    tuple of four floats between 0 and 1 indicating (left, bottom, width, height).
- **nanmean** : bool, optional (default = False)
    If True, NaNs in the data will be ignored when averaging across layers.

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
