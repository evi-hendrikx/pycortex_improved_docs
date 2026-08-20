# cortex.database.Database (cortex.db)

## Current signature (from source)
```python
class Database(object):
    def __init__(self, filestore=default_filestore):
```
A module-level singleton instance, `db = Database()`, is created at import time
(`cortex/database.py:820`) and is what users actually interact with as `cortex.db`.

## Where this is documented today
- Source docstring (class-level, minimal): [cortex/database.py:144-153](cortex/database.py#L144-L153)
- Per-method docstrings scattered throughout [cortex/database.py](cortex/database.py) —
  see per-method notes below; several methods have no docstring at all.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.database.Database.html

## Issues with current documentation
- **Class-level docstring is minimal** ("Surface database") and doesn't explain the
  `cortex.db` singleton convention, the on-disk `filestore` layout, or attribute-style
  subject access (`db.S1` — via `__getattr__`).
- **Several public methods have no docstring at all**: `get_overlay`, `save_mask`,
  `get_mask`, `get_cache`, `make_subj`.
- **`get_overlay` has a self-admitted broken code path**, documented only in an inline
  comment, not surfaced anywhere else: `"NOTE: This try loop is broken, in that it does
  nothing for the intended use case (loading an overlay from a packed subject) - needs
  fixing."` (`database.py:354-355`). See `_notes.md`.
- **`get_anat`'s docstring is truncated mid-sentence**: `"type : str \n    Type of
  anatomical volume to return. This should be the name of one of the"` — cuts off with no
  actual list of valid values. The valid values are, in fact, the names of functions in
  `cortex.anat` (`'raw'`, `'raw_wm'`, `'brainmask'`, `'whitematter'`) since the
  implementation does `getattr(anat, type)(anatfile, subject, **kwargs)`; this
  cross-reference is missing entirely.
- **`get_anat`'s Returns section says "volume : nibabel object \n Volume containing"** —
  also truncated/incomplete, and doesn't mention the `xfmname` branch returns something
  different (a resampled numpy array via `cortex.volume.anat2epispace`, not a nibabel
  object) when `xfmname` is given.
- **`__dir__` returns an incomplete method list** — it hardcodes
  `["save_xfm", "get_xfm", "get_surf", "get_anat", "get_surfinfo", "subjects", "get_mask",
  "get_overlay", "get_cache", "get_view", "save_view", "get_mnixfm",
  "get_mri_surf2surf_matrix"]` plus subject names, omitting `get_paths`,
  `reload_subjects`, `save_mask`, `get_coords`, `get_shared_voxels`, `clear_cache`, and
  `make_subj` — all of which are still fully callable, just invisible to tab-completion/
  `dir(cortex.db)`. Not documented anywhere as a known gap.
- **`save_view`'s docstring describes `get_view`'s behavior, not its own.** Both methods
  carry the identical opening description, "Set the view for an open webshow instance from
  a saved view" — accurate for `get_view` (which loads a saved view and applies it to a
  live viewer), but backwards for `save_view` (whose body actually *captures* the live
  viewer's current view and writes it to disk — the reverse direction). Only the `Notes`
  line at the bottom of each (`vw.save_view(...)` vs. `vw.get_view(...)`) differs.
- **`get_coords` is deprecated** (issues `DeprecationWarning`, "Please use a Mapper object
  instead") but this isn't mentioned in its own docstring text, only enforced at runtime.
- **`make_subj` and `clear_cache` are destructive, interactive (input()-driven) operations
  with no docstring (`make_subj`) or an essentially empty one (`clear_cache`)** — both
  delete files from disk, `make_subj` after a raw `input("... Type YES\n")` prompt (case-
  sensitive, must be exactly `"YES"`), `clear_cache` after a `y/n`-style prompt only in one
  branch. Neither documents what gets deleted or that they block waiting for terminal
  input (unusable in a non-interactive/headless context without adaptation).
- **No Raises sections** on any method.
- **No Examples section** for the class as a whole.
- **`get_surf` is decorated with `@_memo`** (a simple memoization decorator defined earlier
  in the file) — repeated calls with the same arguments return a cached result rather than
  re-reading from disk; this caching behavior is invisible from the docstring and could
  surprise a caller who mutates the returned arrays in place expecting fresh reads next
  time.

## Fixed documentation

### Summary
`Database` (accessed as the module-level singleton `cortex.db`) is pycortex's interface to
the on-disk subject data store ("filestore"): surfaces, anatomical volumes, transforms,
masks, overlays, and cached derived data. Individual subjects are also accessible as
attributes, e.g. `cortex.db.S1`.

### Public methods and properties
- **`.subjects`** (property) : dict of `SubjectDB` — all subjects found in the filestore,
  keyed by name. Lazily scanned from disk on first access and cached; call
  `.reload_subjects()` to force a rescan.
- **`.reload_subjects()`** — Force the reload of the subject dictionary.
- **`.get_anat(subject, type='raw', xfmname=None, recache=False, order=1, **kwargs)`** →
  nibabel image, or ndarray if `xfmname` is given
    Return anatomical information from the filestore. Anatomical information is defined as
    any volume-space anatomical information pertaining to the subject, such as T1 image,
    white matter masks, etc. Volumes not found in the database will be automatically
    generated (by calling the matching function in `cortex.anat`, e.g. `'raw'`, `'raw_wm'`,
    `'brainmask'`, `'whitematter'` — see Issues). `type` : type of anatomical volume to
    return. `recache` : regenerate the information. If `xfmname` is given, the volume is
    additionally resampled into that transform's functional space (via
    `cortex.volume.anat2epispace`, using interpolation `order`) and an ndarray is returned
    instead of a nibabel object.
- **`.get_surfinfo(subject, type="curvature", recache=False, **kwargs)`** → `Vertex` or
  `npzfile`
    Return auxiliary surface information from the filestore (curvature, distortion,
    sulcaldepth, etc. — see `cortex.surfinfo`). A `Vertex` is returned if the underlying
    data has "left"/"right" entries; otherwise the raw `npz` file object is returned
    (remember to close it). Not found in the filestore → auto-generated via the matching
    function in `cortex.surfinfo`.
- **`.get_mri_surf2surf_matrix(subject, surface_type, hemi='both', fs_subj=None,
  target_subj='fsaverage', **kwargs)`** → list of sparse matrices
    Get the matrix generated by FreeSurfer's `mri_surf2surf` to map one subject's surface
    to another's (`cortex.freesurfer.get_mri_surf2surf_matrix`). Cached on disk after first
    computation. Requires a FreeSurfer environment the first time (uncached) it's called
    for a given subject/surface/hemi combination.
- **`.get_overlay(subject, overlay_file=None, **kwargs)`** → overlay object
    Load the subject's ROI/sulcus overlay SVG (default `overlays.svg`, or `overlay_file` if
    given) as a `cortex.svgoverlay` object, auto-importing from a legacy `rois.svg` if
    present. **No docstring in source**; has a known-broken code path for packed-subject
    loading — see Issues.
