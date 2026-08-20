# cortex.utils.get_cmap

## Current signature (from source)
```python
def get_cmap(name):
```

## Where this is documented today
- Source docstring: [cortex/utils.py:1137-1149](cortex/utils.py#L1137-L1149)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.get_cmap.html

## Issues with current documentation
- **No Raises section** — raises a bare `Exception('Unkown color map!')` (note: typo,
  "Unkown") if `name` isn't a pycortex colormap image file and isn't a recognized
  matplotlib colormap name — a generic `Exception`, not a more specific/catchable type
  like `ValueError`/`KeyError`.
- **Likely uses a removed/deprecated Matplotlib API.** `plt.cm.get_cmap(name)`
  (`utils.py:1166`) was deprecated starting in Matplotlib 3.7 and **removed in Matplotlib
  3.9** in favor of `matplotlib.colormaps[name]` / `matplotlib.pyplot.get_cmap(name)` (the
  top-level function, not `plt.cm.get_cmap`). On Matplotlib >= 3.9, any `name` that isn't
  a pycortex colormap file will hit this line, raise `AttributeError` (since
  `plt.cm.get_cmap` no longer exists), and be swallowed by the bare `except:` clause
  (`utils.py:1167`) into the generic `"Unkown color map!"` exception — masking the real
  cause. Flagged, not fixed — see `_notes.md`.
- **Doesn't cross-reference the more commonly-used path**: most users set a colormap via
  `cmap=` on `Volume`/`Vertex`/etc. directly, which internally does equivalent resolution
  via `Dataview.get_cmapdict`, not via calling `get_cmap` themselves.

## Fixed documentation

### Summary
Gets a colormap, by name — first checking pycortex's own colormap image directory, then
falling back to matplotlib's built-in colormaps.

### Parameters
- **name** : str
    Name of colormap to get. Checked first against pycortex colormap image files
    (`<cmapdir>/<name>.png`), then against matplotlib's registered colormap names.

### Returns
- **cmap** : `matplotlib.colors.ListedColormap` or other matplotlib `Colormap`
    Matplotlib colormap object. A `ListedColormap` built from the pycortex `.png` file if
    `name` matched one; otherwise whatever `Colormap` subclass matplotlib returns for a
    built-in name.

### Raises
- `Exception` (generic — message: `"Unkown color map!"`, including the typo) — `name`
  doesn't match a pycortex colormap file or a matplotlib colormap name. **On Matplotlib >=
  3.9, this same generic exception is also raised for otherwise-valid matplotlib colormap
  names**, because the internal `plt.cm.get_cmap` call no longer exists on those versions
  — see Issues.

### Notes
- Registers newly-loaded pycortex colormaps with matplotlib (`register_cmap`) as a side
  effect, so subsequent lookups by the same name resolve faster; a "already registered"
  message is printed (not raised) if registration fails because it's already registered.
- Most users won't call this directly — passing `cmap="name"` to `Volume`/`Vertex`/etc.
  resolves colormaps through equivalent logic internally.

### Example
```python
import cortex

cmap = cortex.utils.get_cmap("RdBu_r")       # matplotlib built-in
# cmap = cortex.utils.get_cmap("my_custom")  # a pycortex colormap .png, if present
```

## Confidence / open questions
- The Matplotlib >= 3.9 `plt.cm.get_cmap` removal is based on Matplotlib's own published
  deprecation timeline (deprecated 3.7, removed 3.9), not on running this exact code
  against a Matplotlib >= 3.9 install in this pass — recommend maintainers verify against
  their supported Matplotlib version range.
- **Recommendation for maintainers:** replace `plt.cm.get_cmap(name)` with
  `matplotlib.colormaps[name]` (or `plt.get_cmap(name)`, the top-level function) for
  forward compatibility; use a specific exception type instead of a generic `Exception`
  with a typo'd message; narrow the bare `except:` so real errors aren't masked.
