# cortex.anat.brainmask

## Current signature (from source)
```python
def brainmask(outfile, subject):
```

## Where this is documented today
- Source docstring: none. [cortex/anat.py:17-22](cortex/anat.py#L17-L22)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.anat.brainmask.html
  (no docstring content to render beyond the bare signature).

## Issues with current documentation
- **No docstring at all.** Parameters, return value, side effects, and the FSL dependency
  are entirely undocumented.
- **No indication that this requires FSL** (`bet`, via the configured `fsl_prefix`) to be
  installed and on `PATH`.
- **Failure mode is an `assert`, not an exception with a message aimed at users** —
  `assert sp.call(...) == 0, "Error calling fsl-bet"` raises a bare `AssertionError` if
  `bet` fails or isn't found, which is easy to miss in a stack trace.

## Fixed documentation

### Summary
Brain-extracts (skull-strips) a subject's raw anatomical image using FSL's `bet`, writing
the result to `outfile`.

### Parameters
- **outfile** : str
    Path to write the brain-masked NIfTI image to.
- **subject** : str
    Subject identifier; must exist in the pycortex database with a `raw` anatomical image
    (`cortex.db.get_anat(subject, type='raw')`).

### Returns
`None`. Writes `outfile` as a side effect.

### Raises
- `AssertionError` — the FSL `bet` call returns a non-zero exit status (e.g. FSL not
  installed, `fsl_prefix` misconfigured in `options.cfg`, or `subject` has no raw
  anatomical image in the database).

### Notes
- **Requires FSL** (`bet` on `PATH`, honoring the `[basic] fsl_prefix` config option).
- Prints progress (`'Brain masking anatomical...'`) and the exact shell command run.

### Example
```python
import cortex

# Requires FSL and a subject "S1" with a raw anatomical image already in the
# pycortex database.
cortex.anat.brainmask("S1_brainmask.nii.gz", "S1")
```

## Confidence / open questions
- Did not run FSL's `bet` in this pass to confirm exact failure behavior/output format —
  described from source reading only.
- **Recommendation for maintainers:** add a docstring (none exists currently); raise a more
  informative exception than a bare `AssertionError` on `bet` failure.
