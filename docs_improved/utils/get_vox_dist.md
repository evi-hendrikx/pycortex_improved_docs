# cortex.utils.get_vox_dist

## Current signature (from source)
```python
def get_vox_dist(subject, xfmname, surface="fiducial", max_dist=np.inf):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:343-366](cortex/utils.py#L343-L366)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_vox_dist.html

## Issues with current documentation
- **`surface` parameter is entirely missing from the docstring's `Parameters` section**,
  despite being a real, named parameter in the signature — only `subject`, `xfmname`, and
  `max_dist` are documented.
- **No Raises section.**
- **`argdist`'s meaning ("index of the closest point on the surface") doesn't say whether
  the index is into the merged (both-hemisphere) or per-hemisphere vertex array** — it's
  into the merged array, from `db.get_surf(subject, surface, merge=True)`, which isn't
  stated.

## Fixed documentation

### Summary
Get the distance (in mm) from each functional voxel to the closest point on the surface.

### Parameters
- **subject** : str
    Name of the subject
- **xfmname** : str
    Name of the transform
- **surface** : str, optional
    Name of the surface to measure distance to (e.g. `'fiducial'`, `'wm'`, `'pia'`).
    Default `'fiducial'`.
- **max_dist** : nonnegative float, optional
    Limit computation to only voxels within `max_dist` mm of the surface. Makes
    computation orders of magnitude faster for high-resolution volumes.

### Returns
- **dist** : ndarray (z, y, x)
    Array with the same shape as the reference image of `xfmname` containing the distance
    (in mm) of each voxel to the closest point on the surface.
- **argdist** : ndarray (z, y, x)
    Array with the same shape as the reference image of `xfmname` containing, for each
    voxel, the index of the closest point on the surface — an index into the merged
    (both-hemisphere) vertex array returned by `cortex.db.get_surf(subject, surface,
    merge=True)`.

### Raises
Propagates errors from `cortex.database.Database.get_surf`/`get_xfm` if `subject`/
`xfmname`/`surface` are invalid.

### Notes
- No FreeSurfer/FSL/GUI dependency.
- With `max_dist=np.inf` (default), every voxel gets a real distance/index — potentially
  slow for high-resolution volumes; setting a finite `max_dist` skips distant voxels
  (their `argdist` becomes an out-of-range sentinel index from `cKDTree.query`'s
  `distance_upper_bound` behavior — not returned as NaN).

### Example
```python
import cortex

dist, argdist = cortex.utils.get_vox_dist("S1", "fullhead", surface="wm", max_dist=10)
```

## Confidence / open questions
- Did not independently verify the exact sentinel value `cKDTree.query` returns for
  voxels beyond `distance_upper_bound` in this pass (scipy convention: `dist=inf`,
  `argdist=tree.n`, i.e. one past the last valid index) — stated based on general scipy
  `cKDTree.query` documentation, not re-derived from pycortex-specific testing.
- **Recommendation for maintainers:** add `surface` to the docstring's `Parameters`
  section (currently missing entirely); document the out-of-range sentinel behavior for
  voxels beyond `max_dist`.
