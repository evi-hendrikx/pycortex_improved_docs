# cortex.utils.get_aseg_mask

## Current signature (from source)
```python
def get_aseg_mask(subject, aseg_name, xfmname=None, order=1, threshold=None, **kwargs):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:605-644](cortex/utils.py#L605-L644) — already
  thorough (Parameters, Returns, Notes with a cross-reference).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_aseg_mask.html

## Issues with current documentation
- **No Raises section** — raises `ValueError` ("Unknown aseg_name!") if `aseg_name`
  doesn't match any partition name (exact or substring), not documented.
- **`**kwargs` forwarding target unstated** — forwarded to `cortex.volume.anat2epispace`
  (only when `xfmname` is given); its accepted keywords aren't enumerated here (see
  `volume/anat2epispace.md`).
- **The docstring's own cross-reference typo**: says "See also
  `cortex.freesurfer.fs_aseg_mask.keys()`" — the actual dict is `fs_aseg_dict` (imported as
  `from .freesurfer import fs_aseg_dict`), not `fs_aseg_mask`. `fs_aseg_mask` does not
  exist. This is a real docstring error (wrong attribute name), not fixed here.

## Fixed documentation

### Summary
Return an epi space mask of the given ID from freesurfer's automatic segmentation.

### Parameters
- **subject** : str
    pycortex subject ID
- **aseg_name** : str or list
    Name of brain partition or partitions to return. See freesurfer web site for
    partition names:
    https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/AnatomicalROI/FreeSurferColorLUT
    ... or inspect `cortex.freesurfer.fs_aseg_dict.keys()` (the shipped docstring
    incorrectly names this `fs_aseg_mask` — see Issues). Currently (2017.03) only the
    first 256 indices in the freesurfer lookup table are supported. If a name is provided
    that does not exactly match any of the freesurfer partitions, the function will search
    for all partitions that contain that name (caps are ignored). For example,
    'white-matter' will generate a mask that combines masks for the following partitions:
    'Right-Cerebral-White-Matter', 'Left-Cerebellum-White-Matter',
    'Right-Cerebellum-White-Matter', and 'Left-Cerebral-White-Matter').
- **xfmname** : str
    Name for transform of mask to functional space. If `None`, anatomical-space mask is
    returned.
- **order** : int, [0-5]
    Order of spline interpolation for transform from anatomical to functional space
    (ignored if xfmname is None). 0 is like nearest neighbor; 1 returns bilinear
    interpolation of mask from anatomical space. To convert either of these volumes to a
    binary mask for voxel selection, set the `threshold` argument. Setting order > 1 is
    not recommended, as it will give values outside the range of 0-1.
- **threshold** : scalar
    Threshold value for aseg mask. If None, function returns result of spline
    interpolation of mask as transformed to functional space (will have continuous float
    values from 0-1)
- **\*\*kwargs**
    Forwarded to `cortex.volume.anat2epispace` (only used when `xfmname` is given) — see
    `volume/anat2epispace.md`.

### Returns
- **mask** : array
    array with float or boolean values denoting the location of the requested cortical
    partition.

### Raises
- `ValueError` — `aseg_name` (or, for a list, any entry) doesn't exactly match, or
  substring-match, any known freesurfer aseg partition name ("Unknown aseg_name!").

### Notes
See also `get_anat(subject, type='aseg')`.

No FreeSurfer/FSL/GUI dependency at call time (requires `subject`'s `aseg` anatomical
already generated/imported — see `cortex.database.Database.get_anat`).

### Example
```python
import cortex

mask = cortex.utils.get_aseg_mask("S1", "white-matter", xfmname="fullhead", threshold=0.5)
```

## Confidence / open questions
- The `fs_aseg_mask` vs. `fs_aseg_dict` naming discrepancy is confirmed by direct reading
  of the import statement (`from .freesurfer import fs_aseg_dict`, `utils.py:27`) vs. the
  docstring text (`utils.py:615`).
- **Recommendation for maintainers:** fix the `fs_aseg_mask` → `fs_aseg_dict` typo in the
  docstring; add a Raises section.
