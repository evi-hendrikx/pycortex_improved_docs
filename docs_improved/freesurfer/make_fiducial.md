# cortex.freesurfer.make_fiducial

## Current signature (from source)
```python
def make_fiducial(fs_subject, freesurfer_subject_dir=None):
```

## Where this is documented today
- Source docstring: `"""Make fiducial surface (halfway between white matter and pial
  surfaces)\n    """` (one line). [cortex/freesurfer.py:398-405](cortex/freesurfer.py#L398-L405)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.make_fiducial.html

## Issues with current documentation
- **No Parameters/Returns/Raises sections at all.**
- **Doesn't mention it always uses the `smoothwm` surface** for white matter (hard-coded
  `get_surf(fs_subject, hemi, "smoothwm", ...)`, not configurable via a parameter) — worth
  knowing since `import_subj`'s `whitematter_surf` parameter (which can be `'white'`
  instead) has no effect on what `make_fiducial` itself uses internally.
- **Doesn't mention where the output is written** (into the FreeSurfer subject directory,
  not the pycortex database — a common point of confusion per a comment in
  `import_subj`: `"NOTE: these are IN THE FREESURFER $SUBJECTS_DIR !! which can cause
  confusion."`).
- **No mention this processes both hemispheres** (loops over `['lh', 'rh']`
  unconditionally).

## Fixed documentation

### Summary
Make fiducial surface (halfway between white matter and pial surfaces), for both
hemispheres, writing the result into the FreeSurfer subject's own `surf/` directory (not
the pycortex database).

### Parameters
- **fs_subject** : str
    Freesurfer subject ID.
- **freesurfer_subject_dir** : str, optional
    Freesurfer subjects directory. `None` defaults to `$SUBJECTS_DIR`.

### Returns
`None`. Writes `<freesurfer_subject_dir>/<fs_subject>/surf/{lh,rh}.fiducial` as a side
effect.

### Raises
Propagates file-not-found errors from `get_surf`/`parse_surf` if the subject's `smoothwm`
or `pial` surfaces aren't present.

### Notes
- **Always uses the `smoothwm` surface** for the white-matter side of the average — not
  configurable via a parameter here (contrast with `import_subj`'s `whitematter_surf`,
  which controls a *different* import step, not this function).
- Output is written into the **FreeSurfer** subject directory
  (`$SUBJECTS_DIR/<fs_subject>/surf/`), not the pycortex database — easy to confuse with
  pycortex's own fiducial-surface handling.
- Called automatically as part of `cortex.freesurfer.import_subj`.

### Example
```python
import cortex.freesurfer as fs

# Writes lh.fiducial and rh.fiducial into $SUBJECTS_DIR/S1/surf/
fs.make_fiducial("S1")
```

## Confidence / open questions
- **Recommendation for maintainers:** expand the one-line docstring to state the
  hard-coded `smoothwm` dependency and the FreeSurfer (not pycortex) output location.
