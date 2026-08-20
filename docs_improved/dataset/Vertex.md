# cortex.dataset.Vertex (cortex.Vertex)

## Current signature (from source)
```python
class Vertex(VertexData, Dataview):
    def __init__(
        self,
        data: npt.NDArray,
        subject: str,
        cmap: Optional[str] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        description: str = "",
        **kwargs,
    ):
```
Like `Volume`, `Vertex` uses multiple inheritance: `VertexData` (surface-data storage/
mapping logic, in `cortex/dataset/braindata.py`) + `Dataview` (colormap/display metadata,
in `cortex/dataset/views.py`). See `Volume.md` for the parallel discussion of `Volume`;
this file focuses on what's different for vertex (surface-space) data.

## Where this is documented today
- Source docstrings:
  - `Vertex.__init__`: [cortex/dataset/views.py:451-499](cortex/dataset/views.py#L451-L499)
  - `VertexData` (base class): [cortex/dataset/braindata.py:351-642](cortex/dataset/braindata.py#L351-L642)
  - `BrainData` (base class): [cortex/dataset/braindata.py:18-119](cortex/dataset/braindata.py#L18-L119)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.Vertex.html

## Issues with current documentation
- **Same multiple-inheritance discoverability problem as `Volume`**: `.copy()`, `.exp()`,
  `.left`/`.right`, `.vertices`, `.raw`, `.map()` (a *different, surface-to-surface* `.map`
  than `Volume.map`'s volume-to-surface one — see below), `Vertex.empty(...)`,
  `Vertex.random(...)`, `.blend_curvature(...)` (deprecated), and the numpy-operator
  overloads are all invisible from `Vertex`'s own docstring.
- **`Vertex.map` and `VolumeData.map` share a name but do completely different things** —
  `Volume.map(projection=...)` projects volume data onto a surface (mapper-based), while
  `Vertex.map(target_subj, surface_type="fiducial", hemi="both", fs_subj=None, **kwargs)`
  instead projects surface data from *this* subject's surface onto a *different* subject's
  surface (inter-subject registration via `cortex.freesurfer.vertex_to_vertex`/
  `cortex.db.get_mri_surf2surf_matrix`). This name collision across sibling classes, doing
  materially different things with materially different signatures, is not called out
  anywhere and is a likely source of confusion for anyone who has used `Volume.map` first.
- **`Vertex.map`'s docstring omits its full parameter list.** Only `target_subj` is
  documented; `surface_type`, `hemi`, `fs_subj`, and the `**kwargs` (forwarded to
  `cortex.db.get_mri_surf2surf_matrix`) are entirely undocumented in the `Parameters`
  section (only `target_subj` appears), despite being real, named parameters in the
  signature.
- **`Vertex.map`'s side-effect/dependency requirements are stated ("Requires either previous
  computation of mapping matrices... or active freesurfer environment") but not what error
  results if neither is available**, nor what "previous computation" actually entails
  concretely (a call to `cortex.db.get_mri_surf2surf_matrix` beforehand, or having a
  FreeSurfer `mri_surf2surf`-compatible environment active) — no cross-reference is given.
- **`data` shape docstring is technically accurate but the "fill the other hemisphere with
  zeros" behavior is easy to miss** — it's mentioned in the class docstring's `Parameters`
  section prose but not called out as a common gotcha (e.g. computing percentile-based
  `vmin`/`vmax` over data that includes an artificially-zeroed hemisphere will skew the
  color range if you only meant to supply single-hemisphere data — the docstring doesn't
  warn about this interaction).
- **`.left`/`.right` properties have one-line docstrings** ("Data for only the left/right
  hemisphere vertices") but don't state the returned shape (`(v_hemi,)` or `(t, v_hemi)`
  depending on `.movie`), nor that they return **views/slices of the combined
  zero-padded array**, not necessarily what was originally passed in for the other
  hemisphere.
- **`blend_curvature` is deprecated** (raises a `DeprecationWarning` and has an extensive
  in-source deprecation note pointing to `Vertex2D`/`Volume2D` with alpha-aware colormaps)
  — this deprecation is well-documented in the source docstring already (good), but is not
  surfaced on the API reference page in a way that would stop a new user from reaching for
  it first (Sphinx renders deprecated methods the same as any other unless
  `.. deprecated::` directives are specifically styled — not confirmed either way for the
  live page).
- **No Returns/Raises sections** for `.map`, `.copy`, `.empty`, `.random`, `__getitem__`
  (which explicitly documents its own restriction — "Only works for movie (2D) vertex data"
  — as prose but not as a formal `Raises: TypeError`).
- **No Examples section** anywhere in the class or its inherited methods.

## Fixed documentation

### Summary
Encapsulates a 1D vertex map or 2D vertex movie, plus colormap display metadata.

### Parameters
- **data** : ndarray
    The data. Can be 1D with shape (v,), or 2D with shape (t,v). Here, v can be the number
    of vertices in both hemispheres, or the number of vertices in either one of the
    hemispheres. In that case, the data for the other hemisphere will be filled with
    zeros (a common gotcha — see Issues).
- **subject** : str
    Subject identifier. Must exist in the pycortex database.
- **cmap** : str or matplotlib colormap, optional
    Colormap (or colormap name) to use. If not given defaults to matplotlib default
    colormap.
- **vmin** : float, optional
    Minimum value in colormap. If not given, defaults to the 1st percentile of the data
    (computed over the full, possibly zero-padded, data).
- **vmax** : float, optional
    Maximum value in colormap. If not given defaults to the 99th percentile of the data.
- **description** : str, optional
    String describing this dataset. Displayed in webgl viewer.
- **\*\*kwargs**
    All additional arguments in kwargs are passed to the VertexData and Dataview.

### Returns
N/A for `__init__`. See "Public methods and properties" below.

### Raises
- `ValueError` — `data`'s vertex-axis length doesn't match `llen`, `rlen`, or `llen+rlen`
  for `subject` (message reports all three expected counts).
- `TypeError` — indexing (`vtx[i]`) a non-movie (1D) `Vertex` (movie indexing only).
- `TypeError` — attempting to instantiate `VertexData` directly (not applicable to
  `Vertex` itself).

### Public methods and properties (inherited)
- **`.data`** (property, get/set) — as in `Volume`.
- **`.vertices`** (property) : ndarray, shape `(t, v)` — data with a guaranteed leading time
  axis (length-1 if not a movie).
- **`.left`** / **`.right`** (properties) : ndarray, shape `(v_hemi,)` or `(t, v_hemi)` —
  data restricted to one hemisphere (a slice of the combined, possibly zero-padded, array).
- **`.map(target_subj, surface_type="fiducial", hemi="both", fs_subj=None, **kwargs)`** →
  `Vertex` — maps this data from `self.subject`'s surface to `target_subj`'s surface
  (inter-subject registration), via `cortex.db.get_mri_surf2surf_matrix`. `surface_type`
  selects which surface geometry to base the mapping on (default `"fiducial"`). `hemi`
  restricts output to `"lh"`, `"rh"`, or `"both"` (default; the excluded hemisphere is
  filled with NaN, not zero, when `hemi` is `"lh"` or `"rh"`). `fs_subj` overrides the
  FreeSurfer subject name if it differs from the pycortex `subject`/`target_subj` names.
  `**kwargs` forwarded to `cortex.db.get_mri_surf2surf_matrix`. **Not the same operation as
  `Volume.map`** — see Issues above.
- **`.copy(data)`** → `Vertex` — new object, same subject, display attrs preserved
  (does not re-check hemisphere lengths against the database — faster than constructing
  fresh).
- **`.exp()`** → `Vertex` — `self.copy(np.exp(self.data))`.
- **`.empty(subject, value=0, **kwargs)`** (classmethod) → `Vertex` — constant-valued,
  full both-hemisphere length.
- **`.random(subject, **kwargs)`** (classmethod) → `Vertex` — standard-normal random data,
  full both-hemisphere length.
- **`.save(filename, name=None)`** — as in `Volume` (no mask to also persist, since
  `VertexData` has no `_mask`).
- **`.raw`** (property) → `VertexRGB` — colormapped RGBA version, analogous to `Volume.raw`.
  **Undocumented in source.**
- **`.get_cmapdict()`** → dict, as in `Volume`. **Undocumented in source.**
- **`.priority`** (property, get/set) — as in `Volume`.
- **`.blend_curvature(alpha, threshold=0, brightness=0.5, contrast=0.25, smooth=20)`**
  → `VertexRGB`. **Deprecated** — raises `DeprecationWarning`; use `Vertex2D` (or
  `VertexRGB` directly for already-RGB data) with an alpha-aware 2D colormap instead (see
  the source docstring's migration example, reproduced in Notes below).
- **`__getitem__(idx)`** → `Vertex` — indexes into the time axis of movie (2D) data only;
  raises `TypeError` for non-movie data.
- **Numpy operator overloads** — as in `Volume`, return new `Vertex` objects.
- **`__repr__`** — e.g. `<Vertex data for S1>` or `<Vertex movie data for S1>`.

### Notes
- No FreeSurfer/FSL/GUI dependency for basic construction; `subject` must exist in the
  pycortex database with `wm` (or, as a fallback, `fiducial`) surfaces available.
- `.map(...)` (inter-subject mapping) **does** require either a precomputed surf2surf
  matrix cached in the pycortex database, or a working FreeSurfer environment
  (`mri_surf2surf`) to compute one on demand — this is the one method on `Vertex` with a
  real external-tool dependency.
- Mutability: same as `Volume` — arithmetic/`.copy`/`.exp`/`.map` return new objects;
  direct `.data =` assignment mutates in place without re-validating hemisphere length.
- Migration example for `blend_curvature` (from the source docstring):
  ```python
  # Deprecated:
  #   blended = vtx.blend_curvature(alpha)
  #   cortex.quickshow(blended)
  # Preferred:
  v2d = cortex.Vertex2D(vtx.data, alpha, subject,
                         cmap="fire_alpha",
                         vmin=vtx.vmin, vmax=vtx.vmax,
                         vmin2=0, vmax2=1)
  cortex.quickshow(v2d)
  ```

### Example
```python
import numpy as np
import cortex

subject = "S1"
left, right = cortex.db.get_surf(subject, "fiducial")
n_left, n_right = len(left[0]), len(right[0])

data = np.random.randn(n_left + n_right)
vtx = cortex.Vertex(data, subject, vmin=-2, vmax=2, cmap='RdBu_r')

# Restrict to one hemisphere:
left_data = vtx.left

# Elementwise arithmetic returns a new Vertex:
vtx_scaled = vtx * 2

cortex.quickflat.make_png("example_vertex.png", vtx)
```

## Confidence / open questions
- Could not verify from source alone what `hemi="lh"`/`"rh"` fills the excluded hemisphere
  with in `.map()` beyond reading the arithmetic (`np.nan * np.zeros(...)` — i.e. NaN, not
  zero) at `views.py:577,579`; this is a direct read, not an execution-confirmed behavior.
- Did not run `cortex.db.get_mri_surf2surf_matrix` or a FreeSurfer environment to confirm
  `.map()`'s exact failure mode/exception type when neither a cached matrix nor FreeSurfer
  is available — flagged as unverified.
- **Recommendation for maintainers:** rename `Vertex.map` or `Volume.map` (or at minimum
  cross-reference each in the other's docstring) given the name collision does materially
  different things; complete `Vertex.map`'s Parameters list (`surface_type`, `hemi`,
  `fs_subj`, `**kwargs` are all currently undocumented); add docstrings to `.raw`/
  `.get_cmapdict`.
