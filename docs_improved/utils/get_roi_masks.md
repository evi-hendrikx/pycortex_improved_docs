# cortex.utils.get_roi_masks

## Current signature (from source)
```python
def get_roi_masks(subject, xfmname, roi_list=None, gm_sampler='cortical', split_lr=False,
                  allow_overlap=False, fail_for_missing_rois=True, exclude_empty_rois=False,
                  threshold=None, return_dict=True, overlay_file=None):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:673-748](cortex/utils.py#L673-L748) — one of the
  most thorough docstrings in the codebase (full Parameters, dual-mode Returns, Notes).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_roi_masks.html

## Issues with current documentation
- **No Raises section** — raises `ValueError` for an unrecognized `gm_sampler`, or (per
  the docstring's own text) if `return_dict=False` and `gm_sampler` is mapper-based with
  `threshold=None`; raises `KeyError` (wrapped and re-raised with a clearer message) if a
  requested ROI is missing and `fail_for_missing_rois=True`.
- **The `roi_list=None`/`'Cortex'`-in-`roi_list` interaction has a latent bug in the
  `fail_for_missing_rois=False` fallback branch**: `missing = [r for r in roi_list if not
  r in roi_verts.keys()+['Cortex']]` (`utils.py:784`) calls `.keys()+[...]` — `dict.keys()`
  in Python 3 returns a `dict_keys` view, which does not support `+` with a list (raises
  `TypeError: unsupported operand type(s) for +`). This branch is therefore only reachable
  (and only actually exercised) when `fail_for_missing_rois=False` **and** at least one
  requested ROI is genuinely missing — a fairly specific combination — but when it is hit,
  it appears it would crash with `TypeError` rather than gracefully listing missing ROIs
  as the code intends. Flagged, not fixed — see `_notes.md`.
- **Return-type ambiguity isn't emphasized enough**: `return_dict=False` returns a
  completely different type (`(index_volume, index_labels)` tuple) than the default
  (`dict`) — this is documented via an "- OR -" in the `Returns` section, which is easy to
  skim past.

## Fixed documentation

### Summary
Return a dictionary of roi masks. This function returns a single 3D array with a separate
numerical index for each ROI (when `return_dict=False`), or a dict of per-ROI boolean/
float masks (default).

### Parameters
- **subject** : string
    pycortex subject ID
- **xfmname** : string
    pycortex transformation name
- **roi_list** : list or None
    List of names of ROIs to retrieve (e.g. ['FFA','OFA','EBA']). Names should match the
    ROI layers in the overlays.svg file for the `subject` specified. If None is provided
    (default), all available ROIs for the subject are returned. If 'Cortex' is included in
    roi_list*, a mask of all cortical voxels NOT included in other requested rois is
    included in the output.
    * works for gm_sampler = 'cortical', 'thin', 'thick', or (any scalar value); does not
    work for mapper-based gray matter samplers.
- **gm_sampler** : scalar or string
    How to sample the cortical gray matter. Options are:
    - `<an integer>` — Distance from fiducial surface to define ROI. Reasonable values
      range from 1-3.
    - `'cortical'` — selection of all voxels with centers within the cortical ribbon
      (directly computed from distance of each voxel from fiducial surface). Requires
      separate pial/white-matter surfaces (FreeSurfer-derived).
    - `'thick'` — selection of voxels within 'thick' mask (see `get_cortical_mask`).
    - `'thin'` — selection of voxels within 'thin' mask (see `get_cortical_mask`).
    - `'cortical-liberal'` — all voxels with any part within the cortical ribbon
      (`'line_nearest'` mapper).
    - `'cortical-conservative'` — only the closest voxel to each surface vertex
      (`'nearest'` mapper).
    Mapper-based gm_samplers return floating point values from 0-1 for each voxel
    (reflecting the fraction of that voxel inside the ROI) unless a threshold is provided.
- **threshold** : float [0-1]
    value used to convert probabilistic ROI values to a boolean mask for the ROI.
- **split_lr** : bool
    Whether to separate ROIs into left and right hemispheres (e.g., 'V1' becomes 'V1_L'
    and 'V1_R'). Forced to `True` internally when `return_dict=False`.
- **allow_overlap** : bool
    Whether to allow ROIs to include voxels in other ROIs (default: False). This should
    only be relevant if (a) spline shapes defining ROIs in overlays.svg overlap at all, or
    (b) a low threshold is set for a mapper-based gm_sampler.
- **fail_for_missing_rois** : bool
    Whether to fail if one or more of the rois specified in roi_list are not defined in
    the overlays.svg file. **Setting `False` currently risks a `TypeError` in the fallback
    path when a requested ROI actually is missing** — see Issues.
- **exclude_empty_rois** : bool
    Whether to (drop from the output, not "fail" despite the name) an ROI that is present
    in the overlays.svg file but contains no voxels because the scan didn't target that
    region of the brain.
- **return_dict** : bool
    If True (default), function returns a dictionary of ROI masks; if False, a volume
    with integer indices for each ROI (similar to Freesurfer's aseg masks) and a
    dictionary of how the indices map to ROI names are returned.
- **overlay_file** : str or None
    If None, use the default `overlays.svg` file. Otherwise, use the passed overlay file
    to look for the ROIs.

### Returns
- If `return_dict=True` (default): **roi_masks** : dict — dictionary of arrays; keys are
  ROI names, values are roi masks.
- If `return_dict=False`: **(index_volume, index_labels)** : (array, dict) —
  `index_volume` is a 3D array with a separate numerical index value for each ROI. Index
  values in the left hemisphere are negative (e.g. if V1 in the right hemisphere is 1,
  left-hemisphere V1 is -1). `index_labels` maps roi names to index values (e.g.
  `{'V1': 1}`).

### Raises
- `ValueError` — `gm_sampler` isn't a recognized string or scalar; `return_dict=False`
  combined with a mapper-based `gm_sampler` and `threshold=None`.
- `KeyError` — a requested ROI is missing and `fail_for_missing_rois=True` (re-raised with
  a descriptive message).
- `TypeError` — **likely**, in the `fail_for_missing_rois=False` fallback branch, due to
  `dict_keys + list` not being supported in Python 3 (`utils.py:784`) — see Issues; not
  independently confirmed by execution in this pass.

### Notes
Some gm_samplers may fail if you have very high-resolution data (i.e., with voxels on the
order of the spacing between vertices in your cortical mesh). In such cases, there may be
voxels in the middle of your ROI that are not assigned to the ROI (because no vertex falls
within that voxel). For such cases, it is recommended to use 'cortical', 'thick', or
'thin' as your `gm_sampler`.

### Example
```python
import cortex

roi_masks = cortex.utils.get_roi_masks(
    "S1", "fullhead", roi_list=["V1", "V2", "Cortex"], gm_sampler="cortical",
)
```

## Confidence / open questions
- The `dict_keys + list` `TypeError` is inferred from static reading of `utils.py:784`
  (`roi_verts.keys()+['Cortex']`), which is invalid in Python 3's `dict_keys` API — not
  confirmed by actually triggering the `fail_for_missing_rois=False` + missing-ROI code
  path in this pass.
- **Recommendation for maintainers:** fix `roi_verts.keys()+['Cortex']` to
  `list(roi_verts.keys()) + ['Cortex']`; add a Raises section.
