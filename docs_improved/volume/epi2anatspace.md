# cortex.volume.epi2anatspace

## Current signature (from source)
```python
def epi2anatspace(volumedata, order=1):
```

## Where this is documented today
- Source docstring: [cortex/volume.py:211-225](cortex/volume.py#L211-L225)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.epi2anatspace.html

## Issues with current documentation
- **`volumedata`'s type is stated as "VolumeData"** but the function actually accepts
  anything `cortex.dataset.normalize` can coerce (including raw tuples) — not just a
  `VolumeData`/`Volume` instance directly.
- **No Raises section.**
- **`order`'s description ("0 is nearest, 1 is linear") doesn't mention higher orders are
  accepted** (`scipy.ndimage.affine_transform`'s spline order, 0-5) or that values > 1 can
  produce out-of-range interpolated values (same caveat noted for `get_aseg_mask`'s
  `order`, not cross-referenced here).
- **Uses a deprecated scipy import path**: `from scipy.ndimage.interpolation import
  affine_transform` — `scipy.ndimage.interpolation` is a deprecated shim; the function is
  now available directly as `scipy.ndimage.affine_transform`. Likely still works on
  current scipy (the shim remains for backward compatibility as of recent scipy versions)
  but is worth flagging as using a deprecated import path — see `_notes.md`.

## Fixed documentation

### Summary
Resample an epi volume data into anatomical space using scipy.

### Parameters
- **volumedata** : VolumeData (or anything `cortex.dataset.normalize` accepts, e.g. a
  `Volume`)
    The input epi volumedata object.
- **order** : int, optional
    The order of the resampler, in terms of splines. 0 is nearest, 1 is linear (accepts
    0-5, per `scipy.ndimage.affine_transform`'s `order`; values > 1 are not generally
    recommended for mask-like data, as with similar `order` parameters elsewhere in
    pycortex — see `utils/get_aseg_mask.md`).

### Returns
- **anatspace** : ndarray
    The ND array of the anatomy space data. Out-of-bounds voxels are filled with `NaN`.

### Raises
Propagates errors from `cortex.database.Database.get_anat`/`get_xfm` if the subject/
transform embedded in `volumedata` are invalid.

### Notes
- No FreeSurfer/FSL/GUI dependency — pure scipy resampling.
- Uses the deprecated `scipy.ndimage.interpolation.affine_transform` import path rather
  than `scipy.ndimage.affine_transform` directly (a compatibility shim, not necessarily
  broken on current scipy, but worth updating — see `_notes.md`).

### Example
```python
import cortex

vol = cortex.Volume.random("S1", "fullhead")
anat_space_data = cortex.volume.epi2anatspace(vol)
```

## Confidence / open questions
- Did not verify against the newest scipy release whether
  `scipy.ndimage.interpolation.affine_transform` has been fully removed — treated as a
  "deprecated but likely still present" import based on general scipy deprecation
  practice, not independently confirmed by testing against multiple scipy versions.
- **Recommendation for maintainers:** update the import to `scipy.ndimage.affine_transform`
  directly; add a Raises section.
