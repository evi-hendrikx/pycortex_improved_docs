# cortex.surfinfo.curvature

## Current signature (from source)
```python
def curvature(outfile, subject, smooth=20):
```

## Where this is documented today
- Source docstring: [cortex/surfinfo.py:19-32](cortex/surfinfo.py#L19-L32)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.surfinfo.curvature.html

## Issues with current documentation
- **No Returns section** — returns `None`; the actual result is written to `outfile`.
- **No Raises section.**
- **Not documented as the auto-generation target of `cortex.db.get_surfinfo(subject,
  type="curvature")`** — this function is normally invoked indirectly (via
  `getattr(surfinfo, type)(surfifile, subject, **kwargs)` inside
  `Database.get_surfinfo`), not called directly by most users; that relationship isn't
  mentioned here.
- **`smooth`'s docstring says "float, optional... Default 20"** but the actual type
  passed to `Surface.smooth`'s `factor` parameter, which in turn is used as a coefficient,
  not an iteration count or a physical smoothing radius — the meaning of the number
  (mean-curvature-flow smoothing strength) is only discoverable by reading
  `polyutils.Surface.smooth`.

## Fixed documentation

### Summary
Compute smoothed mean curvature of the fiducial surface for the given subject and save it
to `outfile`.

### Parameters
- **outfile** : str
    Path where the curvature map will be saved as an npz file.
- **subject** : str
    Subject in the pycortex database for whom curvature will be computed.
- **smooth** : float, optional
    Amount of smoothing to apply to the curvature map (forwarded as the `factor` argument
    to `cortex.polyutils.Surface.smooth`; larger values smooth more). Default 20.

### Returns
`None`. Writes `outfile` (an `.npz` with `left`/`right` arrays) as a side effect.

### Raises
Propagates errors from `cortex.database.Database.get_surf` if `subject`'s fiducial surface
isn't available.

### Notes
- No FreeSurfer/FSL/GUI dependency — pure geometry computation via
  `cortex.polyutils.Surface`.
- Normally invoked indirectly via `cortex.db.get_surfinfo(subject, type="curvature",
  smooth=...)`, which handles caching/file-path resolution; calling this function directly
  requires you to manage the output path yourself.

### Example
```python
import cortex

# Direct call (writes to an explicit path):
cortex.surfinfo.curvature("s1_curvature.npz", "S1", smooth=20)

# More typical usage, via the database (handles caching):
curv_vertex = cortex.db.get_surfinfo("S1", type="curvature")
```

## Confidence / open questions
- **Recommendation for maintainers:** add a Returns section and a cross-reference to
  `cortex.db.get_surfinfo` as the typical entry point.
