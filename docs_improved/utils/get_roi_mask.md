# cortex.utils.get_roi_mask

## Current signature (from source)
```python
def get_roi_mask(subject, xfmname, roi=None, projection='nearest'):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:571-590](cortex/utils.py#L571-L590) — already states
  the deprecation and has Parameters/Returns.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_roi_mask.html

## Issues with current documentation
- **No Raises section.**
- **No mention that this uses `Mapper.backwards` internally**, i.e. the "approximate
  inverse" projection described in `mapper/Mapper.md` — the returned masks are
  **continuous-valued** (not boolean), since `mapper.backwards` produces float voxel
  values from a least-squares solve, not a binary mask. This important detail (the output
  is not a clean boolean mask despite the function's name) is not documented.
- **A dead code comment right in the function body** ("This is broken; unclear when/if
  backward mappers ever worked this way") documents an abandoned alternative
  implementation path — worth surfacing to a reader as evidence that this function's
  reliability has been historically uncertain, reinforcing why `get_roi_masks` (plural) is
  the recommended replacement.

## Fixed documentation

### Summary
Return a mask for the given ROI(s). **Deprecated** — use `get_roi_masks` (plural) instead.

### Parameters
- **subject** : str
    Name of subject
- **xfmname** : str
    Name of transform
- **roi** : tuple
    Name of ROI(s) to get masks for. None gets all of them.
- **projection** : str
    Which mapper to use.

### Returns
- **output** : dict
    Dict of ROIs and their masks. **Values are continuous-valued (float) arrays**, the
    result of `cortex.mapper.Mapper.backwards`'s approximate least-squares back-
    projection — not a clean boolean mask, despite similarly-named `get_roi_masks`
    returning proper masks. Threshold the values yourself if you need a boolean mask.

### Raises
Propagates errors from `get_mapper`/`get_roi_verts` (e.g. unrecognized `projection`,
missing ROI).

### Notes
- **Deprecated** — emits a plain `warnings.warn` (not `DeprecationWarning` specifically)
  recommending `get_roi_masks`.
- The function body contains a comment noting an alternative "backward mapper" approach
  is "broken" and of unclear historical reliability — treat this function's exact
  numerical output with some caution; prefer `get_roi_masks`.

### Example
```python
import cortex

# Deprecated -- prefer get_roi_masks() instead.
roi_masks = cortex.utils.get_roi_mask("S1", "fullhead", roi=("V1", "V2"))
```

## Confidence / open questions
- **Recommendation for maintainers:** given this function is already deprecated and has a
  self-documented history of uncertain correctness, consider removing it in a future
  release rather than continuing to maintain it; at minimum, document that its output is
  continuous-valued, not boolean.
