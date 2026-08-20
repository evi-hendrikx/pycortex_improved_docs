# cortex.segment.fix_pia

## Current signature (from source)
```python
def fix_pia(subject):
```

## Where this is documented today
- Source docstring: [cortex/segment.py:548-566](cortex/segment.py#L548-L566)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.segment.fix_pia.html

## Issues with current documentation
Same set of issues as `fix_wm` (near-identical implementation): no Returns/Raises
sections; deprecation notice only present as a runtime warning, referencing a
`rerun_recon()` function that does not exist anywhere in pycortex (see `fix_wm.md` and
`_notes.md`); no mention of the FreeSurfer/Mayavi GUI dependency or blocking `input()`
prompt.

## Fixed documentation

### Summary
Initializes an interface to make pial surface edits. This function will open two windows
-- a tkmedit window that makes the actual edits, as well as a mayavi window to display the
surface. Clicking on the mayavi window will drop markers which can be loaded using the
"Goto Save Point" button in tkmedit.

If you wish to load the other hemisphere, simply close the mayavi window and the other
hemisphere will pop up. Mayavi will stop popping up once the tkmedit window is closed.

Once the tkmedit window is closed, a variety of autorecon options are available. When
autorecon finishes, the new surfaces are immediately imported into the pycortex database.

**Deprecated** — see Notes.

### Parameters
- **subject** : str
    Name of the subject to edit

### Returns
`None`.

### Raises
Propagates `subprocess.CalledProcessError` from `cortex.freesurfer.autorecon` if the user
chooses to run one, and any error from `cortex.freesurfer.import_subj` at the end.

### Notes
- **Deprecated at runtime**, recommending `edit_segmentation()` and a `rerun_recon()`
  function — **`rerun_recon()` does not currently exist in pycortex**, same as noted in
  `fix_wm.md`.
- **Requires FreeSurfer** (`tkmedit`) **and Mayavi**, blocks on interactive windows plus a
  terminal `input()` prompt choosing among autorecon-pia / autorecon-wm / do nothing.
- Re-imports the subject into pycortex automatically after autorecon finishes.

### Example
```python
import cortex

# Deprecated. Requires FreeSurfer + Mayavi installed and a display.
cortex.segment.fix_pia("S1")
```

## Confidence / open questions
- Same as `fix_wm.md`.
- **Recommendation for maintainers:** same as `fix_wm.md`.
