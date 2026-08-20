# cortex.volume.epi2anatspace_fsl

## Current signature (from source)
```python
def epi2anatspace_fsl(volumedata):
```

## Where this is documented today
- Source docstring: [cortex/volume.py:274-277](cortex/volume.py#L274-L277)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.epi2anatspace_fsl.html

## Issues with current documentation
- **The docstring is misleading about what the function does — it doesn't do anything.**
  Immediately after the docstring, the function body is: `#This function is currently
  broken! do not use it! \n raise NotImplementedError` — **every call to this function
  raises `NotImplementedError` unconditionally**, before any of the ~40 lines of
  (otherwise plausible-looking) FSL-based resampling code that follows ever execute. The
  docstring itself gives no hint of this — a reader would reasonably expect this function
  to work.
- **No Raises section** documenting the guaranteed `NotImplementedError`.
- **The dead code that follows uses a hard-coded `"fsl5.0-flirt"` binary name** (not the
  configurable `[basic] fsl_prefix` convention used elsewhere in pycortex, e.g.
  `cortex.align`) — even if un-commented and fixed, this would only work with that exact,
  very old, Ubuntu-style FSL package naming.

## Fixed documentation

### Summary
**Not implemented — always raises `NotImplementedError`.** Intended to resample epi-space
data into the anatomical space for a given subject/transform using FSL's `flirt`
(mirroring `anat2epispace_fsl`'s working implementation, in the opposite direction), but
the current implementation is explicitly marked broken in a source comment and short-
circuits before doing any real work.

### Parameters
- **volumedata** : VolumeData
    (Documented for completeness — not actually usable, since the function always raises
    before touching this argument.)

### Returns
N/A — never returns; always raises.

### Raises
- `NotImplementedError` — **unconditionally**, on every call.

### Notes
- **Do not use.** Per the function's own source comment: `"This function is currently
  broken! do not use it!"`.
- The unreachable code that follows the `raise` would (if ever restored) require FSL with
  the specific legacy binary name `fsl5.0-flirt`, not respecting pycortex's usual
  `[basic] fsl_prefix` configuration.
- For the working, opposite-direction transform, see `cortex.volume.anat2epispace_fsl`.

### Example
```python
import cortex

vol = cortex.Volume.random("S1", "fullhead")
try:
    cortex.volume.epi2anatspace_fsl(vol)
except NotImplementedError:
    print("epi2anatspace_fsl is currently unimplemented/broken; use epi2anatspace instead.")
```

## Confidence / open questions
- Confirmed by direct reading of `volume.py:274-279` — the `raise NotImplementedError`
  is unconditional and precedes all other logic in the function body.
- **Recommendation for maintainers:** either fix and re-enable this function (updating
  the hard-coded `fsl5.0-flirt` to use `fsl_prefix`) or remove the dead code entirely and
  document that `epi2anatspace` (the pure-scipy version) is the supported alternative.