- **`.save_xfm(subject, name, xfm, xfmtype="magnet", reference=None)`**
    Load a transform into the surface database. If the transform exists already, update
    it. If it does not exist, copy the reference epi into the filestore and insert.
    `xfmtype` : `'magnet'` or `'coord'` (raises `TypeError` otherwise). `reference` :
    required if `name` not already in database. Raises `ValueError` if `reference` is
    missing for a new transform, or if masks already exist for `name` (refuses to silently
    invalidate cached masks by changing the transform).
- **`.get_xfm(subject, name, xfmtype="coord")`** → `cortex.xfm.Transform`
    Retrieves a transform from the filestore. `xfmtype` : type of transform to return.
    `name="identity"` is a special case, returning an identity transform built from the
    subject's raw anatomical affine, rather than reading a saved transform (not documented
    in source).
- **`.get_surf(subject, type, hemisphere="both", merge=False, nudge=False)`** → surfaces
    Return the surface pair for the given subject, surface type, and hemisphere. `type` :
    e.g. `fiducial`, `inflated`, `veryinflated`, `hyperinflated`, `superinflated`, `flat`.
    `merge` : vstack the hemispheres, if requesting both. `nudge` : nudge the hemispheres
    apart from each other, for overlapping surfaces (inflated, etc). Returns `left, right`
    if requesting both hemispheres (or merged `pts, polys` if `merge=True`), otherwise
    `pts, polys` for the single requested hemisphere. **Memoized** — repeated calls with
    identical arguments return a cached result (see Issues).
- **`.save_mask(subject, xfmname, type, mask)`** — Save a binary mask array for
  `(subject, xfmname)` under `type`. Raises `IOError` if a mask of that name already
  exists (refuses to overwrite), `ValueError` if `mask`'s shape doesn't match the
  transform's reference image shape. **No docstring in source.**
- **`.get_mask(subject, xfmname, type='thick')`** → ndarray of bool
    Load a saved mask; if not found on disk, auto-generates one via
    `cortex.utils.get_cortical_mask` and saves it for next time. **No docstring in
    source.**
- **`.get_shared_voxels(subject, xfmname, hemi="both", merge=True, use_astar=True,
  recache=False)`** → ndarray
    Get an array indicating which vertices are inappropriately mapped to the same voxel.
    For a given transform and surface, returns an array containing a list of vertices
    which are spatially distant on the cortical surface but that map to the same voxels
    (this occurs at sulcal crossings). Cached on disk; `recache=True` forces regeneration.
