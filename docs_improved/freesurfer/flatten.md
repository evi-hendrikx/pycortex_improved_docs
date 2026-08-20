# cortex.freesurfer.flatten

## Current signature (from source)
```python
def flatten(fs_subject, hemi, patch, freesurfer_subject_dir=None, save_every=None):
```

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:96-125](cortex/freesurfer.py#L96-L125)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.flatten.html

## Issues with current documentation
- **`Returns` section header is present but empty** — no text describing that the function
  returns `True` if flattening ran, or `False` if the user declined the confirmation
  prompt.
- **No Raises section** — `subprocess.check_call` raises `subprocess.CalledProcessError` if
  `mris_flatten` fails.
- **Interactive confirmation prompt undocumented** (blocks on `input()`, same pattern as
  `autorecon`).
- **No explicit statement of the FreeSurfer dependency** (`mris_flatten`) beyond being
  implied by the module.

## Fixed documentation

### Summary
Perform flattening of a brain using freesurfer.

### Parameters
- **fs_subject** : str
    Freesurfer subject ID
- **hemi** : str ['lh' | 'rh']
    hemisphere to flatten
- **patch** : str
    name for freesurfer patch (used as `name` argument to format output of `get_paths()`)
- **freesurfer_subject_dir** : str
    Freesurfer subjects directory location. None defaults to $SUBJECTS_DIR
- **save_every** : int
    If not None, this saves a version of the mesh every `save_every` iterations of the
    flattening process. Useful for determining why a flattening fails.

### Returns
- **flattened** : bool
    `True` if flattening was run (and `mris_flatten` succeeded); `False` if the user
    declined the confirmation prompt (in which case nothing was run).

### Raises
- `subprocess.CalledProcessError` — the `mris_flatten` command exits non-zero.

### Notes
- **Requires FreeSurfer** (`mris_flatten` on `PATH`).
- **Blocks on an interactive `input()` confirmation prompt** ("Flattening takes
  approximately 2 hours! Continue?") before running — not usable unattended without
  modification.
- Runs synchronously; can take on the order of hours for a full flattening.
- Per the source docstring's own `Notes`: there's no live progress feedback beyond
  `save_every`-based intermediate mesh saves; a possible future improvement would be
  streaming `mris_flatten`'s stdout to detect/report progress.

### Example
```python
import cortex.freesurfer as fs

# Requires FreeSurfer and a pre-existing lh.<patch>.patch.3d file for subject "S1".
# Blocks on a confirmation prompt, then runs mris_flatten (can take ~2 hours).
success = fs.flatten("S1", "lh", "flatten_patch", save_every=50)
```

## Confidence / open questions
- Did not run `mris_flatten` in this pass.
- **Recommendation for maintainers:** fill in the empty `Returns` section; document the
  interactive prompt and add a non-interactive override for scripted use.
