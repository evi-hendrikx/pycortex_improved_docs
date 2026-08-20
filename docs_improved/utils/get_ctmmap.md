# cortex.utils.get_ctmmap

## Current signature (from source)
```python
def get_ctmmap(subject, **kwargs):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:135-161](cortex/utils.py#L135-L161) — already
  complete (Parameters, Returns, Notes).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_ctmmap.html

## Issues with current documentation
- **`**kwargs`'s forwarding target (`get_ctmpack`) is named but not enumerated** — the
  docstring says "keyword arguments to pass to get_ctmpack" and highlights `method`, but
  doesn't list `get_ctmpack`'s other real parameters (`types`, `level`, `recache`,
  `decimate`, `external_svg`, `overlays_available`) that are equally valid here.
- **No Raises section.**
- **Approximation caveat missing**: the freesurfer-vertex correspondence is found via
  nearest-neighbor KD-tree query (`cKDTree.query`), not an exact index mapping — for
  decimated/`mg2` surfaces, the "closest point" may not be a perfect one-to-one
  correspondence. Not mentioned.

## Fixed documentation

### Summary
Return a mapping from the vertices in the CTM surface to the vertices in the freesurfer
surface. The mapping is a numpy array, such that `ctm2fs_left[i] = j` means that the i-th
vertex in the CTM surface corresponds to the j-th vertex in the freesurfer surface.

### Parameters
- **subject** : str
    Subject name
- **\*\*kwargs**
    Keyword arguments to pass to `get_ctmpack`. The most relevant keyword for this
    function is the `method` kwarg (either `mg2` or `raw`); also accepts `get_ctmpack`'s
    `types`, `level`, `recache`, `decimate`, `external_svg`, `overlays_available`.

### Returns
- **ctm2fs_left** : array (n_vertices_left,)
    Mapping from CTM vertices to freesurfer vertices for the left hemisphere.
- **ctm2fs_right** : array (n_vertices_right,)
    Mapping from CTM vertices to freesurfer vertices for the right hemisphere.

### Raises
Propagates errors from `get_ctmpack`/`cortex.database.Database.get_surf` (e.g. missing
pia/fiducial surfaces).

### Notes
This mapping is absolutely necessary when the CTM surfaces are saved with the `mg2`
method, which corresponds to storing surfaces with a compressed format.

The correspondence is found via **nearest-neighbor spatial matching** (a KD-tree query
against the pia, or fiducial as fallback, surface), not an exact stored index mapping — for
decimated or heavily compressed meshes this is an approximation, not guaranteed to be a
perfect one-to-one correspondence.

### Example
```python
import cortex

ctm2fs_left, ctm2fs_right = cortex.utils.get_ctmmap("S1", method="mg2")
```

## Confidence / open questions
- **Recommendation for maintainers:** enumerate `get_ctmpack`'s full forwarded parameter
  list; note the nearest-neighbor-approximation nature of the mapping.
