# cortex.utils.get_hemi_masks

## Current signature (from source)
```python
def get_hemi_masks(subject, xfmname, type='nearest'):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:382-397](cortex/utils.py#L382-L397) — `type` has no
  description, `Returns` section is present but empty.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_hemi_masks.html

## Issues with current documentation
- **`type` parameter has no description at all** in the `Parameters` section.
- **`Returns` section header is present but has zero content.**
- **No Raises section** — an unrecognized `type` propagates a bare `KeyError` from
  `cortex.mapper.get_mapper` (see `mapper/get_mapper.md`).
- **Doesn't explain what "hemisphere mask" actually means**: this delegates entirely to
  `cortex.mapper.get_mapper(...).hemimasks` — a volume-shaped boolean mask per hemisphere,
  marking which voxels that hemisphere's surface mapping touches (not a strict left/right
  spatial split — see `mapper/Mapper.md`'s `.hemimasks` property).

## Fixed documentation

### Summary
Returns a binary mask of the left and right hemisphere surface voxels for the given
subject.

### Parameters
- **subject** : str
    Name of subject
- **xfmname** : str
    Name of transform
- **type** : str
    Projection/mapper type used to determine which voxels belong to each hemisphere's
    surface (any `cortex.mapper.get_mapper` projection name, e.g. `'nearest'`,
    `'trilinear'`, `'line_nearest'`). Default `'nearest'`.

### Returns
- **[left_mask, right_mask]** : list of 2 ndarrays of bool, shape matching the reference
  volume
    Per-hemisphere voxel masks (via `cortex.mapper.Mapper.hemimasks`) — `True` where that
    hemisphere's surface mapping touches the voxel.

### Raises
- `KeyError` — `type` is not a recognized `cortex.mapper.get_mapper` projection name.

### Notes
No FreeSurfer/FSL/GUI dependency; requires the subject's surfaces and `xfmname` to already
exist in the pycortex database (mapper cache generated on first use — see
`mapper/get_mapper.md`).

### Example
```python
import cortex

left_mask, right_mask = cortex.utils.get_hemi_masks("S1", "fullhead")
```

## Confidence / open questions
- **Recommendation for maintainers:** fill in `type`'s description and the empty
  `Returns` section.
