# cortex.mni.compute_mni_transform

## Current signature (from source)
```python
def compute_mni_transform(subject, xfm, template=default_template):
```
`default_template` is `$FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz`, computed at
import time (falling back to `/usr/share/fsl/5.0` with a warning if `$FSLDIR` is unset).

## Where this is documented today
- Source docstring: [cortex/mni.py:32-50](cortex/mni.py#L32-L50) — one of the more
  complete docstrings found in this codebase (has Parameters and Returns).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.mni.compute_mni_transform.html

## Issues with current documentation
- **No Raises section.** `subprocess.call(cmd)`'s return code is never checked — if FSL's
  `flirt` isn't installed or fails, the function silently continues and later raises a
  confusing `OSError`/parse error from `np.loadtxt(anat_to_mni_xfm)` trying to read a
  nonexistent or empty output file, rather than a clear "flirt failed" message.
- **No mention this requires FSL** (`flirt`), nor of the `$FSLDIR`/`fsl_prefix`
  configuration this module depends on at import time.
- **Leftover temp file**: `anat_to_mni_xfm = tempfile.mktemp()` is created and never
  cleaned up after use.
- **No mention this is cached elsewhere** — `cortex.database.Database.get_mnixfm` wraps
  this exact function with disk caching; a user who doesn't know that may unnecessarily
  recompute this (slow, FSL-based) transform repeatedly instead of using `db.get_mnixfm`.

## Fixed documentation

### Summary
Compute transform from the space specified by `xfm` to MNI standard space.

### Parameters
- **subject** : str
    Subject identifier
- **xfm** : str
    Name of functional space transform. Can be 'identity' for anat space.
- **template** : str, optional
    Path to MNI template volume. Defaults to FSL's MNI152_T1_1mm_brain.

### Returns
- **numpy.ndarray**
    Transformation matrix from the space specified by `xfm` to MNI space.

### Raises
- No explicit exceptions raised by this function itself, but a failed `flirt` call (return
  code not checked) will typically surface as an unrelated `OSError`/parsing error a few
  lines later when the (missing or empty) output matrix file is loaded.
- Propagates errors from `cortex.database.Database.get_anat`/`get_xfm` if `subject`/`xfm`
  are invalid.

### Notes
- **Requires FSL** (`flirt` on `PATH`, respecting `[basic] fsl_prefix`) and the `$FSLDIR`
  environment variable (used to locate the default MNI template at import time).
- Leaves a temporary `.mat`-format file on disk (via `tempfile.mktemp()`, not cleaned up).
- **Prefer `cortex.db.get_mnixfm(subject, xfm)`** for typical use — it wraps this exact
  computation with disk caching, avoiding redundant (slow) `flirt` runs.

### Example
```python
import cortex

# Requires FSL installed and configured ($FSLDIR set).
func_to_mni = cortex.mni.compute_mni_transform("S1", "fullhead")
```

## Confidence / open questions
- Did not run FSL's `flirt` in this pass.
- **Recommendation for maintainers:** check `subprocess.call`'s return code and raise a
  clear error on failure; clean up the temp file; cross-reference `db.get_mnixfm` from
  this docstring.
