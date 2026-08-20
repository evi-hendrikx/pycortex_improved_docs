# cortex.mapper.Mapper

## Current signature (from source)
```python
class Mapper(object):
    '''Maps data from epi volume onto surface using various projections'''
    def __init__(self, left, right, shape, subject, xfmname):
```
Base class for all mapper types (`cortex.mapper.point.PointNN`/`PointTrilin`/etc.,
`cortex.mapper.patch.*`, `cortex.mapper.line.*`) — subclasses differ only in how
`_getmask`/the underlying sampler works; the public interface documented here (`__call__`,
`.backwards`, `.mask`, `.hemimasks`, `.from_cache`) is shared by all of them. Users
normally obtain a `Mapper` via `cortex.mapper.get_mapper` rather than constructing one
directly.

## Where this is documented today
- Source docstring (class-level, one line): [cortex/mapper/mapper.py:9-10](cortex/mapper/mapper.py#L9-L10)
- `__init__`, `__call__`, `mask`, `hemimasks`, `from_cache` have no docstrings; `.backwards`
  has a short one. [cortex/mapper/mapper.py](cortex/mapper/mapper.py)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.mapper.Mapper.html

## Issues with current documentation
- **`__init__` has no docstring** — `left`/`right` (sparse voxel→vertex weight matrices
  per hemisphere), `shape` (volume shape), `subject`, `xfmname` are all undocumented.
- **`__call__` (the primary way a `Mapper` is used — `mapper(volume_or_vertex_data)`) has
  no docstring at all.** Its behavior is genuinely dual-purpose and non-obvious: calling it
  with `Volume`-like data projects volume→vertex and returns a `Vertex`; calling it with
  `Vertex`-like data instead **slices/reorders** the vertex data per-hemisphere (via
  `self.idxmap`, if set) and returns a `(left, right)` tuple — a completely different
  operation, not a projection at all in that branch. None of this is documented.
- **`.mask`/`.hemimasks` properties have no docstrings** — not obvious that `.mask` is a
  single combined boolean volume-shaped array (voxels touched by either hemisphere's
  mapping) while `.hemimasks` is a list of two separate per-hemisphere boolean arrays.
- **`.from_cache` classmethod has no docstring** — the expected `.npz` file format
  (`left_data`/`left_indices`/`left_indptr`/`left_shape`, mirrored for `right`, plus
  `shape`) is only discoverable by reading `_savecache`.
- **`.backwards`'s docstring is present but incomplete**: doesn't mention this is an
  *approximate* inverse (documented as "not particularly accurate" only in
  `VertexData.volume`'s docstring, not here), doesn't explain the regularized
  least-squares approach used (`splu` factorization of a slightly-regularized Gram
  matrix), and doesn't mention the first call for a given mapper is more expensive (the
  factorization is cached in `self._backmapper` afterward).
- **No Returns/Raises sections anywhere.**
- **`idxmap` (used inside `__call__` to optionally reorder/subset vertices) is confirmed
  dead/vestigial**: grepping the entire `cortex/mapper/` package, it is set to `None` in
  `__init__` and never reassigned anywhere — in `Mapper` itself or any subclass
  (`point.py`, `patch.py`, `line.py`). Every `if self.idxmap is not None:` branch in
  `__call__` is therefore currently unreachable in practice. See `_notes.md`.

## Fixed documentation

### Summary
Maps data from epi volume onto surface using various projections. Callable — projects
`Volume`-like data to vertex space, or reorders `Vertex`-like data per hemisphere.
Normally obtained via `cortex.mapper.get_mapper` rather than constructed directly.

### Parameters (`__init__`)
- **left** : scipy.sparse matrix, shape (n_left_vertices, n_voxels)
    Sparse voxel→vertex weight matrix for the left hemisphere.
- **right** : scipy.sparse matrix, shape (n_right_vertices, n_voxels)
    Sparse voxel→vertex weight matrix for the right hemisphere.
- **shape** : tuple of int
    Shape of the functional volume this mapper projects from/to.
- **subject** : str
    Subject identifier.
- **xfmname** : str
    Transform name.

### Public methods and properties
- **`.from_cache(cachefile, subject, xfmname)`** (classmethod) → `Mapper`
    Load a previously-cached mapper from an `.npz` file (as written by `_savecache`),
    containing sparse-matrix components (`{left,right}_{data,indices,indptr,shape}`) and
    `shape`.
- **`.mask`** (property) : ndarray of bool, shape `self.shape`
    Volume-shaped mask of voxels contributing to either hemisphere's mapping.
- **`.hemimasks`** (property) : list of 2 ndarrays of bool, shape `self.shape` each
    Per-hemisphere (left, right) versions of `.mask`.
- **`__call__(data)`** →  `Vertex` (if `data` is volume-like) or `(left, right)` tuple (if
  `data` is `Vertex`-like)
    - If `data` is a `Volume`/volume-like tuple: projects the volume through the sparse
      `left`/`right` mapping matrices and returns a `cortex.Vertex` with the combined
      (optionally `idxmap`-reordered) result.
    - If `data` is a `cortex.Vertex` (or `raw`/RGB vertex data): **not a projection** —
      splits the vertex data into `(left, right)` by hemisphere length (optionally
      reordered via `self.idxmap`, if set — see Issues) and returns the pair directly, no
      volume involved.
- **`.backwards(vertexdata)`** → `Volume` (if `vertexdata` is a `Vertex`) or ndarray
  (otherwise)
    Projects vertex data back into volume space. If a `Vertex` object is provided, a
    `Volume` object is returned; if an array is provided, an array is returned. Uses a
    regularized least-squares solve (cached `splu` factorization of the mapping matrix's
    Gram matrix, computed on first use and reused thereafter) — an **approximate** inverse,
    not exact.

### Returns
See per-method entries above.

### Raises
Not validated at this level — malformed `data` shapes will surface as low-level
`numpy`/`scipy.sparse` errors.

### Notes
- Users typically obtain a `Mapper` via `cortex.mapper.get_mapper(subject, xfmname, type=...)`
  rather than constructing `Mapper`/its subclasses directly.
- `.backwards` is explicitly noted elsewhere in pycortex (in `VertexData.volume`'s
  docstring) as "not particularly accurate" — treat it as an approximation.
- The first call to `.backwards` for a given mapper instance is more expensive (computes
  and caches a sparse LU factorization); subsequent calls reuse it.

### Example
```python
import cortex

mapper = cortex.mapper.get_mapper("S1", "fullhead", type="nearest")

vol = cortex.Volume.random("S1", "fullhead")
vtx = mapper(vol)             # Volume -> Vertex projection

vtx_back = mapper.backwards(vtx)   # approximate inverse: Vertex -> Volume
```

## Confidence / open questions
- The `idxmap` dead-code finding is based on a full-package grep for `idxmap` across
  `cortex/mapper/*.py` (only appears in `mapper.py`, always either initialized to `None`
  or read) — not on tracing runtime behavior via execution.
- **Recommendation for maintainers:** add docstrings to `__init__`, `__call__` (especially
  its dual Volume/Vertex behavior), `.mask`/`.hemimasks`, and `.from_cache`; clarify
  `.backwards`'s approximate nature and caching behavior directly in its own docstring.
