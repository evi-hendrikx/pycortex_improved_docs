# cortex.freesurfer.get_surf

## Current signature (from source)
```python
def get_surf(subject, hemi, type, patch=None, flatten_step=None, freesurfer_subject_dir=None):
```
Note: this is a *different* function from `cortex.database.Database.get_surf` (accessed as
`cortex.db.get_surf`) and from `cortex.dataset.Dataset.get_surf` — same name, three
unrelated implementations, in three different modules. See `_notes.md`.

## Where this is documented today
- Source docstring: `"""Read freesurfer surface file\n    """` (one line).
  [cortex/freesurfer.py:487-521](cortex/freesurfer.py#L487-L521)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.get_surf.html

## Issues with current documentation
- **No Parameters/Returns/Raises sections at all.**
- **Same name as two other, unrelated `get_surf` functions** in pycortex
  (`cortex.database.Database.get_surf` and `cortex.dataset.Dataset.get_surf`) — this one
  reads directly from a FreeSurfer `$SUBJECTS_DIR`, not from the pycortex database/filestore.
  This is not called out anywhere and is a likely source of confusion.
- **`type="patch"` behavior is a special case not explained**: passing `type="patch"`
  forces the underlying full surface to be `smoothwm` (hard-coded), regardless of what
  patch is being loaded, and requires `patch` to be given (`assert patch is not None`,
  which raises a bare, message-less `AssertionError` if omitted). This isn't documented.
- **Return value's shape depends on `type`/`patch`** and is not stated: returns
  `(pts, polys, idx)` where `idx` means different things — for `type="patch"`, `idx`
  distinguishes interior (`1`) vs. boundary (`-1`) patch vertices in the *full* surface's
  index space; otherwise `idx` is the surface's curvature array (via `get_curv`, an
  entirely different meaning for the third return value depending on the call).
- **`flatten_step`'s purpose and format are undocumented** — appends a zero-padded frame
  number (`'%04d'%flatten_step`) to the patch filename, meant to read an intermediate
  save from `flatten(..., save_every=...)`.

## Fixed documentation

### Summary
Read freesurfer surface file — the full surface, optionally clipped/positioned according
to a patch file (e.g. a flattened patch), for a subject in the FreeSurfer `$SUBJECTS_DIR`
(not the pycortex database).

### Parameters
- **subject** : str
    Freesurfer subject name.
- **hemi** : str ['lh' | 'rh']
    Hemisphere to load.
- **type** : str
    Surface type to load, e.g. `'smoothwm'`, `'pial'`, `'inflated'`, or the special value
    `'patch'` (see Notes).
- **patch** : str, optional
    Name of a patch file to apply. Required (raises `AssertionError`) when `type="patch"`;
    optional otherwise, in which case the loaded full surface is additionally clipped to
    the patch's vertices/faces.
- **flatten_step** : int, optional
    If given, appends a zero-padded iteration number to the patch filename, to load an
    intermediate save written by `cortex.freesurfer.flatten(..., save_every=...)`.
- **freesurfer_subject_dir** : str, optional
    FreeSurfer subjects directory. `None` defaults to `$SUBJECTS_DIR`.

### Returns
- **pts** : ndarray, shape (n_vertices, 3)
- **polys** : ndarray, shape (n_faces, 3)
- **third value** :
    If `type="patch"`: `idx`, an ndarray of shape (n_vertices,) marking each full-surface
    vertex as `1` (interior patch vertex), `-1` (boundary patch vertex), or `0` (not in
    the patch). Otherwise: the surface's curvature array, via
    `cortex.freesurfer.get_curv(subject, hemi, ...)`.

### Raises
- `AssertionError` — `type="patch"` but `patch` is `None`.
- `FileNotFoundError`/`struct.error` — propagated from `parse_surf`/`parse_patch` if the
  expected files don't exist or don't match the expected format.

### Notes
- **Reads from the FreeSurfer subject directory, not the pycortex database** — do not
  confuse with `cortex.db.get_surf` (pycortex filestore) or `cortex.Dataset.get_surf`
  (packed HDF5 contents).
- The base surface loaded is whichever `type` specifies (e.g. `'pial'`, `'inflated'`) —
  except when `type` is literally `"patch"`, in which case the underlying full surface is
  hard-coded to `smoothwm` regardless of which patch is requested.

### Example
```python
import cortex.freesurfer as fs

# Full pial surface, no patch:
pts, polys, curv = fs.get_surf("S1", "lh", "pial")

# Patch (requires a previously-flattened lh.<patch>.patch.3d file):
pts, polys, idx = fs.get_surf("S1", "lh", "patch", patch="flattenv01.flat")
```

## Confidence / open questions
- The exact interior/boundary/`0` semantics of the returned `idx` array for `type="patch"`
  were reconstructed from `freesurfer.py:503-519` by static reading, not execution.
- **Recommendation for maintainers:** rename this function (or `cortex.db.get_surf`) to
  avoid the three-way name collision across `cortex.freesurfer`, `cortex.database`, and
  `cortex.dataset`; document the dual meaning of the third return value; give
  `type="patch"`'s `assert patch is not None` a real error message.
