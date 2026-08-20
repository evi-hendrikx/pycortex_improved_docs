# cortex.volume.anat2epispace

## Current signature (from source)
```python
def anat2epispace(anatdata, subject, xfmname, order=1):
```
**Scope note**: the design doc's checklist lists `anat2epispace` under both
`cortex.utils` and `cortex.volume`. It is defined only once, here in
`cortex/volume.py` (imported into `cortex.utils` as `from .volume import
anat2epispace`) — documented once, in this file. See `_notes.md`.

## Where this is documented today
- Source docstring: [cortex/volume.py:242-260](cortex/volume.py#L242-L260)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.anat2epispace.html

## Issues with current documentation
- **No Raises section.**
- **`order`'s description ("Order of spline interpolation") doesn't state the valid range
  (0-5) or the same "values > 1 not recommended for mask-like data" caveat** noted
  elsewhere (`get_aseg_mask`, `epi2anatspace`) for the identical parameter — not
  cross-referenced.
- **`db.get_anat(subject)` is called with no `type=` argument**, defaulting to `'raw'`
  (per `Database.get_anat`'s own default) — this function always resamples relative to
  the subject's raw anatomical, not any other anatomical type; not stated.
- **Uses the same deprecated scipy import path** as `epi2anatspace` (`scipy.ndimage.
  interpolation.affine_transform`) — see `epi2anatspace.md`/`_notes.md`.

## Fixed documentation

### Summary
Resamples data from anatomical space into epi space.

### Parameters
- **anatdata** : ndarray
    data in anatomical space, matching the subject's raw anatomical image's shape.
- **subject** : str
    Name of subject
- **xfmname** : str
    Name of transform
- **order** : int, optional
    Order of spline interpolation (0-5, per `scipy.ndimage.affine_transform`). 0 is
    nearest-neighbor; values > 1 aren't generally recommended for mask-like/binary data.

### Returns
- **epidata** : ndarray
    data in EPI space. Out-of-bounds voxels are filled with `NaN`.

### Raises
Propagates errors from `cortex.database.Database.get_anat`/`get_xfm` if `subject`/
`xfmname` are invalid.

### Notes
- Always resamples relative to the subject's **raw** anatomical (`db.get_anat(subject)`,
  no `type=` override available here).
- No FreeSurfer/FSL/GUI dependency — pure scipy resampling.
- Uses the deprecated `scipy.ndimage.interpolation.affine_transform` import path — see
  `epi2anatspace.md`.
- Used internally by `cortex.utils.get_aseg_mask` (when `xfmname` is given) and imported
  directly into `cortex.utils`'s namespace.

### Example
```python
import numpy as np
import cortex

anat = cortex.db.get_anat("S1", "raw")
anat_data = np.asarray(anat.dataobj).T  # matches anat2epispace's expected orientation
epi_data = cortex.volume.anat2epispace(anat_data, "S1", "fullhead")
```

## Confidence / open questions
- Same scipy-import-path caveat as `epi2anatspace.md`.
- **Recommendation for maintainers:** update the scipy import; add a Raises section;
  cross-reference the `order` parameter's shared caveats across the several pycortex
  functions that expose an identical `order` parameter (`get_aseg_mask`, `epi2anatspace`,
  `anat2epispace`).
