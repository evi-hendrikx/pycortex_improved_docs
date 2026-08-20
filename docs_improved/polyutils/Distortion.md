# cortex.polyutils.Distortion

## Current signature (from source)
```python
class Distortion(object):
    def __init__(self, flat, ref, polys):
```

## Where this is documented today
- Source docstring: [cortex/polyutils/distortion.py:5-21](cortex/polyutils/distortion.py#L5-L21)
  (class + both properties are fully documented — one of the best-documented classes found
  in this codebase).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.polyutils.Distortion.html

## Issues with current documentation
- **No Raises section** for either property (e.g. mismatched `flat`/`ref`/`polys` shapes
  will surface as low-level numpy broadcasting errors, not a clear message).
- **No Examples section.**
- **No cross-reference to `cortex.surfinfo.distortion`**, the higher-level function that
  actually generates and caches per-subject distortion `.npz` files using this class —
  users are more likely to encounter `cortex.surfinfo.distortion` first.

## Fixed documentation

### Summary
Used to compute distortion metrics between fiducial and another (e.g. flat) surface.

### Parameters
- **flat** : 2D ndarray, shape (total_verts, 3)
    Location of each vertex in flatmap space.
- **ref** : 2D ndarray, shape (total_verts, 3)
    Location of each vertex in fiducial (reference) space.
- **polys** : 2D ndarray, shape (total_polys, 3)
    Triangle vertex indices in both `flat` and `ref`.

### Public methods and properties
- **`.areal`** (property) → 1D ndarray, shape (total_verts,)
    Compute areal distortion of the flatmap. Areal distortion is calculated at each
    triangle as the log2 ratio of the triangle area in the flatmap to the area in the
    reference surface. Distortion values are then resampled onto the vertices. A value of
    0 indicates equal areas (no distortion); +1 indicates the flatmap area is 2x the
    reference (expansion); -1 indicates the flatmap area is 1/2x the reference
    (compression). See:
    http://brainvis.wustl.edu/wiki/index.php/Caret:Operations/Morphing
- **`.metric`** (property) → 1D ndarray, shape (total_verts,)
    Compute metric distortion of the flatmap. Calculated as the difference in squared
    distance from each vertex to its neighbors between the flatmap and the reference.
    Positive values mean vertices are farther from their neighbors in the flatmap than in
    the reference (expansion). See: Fischl, Sereno, and Dale, 1999.

### Returns
See per-property entries above.

### Raises
Not validated — mismatched shapes between `flat`, `ref`, and `polys` will surface as
low-level `numpy` broadcasting/indexing errors.

### Notes
- No FreeSurfer/FSL/GUI dependency.
- `.metric` requires `networkx` (imported lazily).
- `cortex.surfinfo.distortion` is the higher-level, cached, per-subject entry point that
  constructs and uses this class — most users will want that function instead of
  constructing `Distortion` directly.

### Example
```python
import cortex

subject = "S1"
(flat_pts, flat_polys), _ = cortex.db.get_surf(subject, "flat")
(fid_pts, fid_polys), _ = cortex.db.get_surf(subject, "fiducial")

dist = cortex.polyutils.Distortion(flat_pts, fid_pts, flat_polys)
areal_distortion = dist.areal
metric_distortion = dist.metric
```

## Confidence / open questions
- **Recommendation for maintainers:** add a cross-reference to `cortex.surfinfo.distortion`
  from this class's docstring, since that's the more commonly used entry point.
