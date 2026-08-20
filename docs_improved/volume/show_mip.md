# cortex.volume.show_mip

## Current signature (from source)
```python
def show_mip(data, **kwargs):
```

## Where this is documented today
- Source docstring: `'''Display a maximum intensity projection for the data, using three
  subplots'''` (one line). [cortex/volume.py:186-193](cortex/volume.py#L186-L193)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.show_mip.html

## Issues with current documentation
- **No Parameters/Returns/Raises sections.**
- **`**kwargs` forwarding target unstated** — forwarded directly to
  `matplotlib.axes.Axes.imshow` for all three subplots identically.
- **No explanation of which axis each of the three subplots projects along** — `data.max(0)`,
  `.max(1)`, `.max(2)` fill subplot positions 221, 222, 223 respectively (no subplot for a
  4th combined view; position 224 is left empty).
- **`data`'s expected shape/type isn't stated** — a plain 3D ndarray (not a `Volume`/
  `Dataview` — unlike most of this module's other functions, `show_mip` does not call
  `cortex.dataset.normalize`).

## Fixed documentation

### Summary
Display a maximum intensity projection for the data, using three subplots — one for each
axis's max-intensity projection.

### Parameters
- **data** : ndarray, shape (z, y, x)
    3D volumetric data (a plain ndarray, not a `Volume`/`Dataview` — this function does
    not call `cortex.dataset.normalize`).
- **\*\*kwargs**
    Forwarded to `matplotlib.axes.Axes.imshow` for all three subplots (e.g. `cmap`,
    `vmin`, `vmax`).

### Returns
- **fig** : `matplotlib.figure.Figure`
    A 2x2-subplot figure with `data.max(0)` (subplot 221), `data.max(1)` (subplot 222),
    and `data.max(2)` (subplot 223) shown as maximum-intensity projections. The fourth
    subplot position (224) is left empty.

### Raises
Not validated — non-3D `data` will surface as a low-level error from `.max(axis)`/
`imshow`.

### Notes
No FreeSurfer/FSL/GUI dependency beyond matplotlib.

### Example
```python
import numpy as np
import cortex

vol = np.random.randn(30, 100, 100)
fig = cortex.volume.show_mip(vol, cmap="gray")
```

## Confidence / open questions
- **Recommendation for maintainers:** document which axis each subplot projects along;
  add a Returns section.
