# cortex.dataset.Vertex2D (cortex.Vertex2D)

## Current signature (from source)
```python
class Vertex2D(Dataview2D):
    def __init__(
        self,
        dim1: Union[npt.NDArray, Vertex],
        dim2: Union[npt.NDArray, Vertex],
        subject: Optional[str] = None,
        description: str = "",
        cmap: Optional[str] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        vmin2: Optional[float] = None,
        vmax2: Optional[float] = None,
        **kwargs,
    ):
```
Surface-space counterpart to `Volume2D` (see `Volume2D.md` — most of the design and
documentation issues are shared; this file covers what's specific to `Vertex2D`).

## Where this is documented today
- Source docstring: [cortex/dataset/view2D.py:210-272](cortex/dataset/view2D.py#L210-L272)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.Vertex2D.html

## Issues with current documentation
- Same `vmin`/`vmax`/`vmin2`/`vmax2` `"TODO:WHAT"` placeholder issue as `Volume2D` (see
  `Volume2D.md`) — identical copy-pasted docstring text.
- Same "two ways to construct" validation rules undocumented in prose (raises `TypeError`
  for mixed `Vertex`/raw-array `dim1`/`dim2`, mismatched `.subject`, or `subject` given
  redundantly alongside `Vertex` objects).
- **Inconsistent internal type-check**: the `__init__` body checks `isinstance(dim1,
  VertexData)` (the base class) but later re-checks `isinstance(dim2, self._cls)` where
  `self._cls = VertexData` — these are equivalent in practice (since `Vertex` **is a**
  `VertexData`), but worth noting for maintainers since `Volume2D`'s equivalent code
  consistently uses `self._cls` throughout instead of mixing `VertexData` directly and
  `self._cls` — cosmetic-only currently, flagged as a minor inconsistency, not a bug, in
  `_notes.md`.
- **`blend_curvature` is attached to the class via `blend_curvature = _cls.blend_curvature`
  ("hacky inheritance", per the source's own comment)** rather than real inheritance — this
  works at runtime (unbound function assigned as a class attribute, called with `self` as
  usual) but is invisible to some documentation tooling that inspects the MRO, and the
  in-source comment calling it "hacky" is itself useful context that isn't otherwise
  reflected in any docstring.
- **No Returns/Raises/Examples sections.**
- **`.vertices` property docstring is entirely absent** — it simply returns
  `self.raw.vertices`, undocumented.
- Same 2D-colormap-is-an-image-file caveat as `Volume2D` applies here too, and is equally
  undocumented.

## Fixed documentation

### Summary
Contains two vertex maps for simultaneous visualization, jointly colormapped via a 2D
colormap image.

### Parameters
- **dim1** : ndarray or Vertex
    The first vertex map. Can be a 1D array (see Vertex for details), or a Vertex.
- **dim2** : ndarray or Vertex
    The second vertex map. Same rules as `dim1`; mixing types, or a Vertex with a
    mismatched subject, raises `TypeError`.
- **subject** : str, optional
    Subject identifier. Must exist in the pycortex database. If not given, dim1 must be a
    Vertex from which the subject can be extracted.
- **description** : str, optional
    String describing this dataset. Displayed in webgl viewer.
- **cmap** : str, optional
    Name of a 2D colormap **image file**, not a matplotlib colormap (see `Volume2D.md`).
    If not given defaults to the `default_cmap2d` in your pycortex options.cfg file.
- **vmin** : float, optional
    Minimum value in colormap for dim1. If not given defaults to `dim1.vmin` (the shipped
    docstring says "TODO:WHAT" here — see `Volume2D.md`'s Issues).
- **vmax** : float, optional
    Maximum value in colormap for dim1. If not given defaults to `dim1.vmax`.
- **vmin2** : float, optional
    Minimum value in colormap for dim2. If not given defaults to `dim2.vmin`.
- **vmax2** : float, optional
    Maximum value in colormap for dim2. If not given defaults to `dim2.vmax`.
- **\*\*kwargs**
    All additional arguments in kwargs are passed to the VertexData and Dataview.

### Returns
N/A for `__init__`.

### Raises
- `TypeError` — mismatched `Vertex`/raw-array type-category between `dim1`/`dim2`;
  redundant `subject` given with `Vertex` objects; missing `subject` with raw arrays;
  mismatched `.subject` between `dim1`/`dim2` when both are `Vertex` objects.
- File/lookup errors if `cmap` doesn't match an existing 2D colormap image.

### Public methods and properties (inherited from `Dataview2D`)
- **`.raw`** (property) → `VertexRGB` — the two channels jointly colormapped, via
  `Dataview2D._to_raw(self.dim1.data, self.dim2.data)`. Alpha defaults to opaque unless
  `'alpha'` is in `self.attrs`; NaN in either channel → alpha=0.
- **`.vertices`** (property) → ndarray, shape `(t, v, 4)` — shortcut for `self.raw.vertices`
  (the colormapped RGBA data). **Undocumented in source.**
- **`.subject`** (property, from `Dataview2D`) — proxies `self.dim1.subject`.
- **`.blend_curvature(...)`** — attached from `VertexData.blend_curvature` via direct
  attribute assignment (not MRO inheritance); same signature/behavior/deprecation status as
  `Vertex.blend_curvature` (see `Vertex.md`) — **deprecated**, prefer constructing a
  `Vertex2D` directly with an alpha-aware colormap instead (which is somewhat circular
  advice when you're already looking at `Vertex2D`'s own docs — the deprecation notice is
  really aimed at plain-`Vertex` users).
- **`.uniques(collapse=False)`** — as in `Volume2D`.
- **`__repr__`** — e.g. `<2D vertex data for (S1)>`.

### Notes
- No FreeSurfer/FSL/GUI dependency.
- Same 2D-colormap-as-image-file behavior and non-perceptually-uniform colormap warning as
  `Volume2D` (see `Volume2D.md`).

### Example
```python
import numpy as np
import cortex

subject = "S1"
left, right = cortex.db.get_surf(subject, "fiducial")
nverts = len(left[0]) + len(right[0])

value = np.random.randn(nverts)
confidence = np.random.rand(nverts)

v2d = cortex.Vertex2D(
    value, confidence, subject,
    vmin=-2, vmax=2,
    vmin2=0, vmax2=1,
    cmap="RdBu_covar",
)
cortex.quickflat.make_png("example_vertex2d.png", v2d)
```

## Confidence / open questions
- Same colormap-file-existence caveat as `Volume2D.md` — not independently verified against
  an installed colormap directory.
- **Recommendation for maintainers:** same as `Volume2D` (fix the `TODO:WHAT` placeholders);
  additionally, consider giving `blend_curvature`'s "hacky inheritance" (`blend_curvature =
  _cls.blend_curvature`) a proper docstring override on `Vertex2D`/`VertexRGB` themselves
  rather than relying on the reader to trace it back to `VertexData.blend_curvature`.
