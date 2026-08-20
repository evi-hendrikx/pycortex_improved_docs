# cortex.freesurfer.import_subj

## Current signature (from source)
```python
def import_subj(
    freesurfer_subject,
    pycortex_subject=None,
    freesurfer_subject_dir=None,
    whitematter_surf="smoothwm",
):
```

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:144-183](cortex/freesurfer.py#L144-L183)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.import_subj.html

## Issues with current documentation
- **No Returns section** — returns `None` always.
- **No Raises section** — raises `ValueError` if FreeSurfer isn't sourced and
  `freesurfer_subject_dir` isn't given; propagates `subprocess.CalledProcessError`-style
  failures from `mri_convert`/`mris_convert` (via `sp.check_output`, which raises
  `subprocess.CalledProcessError` on non-zero exit).
- **The docstring's warning about overwriting is slightly inaccurate**: it says this
  "will overwrite (after giving a warning and an option to continue) the pre-existing
  subject" — the actual confirmation prompt (`"Type YES"`) lives inside
  `cortex.database.Database.make_subj`, not in `import_subj` itself; worth a cross-
  reference since a reader of just this docstring won't see where that happens.
- **No mention that this re-initializes the global `cortex.db` singleton** at the end
  (`database.db = database.Database()`) — a real, somewhat surprising side effect: any
  other code holding a reference to the *old* `cortex.db` object (e.g. `db = cortex.db`
  captured before the call) will not see the newly imported subject, since `cortex.db` is
  rebound to a new instance rather than mutated in place.
- **No mention of the specific external commands invoked** (`mri_convert`,
  `mris_convert --to-scanner`) beyond "command line functions from freesurfer."

## Fixed documentation

### Summary
Imports a subject from freesurfer. This will overwrite (after giving a warning and an
option to continue) the pre-existing subject, including all blender cuts, masks,
transforms, etc., and re-generate surface info files (curvature, sulcal depth, thickness)
stored in the surfinfo/ folder for the subject. All cached files for the subject will be
deleted.

### Parameters
- **freesurfer_subject** : str
    Freesurfer subject name
- **pycortex_subject** : str, optional
    Pycortex subject name. By default it uses the freesurfer subject name. It is advised
    to stick to that convention, if possible (your life will go more smoothly.)
- **freesurfer_subject_dir** : str, optional
    Freesurfer subject directory to pull data from. By default uses the directory given
    by the environment variable $SUBJECTS_DIR.
- **whitematter_surf** : str, optional
    Which whitematter surface to import as 'wm'. By default uses 'smoothwm', but that
    surface is smoothed and may not be appropriate. A good alternative is 'white'.

### Returns
`None`.

### Raises
- `ValueError` — FreeSurfer isn't sourced (`$SUBJECTS_DIR` unset) and
  `freesurfer_subject_dir` wasn't given.
- `ValueError` (from `cortex.database.Database.make_subj`) — user declines the "Type YES"
  overwrite confirmation for a pre-existing pycortex subject of the same name.
- `subprocess.CalledProcessError` — `mri_convert`/`mris_convert` fails.

### Notes
This function uses command line functions from freesurfer (`mri_convert`,
`mris_convert --to-scanner`), so you should make sure to have freesurfer sourced before
running this function.

This function will also generate the fiducial surfaces for the subject, which are halfway
between the white matter and pial surfaces (via `make_fiducial`). The surfaces will be
stored in the freesurfer subject's directory. These fiducial surfaces are used for cutting
and flattening.

**Additional side effects not in the original docstring:**
- **Destructive**: overwriting an existing pycortex subject of the same name (via
  `cortex.database.Database.make_subj`) deletes its entire existing directory tree,
  after an interactive `input()` confirmation requiring the exact text `"YES"`.
- **Re-initializes the global `cortex.db` singleton** (`database.db =
  database.Database()`) at the end of the import — any previously-captured reference to
  the old `cortex.db` object will not reflect the new subject; re-access `cortex.db` (or
  re-import) afterward.
- Surfaces are converted with `mris_convert --to-scanner`, so the resulting gifti surfaces
  are stored in scanner coordinates and will look misaligned relative to the anatomical
  volumes when viewed in FreeView (which expects TKR coordinates) — this is expected and
  fine for pycortex's own use.

### Example
```python
import cortex.freesurfer as fs

# Requires FreeSurfer sourced ($SUBJECTS_DIR set) and freesurfer_subject already
# recon-all'd. Prompts for confirmation if a pycortex subject of the same name exists.
fs.import_subj("S1", pycortex_subject="S1", whitematter_surf="white")
```

## Confidence / open questions
- Did not run FreeSurfer commands in this pass; described from source reading.
- **Recommendation for maintainers:** add Returns/Raises; explicitly document the
  `cortex.db` re-initialization side effect, since it's easy to miss and can cause stale-
  reference bugs in longer-running sessions.
