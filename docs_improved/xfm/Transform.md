# cortex.xfm.Transform

## Current signature (from source)
```python
class Transform(object):
    def __init__(self, xfm, reference):
```

## Where this is documented today
- Source docstring (class-level, one line): [cortex/xfm.py:7-11](cortex/xfm.py#L7-L11)
- `from_fsl`, `to_fsl`, `from_freesurfer`, `to_freesurfer` are well-documented (full
  NumPy-style docstrings with Notes on direction conventions). `__init__`, `__call__`,
  `.inv`, `__mul__`/`__rmul__`, `.save`, `__repr__` have no docstrings at all.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.xfm.Transform.html

## Issues with current documentation
- **`__init__` has no docstring** — `xfm`'s expected shape/type (a 4x4 affine matrix) and
  `reference`'s three accepted forms (path string, `(z, y, x)` shape tuple, or a nibabel
  image object) are undocumented.
- **A real edge-case bug in `__init__`'s string-reference handling**: if `reference` is a
  `str` that `nibabel.load` fails to open (raises `IOError`), the `except` branch sets
  `self.reference = reference` (the raw string) but **never sets `self.shape`** — any
  later access to `.shape` (used internally by `.inv`, `__mul__`, `__rmul__`) raises
  `AttributeError`. This only triggers for an invalid/unreadable path string, not the
  mainline cases (tuple, nibabel image, or a loadable path), but is a real gap. Flagged,
  not fixed — see `_notes.md`.
- **`__call__` has no docstring** — `Transform` instances are callable
  (`xfm_instance(pts)`) to apply the affine to a set of 3D points; this core usage pattern
  is entirely undocumented.
- **`.inv` (property) has no docstring** — returns a new `Transform` with the matrix
  inverted (does not mutate `self`).
- **`__mul__`/`__rmul__` have no docstrings** — `Transform` instances support `*`
  composition with other `Transform`s or raw 4x4 matrices (matrix-multiplying the
  underlying affines); not documented at all despite being a natural, likely-used
  operation (`cortex.align.automatic`/`compute_mni_transform`-style code composes
  transforms this way internally).
- **`.save` has no docstring** — raises `ValueError` for reference-free transforms
  (constructed from a shape tuple), not documented.
- **No Raises sections anywhere in the class.**
- **No Examples section for the class overall** (though `from_fsl`/`from_freesurfer` each
  have a `Notes` section explaining the expected external-tool call convention).

## Fixed documentation

### Summary
A standard affine transform. Typically holds a transform from anatomical magnet space to
epi file space. Callable (applies the affine to 3D points), composable via `*`, and
convertible to/from FSL and FreeSurfer transform conventions.

### Parameters (`__init__`)
- **xfm** : ndarray, shape (4, 4)
    The affine transformation matrix.
- **reference** : str, tuple, or nibabel image
    Either: a path to a nibabel-readable reference image (defines both `.reference` and
    `.shape`); a `(z, y, x)` shape tuple for a reference-free transform (only `.shape` is
    set, `.reference` stays `None`); or a nibabel image object directly (defines both).
    **Caveat**: if a `str` path is given that `nibabel.load` cannot open, `.shape` is
    never set (see Issues) — only pass a valid, loadable path, or use the tuple form for
    a reference-free transform.

### Public methods and properties
- **`__call__(pts)`** → ndarray, shape (n, 3)
    Apply the affine transform to a set of 3D points `pts` (shape `(n, 3)`), returning the
    transformed points.
- **`.inv`** (property) → `Transform`
    A new `Transform` with the matrix inverted (`np.linalg.inv(self.xfm)`), sharing the
    same reference/shape. Does not mutate `self`.
- **`__mul__(other)` / `__rmul__(other)`** → `Transform`
    Compose this transform with another `Transform` (or raw 4x4 matrix) via matrix
    multiplication (`self.xfm @ other.xfm` or `other.xfm @ self.xfm` respectively). The
    resulting `Transform` keeps `self`'s reference/shape.
