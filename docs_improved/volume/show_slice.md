# cortex.volume.show_slice

## Current signature (from source)
```python
def show_slice(dataview, **kwargs):
```

## Where this is documented today
- Source docstring: none. [cortex/volume.py:138-184](cortex/volume.py#L138-L184)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.show_slice.html
  (no docstring content beyond the bare signature).

## Issues with current documentation
- **No docstring at all**, despite being an interactive, stateful GUI function with
  nontrivial mouse-driven controls.
- **No Parameters/Returns/Raises sections.**
- **`**kwargs` forwarding target is undocumented** — forwarded to
  `matplotlib.axes.Axes.imshow` for the functional overlay (merged with default
  `vmin`/`vmax`/`cmap` taken from `dataview`).
- **The interactive controls (mouse scroll = change slice index, mouse click = cycle
  through the three anatomical axes) are entirely undocumented** — only discoverable by
  reading the `scrollslice`/`switchslice` callback implementations.
- **No mention this requires `dataview` to be volumetric** (`TypeError` raised for
  non-`Volume` input) or that it displays an anatomical underlay resampled from
  `epi2anatspace`.

## Fixed documentation

### Summary
Interactively display a single anatomical slice (from the subject's raw anatomical image)
with a functional data overlay (resampled into anatomical space via `epi2anatspace`), with
mouse controls to scroll through slices and switch which axis is sliced.

### Parameters
- **dataview** : `cortex.Volume` (or anything `cortex.dataset.normalize` resolves to a
  `Volume`)
    Volumetric data to overlay. Raises `TypeError` if it resolves to non-volumetric data.
- **\*\*kwargs**
    Forwarded to `matplotlib.axes.Axes.imshow` for the functional overlay layer, merged
    with (and overriding) default `vmin`/`vmax`/`cmap` values taken from `dataview`.

### Returns
- **fig** : `matplotlib.figure.Figure`
    The interactive figure. Mouse controls (attached via `fig.canvas.mpl_connect`):
    scroll wheel up/down changes the current slice index; mouse click cycles which of the
    three volume axes is being sliced.

### Raises
- `TypeError` — `dataview` does not resolve to a `cortex.Volume`.

### Notes
- Values below `dataview.vmin` are set to `NaN` in the overlay (so the anatomical
  underlay shows through for sub-threshold voxels).
- No FreeSurfer/FSL dependency at call time; requires the subject's raw anatomical and
  the given transform to already be in the pycortex database.
- Interactive — requires an interactive matplotlib backend with mouse event support.

### Example
```python
import cortex

vol = cortex.Volume.random("S1", "fullhead")
fig = cortex.volume.show_slice(vol, cmap="RdBu_r")
# Scroll to change slice; click to cycle axes.
```

## Confidence / open questions
- Did not exercise the interactive mouse controls in this pass (requires a GUI backend).
- **Recommendation for maintainers:** add a docstring covering the mouse controls, the
  `TypeError` precondition, and the `**kwargs` forwarding target (currently entirely
  undocumented).
