# cortex.utils.get_cortical_mask

## Current signature (from source)
```python
def get_cortical_mask(subject, xfmname, type='nearest'):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:293-321](cortex/utils.py#L293-L321) — already
  reasonably complete.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_cortical_mask.html

## Issues with current documentation
- **No Raises section** — an unrecognized `type` falls through to
  `get_mapper(subject, xfmname, type=type).mask`, which raises a bare `KeyError` (see
  `mapper/get_mapper.md`) rather than a clear message specific to this function.
- **The `'cortical'` branch's `print("%0.3f%%"%(...))` progress-printing side effect
  (every 100 vertices) isn't mentioned** — can be noisy for large surfaces.
- **No mention this is the auto-generation target of `cortex.db.get_mask`** when a named
  mask isn't already cached — `Database.get_mask` calls this function internally on a
  cache miss.

## Fixed documentation

### Summary
Gets the cortical mask for a particular transform.

### Parameters
- **subject** : str
    Subject name
- **xfmname** : str
    Transform name
- **type** : str
    Mask type, one of {"cortical", "thin", "thick", "nearest", "line_nearest"}.
    - 'cortical' includes voxels contained within the cortical ribbon, between the
      freesurfer-estimated white matter and pial surfaces.
    - 'thin' includes voxels that are < 2mm away from the fiducial surface.
    - 'thick' includes voxels that are < 8mm away from the fiducial surface.
    - 'nearest' includes only the voxels overlapping the fiducial surface.
    - 'line_nearest' includes all voxels that have any part within the cortical ribbon.

### Returns
- **mask** : array
    boolean mask array for cortical voxels in functional space

### Raises
- `KeyError` — `type` is not one of the five documented values *and* isn't a recognized
  `cortex.mapper.get_mapper` projection type either (falls through to `get_mapper`, which
  raises `KeyError` for an unrecognized `type`; see `mapper/get_mapper.md`).

### Notes
"nearest" is a conservative "cortical" mask, while "line_nearest" is a liberal "cortical"
mask.

The `'cortical'` branch prints progress (`"X.XXX%"`) to stdout every 100 vertices — can be
noisy for large surfaces, no way to silence via a parameter.

Auto-generation target of `cortex.db.get_mask(subject, xfmname, type)` on a cache miss —
most users will go through that (cached) entry point rather than calling this directly.

### Example
```python
import cortex

mask = cortex.utils.get_cortical_mask("S1", "fullhead", type="thin")

# More typical usage (handles caching):
mask = cortex.db.get_mask("S1", "fullhead", "thin")
```

## Confidence / open questions
- **Recommendation for maintainers:** raise a clearer error for an unrecognized `type`
  rather than falling through to a mapper-related `KeyError`; add a Raises section.
