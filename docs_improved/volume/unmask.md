# cortex.volume.unmask

## Current signature (from source)
```python
def unmask(mask, data):
```

## Where this is documented today
- Source docstring: [cortex/volume.py:10-33](cortex/volume.py#L10-L33) — already
  reasonably thorough.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.unmask.html

## Issues with current documentation
- **`mask`/`data` types are stated only as "array_like"**, with no shape information —
  the actual accepted shapes (`mask`: boolean, shape `(z, y, x)`; `data`: `(nvox,)`,
  `(t, nvox)`, or an RGB(A) variant with a trailing `(3,)`/`(4,)` channel axis of dtype
  `uint8`) are only discoverable by reading the body.
- **No Raises section** — raises `ValueError` if the number of `True` values in `mask`
  doesn't match `data`'s voxel-count axis; `TypeError` if `data` has a trailing 3/4-length
  axis but isn't `uint8`.
- **The "otherwise returns a MaskedArray" behavior's masked-*where* isn't spelled out**:
  the mask on the returned `MaskedArray` marks voxels **outside** the input `mask` (i.e.
  `~mask`, broadcast across the leading `data` axis) as masked/invalid — worth stating
  explicitly since "masked" could otherwise be misread as marking the *included* voxels.
- **`.squeeze()` on the return value isn't mentioned** — a single-timepoint (`data.shape[0]
  == nvox`, no explicit leading time axis) call collapses any resulting length-1 axes,
  which affects the returned shape in a way not obvious from the docstring.

## Fixed documentation

### Summary
unmask(mask, data)

Unmask the data, assuming it's been masked. Creates a volume the same size as `mask`
containing `data` at the locations where `mask` is True.

If `data` is RGB valued (dtype uint8 and last dim is 3 or 4), the area outside the mask
will be filled with zeros. Otherwise, a numpy MaskedArray will be returned.

### Parameters
- **mask** : ndarray of bool, shape (z, y, x)
    The data mask.
- **data** : ndarray, shape (nvox,), (t, nvox), or with a trailing (3,) / (4,) RGB(A)
  channel axis (dtype uint8)
    Actual MRI data to unmask, where `nvox = mask.sum()`.

### Returns
- **unmasked** : ndarray or `numpy.ma.MaskedArray`
    Volume same size as `mask` but same dtype as `data`. For RGB(A) `uint8` data, an
    ordinary `uint8` array with the region outside `mask` filled with zeros (alpha=0 for
    RGB input). Otherwise, a `MaskedArray` whose mask marks voxels **outside** `mask` (not
    inside) as invalid. Any resulting length-1 leading axes are squeezed out.

### Raises
- `ValueError` — the number of `True` entries in `mask` doesn't match `data`'s voxel-count
  axis ("Invalid mask for the data").
- `TypeError` — `data`'s last axis has length 3 or 4 but `data.dtype != np.uint8`.

### Notes
No FreeSurfer/FSL/GUI dependency — pure numpy.

### Example
```python
import numpy as np
import cortex

mask = np.random.rand(10, 20, 20) > 0.5
data = np.random.randn(mask.sum())
volume = cortex.volume.unmask(mask, data)
print(volume.shape)  # (10, 20, 20), masked outside `mask`
```

## Confidence / open questions
- **Recommendation for maintainers:** state `mask`/`data`'s real shapes in the docstring
  instead of "array_like"; clarify the masked-array's mask polarity explicitly.
