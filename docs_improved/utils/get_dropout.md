# cortex.utils.get_dropout

## Current signature (from source)
```python
def get_dropout(subject: str, xfmname: str, power: float = 20):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:888-917](cortex/utils.py#L888-L917)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_dropout.html

## Issues with current documentation
- **`power`'s description is a bare colon** (`power :` with nothing after it) — no
  explanation of what the exponent controls.
- **No Raises section.**
- **Algorithm not explained**: the docstring doesn't describe *how* dropout is estimated
  (from the intensity of the transform's reference EPI image — low-intensity voxels are
  assumed to reflect signal dropout — with `power` controlling how sharply low-intensity
  regions are emphasized: `(1 - normalized_intensity) ** power`).
  4D reference images are automatically collapsed by averaging across the first axis, not
  documented.
- **Already used and partially explained in `quickflat/make_figure.md`'s Issues section**
  (as the default `with_dropout=True` implementation) — worth a direct cross-reference
  from here too.

## Fixed documentation

### Summary
Create a dropout Volume showing where EPI signal is very low.

### Parameters
- **subject** : str
    Name of subject
- **xfmname** : str
    Name of transform
- **power** : float, optional
    Exponent controlling how sharply low-intensity (likely-dropout) regions are
    emphasized in the output: the reference image is normalized to [0, 1], inverted, and
    raised to `power` — i.e. `(1 - normalized_intensity) ** power`. Higher values
    concentrate high output values more tightly on the very lowest-intensity voxels.
    Default 20.

### Returns
- **volume** : `cortex.Volume`
    Pycortex volume of low signal locations (higher values = more likely dropout), scaled
    roughly to [0, 1].

### Raises
Propagates errors from `cortex.database.Database.get_xfm` if `subject`/`xfmname` are
invalid.

### Notes
- If the transform's reference image is 4D (a time series), it is collapsed to 3D by
  averaging across the first axis before computing dropout.
- Voxels with exactly zero intensity are replaced with the mean of all nonzero voxels
  before normalization (to avoid a spurious all-dropout signal from background/masked
  voxels).
- No FreeSurfer/FSL/GUI dependency.
- This is the function used internally by `cortex.quickflat.make_figure`'s
  `with_dropout=True`/numeric-power behavior — see `quickflat/make_figure.md`.

### Example
```python
import cortex

dropout_vol = cortex.utils.get_dropout("S1", "fullhead", power=20)
cortex.quickflat.make_png("dropout.png", dropout_vol)
```

## Confidence / open questions
- **Recommendation for maintainers:** fill in `power`'s description (currently blank);
  add a Returns-adjacent note about the 4D-reference-image averaging and zero-intensity
  handling.
