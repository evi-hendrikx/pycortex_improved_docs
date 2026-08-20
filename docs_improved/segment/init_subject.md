# cortex.segment.init_subject

## Current signature (from source)
```python
def init_subject(subject, filenames, do_import_subject=False, **kwargs):
```

## Where this is documented today
- Source docstring: [cortex/segment.py:24-51](cortex/segment.py#L24-L51)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.segment.init_subject.html

## Issues with current documentation
- **No Returns section** — returns `None` always.
- **No Raises section** — `subprocess.call`'s return code for the initial `recon-all`
  command (importing the anatomical) is not checked, so a failure there is silent; only
  `cortex.freesurfer.autorecon`'s own internal `subprocess.check_call` (in the subsequent
  full recon step) would actually raise on failure.
- **`**kwargs`'s forwarding target is named ("passed to cortex.freesurfer.autorecon()")
  but not enumerated** — doesn't list `autorecon`'s actual parameters (`type`, `parallel`,
  `n_cores`) or that `autorecon` itself blocks on an interactive confirmation prompt for
  most `type` values (see `freesurfer/autorecon.md`).
- **The deprecated `run_all` kwarg (still handled for backward compatibility) isn't
  mentioned in the `Parameters` section** — only discoverable by reading the function body.

## Fixed documentation

### Summary
Run the first initial segmentation for a subject's anatomy (in Freesurfer). This function
creates a Freesurfer subject and runs autorecon-all, then (optionally) imports the subject
into the pycortex database.

NOTE: This function requires a functional Freesurfer install! Also, still can't handle T2
weighted anatomical volume input. Please use Freesurfer directly (and then import) for
advanced recon-all input options; this is just a convenience function.

### Parameters
- **subject** : str
    The name of the subject (this subject is created in the Freesurfer SUBJECTS_DIR)
- **filenames** : str or list
    Freesurfer-compatible filename(s) for the anatomical image(s). This can be the first
    dicom file of a series of dicoms, a nifti file, an mgz file, etc.
- **do_import_subject** : bool
    Whether to import the Freesurfer-processed subject (without further editing) into
    pycortex. False by default, since we recommend editing (or at least inspecting) the
    brain mask and white matter segmentations prior to importing into pycortex.
- **\*\*kwargs** : keyword arguments passed to `cortex.freesurfer.autorecon()`
    Useful ones: `parallel=True`, `n_cores=4` (or more, if you have them). See
    `freesurfer/autorecon.md` for the full parameter list and its own interactive-prompt
    behavior. `run_all` (deprecated, still accepted) sets `do_import_subject` instead.

### Returns
`None`.

### Raises
- Propagates `subprocess.CalledProcessError` from `cortex.freesurfer.autorecon`'s internal
  `recon-all` call. The function's own initial `recon-all` import step (for the raw
  anatomical) does not check its return code, so a failure there is silent and the
  function proceeds regardless.

### Notes
- **Requires a functional FreeSurfer install** (`recon-all` on `PATH`).
- Runs two long external processes synchronously: an initial `recon-all` import of the
  anatomical, then the full `autorecon-all` pipeline via `cortex.freesurfer.autorecon`
  (which itself may block on an interactive confirmation prompt — see
  `freesurfer/autorecon.md`).
- Does not currently support T2-weighted input.

### Example
```python
import cortex

# Requires FreeSurfer installed. Blocks for a long time (recon-all can take hours);
# autorecon() may also prompt for interactive confirmation.
cortex.segment.init_subject("S1", "/path/to/anatomical.nii.gz", parallel=True, n_cores=4)
```

## Confidence / open questions
- Did not run FreeSurfer's `recon-all` in this pass.
- **Recommendation for maintainers:** check the initial `recon-all` call's return code;
  document `run_all`'s deprecation in the `Parameters` section, not just handle it
  silently.
