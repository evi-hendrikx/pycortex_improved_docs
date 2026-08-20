# cortex.quickflat.make_png

## Current signature (from source)
```python
def make_png(
    fname: Union[str, os.PathLike, IO],
    braindata: dataset.Dataview,
    recache: bool = False,
    pixelwise: bool = True,
    sampler: str = 'nearest',
    height: int = 1024,
    bgcolor: Optional[ColorType] = None,
    dpi: int = 100,
    **kwargs,
) -> None:
```

## Where this is documented today
- Source docstring: [cortex/quickflat/view.py:240-306](cortex/quickflat/view.py#L240-L306)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.quickflat.make_png.html
  (autodoc-generated from this docstring; flat listing truncates to
  `make_png(fname, braindata[, recache, ...])`).

## Issues with current documentation
- **`**kwargs` is completely undocumented as a forwarding mechanism.** The signature ends
  in `**kwargs`, and the body does
  `make_figure(braindata, recache=..., pixelwise=..., sampler=..., height=..., **kwargs)`.
  The docstring lists many of `make_figure`'s parameters directly inline (as if they were
  `make_png`'s own named parameters — `thick`, `depth`, `with_rois`, etc.) but never states
  that they actually arrive via `**kwargs`, nor that literally *any* other `make_figure`
  keyword (e.g. `fig`, `cutout`, `roi_list`, `curvature_brightness`, ...) is also silently
  accepted and forwarded. A user reading only this docstring would not know `cutout=` or
  `roi_list=` work here at all.
- **`thick` is documented but not in the signature.** The docstring lists `thick : int` as
  a parameter of `make_png`, but `thick` is not a named parameter of `make_png` — it only
  works because it's swallowed by `**kwargs` and forwarded to `make_figure`. This is
  docstring/code drift: the docstring implies a fixed, closed parameter list that doesn't
  match the actual (open, kwargs-forwarding) signature.
- **No Returns section** — the function returns `None` (it writes a file/stream as a side
  effect); this isn't stated anywhere.
- **No Raises section.**
- **No Examples section.**
- **`fname` type is under-specified.** The docstring says `str`, but the real signature
  (and `fig.savefig` which it delegates to) also accepts an open binary file-like object /
  `os.PathLike`.
- **`bgcolor` semantics not fully explained.** `None` (default) produces a *transparent*
  PNG (`transparent=True` passed to `savefig`); any other color produces an *opaque* PNG
  filled with that color. This transparent/opaque distinction is stated but easy to miss
  since it's phrased only as "`None` gives transparent background."
- **DPI is applied twice / figure is resized after `make_figure` already sized it.**
  `make_png` calls `make_figure(..., height=height, **kwargs)` (note: `dpi` is *not*
  forwarded to `make_figure`, so `make_figure` renders using its own default `dpi=100`
  regardless of what `dpi` the caller passed to `make_png`), then separately does
  `fig.set_size_inches(imsize[::-1] / dpi)` and passes `dpi=dpi` to `savefig`. This means
  `dpi` in `make_png` only affects the final PNG's reported pixel density / physical
  print size, not any rendering quality — worth stating explicitly since it's a common
  source of "why doesn't dpi change my image resolution" confusion (the image's *pixel*
  resolution is fixed by `height`, not `dpi`).
- Same underlying **kwargs-chain gaps as `make_figure`** apply transitively (see
  `make_figure.md`): `sampler` options, `shadow` bug, disk-cache side effects, etc.

## Fixed documentation

### Summary
Create a PNG of the VertexData or VolumeData on a flatmap.

### Parameters
- **fname** : str
    Filename for where to save the PNG file
- **braindata** : Dataview (e.g. instance of cortex.Volume, cortex.Vertex, ...)
    the data you would like to plot on a flatmap
- **recache** : boolean
    Whether or not to recache intermediate files. Takes longer to plot this way, potentially
    resolves some errors. Useful if you've made changes to the alignment
- **pixelwise** : bool
    Use pixel-wise mapping
- **sampler** : str
    Name of sampling function used to sample underlying volume data. Options are
    'nearest', 'trilinear', 'gaussian', 'lanczos'.
- **height** : int
    Height of the image to render. Automatically scales the width for the aspect of
    the subject's flatmap
- **bgcolor** : matplotlib colorspec
    Color of background of image. `None` gives transparent background.
- **dpi** : int
    DPI of the generated image. Controls file metadata/print size, not pixel resolution.
    Not forwarded into the inner `make_figure` call (see Issues).
- **\*\*kwargs** : forwarded to `cortex.quickflat.make_figure`
    Any other `make_figure` keyword, e.g. `thick`, `depth`, `with_rois`, `with_sulci`,
    `with_curvature`, `cutout`, `fig`, `roi_list`, `linewidth`, `linecolor`, `roifill`,
    `shadow`, `labelsize`, `labelcolor`, `colorbar_location`, `nanmean`. See
    `make_figure.md` for the full list.

### Returns
`None`. The PNG is written to `fname` as a side effect; the matplotlib figure created
internally is closed (`fig.clf(); plt.close(fig)`) before the function returns.

### Raises
Propagates anything `make_figure` can raise (see `make_figure.md`: `TypeError`,
`ValueError`, `KeyError`), plus whatever `matplotlib.figure.Figure.savefig` raises for an
invalid `fname` (e.g. `FileNotFoundError` if the destination directory doesn't exist,
`OSError` for a bad path).

### Notes
- Same disk-cache side effects as `make_figure` (writes/reads `.npz` cache files under the
  subject's pycortex cache directory).
- No FreeSurfer/FSL/GUI dependency for this function itself (same caveats as `make_figure`
  regarding needing the subject already set up in the pycortex database).

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
volume_shape = cortex.db.get_xfm(subject, xfm).shape
data = np.random.randn(*volume_shape)
vol = cortex.Volume(data, subject, xfm, vmin=-2, vmax=2, cmap='RdBu_r')

# with_curvature and cutout are not in make_png's own signature -- they are
# forwarded via **kwargs straight through to make_figure.
cortex.quickflat.make_png(
    "example_flatmap.png",
    vol,
    with_curvature=True,
    bgcolor="white",
    height=512,
)
```

## Confidence / open questions
- The claim that `dpi` passed to `make_png` does not affect the internal `make_figure` call
  is based on static reading of `view.py:292-297` (the `make_figure(...)` call omits `dpi=`
  entirely) — confirmed by source inspection, not by running the code.
- Recommendation for maintainers: either forward `dpi` into the inner `make_figure` call (so
  the two functions' `dpi` behave consistently) or document explicitly why it's intentionally
  not forwarded; state the `**kwargs` forwarding target and full effective keyword list in
  the real docstring; add `Returns`/`Raises`/`Examples` sections; remove the stray
  `thick`-documented-but-not-a-parameter line or explicitly mark it as "forwarded via
  `**kwargs`".
