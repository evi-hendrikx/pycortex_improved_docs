# cortex.utils.add_roi

## Current signature (from source)
```python
def add_roi(data, name="new_roi", open_inkscape=True, add_path=True,
            overlay_file=None, **kwargs):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:400-431](cortex/utils.py#L400-L431)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.add_roi.html

## Issues with current documentation
- **The docstring's own sentence is cut off**: "Use the **kwargs inputs to specify" — ends
  mid-sentence with no completion.
- **`**kwargs`'s forwarding target is named ("Passed to cortex.quickflat.make_png") but
  not enumerated** — see `quickflat/make_png.md` for the full chain (which itself forwards
  to `make_figure`). This function also hard-codes `height=1024, with_rois=False,
  with_labels=False` when calling `make_png`, so those three specific kwargs cannot be
  overridden via `**kwargs` (passing them would raise `TypeError: got multiple values`).
- **No Returns section** — returns `None` if `open_inkscape=False`; returns the exit code
  (`int`) of the Inkscape subprocess call if `open_inkscape=True`. This dual return
  behavior isn't documented.
- **No Raises section** — raises `TypeError` if `data` normalizes to a `Dataset` rather
  than a single `Dataview`.
- **No mention this requires Inkscape installed** (`options.cfg`'s
  `[dependency_paths] inkscape`) when `open_inkscape=True` (the default).

## Fixed documentation

### Summary
Add new flatmap image to the ROI file for a subject. (The subject is specified in
creation of the data object.) Creates a flatmap image from the `data` input, and adds that
image as a sub-layer to the data layer in the rois.svg file stored for the subject in the
pycortex database. Most often, this is data to be used for defining a region (or several
regions) of interest, such as a localizer contrast (e.g. a t map of Faces > Houses).

### Parameters
- **data** : DataView
    The data used to generate the flatmap image.
- **name** : str, optional
    Name that will be assigned to the `data` sub-layer in the rois.svg file (e.g. 'Faces >
    Houses, t map, p<.005' or 'Retinotopy - Rotating Wedge')
- **open_inkscape** : bool, optional
    If True, Inkscape will automatically open the ROI file.
- **add_path** : bool, optional
    If True, also adds a sub-layer to the `rois` new SVG layer will automatically be
    created in the ROI group with the same `name` as the overlay.
- **overlay_file** : str, optional
    Custom overlays.svg file to use instead of the default one for this subject (if not
    None). Default None.
- **\*\*kwargs**
    Passed to `cortex.quickflat.make_png` (see `quickflat/make_png.md` for the full,
    kwargs-forwarded parameter list — includes `make_figure`'s parameters transitively).
    Note that `height`, `with_rois`, and `with_labels` are already set internally
    (`height=1024, with_rois=False, with_labels=False`) — passing those again raises
    `TypeError`.

### Returns
- `None` if `open_inkscape=False`.
- `int` (the Inkscape subprocess's exit code) if `open_inkscape=True`.

### Raises
- `TypeError` — `data` normalizes to a `cortex.Dataset` rather than a single `Dataview`
  ("Please specify a data view").

### Notes
- **Requires Inkscape installed** (path from `options.cfg`'s
  `[dependency_paths] inkscape`) when `open_inkscape=True` — opens it as a subprocess,
  with version-dependent CLI flags (pre-/post-1.0 Inkscape).
- Writes to the subject's overlay SVG file (`overlays.svg`, or `overlay_file` if given) as
  a side effect.

### Example
```python
import cortex

subject = "S1"
xfm = "fullhead"
shape = cortex.db.get_xfm(subject, xfm).shape
import numpy as np
localizer = cortex.Volume(np.random.randn(*shape), subject, xfm, vmin=-3, vmax=3)

cortex.utils.add_roi(localizer, name="Faces > Houses", open_inkscape=True)
```

## Confidence / open questions
- Did not run Inkscape in this pass.
- **Recommendation for maintainers:** complete the cut-off docstring sentence; add
  Returns/Raises; document the internally-fixed `make_png` kwargs that can't be
  overridden.
