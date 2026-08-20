# cortex.dataset.Volume2D (cortex.Volume2D)

## Current signature (from source)
```python
class Volume2D(Dataview2D):
    def __init__(
        self,
        dim1: Union[npt.NDArray, Volume],
        dim2: Union[npt.NDArray, Volume],
        subject: Optional[str] = None,
        xfmname: Optional[str] = None,
        description: str = "",
        cmap: Optional[str] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        vmin2: Optional[float] = None,
        vmax2: Optional[float] = None,
        **kwargs,
    ):
```
`Volume2D` inherits from `Dataview2D` (in `cortex/dataset/view2D.py`), the abstract base for
all "two-dimensional colormap" views (data jointly colormapped along two axes, e.g. value +
uncertainty, or value + significance).

## Where this is documented today
- Source docstrings:
  - `Volume2D.__init__`: [cortex/dataset/view2D.py:112-175](cortex/dataset/view2D.py#L112-L175)
  - `Dataview2D` (base, largely undocumented): [cortex/dataset/view2D.py:15-110](cortex/dataset/view2D.py#L15-L110)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.Volume2D.html

## Issues with current documentation
- **`vmin`/`vmax`/`vmin2`/`vmax2` docstrings are literally placeholders**: "If not given
  defaults to TODO:WHAT" — copy-pasted four times verbatim in the source docstring. This is
  the clearest docstring/code drift in the whole `cortex.dataset` module: the actual default
  logic (visible in `__init__`'s body) is well-defined — `vmin`/`vmax` default to `dim1`'s
  own `vmin`/`vmax` (which are themselves 1st/99th percentile if `dim1` was constructed
  from a raw array without explicit bounds), and `vmin2`/`vmax2` default to `dim2`'s.
- **`state` parameter (accepted via `**kwargs` → `Dataview2D.__init__`) has no docstring
  at all** (`Dataview2D.__init__`'s own docstring is entirely missing — the class has zero
  docstring text on `__init__` itself; only the `Volume2D` subclass docstring exists).
- **The "two ways to construct" pattern (raw arrays + subject/xfmname, vs. two `Volume`
  objects) is documented via parameter *type* unions (`ndarray or Volume`) but the actual
  validation rules — that mixing a `Volume` for `dim1` with a raw array for `dim2` raises
  `TypeError`, that `subject`/`xfmname` must be `None` when passing `Volume` objects, that
  both `Volume`s must share the same `.subject` — are not spelled out in prose.**
- **No Returns/Raises sections.**
- **No Examples section.**
- **`.raw` property has a one-line docstring** ("VolumeRGB object containing the colormapped
  data from this object") but doesn't mention it raises `ValueError` if `dim1.xfmname !=
  dim2.xfmname`, nor explain the two different code paths (fast path using masked `.data`
  directly when both dims share an identical mask shape/values, vs. falling back to full
  `.volume` unmasking otherwise).
- **Colormap format (`cmap`) is under-specified for 2D views specifically.** Unlike 1D
  `Volume`/`Vertex` (where `cmap` can be any matplotlib colormap name/instance), `Volume2D`
  (via `Dataview2D._to_raw`) **only** accepts the name of a 2D colormap **image file**
  (`<cmapdir>/<cmap>.png`, read via `plt.imread`) — passing an ordinary 1D matplotlib
  colormap name here will raise a file-not-found-style error, not a graceful validation
  message. This distinction (2D colormaps are literally image files, not
  `matplotlib.colors.Colormap` objects) is not documented anywhere on `Volume2D` or
  `Dataview2D`.
- **Non-perceptually-uniform colormap warning is undocumented as a *feature*.** `.raw`
  triggers `_warn_non_perceptually_uniform_colormap`, which issues a `UserWarning`
  suggesting a perceptually-uniform alternative for a handful of legacy 2D colormap names
  (`BuOr_2D`, `RdBu_covar`, `RdBu_covar2`, `RdBu_covar_alpha`, `RdGn_covar`, `hot_alpha`) —
  useful behavior, not mentioned in any docstring.

## Fixed documentation

### Summary
Contains two 3D volumes for simultaneous visualization, jointly colormapped via a 2D
colormap image.

### Parameters
- **dim1** : ndarray or Volume
    The first volume. Can be a 1D or 3D array (see Volume for details), or a Volume.
- **dim2** : ndarray or Volume
    The second volume. Same rules as `dim1`; mixing an array with a Volume, or a Volume
    with a mismatched subject, raises `TypeError`.
- **subject** : str, optional
    Subject identifier. Must exist in the pycortex database. If not given, dim1 must be a
    Volume from which the subject can be extracted.
- **xfmname** : str, optional
    Transform name. Must exist in the pycortex database. If not given, dim1 must be a
    Volume from which the subject can be extracted.
- **description** : str, optional
    String describing this dataset. Displayed in webgl viewer.
- **cmap** : str, optional
    Name of a 2D colormap **image file**, not a matplotlib colormap (see Issues). If not
    given defaults to the `default_cmap2d` in your pycortex options.cfg file.
- **vmin** : float, optional
    Minimum value in colormap for dim1. If not given defaults to `dim1.vmin` (the shipped
    docstring says "TODO:WHAT" here — see Issues).
- **vmax** : float, optional
    Maximum value in colormap for dim1. If not given defaults to `dim1.vmax`.
- **vmin2** : float, optional
    Minimum value in colormap for dim2. If not given defaults to `dim2.vmin`.
- **vmax2** : float, optional
    Maximum value in colormap for dim2. If not given defaults to `dim2.vmax`.
- **\*\*kwargs**
    All additional arguments in kwargs are passed to the VolumeData and Dataview.

### Returns
N/A for `__init__`.

### Raises
- `TypeError` — `subject`/`xfmname` given together with `Volume` objects for `dim1`/`dim2`;
  `dim2` not matching `dim1`'s type-category (`Volume` vs. raw array); mismatched
  `.subject` between two `Volume` args for `dim1`/`dim2`; `subject`/`xfmname` missing when
  raw arrays are given.
- `ValueError` (on `.raw` access) — `dim1.xfmname != dim2.xfmname`.
- File/lookup errors (from `plt.imread`) if `cmap` doesn't correspond to an existing 2D
  colormap PNG.

### Public methods and properties (inherited from `Dataview2D`)
- **`.raw`** (property) → `VolumeRGB` — the two channels jointly colormapped into RGBA.
  Uses per-pixel/voxel `.data` directly when both dims are identically masked (fast path),
  else falls back to full `.volume` arrays. Alpha defaults to opaque unless `'alpha'` is
  present in `self.attrs`, and NaN in either channel yields alpha=0.
- **`.xfmname`** (property) : str — proxies `self.dim1.xfmname`.
- **`.subject`** (property, from `Dataview2D`) : str — proxies `self.dim1.subject`.
- **`.uniques(collapse=False)`** — generator yielding `self.dim1`, `self.dim2` (or, if
  `collapse=True`, behavior inherited from base — see `_notes.md` for a discrepancy noted
  between `Dataview2D.uniques` and `DataviewRGB.uniques`'s handling of `collapse`).
- **`.save(...)` / HDF I/O** — via `Dataview._write_hdf`/`to_json` (internal; not typically
  called directly by users — used by `Dataset.save`).
- **`__repr__`** — e.g. `<2D volumetric data for (S1, fullhead)>`.

### Notes
- No FreeSurfer/FSL/GUI dependency for construction.
- `.raw` performs the actual colormap image lookup/read (`plt.imread`) and can issue a
  `UserWarning` for a short list of legacy non-perceptually-uniform 2D colormap names,
  suggesting a `PU_*`-prefixed perceptually-uniform alternative.
- Not to be confused with `VolumeRGB` (3+ explicit color channels, no 2D-colormap-image
  lookup) — `Volume2D` is specifically for the "two continuous quantities jointly
  colormapped via an image-based 2D LUT" use case.

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
shape = cortex.db.get_xfm(subject, xfm).shape

value = np.random.randn(*shape)          # e.g. an effect size
confidence = np.random.rand(*shape)      # e.g. 0-1 confidence/significance

v2d = cortex.Volume2D(
    value, confidence, subject, xfm,
    vmin=-2, vmax=2,      # color range for `value`
    vmin2=0, vmax2=1,     # range for `confidence`
    cmap="RdBu_covar",    # a 2D colormap image shipped with pycortex
)
cortex.quickflat.make_png("example_volume2d.png", v2d)
```

## Confidence / open questions
- Could not confirm from source alone the full list of 2D colormap `.png` files shipped by
  default with a pycortex install (they live under the `[webgl] colormaps` config
  directory, populated at install time) — the names used in the example (`"RdBu_covar"`)
  are taken from `_warn_non_perceptually_uniform_colormap`'s mapping table in
  `view2D.py:293-304`, which implies they exist, but this was not independently verified
  against an actual installed colormap directory in this pass.
- **Recommendation for maintainers:** replace the four `TODO:WHAT` placeholders in the
  docstring with the actual default-resolution logic (from `dim1`/`dim2`); document that
  `cmap` for 2D views means an image file, not a matplotlib colormap object/name, since this
  is a meaningful behavioral difference from `Volume`/`Vertex`'s `cmap` parameter that could
  otherwise cause a confusing failure.
