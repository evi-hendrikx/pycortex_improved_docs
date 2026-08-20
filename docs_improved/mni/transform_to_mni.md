# cortex.mni.transform_to_mni

## Current signature (from source)
```python
def transform_to_mni(volumedata, func_to_mni, template=default_template):
```

## Where this is documented today
- Source docstring: [cortex/mni.py:76-97](cortex/mni.py#L76-L97)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.mni.transform_to_mni.html

## Issues with current documentation
- **No Raises section** — same unchecked-`subprocess.call` issue as
  `compute_mni_transform` (a failed `flirt` surfaces as a confusing downstream error from
  `nibabel.load` on a missing output file, not a clear message).
- **No mention this requires FSL**, nor that `volumedata` must support `.save_nii` (i.e.
  be a `Volume`/`VolumeData`, not an arbitrary array — the docstring's type is stated as
  "VolumeData" but doesn't cross-reference `Volume.save_nii`).
- **Three temp files created and never cleaned up** (`func_nii`, `func_to_mni_xfm`,
  `func_in_mni` — the last one is the actual return value's backing file, so it can't be
  deleted before returning, but is also never cleaned up afterward by the caller since
  there's no indication it's a temp file at all).

## Fixed documentation

### Summary
Transform data in `volumedata` to MNI space, resample at the resolution of the atlas
image.

### Parameters
- **volumedata** : VolumeData
    Data to be transformed to MNI space. Must support `.save_nii` (e.g. a `cortex.Volume`).
- **func_to_mni** : numpy.ndarray
    Transformation matrix from the space of `volumedata` to MNI space. Get this from
    `compute_mni_transform` (or `cortex.db.get_mnixfm`).
- **template** : str, optional
    Path to MNI template volume, used as reference for flirt. Defaults to FSL's
    MNI152_T1_1mm_brain.

### Returns
- **nibabel.nifti1.Nifti1Image**
    `volumedata` after transformation to MNI space. Backed by a temporary file on disk
    (not automatically cleaned up — see Notes).

### Raises
- No explicit exceptions from this function; a failed `flirt` call (return code unchecked)
  surfaces as a `FileNotFoundError`-style error from `nibabel.load` on the missing output.

### Notes
- **Requires FSL** (`flirt`).
- **Leaves temporary files on disk**, including the file backing the returned
  `Nifti1Image` — copy/save the result if you need it to persist beyond the temp
  directory's lifetime, and be aware repeated calls accumulate temp files.

### Example
```python
import cortex

vol = cortex.Volume.random("S1", "fullhead")
func_to_mni = cortex.db.get_mnixfm("S1", "fullhead")
mni_img = cortex.mni.transform_to_mni(vol, func_to_mni)
mni_img.to_filename("s1_in_mni.nii.gz")  # persist beyond the temp file
```

## Confidence / open questions
- Did not run FSL's `flirt` in this pass.
- **Recommendation for maintainers:** check `subprocess.call`'s return code; document that
  the returned image is backed by an uncollected temp file.