- **`.get_coords(subject, xfmname, hemisphere="both", magnet=None)`** → list of ndarray
    Calculate the coordinates of each vertex in the epi space by transforming the
    fiducial to the coordinate space. `hemisphere` : which hemisphere to return; "both"
    returns concatenated. **Deprecated** — emits `DeprecationWarning`, "Please use a Mapper
    object instead" (not stated in the docstring text itself).
- **`.get_cache(subject)`** → str
    Return (creating if necessary) the cache directory path for `subject`. **No docstring
    in source.**
- **`.clear_cache(subject, clear_all_caches=True)`**
    Clears config-specified and default file caches for a subject. **Destructive** — deletes
    and recreates cache directories on disk; may prompt interactively (`input()`) if
    `clear_all_caches=False` and files exist in the default cache location.
- **`.get_paths(subject)`** → dict
    Get a dictionary with a list of all candidate filenames for associated data, such as
    roi overlays, flatmap caches, and ctm caches.
- **`.make_subj(subject)`**
    Create the on-disk directory structure for a new subject
    (`transforms`/`anatomicals`/`cache`/`surfaces`/`surface-info`/`views`). **Destructive
    and interactive** — if `subject` already exists, prompts via `input()` requiring the
    exact text `"YES"` to confirm deleting the *entire* existing subject directory tree
    (including surfaces, transforms, everything) before recreating it; raises `ValueError`
    if not confirmed. **No docstring in source.**
- **`.save_view(vw, subject, name, is_overwrite=False)`**
    Captures the current view state from the live `cortex.webshow` instance `vw` (via
    `vw._capture_view()`) and saves it to disk as `name`. Raises `IOError` if `name`
    already exists and `is_overwrite=False`. **The shipped docstring describes the
    opposite operation** ("Set the view for an open webshow instance from a saved view") —
    that description actually matches `get_view`'s behavior, not this method's; see Issues.
- **`.get_view(vw, subject, name)`**
    Loads the previously-saved view named `name` from disk and applies it to the live
    `cortex.webshow` instance `vw` (via `vw._set_view(**view)`). Its docstring text is
    accurate for what *this* method does, but is identical to `save_view`'s (copy-pasted),
    which describes `get_view`'s behavior rather than its own — see Issues.
- **`.get_mnixfm(subject, xfm, template=None)`** → ndarray
    Get transform from the space specified by `xfm` to MNI space. Equivalent to
    `cortex.mni.compute_mni_transform`, but caches the result on disk. `xfm` can be
    `'identity'` for anatomical space. `template` : path to MNI template volume; `None`
    uses the default from `cortex.mni`.

### Raises
See per-method entries above for method-specific exceptions (`TypeError`, `ValueError`,
`IOError` are the most common, generally for invalid transform types, missing required
arguments, or refusing a destructive overwrite).

### Notes
- `cortex.db` is a ready-made singleton instance — you should not normally need to
  construct `Database()` yourself.
- Filestore location is `[basic] filestore` in `options.cfg` by default
  (`default_filestore`, imported from `cortex.options`).
- Several methods (`get_anat`, `get_surfinfo`, `get_mask`) transparently auto-generate
  missing derived data on first access, which can trigger slow external-tool calls (FSL/
  FreeSurfer, via `cortex.anat`/`cortex.surfinfo`/`cortex.utils`) and write files to the
  filestore as a side effect.
- `make_subj` and `clear_cache` require interactive terminal input in some code paths and
  are destructive — do not call them in unattended/headless scripts without care.

### Example
```python
import cortex

# The module-level singleton -- this is what you actually use:
db = cortex.db

print(sorted(db.subjects.keys()))

# Attribute-style access to a subject:
s1 = db.S1

# Load a surface:
pts, polys = db.get_surf("S1", "fiducial", merge=True)

# Load (or auto-generate) a cortical mask:
mask = db.get_mask("S1", "fullhead", "thick")
```

## Confidence / open questions
- Did not execute `make_subj`/`clear_cache` in this pass (both destructive and
  interactive) — behavior described from static source reading only.
- Could not verify from source alone what "packed subject" loading via `self.auxfile` is
  meant to look like once the acknowledged-broken `get_overlay` code path is fixed —
  flagged in `_notes.md` for maintainers rather than guessed at here.
- **Recommendation for maintainers:** fix the truncated `get_anat` docstring (`Parameters`
  and `Returns` both cut off mid-sentence); add docstrings to `get_overlay`, `save_mask`,
  `get_mask`, `get_cache`, `make_subj`; fix `save_view`'s docstring, which currently
  describes `get_view`'s behavior instead of its own; complete `__dir__`'s method list, or
  remove the override and rely on Python's default; fix or remove the acknowledged-broken
  `get_overlay` packed-subject code path.
