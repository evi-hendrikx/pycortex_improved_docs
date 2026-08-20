# cortex.mapper.get_mapper

## Current signature (from source)
```python
def get_mapper(subject, xfmname, type='nearest', recache=False, **kwargs):
```

## Where this is documented today
- Source docstring: none. [cortex/mapper/__init__.py:10-41](cortex/mapper/__init__.py#L10-L41)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.mapper.get_mapper.html
  (no docstring content beyond the bare signature).

## Issues with current documentation
- **No docstring at all.**
- **`type` accepts 10 distinct values not listed anywhere**: `'nearest'`, `'trilinear'`,
  `'gaussian'`, `'lanczos'`, `'const_patch_nn'`, `'const_patch_trilin'`,
  `'const_patch_lanczos'`, `'line_nearest'`, `'line_trilinear'`, `'line_lanczos'` — mapping
  to classes in `cortex.mapper.point`/`.patch`/`.line`. Passing anything else raises a bare
  `KeyError`, not a clear error message.
- **`**kwargs` forwarding is completely undocumented.** Extra kwargs are forwarded to the
  chosen mapper class's `_getmask` classmethod (ultimately, for `point.*` mappers, to the
  underlying sampler function in `cortex.mapper.samplers`, e.g. `gaussian`'s `sigma`/
  `window`, `lanczos`'s `window`). This chain is invisible from `get_mapper` itself.
  `**kwargs` also gets encoded into the cache filename (`'_'.join('%s%s'%(k,v) ...)`), so
  changing a kwarg value produces a differently-named, independently-cached mapper file.
- **No Returns section** — returns a `Mapper` subclass instance (see `Mapper.md`).
- **No Raises section** — `KeyError` for an unrecognized `type`; propagates database/file
  errors if `subject`/`xfmname` don't exist.
- **Caching behavior is undocumented**: results are cached to `.npz` files under the
  subject's pycortex cache directory, keyed by `xfmname`, mapper type, and any `**kwargs`;
  the cache is considered valid if it's newer than the transform file (`os.stat(...).st_mtime`
  comparison), and always considered valid for `xfmname == "identity"` regardless of
  timestamps. `recache=True` forces regeneration.

## Fixed documentation

### Summary
Get (from cache) or build a `cortex.mapper.Mapper` object that projects data between a
subject's functional volume space and cortical surface (vertex) space, using the named
projection method.

### Parameters
- **subject** : str
    Subject identifier; must exist in the pycortex database.
- **xfmname** : str
    Transform name; must exist in the pycortex database (or be `"identity"`).
- **type** : str, default `'nearest'`
    Projection method. One of `'nearest'`, `'trilinear'`, `'gaussian'`, `'lanczos'`
    (point-sampling methods, in `cortex.mapper.point`), `'const_patch_nn'`,
    `'const_patch_trilin'`, `'const_patch_lanczos'` (patch-based, in
    `cortex.mapper.patch`), or `'line_nearest'`, `'line_trilinear'`, `'line_lanczos'`
    (line-sampling through cortical thickness, in `cortex.mapper.line`).
- **recache** : bool, default `False`
    Force regeneration of the cached mapper instead of reusing an existing `.npz` cache
    file.
- **\*\*kwargs**
    Forwarded to the chosen mapper class's mask-construction step and, for point mappers,
    ultimately to the corresponding function in `cortex.mapper.samplers` — e.g.
    `sigma`/`window` for `'gaussian'`, `window` for `'lanczos'`. Also becomes part of the
    cache filename, so different kwarg values produce independently-cached mappers.

### Returns
- **mapper** : `cortex.mapper.Mapper` subclass instance
    A callable mapper object (see `Mapper.md`) for converting between volume and vertex
    space for `(subject, xfmname)`.

### Raises
- `KeyError` — `type` is not one of the ten recognized projection names.
- Propagates errors from `cortex.database.Database.get_xfm`/`get_surf` if `subject`/
  `xfmname` are invalid, or from the sampler function if `**kwargs` contains unrecognized
  keys for the chosen mapper type.

### Notes
- **Disk cache side effect**: builds and writes a `.npz` mapper cache file under the
  subject's pycortex cache directory the first time a given
  `(xfmname, type, kwargs)` combination is requested; subsequent calls reuse it unless
  `recache=True`. Can be slow the first time (computes fiducial/flat surface projections).
- No FreeSurfer/FSL/GUI dependency, but requires the subject's fiducial (and, ideally,
  flat) surfaces to already exist in the pycortex database.

### Example
```python
import cortex

mapper = cortex.mapper.get_mapper("S1", "fullhead", type="line_nearest")
vtx = mapper(cortex.Volume.random("S1", "fullhead"))
```

## Confidence / open questions
- Could not verify from source alone the exact cache-invalidation edge cases (e.g.
  clock-skew scenarios for the mtime comparison) — described from static reading of
  `__init__.py:36-41` only.
- **Recommendation for maintainers:** add a docstring documenting `type`'s ten valid
  values and the `**kwargs` forwarding/caching behavior; raise a clearer error than a bare
  `KeyError` for an unrecognized `type`.
