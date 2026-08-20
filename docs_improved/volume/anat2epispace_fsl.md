# cortex.volume.anat2epispace_fsl

## Current signature (from source)
```python
def anat2epispace_fsl(data, subject, xfmname):
```

## Where this is documented today
- Source docstring: [cortex/volume.py:325-328](cortex/volume.py#L325-L328)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.anat2epispace_fsl.html

## Issues with current documentation
- **No Parameters/Returns/Raises sections at all** beyond a one-line summary.
- **No mention this requires FSL** and shells out to a **hard-coded `"fsl5.0-flirt"`
  binary** (`volume.py:352`), not the configurable `[basic] fsl_prefix` convention used
  elsewhere in pycortex (e.g. `cortex.align`) — will fail with `FileNotFoundError`/
  command-not-found on any system where the FSL executable isn't literally named
  `fsl5.0-flirt` (i.e. most modern FSL installations, which typically just provide
  `flirt`). Flagged as a likely portability bug, not fixed — see `_notes.md`.
- **`data` isn't passed through `cortex.dataset.normalize`** — unlike its sibling
  `epi2anatspace_fsl` (which does normalize its input, in the dead code path), this
  function expects a raw `ndarray` directly, not a `Volume`/`VolumeData` object. Not
  stated, and inconsistent with the rest of this module's conventions.
- **Leftover temp files**: creates `.mat` and `.nii` temp files via `tempfile.mktemp()`
  for the transform and input data; only the final resliced output's `.gz`/input `.nii`
  are cleaned up — the `.mat` transform file is never removed.
- **No indication that this is (per its file position, right after the "broken, do not
  use" `epi2anatspace_fsl`) apparently the still-"working" (non-stubbed-out) direction**
  — worth stating explicitly that, unlike its sibling, this one isn't short-circuited by a
  `NotImplementedError`, though it shares the same hard-coded-binary portability risk.

## Fixed documentation

### Summary
Resamples anat-space data into the epi space for the given subject and transformation,
using FSL's `flirt`.

### Parameters
- **data** : ndarray
    Anatomical-space data to resample (a raw array, matching the subject's raw anatomical
    image's orientation — **not** a `Volume`/`VolumeData` object; unlike some sibling
    functions, this one does not call `cortex.dataset.normalize`).
- **subject** : str
    Name of subject.
- **xfmname** : str
    Name of transform.

### Returns
- **outdata** : ndarray
    The resliced (epi-space) data, loaded back from FSL's output NIfTI file.

### Raises
- `FileNotFoundError`/`OSError`-style failure from `subprocess.call` — if the hard-coded
  `fsl5.0-flirt` binary isn't present under that exact name on `PATH` (see Issues; this
  will affect most modern FSL installations, which typically install a plain `flirt`).
- Propagates errors from `cortex.database.Database.get_xfm`/`get_anat` if `subject`/
  `xfmname` are invalid.

### Notes
- **Requires FSL, specifically a binary literally named `fsl5.0-flirt`** on `PATH` — does
  not respect pycortex's usual `[basic] fsl_prefix` configuration used elsewhere (e.g.
  `cortex.align`). Likely to fail outright on any FSL install that only provides `flirt`.
- **Leaves a temporary `.mat` transform file on disk**, uncollected (the `.nii` input and
  `.nii.gz` output are cleaned up; the `.mat` is not).
- Unlike `epi2anatspace_fsl` (its sibling, in the opposite direction), this function is
  **not** stubbed out with `NotImplementedError` — but shares the same hard-coded-binary
  risk.

### Example
```python
import numpy as np
import cortex

anat = cortex.db.get_anat("S1", "raw")
anat_data = np.asarray(anat.dataobj).T

# Requires FSL with a binary literally named "fsl5.0-flirt" on PATH.
epi_data = cortex.volume.anat2epispace_fsl(anat_data, "S1", "fullhead")
```

## Confidence / open questions
- Did not run FSL's `flirt`/`fsl5.0-flirt` in this pass; the hard-coded-binary-name
  concern is based on static reading of `volume.py:352` and general knowledge that recent
  FSL packaging conventions typically install `flirt` without the `fsl5.0-` prefix — not
  independently verified against a specific FSL version's actual binary naming.
- **Recommendation for maintainers:** replace the hard-coded `"fsl5.0-flirt"` with
  `"{fsl_prefix}flirt"` (matching `cortex.align`'s convention); add
  Parameters/Returns/Raises; clean up the leftover `.mat` temp file; consider normalizing
  `data` via `cortex.dataset.normalize` for consistency with `epi2anatspace_fsl`.
