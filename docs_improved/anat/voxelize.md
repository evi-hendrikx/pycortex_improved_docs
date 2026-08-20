# cortex.anat.voxelize

## Current signature (from source)
```python
def voxelize(outfile, subject, surf='wm', mp=True):
```

## Where this is documented today
- Source docstring: `'''Voxelize the whitematter surface to generate the white matter
  mask'''` (one line). [cortex/anat.py:71-85](cortex/anat.py#L71-L85)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.anat.voxelize.html

## Issues with current documentation
- **The one-line docstring hardcodes "whitematter" despite `surf` being a general
  parameter** — the function voxelizes whichever named surface you pass (`surf='wm'` is
  just the default), e.g. `surf='pia'` works equally well; the docstring doesn't mention
  `surf` is configurable at all.
- **No Parameters/Returns/Raises sections.**
- **`mp` (multiprocessing toggle, forwarded to `cortex.polyutils.voxelize`) is completely
  undocumented** — not mentioned anywhere.
- **Both hemispheres are voxelized and combined (via `+=` on a boolean array) but this
  isn't stated** — `db.get_surf(subject, surf, nudge=False)` yields one `(pts, polys)` pair
  per hemisphere, and the loop accumulates a mask across both.
- **Return value is undocumented and its axis order relative to the saved file is a
  potential gotcha**: the function returns `vox.T` (transposed) while saving
  `nibabel.Nifti1Image(vox, ...)` (untransposed) to `outfile` — the in-memory return value
  and the on-disk file are **not** the same array orientation. Not mentioned anywhere.

## Fixed documentation

### Summary
Voxelize the whitematter surface to generate the white matter mask (or, more generally,
voxelizes any named surface into a binary volume matching the subject's raw anatomical
image grid).

### Parameters
- **outfile** : str
    Path to write the voxelized mask NIfTI image to.
- **subject** : str
    Subject identifier; must exist in the pycortex database.
- **surf** : str, optional
    Name of the surface to voxelize (e.g. `'wm'`, `'pia'`). Default `'wm'`.
- **mp** : bool, optional
    Whether to use multiprocessing in the underlying `cortex.polyutils.voxelize` call.
    Default `True`.

### Returns
- **vox** : ndarray of bool, shape matching the raw anatomical image, **transposed**
  relative to what's written to `outfile` (the saved NIfTI file is untransposed;
  `nib.affine`/`nib.header` come from the subject's raw anatomical image). Voxels inside
  either hemisphere's surface are `True`.

### Raises
Propagates anything raised by `cortex.database.Database.get_surf`/`get_anat` (e.g. missing
surface/anatomical data for `subject`) or `cortex.polyutils.voxelize`.

### Notes
- No FreeSurfer/FSL/GUI dependency beyond the subject already having the requested `surf`
  and a raw anatomical image in the pycortex database.
- Both hemispheres are voxelized and combined into one mask.
- The returned array and the saved file are transposed relative to each other — if you use
  the return value directly (rather than reloading `outfile`), account for this.

### Example
```python
import cortex

# Requires subject "S1" with wm surfaces and a raw anatomical image in the database.
vox = cortex.anat.voxelize("S1_wm_voxelized.nii.gz", "S1", surf="wm")
print(vox.shape, vox.dtype)  # transposed relative to the saved file
```

## Confidence / open questions
- The transpose discrepancy between the return value and the saved file is confirmed by
  direct reading of `anat.py:82-85` (`nib = nibabel.Nifti1Image(vox, ...); ... return
  vox.T`), not by execution.
- **Recommendation for maintainers:** expand the docstring beyond the current one-liner to
  cover `surf`/`mp`/return value; consider returning the same orientation as what's saved
  to avoid the transpose trap.
