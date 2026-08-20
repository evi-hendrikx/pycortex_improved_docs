# cortex.surfinfo.tissots_indicatrix

## Current signature (from source)
```python
def tissots_indicatrix(outfile, sub, radius=10, spacing=50):
```

## Where this is documented today
- Source docstring: [cortex/surfinfo.py:99-118](cortex/surfinfo.py#L99-L118)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.surfinfo.tissots_indicatrix.html

## Issues with current documentation
- **No Returns section.**
- **No Raises section.**
- **No mention that disc placement is randomized** (`np.random.randint`) with no seed
  parameter exposed — repeated calls produce different results; not stated.
- **`centers` output field (saved in `outfile` alongside `left`/`right`) isn't documented
  at all** — the docstring only describes an "indicatrix map," not the saved centers array
  or its ragged (object-dtype) shape.
- **Not documented as the auto-generation target of `cortex.db.get_surfinfo(subject,
  type="tissots_indicatrix")`.**
- **No performance note** — for small `spacing` relative to surface size this can place
  many discs and take a while (repeated geodesic-distance computations per candidate
  center).

## Fixed documentation

### Summary
Compute a Tissot's indicatrix for the given subject and save the result to a file. This
involves randomly filling in discs of fixed geodesic radius on the fiducial surface.

See https://en.wikipedia.org/wiki/Tissot's_indicatrix for more info.

### Parameters
- **outfile** : str
    Path where the indicatrix map will be saved.
- **sub** : str
    Subject in the pycortex database for whom the indicatrix will be computed.
- **radius** : float, optional
    The geodesic radius of each disc in mm. Default 10.
- **spacing** : float, optional
    The minimum distance between disc centers in mm. Default 50.

### Returns
`None`. Writes `outfile` as a side effect — an `.npz` with:
- `left`, `right` : ndarray of 0/1, shape (n_verts_hemi,) — indicatrix disc membership per
  vertex.
- `centers` : object-dtype ndarray of two variable-length int arrays — the (randomly
  chosen) disc-center vertex indices for each hemisphere.

### Raises
Propagates errors from `cortex.database.Database.get_surf` if `subject`'s fiducial surface
isn't available.

### Notes
- **Non-deterministic**: disc centers are chosen via `np.random.randint` with no seed
  parameter — results differ between calls (seed `numpy`'s global RNG yourself if you need
  reproducibility).
- Can be slow for small `spacing`/large surfaces, since it repeatedly computes geodesic
  distance (`cortex.polyutils.Surface.geodesic_distance`) for each new candidate center.
- No FreeSurfer/FSL/GUI dependency.
- Normally invoked indirectly via `cortex.db.get_surfinfo(subject,
  type="tissots_indicatrix", radius=..., spacing=...)`.

### Example
```python
import numpy as np
import cortex

np.random.seed(0)  # for reproducibility, since disc placement is randomized
cortex.surfinfo.tissots_indicatrix("s1_tissots.npz", "S1", radius=10, spacing=50)
```

## Confidence / open questions
- **Recommendation for maintainers:** add a `seed` parameter (or document how to control
  reproducibility); add a Returns section documenting the `centers` output.
