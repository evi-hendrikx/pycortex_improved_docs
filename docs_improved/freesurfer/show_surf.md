# cortex.freesurfer.show_surf

## Current signature (from source)
```python
def show_surf(subject, hemi, type, patch=None, curv=True, freesurfer_subject_dir=None):
```

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:896-912](cortex/freesurfer.py#L896-L912)
  (`type`, `patch`, `curv`, `freesurfer_subject_dir` entries are all present but have
  **empty** descriptions).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.show_surf.html

## Issues with current documentation
- **Most parameter descriptions are blank** — `type`, `patch`, `curv`, and
  `freesurfer_subject_dir` are listed with no description text at all.
- **The function is explicitly deprecated at runtime** (`warnings.warn('Deprecated and
  probably broken! Try cortex.segment.show_surf() ...')`) but this is not reflected in the
  docstring text itself, only as a runtime warning.
- **No Returns section** — returns `(fig, surf)`, Mayavi figure/surface objects.
- **No mention of the Mayavi/TVTK GUI dependency**, nor that this opens an interactive 3D
  window and blocks (`mlab.show()`) until closed.
- **`os.environ['SUBJECTS_DIR']` is read unconditionally inside the function body**
  (for the click-picker callback's output path), independent of the
  `freesurfer_subject_dir` parameter — meaning `$SUBJECTS_DIR` must be set even if you
  passed an explicit `freesurfer_subject_dir`, and this raises `KeyError` if unset. Not
  documented.

## Fixed documentation

### Summary
Show a surface from a Freesurfer subject directory using Mayavi. **Deprecated and
"probably broken"** per its own runtime warning — use `cortex.segment.show_surf()`
instead, which uses MeshLab rather than Mayavi.

### Parameters
- **subject** : str
    Freesurfer subject name
- **hemi** : str ['lh' | 'rh']
    Left or right hemisphere
- **type** : str
    Surface type to display (e.g. `'inflated'`, `'pial'`), forwarded to
    `cortex.freesurfer.get_surf`.
- **patch** : str, optional
    Name of a patch file to display instead of the full surface, forwarded to `get_surf`.
- **curv** : bool
    Whether to color the surface by curvature (loaded via `get_curv`) instead of by the
    patch interior/boundary index.
- **freesurfer_subject_dir** : str, optional
    FreeSurfer subjects directory for surface loading. Note: independent of this, the
    function also reads `$SUBJECTS_DIR` directly (unconditionally) for the click-picker's
    output file path — set `$SUBJECTS_DIR` regardless of what you pass here.

### Returns
- **fig** : `mayavi.core.scene.Scene`
- **surf** : Mayavi surface pipeline object

### Raises
- `KeyError` — `$SUBJECTS_DIR` environment variable is not set (read unconditionally,
  independent of `freesurfer_subject_dir`).
- Import errors if Mayavi/TVTK are not installed.

### Notes
- **Deprecated** — emits `DeprecationWarning`-style message at call time recommending
  `cortex.segment.show_surf()` instead.
- **Requires Mayavi and TVTK** (GUI dependency) and opens a blocking interactive 3D window
  (`mlab.show()`) — not usable headless.
- Clicking on the surface in the viewer writes the picked point's coordinates to
  `$SUBJECTS_DIR/<subject>/tmp/edit.dat`.

### Example
```python
import cortex.freesurfer as fs

# Deprecated -- prefer cortex.segment.show_surf() instead.
# Requires Mayavi/TVTK installed and a display; opens a blocking GUI window.
fig, surf = fs.show_surf("S1", "lh", "inflated")
```

## Confidence / open questions
- Did not run this function (Mayavi GUI, blocking) in this pass.
- **Recommendation for maintainers:** fill in the blank parameter descriptions; state the
  deprecation in the docstring text itself, not just a runtime warning; consider removing
  this function per its own "probably broken" warning, in favor of
  `cortex.segment.show_surf`.