- **`.save(subject, name, xfmtype="magnet")`**
    Save this transform into the pycortex database as `(subject, name)`, via
    `cortex.database.Database.save_xfm`. Raises `ValueError` if this is a reference-free
    transform (constructed from a shape tuple, with no `.reference`).
- **`.from_fsl(xfm, func_nii, anat_nii)`** (classmethod) → `Transform`
    Converts an fsl transform to a pycortex transform. Converts a transform computed
    using FSL's FLIRT to a `Transform` object. The transform must have been computed FROM
    the nifti volume specified in `func_nii` TO the volume specified in `anat_nii` (i.e.
    `flirt -in <func_nii> -ref <anat_nii> ...`).
- **`.to_fsl(anat_nii, direction='func>anat')`** → ndarray, shape (4, 4)
    Converts a pycortex transform to an FSL transform, using the transform's stored
    reference and the given anatomical file. **Only works for `"coord"`-type transforms —
    fails hard for `"magnet"` transforms** (per its own Notes section).
- **`.from_freesurfer(fs_register, func_nii, subject, freesurfer_subject_dir=None)`**
  (classmethod) → `Transform`
    Converts a FreeSurfer transform (e.g. from `bbregister`) to a pycortex transform.
    Requires FreeSurfer's `mri_info` on `PATH`.
- **`.to_freesurfer(fs_register, subject, freesurfer_subject_dir=None)`** → ndarray,
  shape (4, 4)
    Converts a pycortex transform to FreeSurfer's `register.dat` format, writing it to
    `fs_register`. Requires FreeSurfer's `mri_info` on `PATH` and `subject`'s raw
    anatomical already in the pycortex database.
- **`__repr__`** — `"<Transform into <reference filename> space>"`, or `"<Reference free
  affine transform>"` if no reference file is available.

### Returns
See per-method entries above.

### Raises
- `ValueError` — `.save()` on a reference-free transform.
- `AttributeError` — `.shape`/`.inv`/`__mul__`/`__rmul__` on a `Transform` constructed
  with an unreadable string `reference` (see Issues).
- `subprocess.CalledProcessError`/`OSError` — `from_freesurfer`/`to_freesurfer` if
  FreeSurfer's `mri_info` isn't installed or fails.

### Notes
- `from_fsl`/`to_fsl` and `from_freesurfer`/`to_freesurfer` each document (in their own
  docstrings) the exact external-tool call convention (`flirt -in ... -ref ...` /
  `bbregister --s ... --mov ... --reg ...`) the resulting transform assumes — read those
  before using either conversion pair, direction conventions are easy to get backwards.
- `to_fsl` explicitly fails for `"magnet"`-type transforms — only use it with `"coord"`
  transforms (e.g. from `cortex.db.get_xfm(subject, xfmname, xfmtype="coord")`).
- No FreeSurfer/FSL dependency for the core `Transform` class itself (`__init__`,
  `__call__`, `.inv`, `*` composition, `.save`) — only the `from_freesurfer`/
  `to_freesurfer` conversion methods require FreeSurfer, and `to_fsl`/`from_fsl` operate
  on already-loaded matrices/files (no FSL subprocess calls themselves).

### Example
```python
import cortex
import numpy as np

xfm = cortex.db.get_xfm("S1", "fullhead", xfmtype="coord")

# Apply the transform to a set of 3D points:
pts = np.random.randn(10, 3)
transformed = xfm(pts)

# Invert and compose:
inv_xfm = xfm.inv
identity_ish = xfm * inv_xfm

# Convert to FSL format (only valid for "coord" transforms):
anat = cortex.db.get_anat("S1", "raw").get_filename()
fsl_matrix = xfm.to_fsl(anat)
```

## Confidence / open questions
- The `.shape`-unset edge case for an unreadable string `reference` is confirmed by
  static reading of `xfm.py:16-22`, not by execution.
- Did not run the FreeSurfer-dependent conversion methods (`from_freesurfer`,
  `to_freesurfer`) in this pass.
- **Recommendation for maintainers:** add docstrings to `__init__`, `__call__`, `.inv`,
  `__mul__`/`__rmul__`, `.save`; fix the string-reference-load-failure path to either set
  `.shape` to something sensible or raise a clear error instead of leaving it unset.
