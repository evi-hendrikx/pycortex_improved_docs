# cortex.surfinfo.distortion

## Current signature (from source)
```python
def distortion(outfile, subject, dist_type='areal', smooth=20):
```

## Where this is documented today
- Source docstring: [cortex/surfinfo.py:40-64](cortex/surfinfo.py#L40-L64)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.surfinfo.distortion.html

## Issues with current documentation
- **No Returns section.**
- **No Raises section** — `dist_type` isn't validated up front; an invalid value raises
  `AttributeError` from `getattr(polyutils.Distortion(...), dist_type)`, not a clear
  message.
- **Not cross-referenced to `cortex.polyutils.Distortion`**, the class that actually
  implements `'areal'`/`'metric'` (this function's docstring duplicates
  `Distortion.areal`/`.metric`'s explanations rather than pointing to them).
- **Not documented as the auto-generation target of `cortex.db.get_surfinfo(subject,
  type="distortion")`**, same gap as `curvature`.

## Fixed documentation

### Summary
Compute distortion of flatmap relative to fiducial surface and save it at `outfile`.
Several different types of distortion are available:

'areal': computes the areal distortion for each triangle in the flatmap, defined as the
log ratio of the area in the fiducial mesh to the area in the flat mesh. Returns a
per-vertex value that is the average of the neighboring triangles. See:
http://brainvis.wustl.edu/wiki/index.php/Caret:Operations/Morphing

'metric': computes the linear distortion for each vertex in the flatmap, defined as the
mean squared difference between distances in the fiducial map and distances in the
flatmap, for each pair of neighboring vertices. See Fischl, Sereno, and Dale, 1999.

(Implemented via `cortex.polyutils.Distortion` — see `polyutils/Distortion.md`.)

### Parameters
- **outfile** : str
    Path where the distortion map will be saved as an npz file.
- **subject** : str
    Subject in the pycortex database for whom distortion will be computed.
- **dist_type** : {'areal', 'metric'}, optional
    Type of distortion to compute (must be a valid `cortex.polyutils.Distortion` property
    name — not validated up front; see Raises). Default 'areal'.
- **smooth** : float, optional
    Amount of smoothing to apply to the distortion map before returning (forwarded as the
    `factor` argument to `cortex.polyutils.Surface.smooth`). Default 20.

### Returns
`None`. Writes `outfile` (an `.npz` with `left`/`right` arrays) as a side effect.

### Raises
- `AttributeError` — `dist_type` is not a valid property of `cortex.polyutils.Distortion`
  (i.e. not `'areal'` or `'metric'`).
- Propagates errors from `cortex.database.Database.get_surf` if `subject`'s fiducial/flat
  surfaces aren't available.

### Notes
- No FreeSurfer/FSL/GUI dependency.
- Normally invoked indirectly via `cortex.db.get_surfinfo(subject, type="distortion",
  dist_type=..., smooth=...)`.

### Example
```python
import cortex

cortex.surfinfo.distortion("s1_distortion.npz", "S1", dist_type="metric", smooth=20)
```

## Confidence / open questions
- **Recommendation for maintainers:** validate `dist_type` up front with a clear
  `ValueError`; cross-reference `cortex.polyutils.Distortion` instead of duplicating its
  explanation.
