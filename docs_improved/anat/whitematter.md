# cortex.anat.whitematter

## Current signature (from source)
```python
def whitematter(outfile, subject, do_voxelize=False):
```

## Where this is documented today
- Source docstring: none. [cortex/anat.py:24-69](cortex/anat.py#L24-L69)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.anat.whitematter.html
  (no docstring content beyond the bare signature).

## Issues with current documentation
- **No docstring at all**, despite non-trivial, three-tier fallback logic and multiple
  external tool dependencies (`cortex.polyutils.voxelize`, a FreeSurfer-derived `raw_wm`
  volume, or FSL's `fast`).
- **`do_voxelize` is misleadingly named/gated.** Reading the body: if `do_voxelize=True`,
  it calls `voxelize(outfile, subject, surf="wm")` and, on success, returns without
  attempting anything else. If `do_voxelize=False` (the default) **or** if voxelizing
  raises anything other than `IOError`, the `try` block's `raise IOError` (when
  `do_voxelize=False`) or a real exception from `voxelize` both fall into the `except
  IOError:` handler — but `voxelize` itself can raise things other than `IOError` (e.g. if
  `db.get_surf`/`polyutils.voxelize` fail differently), in which case those propagate
  uncaught rather than falling through to the FreeSurfer/FSL fallback. This distinction is
  invisible without reading the source.
- **Undocumented fallback chain**: tries a FreeSurfer-derived `raw_wm` volume first
  (thresholding label value 250), and if that raises *any* exception, falls back to FSL's
  `fast` segmentation (with a further internal fallback to `--nopve --nobias` if the first
  `fast` attempt produces an all-zero mask). None of this is stated anywhere.
- **No Returns section** — always returns `None` (unlike `voxelize`, which returns an
  array).
- **No mention of required external tools** (FreeSurfer-processed data, or FSL's `fast`)
  depending on which fallback path is taken.
- **Bare `except:` clause** in the FreeSurfer-attempt block (catches literally any
  exception, including e.g. `KeyboardInterrupt`) before falling back to FSL — a code
  smell, not fixed here per project scope, flagged in `_notes.md`.

## Fixed documentation

### Summary
Generates a white-matter mask for `subject`, writing it to `outfile`, trying (in order) a
directly-voxelized surface, a FreeSurfer-derived segmentation, and FSL's `fast` as
fallbacks.

### Parameters
- **outfile** : str
    Path to write the white-matter mask NIfTI image to.
- **subject** : str
    Subject identifier; must exist in the pycortex database.
- **do_voxelize** : bool, optional
    If `True`, generate the mask by voxelizing the subject's `wm` surface directly (via
    `cortex.anat.voxelize`) instead of using a FreeSurfer/FSL segmentation. Default
    `False`.

### Returns
`None`. Writes `outfile` as a side effect.

### Raises
- Whatever `cortex.anat.voxelize`/`cortex.polyutils.voxelize` raises, if `do_voxelize=True`
  and it fails with something other than `IOError` (not caught by the fallback logic).
- `AssertionError` — an FSL `fast`/`fslmaths` call in the fallback path returns non-zero.
- `AssertionError` — the final generated FSL-based mask sums to less than 0 (in practice
  this condition can never actually trigger, since a non-negative sum is always true for a
  binary mask — see `_notes.md`).

### Notes
- **External dependencies vary by code path**: `do_voxelize=True` needs no external tool
  beyond the subject's surfaces already being in the pycortex database; the default path
  needs either a FreeSurfer-derived `raw_wm` anatomical volume already in the database, or
  (as a further fallback) a working FSL installation (`fast`, `fslmaths`).
- Writes/removes a temporary working directory during the FSL fallback path.

### Example
```python
import cortex

# Voxelize the wm surface directly (no FreeSurfer/FSL segmentation step):
cortex.anat.whitematter("S1_wm_mask.nii.gz", "S1", do_voxelize=True)

# Default: try FreeSurfer-derived segmentation, falling back to FSL fast if needed.
cortex.anat.whitematter("S1_wm_mask.nii.gz", "S1")
```

## Confidence / open questions
- The claim that non-`IOError` exceptions from `voxelize` propagate uncaught (rather than
  triggering the FreeSurfer/FSL fallback) is based on static reading of the `try/except
  IOError` structure in `anat.py:25-30`, not execution.
- Did not run the FreeSurfer or FSL fallback paths in this pass.
- **Recommendation for maintainers:** add a docstring; replace the bare `except:` with a
  narrower exception type; the final `assert arr.sum() >= 0` check appears to be a
  tautology for a mask array (always non-negative) and likely should check for a nonzero
  sum instead, mirroring the earlier all-zero check on the first `fast` attempt — flagged
  as a possible logic bug, not fixed here (see `_notes.md`).
