# cortex.utils.get_roi_verts

## Current signature (from source)
```python
def get_roi_verts(subject, roi=None, mask=False, overlay_file=None):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:466-488](cortex/utils.py#L466-L488) — already
  reasonably complete.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_roi_verts.html

## Issues with current documentation
- **No Raises section** — an ROI name not present in the overlay raises `KeyError` (from
  `svg.rois.get_mask(name)`), not documented.
- **The "recover medial-wall/cut vertices" behavior is implemented but not explained in
  the docstring** — the function's body does nontrivial work to add back vertices that
  exist in the full fiducial surface but were excluded from the flat surface (cuts/medial
  wall), by walking each ROI's flat-surface vertices' full-surface neighbors. This
  behavior (why the returned vertex sets can include vertices not in the flat surface at
  all) is invisible from the docstring.
- **`mask=True`'s empty-ROI warning behavior isn't documented**: if an ROI mask ends up
  with zero `True` entries, a `UserWarning` ("No vertices found in {name}!") is issued.

## Fixed documentation

### Summary
Return vertices for the given ROIs, or all ROIs if none are given.

### Parameters
- **subject** : str
    Name of the subject
- **roi** : str, list or None, optional
    ROIs to fetch. Can be ROI name (string), a list of ROI names, or None, in which case
    all ROIs will be fetched.
- **mask** : bool
    if True, return a logical mask across vertices for the roi if False, return a list of
    indices for the ROI
- **overlay_file** : None or str
    Pass another overlays file instead of the default overlays.svg

### Returns
- **roidict** : dict
    Dictionary of {roi name : roi verts}. ROI verts are for both hemispheres, with right
    hemisphere vertex numbers sequential after left hemisphere vertex numbers.

### Raises
- `KeyError` — a requested ROI `name` (in `roi`) doesn't exist in the overlay SVG's ROI
  layer.
- `UserWarning` (not an exception) — if `mask=True` and an ROI's mask ends up empty
  (no matching vertices).

### Notes
- **Recovers cut/medial-wall vertices**: ROI vertex indices are first computed against
  the subject's flat surface (which excludes cut/medial-wall vertices), then expanded to
  include any full (fiducial) surface neighbor vertices that were excluded from the flat
  surface — so returned vertex indices/masks are not strictly a subset of the flat
  surface's own vertex set.
- No FreeSurfer/FSL/GUI dependency; requires the subject to already have flat and
  fiducial surfaces and an overlay SVG with ROI shapes.

### Example
```python
import cortex

roi_verts = cortex.utils.get_roi_verts("S1", roi=["V1", "V2"])
roi_masks = cortex.utils.get_roi_verts("S1", roi="V1", mask=True)
```

## Confidence / open questions
- **Recommendation for maintainers:** add a Raises section; briefly explain the
  medial-wall-vertex-recovery behavior in the docstring itself, since it affects what the
  returned indices actually mean.
