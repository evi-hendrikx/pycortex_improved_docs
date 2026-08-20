# cortex.volume.mosaic

## Current signature (from source)
```python
def mosaic(data, dim=0, show=True, **kwargs):
```

## Where this is documented today
- Source docstring: [cortex/volume.py:87-100](cortex/volume.py#L87-L100)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.mosaic.html

## Issues with current documentation
- **No Returns section** — returns `(output, (nwide, ntall))`, not documented at all.
- **No Raises section** — raises `ValueError` for `data.ndim` not in `{3, 4}`.
- **`**kwargs`'s forwarding target is unstated** — forwarded to `matplotlib.pyplot.imshow`
  when `show=True` (e.g. `cmap`, `vmin`, `vmax`); not mentioned.
- **RGB(A) handling (`data.dtype == np.uint8`) isn't mentioned in the docstring** — the
  function has a separate code path for `uint8` RGB(A) volumes (assembling an RGBA mosaic
  image) vs. plain scalar data (NaN-padded mosaic); only discoverable by reading the body.
- **4D data's extra dimension isn't explained** — `data.ndim==4` is accepted (per the
  `ValueError` check) but the mosaic-tiling logic operates on `data.shape` generically;
  what a 4th axis represents (e.g. an RGB(A) channel axis vs. a time axis) isn't clarified
  in the docstring itself, only implicit from the `uint8`/shape[3] handling later.

## Fixed documentation

### Summary
Turns volume data into a mosaic, useful for quickly viewing volumetric data with
radiological convention (left side of figure is right side of subject).

### Parameters
- **data** : array_like
    3D volumetric data to mosaic (or 4D with a trailing RGB(A) channel axis of length 3/4,
    dtype `uint8`, for color data).
- **dim** : int
    Dimension across which to mosaic. Default 0.
- **show** : bool
    Display mosaic with matplotlib? Default True.
- **\*\*kwargs**
    Forwarded to `matplotlib.pyplot.imshow` when `show=True` (e.g. `cmap`, `vmin`, `vmax`).

### Returns
- **output** : ndarray, shape (mosaic_height, mosaic_width) or (..., 4) for RGBA input
    The assembled mosaic image, tiled with a 1-pixel black border between slices; NaN-
    padded for scalar (non-`uint8`) input, or zero-alpha-padded for RGB(A) input.
- **(nwide, ntall)** : tuple of int
    Number of tiles across and down the mosaic grid.

### Raises
- `ValueError` — `data.ndim` is not 3 or 4 ("Invalid data shape").

### Notes
No FreeSurfer/FSL dependency; requires matplotlib if `show=True`.

### Example
```python
import numpy as np
import cortex

vol = np.random.randn(30, 100, 100)
mosaic_img, (nwide, ntall) = cortex.volume.mosaic(vol, dim=0, cmap="gray")
```

## Confidence / open questions
- **Recommendation for maintainers:** add a Returns section documenting the `(output,
  (nwide, ntall))` tuple and the RGB(A)-vs-scalar dtype branching.
