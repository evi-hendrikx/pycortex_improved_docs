# cortex.freesurfer.get_curv

## Current signature (from source)
```python
def get_curv(fs_subject, hemi, type='wm', freesurfer_subject_dir=None):
```

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:873-887](cortex/freesurfer.py#L873-L887)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.get_curv.html

## Issues with current documentation
- **No Returns section** — returns the ndarray from `parse_curv` (see `parse_curv.md`).
- **No Raises section.**
- **`type`'s special-casing of `'wm'` vs. everything else is underspecified**: `type='wm'`
  reads `lh.curv` (empty name suffix); any other `type` reads `lh.curv.<type>` — the
  docstring's "'wm' or other type of surface (e.g. 'fiducial' or 'pial')" phrasing implies
  these are real FreeSurfer curv-file suffixes, but there's no guarantee a
  `lh.curv.fiducial` or `lh.curv.pial` file actually exists on disk for a given subject —
  this function does not generate curvature for other surface types, it only looks for a
  pre-existing file with that naming convention.

## Fixed documentation

### Summary
Load freesurfer curv file for a freesurfer subject.

### Parameters
- **fs_subject** : str
    freesurfer subject identifier
- **hemi** : str
    'lh' or 'rh' for left or right hemisphere, respectively
- **type** : str
    'wm' or other type of surface (e.g. 'fiducial' or 'pial'). `'wm'` reads
    `<hemi>.curv`; any other value reads `<hemi>.curv.<type>`, which must already exist on
    disk (this function does not generate curvature files).
- **freesurfer_subject_dir** : str
    directory for Freesurfer subjects (defaults to value for the environment variable
    $SUBJECTS_DIR if None)

### Returns
- **curv** : ndarray, shape (n_vertices,), dtype float32
    Per-vertex curvature values, via `cortex.freesurfer.parse_curv`.

### Raises
- `FileNotFoundError` — the expected `<hemi>.curv[.<type>]` file doesn't exist.

### Notes
- No FreeSurfer command execution — pure file read via `parse_curv`.

### Example
```python
import cortex.freesurfer as fs

curv = fs.get_curv("S1", "lh")           # reads lh.curv
curv_pial = fs.get_curv("S1", "lh", type="pial")  # reads lh.curv.pial, if it exists
```

## Confidence / open questions
- **Recommendation for maintainers:** add a Returns section; clarify that non-`'wm'`
  `type` values require a pre-existing file with that exact naming convention.
