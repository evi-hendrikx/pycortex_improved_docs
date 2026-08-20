# cortex.dataset.Volume (cortex.Volume)

## Current signature (from source)
```python
class Volume(VolumeData, Dataview):
    def __init__(
        self,
        data: npt.NDArray,
        subject: str,
        xfmname: str,
        mask: Optional[npt.NDArray] = None,
        cmap: Optional[str] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        description: str = "",
        **kwargs,
    ):
```
`Volume` inherits from two base classes: `cortex.dataset.braindata.VolumeData` (volumetric
data storage/mapping logic) and `cortex.dataset.views.Dataview` (colormap/display metadata
logic). Its full public interface — used constantly in practice — is spread across all
three classes. This file documents `Volume` as users actually experience it: constructor,
inherited public methods/properties, and operators.

## Where this is documented today
- Source docstrings:
  - `Volume.__init__`: [cortex/dataset/views.py:352-411](cortex/dataset/views.py#L352-L411)
  - `VolumeData` (base class): [cortex/dataset/braindata.py:121-349](cortex/dataset/braindata.py#L121-L349)
  - `BrainData` (base class): [cortex/dataset/braindata.py:18-119](cortex/dataset/braindata.py#L18-L119)
  - `Dataview` (base class, mostly undocumented): [cortex/dataset/views.py:157-336](cortex/dataset/views.py#L157-L336)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.Volume.html — Sphinx
  autodoc typically only renders `__init__`'s own docstring plus a member list; inherited
  method docstrings from `VolumeData`/`BrainData`/`Dataview` may or may not be expanded
  depending on the Sphinx configuration used to build the page — not independently
  confirmed for this specific page in this pass (see Confidence below). Given multiple
  inheritance, at minimum the full picture requires reading three separate source files,
  which the online page does not make discoverable.

## Issues with current documentation
- **Multiple-inheritance origin of the public API is invisible.** A user reading only
  `Volume`'s own docstring has no way to discover `.map()`, `.copy()`, `.save()`,
  `.save_nii()`, `.exp()`, `.masked[...]`, `.volume`, `.raw`, `.data`, `.priority`,
  `.get_cmapdict()`, `Volume.empty(...)`, `Volume.random(...)`, or the numpy-operator
  overloads (`+`, `-`, `*`, `/`, `//`, `**`, unary `-`, `abs()`) — all of which come from
  `VolumeData`/`BrainData`/`Dataview` and are not mentioned in `Volume`'s own docstring at
  all.
- **`mask` parameter behavior under-specified.** The docstring says masked (1D/2D) data
  will auto-load "if the size of the given array matches any of the existing masks in the
  database" and otherwise "an error will be raised" — but doesn't say the error is
  `ValueError: Cannot find a valid mask` (from `_find_mask`), nor that an explicit `mask`
  can also be a `str` naming a saved mask (`db.get_mask(subject, xfmname, mask)`) in
  addition to a raw boolean `ndarray`.
  Note this may also raise an ambiguous match — `_find_mask` returns the **first** matching
  mask file found by `glob.glob`, silently, if more than one saved mask in the database
  happens to have the same voxel count (see `_notes.md`).
  a numpy `ndarray` in addition to a boolean array; `mask > 0` is applied for you.
- **`data` shape rules are stated but the "movie"/"linear" duality that pervades the rest of
  the class (`self.movie`, `self.linear`, `self.shape`) is not explained** in `Volume`'s
  docstring at all — it's only discoverable by reading `VolumeData._check_size`.
- **`vmin`/`vmax` docstring wording ("defaults to the 1st/99th percentile of the data") is
  accurate but doesn't mention this percentile is computed via `np.nan_to_num(self.data)`
  (NaNs treated as 0 for the purposes of picking a default range) — could be surprising for
  sparse/NaN-heavy data.
- **No Returns section anywhere** (not applicable to `__init__` itself, but `map`, `copy`,
  `exp`, `empty`, `random`, `masked[...]`, `.volume`, `.raw` all lack Returns docs beyond a
  one-line type name, several of them (`Dataview.raw`, `.get_cmapdict`) have **no docstring
  at all**).
- **`Dataview.raw` (used constantly, e.g. by `quickflat`/`webgl` internally) has no
  docstring** describing that it returns a `VolumeRGB` (for `Volume`) with a `_nan_mask`
  attribute stashed on it, nor that colors are computed by applying the object's own
  `cmap`/`vmin`/`vmax` via matplotlib and clipping to `[0, 255]` uint8.
- **`.masked[...]` is a genuinely useful but totally undocumented feature.** `Volume` objects
  have a `.masked` attribute (a `_masker` instance) supporting `vol.masked['some_mask_name']`
  to get a new `Volume` restricted to a named saved mask — there is no docstring for
  `_masker` or its `__getitem__`, and it isn't mentioned anywhere in `Volume`'s own
  docstring despite being one of the more commonly used pycortex idioms (e.g.
  `vol.masked['thin']`).
- **The numpy-operator overloads (`+ - * / // ** neg abs`) added dynamically via
  `BrainData._add_numpy_methods()` are invisible to any docstring/IDE/API-reference tooling**
  since they're set with `setattr` at class-definition time, not written as literal `def
  __add__` methods in the source — a maintainer building autodoc-based tooling in the future
  should be aware plain `inspect`/Sphinx autodoc introspection *should* still pick these up
  post-classdef (they exist as real bound methods by the time `Volume` is imported), but no
  docstring/signature is attached, so they'd show as undocumented in any case.
- **`Volume.empty`/`Volume.random` classmethods documented in `VolumeData` refer generically
  to "VolumeData subclass" as the return type** rather than concretely stating that calling
  `Volume.empty(...)` returns a `Volume` (only true because `cls` is bound correctly via
  `@classmethod` — worth being explicit for a first-time reader).
- **No Examples section** on `Volume.__init__` or any inherited method.

## Fixed documentation

### Summary
`Volume` wraps a 3D (or 4D movie) array of data defined in a subject's native functional
(EPI) volume space, together with the subject/transform identifiers needed to render it on
a cortical surface, plus display metadata (colormap, color range, description). It is one
of pycortex's two primary "Dataview" types (the other being `Vertex`).

### Parameters
- **data** : ndarray
    The data to visualize. Accepted shapes:
    - `(z, y, x)` — a single 3D volume matching the transform's reference image shape.
    - `(t, z, y, x)` — a 4D "movie" of `t` volumes.
    - `(v,)` — masked/flattened data for `v` in-cortex voxels (1D). `v` must match the
      voxel count of an existing saved mask for `(subject, xfmname)` in the pycortex
      database (auto-detected — see Raises), or `mask` must be given explicitly.
    - `(t, v)` — masked/flattened movie data (2D), analogous to the above.
- **subject** : str
    Subject identifier; must already exist in the pycortex database (`cortex.db.subjects`).
- **xfmname** : str
    Name of a transform already registered for `subject` in the pycortex database (see
    `cortex.align`), mapping this data's volume space to the subject's anatomical space.
- **mask** : ndarray of bool, str, or None, optional
    Only relevant when `data` is 1D/2D (masked). A boolean array of shape `(z, y, x)`
    marking included voxels, or the name of a saved mask (looked up via
    `cortex.db.get_mask(subject, xfmname, mask)`). `None` (default) auto-detects a saved
    mask whose voxel count matches `data`'s last axis length; raises `ValueError` if none
    match (and picks the first match, silently, if more than one saved mask happens to have
    the same voxel count — see `_notes.md`).
- **cmap** : str or matplotlib `Colormap`, optional
    Colormap name (matplotlib built-in, a pycortex colormap `.png` under
    `<filestore>/colormaps/`, or a `Colormap` instance). `None` uses `options.cfg`'s
    `[basic] default_cmap`.
- **vmin** : float, optional
    Lower colormap bound. `None` defaults to the 1st percentile of `data` (NaNs treated as
    0 via `np.nan_to_num` for this calculation only — the underlying data is unaffected).
- **vmax** : float, optional
    Upper colormap bound. `None` defaults to the 99th percentile of `data` (same NaN
    handling as `vmin`).
- **description** : str, default `""`
    Free-text description shown in the WebGL viewer's data-selection UI.
- **\*\*kwargs**
    Forwarded to `Dataview.__init__` (and, transitively, stored in `self.attrs`). Notable
    keys: `state` (opaque, viewer-internal — undocumented in source, marked
    `TODO: describe what this is` in `VolumeRGB`'s docstring and absent from `Volume`'s),
    `priority` (`int`, default `1` — display ordering in the WebGL viewer's data list; lower
    values are prioritized first per `Dataset.__iter__`'s `sorted(..., key=lambda x:
    x[1].priority)`).

### Returns
N/A for `__init__`. See "Public methods and properties" below for the return type of each.

### Raises
- `ValueError` — invalid `data.ndim` (must be 1, 2, 3, or 4); volumetric (3D/4D) data whose
  shape doesn't match the transform's reference image shape; masked (1D/2D) data whose voxel
  count doesn't match any saved mask when `mask=None`.
- `TypeError` — if you attempt to instantiate the abstract base classes `VolumeData` or
  `Dataview` directly (not applicable to `Volume` itself, but relevant if you're
  subclassing).
- `ValueError` (from `get_cmapdict`/`raw`) — unknown `cmap` name not found among matplotlib
  or pycortex colormaps.

### Public methods and properties (inherited)
- **`.data`** (property, get/set) : ndarray — the raw stored array (transparently
  materialized from an HDF5 dataset if the `Volume` was loaded from a `.hdf` file).
- **`.volume`** (property) : ndarray, shape `(t, z, y, x)` — the data as a full 4D volume,
  with masked (linear) data automatically unmasked via `cortex.volume.unmask` and
  non-movie data given a length-1 time axis.
- **`.masked`** (attribute, a `_masker`) : supports `vol.masked['maskname']` →
  returns a new `Volume` (same subject/xfmname) containing only the mask-selected voxels as
  linear data, via `cortex.db.get_mask`.
- **`.map(projection="nearest")`** → `Vertex` (or `Vertex2D`/`VertexRGB` for those
  subclasses via inherited method resolution — not applicable to plain `Volume`, which maps
  to `Vertex`). Projects volume data onto the cortical surface using
  `cortex.mapper.get_mapper(subject, xfmname, projection)`; copies `vmin`/`vmax`/`cmap`
  onto the result. `projection` accepts any registered pycortex mapper name (e.g.
  `"nearest"`, `"trilinear"`, `"gaussian"`; see `cortex.mapper.get_mapper`).
- **`.copy(data)`** → `Volume` — new `Volume` for the same `subject`/`xfmname`/mask with
  `data` replacing the array; all `Dataview` display attributes (`cmap`, `vmin`, `vmax`,
  `description`, `state`, `attrs`) are preserved. Used internally by the numpy-operator
  overloads and `.exp()`.
- **`.exp()`** → `Volume` — shorthand for `self.copy(np.exp(self.data))`.
- **`.empty(subject, xfmname, value=0, **kwargs)`** (classmethod) → `Volume` — constant-
  valued volume shaped like the transform's reference image; useful for testing/scaffolding.
- **`.random(subject, xfmname, **kwargs)`** (classmethod) → `Volume` — volume filled with
  standard-normal random data, same shape rules as `.empty`.
- **`.save(filename, name=None)`** — append this `Volume` (and its mask, if any) to an HDF5
  file at `filename` (or an already-open `h5py.Group`); raises `TypeError` for non-HDF
  extensions when `filename` is a path string. `name=None` uses the object's hash-derived
  auto `.name`.
- **`.save_nii(filename)`** — write this volume's `.volume` array (3D/4D, transposed to
  NIfTI axis order) to a `.nii`/`.nii.gz` file at `filename`, using the affine of the
  transform's reference image (via `nibabel`). Overwrites `filename` if it exists.
- **`.raw`** (property) → `VolumeRGB` — this data colormapped into RGBA `uint8`, using the
  object's own `cmap`/`vmin`/`vmax`; NaN entries get alpha=0 (an internal `_nan_mask` is
  stashed on the returned object for downstream consumers). This is what
  `cortex.quickflat`/`cortex.webgl` use internally to render the flatmap image.
  → **Not documented in source at all (no docstring on `Dataview.raw`).**
- **`.get_cmapdict()`** → dict with keys `cmap` (resolved matplotlib `Colormap`), `vmin`,
  `vmax`. Raises `ValueError` for an unrecognized `cmap` name.
  → **Not documented in source at all (no docstring).**
- **`.priority`** (property, get/set) : int — shortcut for `self.attrs['priority']`.
- **`.name`** (property) : str — `"__" + <16-char sha1 hash of self.data>` — a
  content-derived identifier used internally for HDF5 storage/deduplication; not meant to
  be human-meaningful.
- **`.uniques(collapse=False)`** — generator; for a plain `Volume` just `yield self` (more
  meaningful for `Dataset`/RGB/2D composite views).
- **Numpy operator overloads** (`+`, `-`, `*`, `/`, `//`, `**`, unary `-`, `abs()`): each
  returns a **new** `Volume` (via `.copy`) with the operator applied to `.data` — these do
  **not** mutate the original object.
- **`__repr__`** — human-readable summary, e.g. `<Volumetric data for (S1, fullhead)>` or
  `<Nearest masked movie data for (S1, fullhead)>` depending on mask/movie status.

### Notes
- No FreeSurfer/FSL/GUI dependency for constructing or manipulating a `Volume` in memory;
  `subject`/`xfmname` must already be registered in the pycortex database (see
  `cortex.align`, `cortex.database.Database`).
- `.map(...)` and `.masked[...]` both perform file I/O against the pycortex database/cache
  the first time they're used for a given mapper/mask combination.
- Mutability: arithmetic/`copy`/`exp` all return **new** `Volume` objects; direct assignment
  to `.data` (`vol.data = new_array`) **does** mutate in place and bypasses the shape/mask
  re-validation that `__init__` performs — reassigning to an incompatible shape will not
  raise immediately (see `_notes.md`).

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
volume_shape = cortex.db.get_xfm(subject, xfm).shape

# 3D volume, explicit color range
data = np.random.randn(*volume_shape)
vol = cortex.Volume(data, subject, xfm, vmin=-2, vmax=2, cmap='RdBu_r',
                     description="Random example data")

# Elementwise arithmetic returns a new Volume:
vol_scaled = vol * 2 + 1

# Project to the cortical surface as a Vertex object:
vtx = vol.map(projection="nearest")

# Save to an HDF5 pycortex dataset file:
cortex.Dataset(example=vol).save("example_dataset.hdf")
```

## Confidence / open questions
- Did not independently verify how Sphinx autodoc actually renders inherited-method
  docstrings on the live `cortex.Volume` API page (would require inspecting the Sphinx
  config, e.g. `:inherited-members:`) — flagged as unconfirmed in "Where this is documented
  today."
- The claim that `_find_mask` returns the first match silently when multiple saved masks
  share a voxel count is based on static reading of `braindata.py:645-660`
  (`glob.glob` + first successful `nvox == np.sum(mask)` wins), not executed.
- Did not verify at runtime that reassigning `.data` directly bypasses shape validation —
  inferred from `data`/`data.setter` in `BrainData` (`braindata.py:49-51`) simply doing
  `self._data = data` with no call back into `_check_size`.
- **Recommendation for maintainers:** add a docstring to `Dataview.raw` and
  `Dataview.get_cmapdict`; document `.masked[...]` somewhere prominent (it's a very commonly
  used feature); consider having `Volume`'s own docstring cross-reference
  `VolumeData`/`Dataview` explicitly since Python multiple inheritance makes the full API
  surface easy to miss; consider making `.data`'s setter re-validate shape/mask consistency,
  or explicitly document that it does not.
