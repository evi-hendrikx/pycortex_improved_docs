# cortex.mni.transform_mni_to_subject

## Current signature (from source)
```python
def transform_mni_to_subject(subject, xfm, volarray, func_to_mni, template=default_template):
```

## Where this is documented today
- Source docstring: [cortex/mni.py:154-179](cortex/mni.py#L154-L179)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.mni.transform_mni_to_subject.html

## Issues with current documentation
- **No Raises section** — same unchecked-`subprocess.call` issue as its siblings.
- **No mention this requires FSL.**
- **`volarray`'s shape requirement is stated loosely** ("should have same size as
  `template`") — doesn't state this isn't validated by the function itself; a
  mismatched-shape `volarray` will be silently written with `template`'s affine
  (`nibabel.Nifti1Image(volarray, affine)`) and only fail later, opaquely, inside `flirt`.
- **Temp files created and never cleaned up**, same pattern as `transform_to_mni`.

## Fixed documentation

### Summary
Transform data in `volarray` from MNI space to functional space specified by `xfm`.

### Parameters
- **subject** : str
    Subject identifier
- **xfm** : str
    Name of functional space that data will be transformed into.
- **volarray** : numpy.ndarray
    3D volume in MNI space (should have same size as `template`; not validated by this
    function — a mismatched shape will only fail inside the `flirt` subprocess call).
- **func_to_mni** : numpy.ndarray
    Transformation matrix from `xfm` space to MNI space. Get this from
    `compute_mni_transform`.
- **template** : str, optional
    Path to MNI template volume, used as reference. Defaults to FSL's MNI152_T1_1mm_brain.

### Returns
- **nibabel.nifti1.Nifti1Image**
    `volarray` after transformation from MNI space to space specified by `xfm`. Backed by
    a temporary file on disk (not automatically cleaned up — see Notes).

### Raises
- No explicit exceptions from this function; a failed `flirt` call (return code unchecked)
  or a shape mismatch between `volarray` and `template` surfaces as an opaque error from
  `flirt` or from `nibabel.load` on a missing/malformed output file.

### Notes
- **Requires FSL** (`flirt`).
- **Leaves temporary files on disk**, including the file backing the returned
  `Nifti1Image`.

### Example
```python
import cortex
import numpy as np

func_to_mni = cortex.db.get_mnixfm("S1", "fullhead")
mni_volume = np.random.randn(182, 218, 182)  # matching the MNI152 1mm template shape
result_img = cortex.mni.transform_mni_to_subject("S1", "fullhead", mni_volume, func_to_mni)
```

## Confidence / open questions
- Did not run FSL's `flirt` in this pass.
- **Recommendation for maintainers:** check `subprocess.call`'s return code and validate
  `volarray`'s shape against `template` up front; document/clean up the temp files.
