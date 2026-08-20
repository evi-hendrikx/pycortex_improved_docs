# cortex.dataset.VolumeRGB (cortex.VolumeRGB)

## Current signature (from source)
```python
class VolumeRGB(DataviewRGB):
    def __init__(
        self,
        channel1: Union[npt.NDArray, Volume],
        channel2: Union[npt.NDArray, Volume],
        channel3: Union[npt.NDArray, Volume],
        subject: Optional[str] = None,
        xfmname: Optional[str] = None,
        alpha: Optional[Union[npt.NDArray, Volume]] = None,
        description: str = "",
        state=None,
        channel1color: Color = Colors.Red,
        channel2color: Color = Colors.Green,
        channel3color: Color = Colors.Blue,
        max_color_value: Optional[float] = None,
        max_color_saturation: float = 1.0,
        vmin: Optional[Union[float, tuple]] = None,
        vmax: Optional[Union[float, tuple]] = None,
        autorange: str = "individual",
        priority: int = 1,
    ):
```
`VolumeRGB` inherits from `DataviewRGB` (in `cortex/dataset/viewRGB.py`), the shared base
for `VolumeRGB`/`VertexRGB`, which itself provides the important `color_voxels` static
method used whenever channel colors are remapped away from pure R/G/B.

## Where this is documented today
- Source docstrings:
  - `VolumeRGB.__init__`: [cortex/dataset/viewRGB.py:356-425](cortex/dataset/viewRGB.py#L356-L425)
  - `DataviewRGB.color_voxels` (static method, the real remapping logic):
    [cortex/dataset/viewRGB.py:163-229](cortex/dataset/viewRGB.py#L163-L229) — unusually,
    this one is actually **well-documented** (full NumPy-style Parameters/Returns),
    a positive counterexample worth noting for maintainers as the standard other
    docstrings in this module should be brought up to.
  - `Colors` (named RGB presets): [cortex/dataset/viewRGB.py:23-34](cortex/dataset/viewRGB.py#L23-L34)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.VolumeRGB.html

## Issues with current documentation
- **`state` parameter documented only as `"TODO: describe what this is"`** — a literal
  placeholder left in the shipped docstring.
- **The "fast path vs. remap path" behavior is not documented at all.** When
  `channel1color/2/3color` are left at their R/G/B defaults *and* `vmin`/`vmax` are both
  `None` *and* `autorange="individual"`, the three channels are used **directly** as
  red/green/blue `Volume` data (no scaling/remapping — i.e. `channel1` values become the
  literal `Volume`'s data, expected already-suitable e.g. `uint8` or already `0-255`-ish
  values for meaningful display). If **any** of those conditions don't hold, the channels
  instead go through `DataviewRGB.color_voxels`, which normalizes each channel to `[0,1]`
  using `vmin`/`vmax` (or auto-computed percentiles per `autorange`), remaps to the given
  channel colors, and combines them in HSV space. These are two **very different**
  numerical treatments of the input data, silently selected by which optional arguments you
  happen to pass — a user who passes `vmin=0` "just to be explicit" gets fundamentally
  different (color-remapped, normalized) output than one who passes nothing at all (raw
  passthrough). This is the single most consequential undocumented behavior in this class.
- **`vmin`/`vmax` docstrings say "single float" or "tuple of three floats"** but don't state
  what happens with a 2-tuple or a tuple of the wrong length (based on the code,
  `channel_vmins = [float(v) for v in vmin]` — a non-length-3 iterable produces a
  `channel_vmins` list of the wrong length, which will misalign with the three channels
  downstream, likely producing wrong colors silently rather than raising — see
  `_notes.md`).
- **`autorange="individual"` is the documented default but the two options ("shared" vs.
  "individual") are described in `color_voxels`'s docstring but not cross-referenced from
  `VolumeRGB`'s own docstring** at all — `VolumeRGB.__init__`'s own Parameters section for
  `autorange` just says "Default is 'individual'" without explaining what the two modes do
  (that detail exists only in the separate `color_voxels` docstring).
- **No Returns/Raises sections** on `__init__` (n/a) or on `.alpha` (property, has a
  one-line docstring "Compute alpha transparency" only), `.volume` (has a partial docstring
  but no Raises), `.to_json`.
- **No Examples section** anywhere.
- **`.alpha` property has real, non-obvious side effects** on every access: if `_alpha` is
  `None`, it constructs and returns a fully-opaque `Volume`; if a raw non-`Volume` array,
  it wraps it in a `Volume(..., vmin=0, vmax=1)` (with a `Warning` if values fall outside
  `[0,1]` for non-`uint8` arrays); and **on every access** it recomputes a NaN mask across
  `red`/`green`/`blue` and forces `alpha.volume[mask] = alpha.vmin` there — i.e. `.alpha` is
  not a cached/static property, it's recomputed (and can therefore be moderately expensive
  for large volumes) every single time it's read. None of this is documented.
- **`channel1color`/`channel2color`/`channel3color` accept `Color` = `tuple[int, int, int]`
  in [0, 255]** (see the `Colors` class for presets) but the docstring's type annotation
  "`tuple<uint8, uint8, uint8>`" is non-standard/non-NumPy-style notation that a reader may
  not immediately parse as "three ints, each 0-255."
- **`max_color_value`/`max_color_saturation` semantics are somewhat opaque** even reading
  `color_voxels`'s (better) docstring — they scale the resulting color's HSV value/
  saturation channels, but there's no worked example anywhere showing what visually changes
  when these are tuned.

## Fixed documentation

### Summary
Contains RGB(A) colors for each voxel, built from three data channels either passed
through directly or remapped/combined through HSV color mixing (see Notes).

### Parameters
- **channel1**, **channel2**, **channel3** : ndarray or `cortex.Volume`
    The three data channels. If `Volume` objects, must share `.subject` (and `.xfmname`
    with `alpha`, if `alpha` is also a `Volume`). If raw arrays, `subject`/`xfmname` are
    required.
- **subject**, **xfmname** : str, optional
    Required only when channels are raw arrays.
- **alpha** : ndarray or `cortex.Volume`, optional
    Per-voxel alpha. `None` → fully opaque. Resolved lazily — see `.alpha` property.
- **description** : str, default `""`
- **state** : optional
    Opaque viewer-state value; format undocumented in source.
- **channel1color**, **channel2color**, **channel3color** : 3-tuple of int (0-255), default
  red/green/blue
    Target display color for each channel, used only on the "remap" path (see Notes).
    Presets available in `cortex.dataset.viewRGB.Colors`.
- **max_color_value** : float in [0, 1], optional
    Caps HSV brightness of combined colors. `None` defaults to the average channel color's
    value.
- **max_color_saturation** : float in [0, 1], default `1.0`
    Caps HSV saturation of combined colors.
- **vmin**, **vmax** : float or 3-tuple of float, optional
    Per-channel bounds mapping to 0/255. A single float applies to all channels; a 3-tuple
    gives per-channel bounds. Any non-`None` value forces the "remap" path (see Notes).
- **autorange** : {'individual', 'shared'}, default `'individual'`
    How auto-bounds are computed when `vmin`/`vmax` are `None`: per-channel percentiles, or
    pooled across all three channels.
- **priority** : int, default `1`
    Display-order priority.

### Returns
N/A for `__init__`.

### Raises
- `TypeError` — inconsistent types across `channel1`/`channel2`/`channel3` (mixing `Volume`
  and raw array); mismatched `.subject` among `Volume` channel args; missing
  `subject`/`xfmname` when raw arrays are given.
- `ValueError` — differing `.xfmname` across `red`/`green`/`blue`/`alpha` once resolved
  ("Cannot handle different transforms per volume"); shape mismatch among the three
  channels (raised inside `color_voxels`, "Volumes are of different shapes"); invalid
  `autorange` value not in `{'shared', 'individual'}`.
- `UserWarning` (not an exception) — via `warnings.warn`, if a channel's `vmin == vmax`
  (that channel is zeroed out), or via the `.alpha` property if a non-`Volume` alpha array
  has values outside `[0, 1]`.

### Public methods and properties (inherited from `DataviewRGB`, plus own)
- **`.alpha`** (property, get/set) : `Volume` — resolves/normalizes the alpha channel on
  every access (see Issues — not cached, and applies a NaN mask across R/G/B automatically).
  Setting `.alpha = ...` stores the raw value in `._alpha` for later resolution.
- **`.volume`** (property) : ndarray, shape `(t, z, y, x, 4)`, dtype `uint8` — the full RGBA
  volume, each of R/G/B/A independently normalized to `uint8` (using each channel's own
  `vmin`/`vmax` if set, else auto-scaled from the data's own min/max).
- **`.raw`** (property) → `self` — `VolumeRGB` is already "raw" (no further colormapping
  needed), so `.raw` is a no-op returning the same object.
- **`.name`** (property) : str — content hash of `.volume` (note: different hashing input
  than `Volume.name`, which hashes `.data` — `.volume` here is already the expanded/
  normalized RGBA array).
- **`.to_json(simple=False)`** — JSON metadata; always reports `vmin=[0]`/`vmax=[0]`-style
  fixed `0-255` range regardless of the constituent channels' own ranges (since the data is
  already color-mapped).
- **`.get_cmapdict()`** → `{}` (empty dict — RGB data has no single colormap).
- **`.uniques(collapse=False)`** — yields `red`, `green`, `blue` (and `alpha`, if set)
  individually unless `collapse=True`, in which case yields `self` as a single unit.
- **`DataviewRGB.color_voxels(...)`** (static method) — the underlying per-voxel color
  remapping/combination logic; already well-documented in source (see "Where this is
  documented today"); callable directly if you want the raw R/G/B/A arrays without
  constructing a `VolumeRGB`.
- **`__repr__`** — e.g. `<RGB volumetric data for (S1, fullhead)>`.

### Notes
- **Fast path vs. remap path** (see Issues above) — this is the most important behavior to
  understand before using this class: pass literal R/G/B `Volume`s with no color/range
  arguments for a direct passthrough; pass any of `channel*color`, `vmin`, `vmax`, or a
  non-`'individual'` `autorange` to trigger normalized HSV-based color remapping instead.
- No FreeSurfer/FSL/GUI dependency.
- `.alpha` recomputes on every access — for performance-sensitive code accessing `.alpha`
  repeatedly on a large volume, consider caching the result yourself.

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
shape = cortex.db.get_xfm(subject, xfm).shape

# "Remap" path: three independent measures, auto-ranged and combined in HSV space.
c1 = np.random.rand(*shape)
c2 = np.random.rand(*shape)
c3 = np.random.rand(*shape)

vol_rgb = cortex.VolumeRGB(
    c1, c2, c3, subject, xfm,
    autorange="individual",
)
cortex.quickflat.make_png("example_volumergb.png", vol_rgb)
```

## Confidence / open questions
- The "fast path vs. remap path" distinction is confirmed by direct reading of
  `viewRGB.py:476-549` (the `if (channel1color == Colors.Red) and ... and vmin is None and
  vmax is None and autorange == "individual":` branch), not by execution.
- Could not determine from source/tests what a non-length-3 `vmin`/`vmax` tuple actually
  does downstream beyond the initial `[float(v) for v in vmin]` conversion (likely a
  broadcasting error or silent misalignment later in `color_voxels`) — flagged as
  unconfirmed; recommend maintainers add explicit length validation.
- **Recommendation for maintainers:** this class's single most valuable documentation fix
  would be explicitly calling out the fast-path/remap-path fork in the docstring's opening
  paragraph, since it silently changes the numeric interpretation of the input data; also
  replace the `state` `"TODO"` placeholder; add length validation (and a clear error
  message) for non-3-length `vmin`/`vmax` tuples.
