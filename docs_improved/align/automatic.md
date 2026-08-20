# cortex.align.automatic

## Current signature (from source)
```python
def automatic(
    subject,
    xfmname,
    reference,
    init="coreg",
    epi_mask=False,
    intermediate=None,
    reference_contrast="t2",
    noclean=False,
):
```
A sibling function, `cortex.align.automatic_fsl(subject, xfmname, reference, noclean=False,
bbrtype="signed", pre_flirt_args="")`, implements the same operation using FSL's FLIRT/BBR
instead of FreeSurfer's `bbregister`/`mri_coreg`. Not in the requested scope list, but
referenced here since `automatic`'s own docstring points to it directly.

## Where this is documented today
- Source docstring: [cortex/align.py:350-412](cortex/align.py#L350-L412)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.align.automatic.html

## Issues with current documentation
- **No Returns section is entirely accurate this time** (it exists and is correct: "None or
  path to temp directory if noclean is True") — flagged here as one of the *better*-
  documented functions in this codebase, for contrast with most others.
- **No Raises section.** `IOError` is raised if the `bbregister` subprocess call returns
  non-zero; this isn't mentioned.
- **No mention of the required environment.** Silently assumes a working FreeSurfer
  environment (`bbregister` on `PATH`, `$SUBJECTS_DIR` set, `subject` already `recon-all`'d)
  — not stated anywhere in the docstring, only discoverable by reading the implementation.
- **`init`'s docstring describes 4 modes reasonably well** but doesn't explicitly state
  what happens if none of `"coreg"`/`"fsl"`/`"header"` match and the string also isn't a
  valid path — `os.path.abspath(init)` never fails on its own (it's pure string
  manipulation), so an invalid `init` string silently becomes a nonexistent `--init-reg`
  path, which only surfaces later as an opaque `bbregister` failure (`IOError`).
- **A stray, no-op `.format(sub=subject, absref=reference, cache=cache)` call remains in the
  source** (`align.py:437`) — the command string `cmd` was already fully built via an
  f-string a few lines earlier, so this `.format()` call has nothing left to substitute and
  does nothing (silently — since there are no unescaped `{}` left in the string). This isn't
  a documentation issue exactly, but it's dead/vestigial code from what looks like a
  refactor from `.format()`-style to f-strings; flagged in `_notes.md`, not fixed here.
- **No Examples section**, and no mention that this launches a lengthy external process
  (registration can take from seconds to a couple of minutes depending on data) that blocks
  until complete (synchronous `subprocess.call`).
- **The printed "mincost" quality summary is a useful diagnostic that's undocumented as a
  return-adjacent side effect** — the function prints `bbregister`'s registration quality
  score to stdout but does not return it; a caller who wants the numeric value
  programmatically must re-read `<cache>/register.dat.mincost` themselves before `noclean`
  cleanup deletes it (impossible unless `noclean=True`) — this limitation isn't mentioned.

## Fixed documentation

### Summary
Perform automatic alignment using Freesurfer's boundary-based registration. The
`reference` image and resulting transform called `xfmname` are stored in the database.

### Parameters
- **subject** : str
    Subject identifier.
- **xfmname** : str
    Name of the transform to be created and stored in the database.
- **reference** : str
    Path to a nibabel-readable image used as the reference for this transform. Usually a
    single (3D) functional data volume.
- **init** : str, default `"coreg"`
    One of `"coreg"`, `"fsl"`, `"header"`, or a path to a transform from the reference
    volume to the anatomical volume. `"coreg"` uses Freesurfer's `mri_coreg` and generally
    performs best; `"fsl"` uses FSL's FLIRT; `"header"` assumes the reference and
    anatomical are already close (same-session acquisitions). An invalid path here isn't
    validated up front — it only surfaces as an opaque `bbregister` failure.
- **epi_mask** : bool, default `False`
    If `True`, passes `--epi-mask` to `bbregister` to mask out spatially distorted areas.
    Recommended when the reference was not distortion corrected.
- **intermediate** : str, optional
    Path to a nibabel-readable image used as an intermediate volume for alignment, useful
    if the reference has a small field-of-view and a whole-brain image from the same
    session is available.
- **reference_contrast** : str, default `"t2"`
    Contrast of the reference image, used to set the `bbregister` contrast flag. `"t2"`
    (BOLD): gray matter brighter than white matter. `"t1"`: the opposite.
- **noclean** : bool, default `False`
    If `True`, intermediate files are not removed from `/tmp` and the returned value is
    the temp directory path.

### Returns
`None`, unless `noclean=True`, in which case the `str` path to the (not-deleted) temporary
working directory is returned (containing, among other files, `register.dat.mincost` with
the registration quality diagnostics).

### Raises
- `IOError` — the `bbregister` subprocess exits with a non-zero status (e.g. FreeSurfer not
  installed/configured, invalid `init` path, `subject` not `recon-all`'d).
- A `UserWarning`-style message is printed via `warnings.warn` on every call (not an
  exception) noting that pycortex 1.2.8+ defaults changed to use `bbregister`/`mri_coreg`
  and pointing to `automatic_fsl` for the old FSL-based behavior.

### Notes
- **Requires a working FreeSurfer installation** (`bbregister`, and `mri_coreg` if
  `init='coreg'`) with `$SUBJECTS_DIR` set and `subject` already processed by `recon-all`.
- Synchronous/blocking — runs an external registration process that can take anywhere from
  seconds to a few minutes.
- Prints the registration quality ("mincost", 0=perfect, values under ~0.5 considered good)
  to stdout, but does not return it programmatically; pass `noclean=True` and read
  `<returned_path>/register.dat.mincost` yourself if you need the number in code.
- On success, saves a `'coord'`-type transform for `(subject, xfmname)` to the pycortex
  database.
- Recommended follow-up (per the docstring): open the result in
  `cortex.align.manual(subject, xfmname)` to visually inspect/fine-tune it.
- Sibling function `cortex.align.automatic_fsl` performs the equivalent alignment using
  FSL's FLIRT/BBR instead — useful if FreeSurfer's `bbregister` performs poorly for your
  data, or FreeSurfer isn't available but FSL is.

### Example
```python
import cortex

# Requires a FreeSurfer-processed subject "S1" and a functional reference volume.
# This call blocks until FreeSurfer's bbregister finishes (no GUI).
cortex.align.automatic(
    "S1",
    "auto_example",
    reference="/path/to/functional_reference.nii.gz",
    reference_contrast="t2",
)

# Recommended: visually inspect the result afterward
cortex.align.manual("S1", "auto_example", inspect_only=True)
```

## Confidence / open questions
- Could not run `bbregister` in this pass to confirm exact failure messages or timing —
  described from source/documentation only.
- The no-op `.format(...)` call is confirmed by static reading (`align.py:425-437`: the
  f-string already interpolates `subject`, and the subsequent `.format()` call has no
  `{sub}`/`{absref}`/`{cache}` placeholders left to fill), not by execution, though this is
  a low-risk/purely-cosmetic observation.
- **Recommendation for maintainers:** state the FreeSurfer/`$SUBJECTS_DIR` requirement
  explicitly in the docstring; add a Raises section; consider validating `init` when it's
  neither a known keyword nor an existing file path, to fail fast with a clear message
  instead of a late, opaque `bbregister` error; remove the vestigial no-op `.format()` call.
