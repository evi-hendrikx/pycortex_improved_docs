# cortex.dataset.VertexRGB (cortex.VertexRGB)

## Current signature (from source)
```python
class VertexRGB(DataviewRGB):
    def __init__(
        self,
        red: Union[npt.NDArray, Vertex],
        green: Union[npt.NDArray, Vertex],
        blue: Union[npt.NDArray, Vertex],
        subject: Optional[str] = None,
        alpha: Optional[Union[npt.NDArray, Vertex]] = None,
        description: str = "",
        state=None,
        channel1color=Colors.Red,
        channel2color=Colors.Green,
        channel3color=Colors.Blue,
        max_color_value=None,
        max_color_saturation=1.0,
        vmin=None,
        vmax=None,
        autorange="individual",
        priority=1,
    ):
```
Surface-space counterpart to `VolumeRGB` (see `VolumeRGB.md` — same base class
`DataviewRGB`, same fast-path/remap-path behavior). This file covers what differs.

## Where this is documented today
- Source docstring: [cortex/dataset/viewRGB.py:657-723](cortex/dataset/viewRGB.py#L657-L723)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.VertexRGB.html

## Issues with current documentation
- **Parameter naming inconsistency vs. `VolumeRGB`**: `VolumeRGB` names its first three
  positional parameters `channel1`/`channel2`/`channel3`; `VertexRGB` instead names them
  `red`/`green`/`blue` directly. Both accept the same `channel1color`/`channel2color`/
  `channel3color` styling parameters (still named `channel*color`, **not** `red_color`
  etc., despite the positional args now being called `red`/`green`/`blue`) — this
  cross-class inconsistency (channel-number-named args paired with color-named args in one
  class, color-named args paired with channel-number-named styling params in the other)
  isn't itself wrong, but is easy to trip over if you're used to one class and switch to the
  other. Not documented/cross-referenced anywhere.
- Same fast-path/remap-path undocumented behavior as `VolumeRGB` (identical logic, see
  `VolumeRGB.md`).
- Same `state` `"TODO: describe what this is"` placeholder.
- Same `.alpha`-recomputed-on-every-access behavior (here operating on `.data`/`.vertices`
  shapes instead of `.volume`).
- **`.left`/`.right` properties here differ subtly from `Vertex.left`/`Vertex.right`**:
  `VertexRGB.left`/`.right` slice `self.vertices` (the already-colormapped `(t, v, 4)` RGBA
  array), not the raw per-channel data — i.e. `vertex_rgb.left` gives you left-hemisphere
  **colors**, not left-hemisphere channel values (for that, use
  `vertex_rgb.red.left`/`.green.left`/`.blue.left` on the underlying `Vertex` channels).
  This is a meaningful semantic difference from plain `Vertex.left`/`.right` and is
  undocumented (no docstring on either property at all).
- No Returns/Raises/Examples sections, same as `VolumeRGB`.

## Fixed documentation

### Summary
Contains RGB(A) colors for each vertex, the surface-space counterpart to `VolumeRGB` (same
fast-path/remap-path behavior — see `VolumeRGB.md`).

### Parameters
- **red**, **green**, **blue** : ndarray or `cortex.Vertex`
    The three data channels. If `Vertex` objects, must share `.subject`.
- **subject** : str, optional
    Required only when channels are raw arrays.
- **alpha** : ndarray or `cortex.Vertex`, optional
    Per-vertex alpha. `None` → fully opaque; resolved lazily via `.alpha`.
- **description** : str, default `""`
- **state** : optional — undocumented in source.
- **channel1color**, **channel2color**, **channel3color** : 3-tuple of int (0-255), default
  red/green/blue — target colors used only on the remap path (note naming mismatch with
  the positional `red`/`green`/`blue` params — see Issues).
- **max_color_value**, **max_color_saturation** : float in [0, 1] — as in `VolumeRGB`.
- **vmin**, **vmax** : float or 3-tuple of float, optional — as in `VolumeRGB`.
- **autorange** : {'individual', 'shared'}, default `'individual'` — as in `VolumeRGB`.
- **priority** : int, default `1`.

### Returns
N/A for `__init__`.

### Raises
Same categories as `VolumeRGB` (`TypeError` for mismatched channel types/subjects,
`ValueError` for shape mismatches or invalid `autorange`).

### Public methods and properties (inherited from `DataviewRGB`, plus own)
- **`.alpha`** (property, get/set) : `Vertex` — as in `VolumeRGB.alpha`, recomputed on
  every access.
- **`.vertices`** (property) : ndarray, shape `(t, v, 4)`, dtype `uint8` — the full RGBA
  per-vertex color array.
- **`.left`** / **`.right`** (properties) : ndarray, shape `(t, v_hemi, 4)` — slices of
  `.vertices` (already-colormapped RGBA), **not** the underlying channel data (see Issues).
  **No docstring in source.**
- **`.raw`** (property) → `self` — no-op, as in `VolumeRGB`.
- **`.name`** (property) : str — content hash of `.vertices`.
- **`.to_json(simple=False)`** — as in `VolumeRGB`, plus (when `simple=True`) `split`
  (left-hemisphere vertex count) and `frames`.
- **`.blend_curvature`** — attached from `VertexData.blend_curvature` (same "hacky
  inheritance" as `Vertex2D`; see `Vertex.md`) — **deprecated**.
- **`.uniques(collapse=False)`** — as in `VolumeRGB`.
- **`__repr__`** — e.g. `<RGB vertex data for (S1)>`.

### Notes
- No FreeSurfer/FSL/GUI dependency.
- Same fast-path/remap-path caveat as `VolumeRGB` — see that file for the full explanation
  of when raw R/G/B values are used directly vs. normalized/recombined.

### Example
```python
import numpy as np
import cortex

subject = "S1"
left, right = cortex.db.get_surf(subject, "fiducial")
nverts = len(left[0]) + len(right[0])

r = np.random.rand(nverts)
g = np.random.rand(nverts)
b = np.random.rand(nverts)

vtx_rgb = cortex.VertexRGB(r, g, b, subject, autorange="individual")
cortex.quickflat.make_png("example_vertexrgb.png", vtx_rgb)
```

## Confidence / open questions
- Same caveats as `VolumeRGB.md` regarding the fast-path/remap-path logic and unvalidated
  tuple lengths for `vmin`/`vmax` (shared implementation via `DataviewRGB.color_voxels`).
- **Recommendation for maintainers:** align parameter naming between `VolumeRGB`
  (`channel1`/`channel2`/`channel3`) and `VertexRGB` (`red`/`green`/`blue`) — or at least
  cross-reference the difference in both docstrings; document that `.left`/`.right` on
  `VertexRGB` return colors, not raw channel values, since this differs from plain `Vertex`.
