# cortex.segment.cut_surface

## Current signature (from source)
```python
def cut_surface(
    cx_subject,
    hemi,
    name="flatten",
    fs_subject=None,
    data=None,
    freesurfer_subject_dir=None,
    flatten_with="freesurfer",
    method=None,
    do_import_subject=True,
    blender_path=default_blender_path,
    recache=True,
    auto_overwrite=False,
    **kwargs,
):
```

## Where this is documented today
- Source docstring: [cortex/segment.py:147-197](cortex/segment.py#L147-L197)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.segment.cut_surface.html

## Issues with current documentation
- **No Returns section** — returns `None` always (returns early, also `None`, if
  flattening is aborted/declined).
- **No Raises section** — raises `ValueError` if fiducial/inflated vertex counts don't
  match, or if `flatten_with` isn't one of the three recognized values; `AssertionError`
  if `flatten_with="blender"` and `method` is `None`.
- **`method`'s docstring says it must be present "When using Blender"** but doesn't state
  this is enforced via a bare `assert method is not None, "..."` (raises
  `AssertionError`, not a more typical `ValueError`/`TypeError`) — worth knowing since
  `assert` statements are stripped when Python is run with `-O`.
- **`**kwargs` forwarding is unstated.** Extra kwargs are forwarded to either
  `cortex.freesurfer.flatten` (when `flatten_with="freesurfer"`) or `flatten_slim` (when
  `flatten_with="SLIM"`) — not mentioned in the docstring at all, and the two targets
  accept different keyword sets.
- **Likely bug when `flatten_with="SLIM"`**: the code sets
  `path_type, flat_type = "slip", "slim"` (`segment.py:294`) — `"slip"` looks like a typo
  for `"slim"`. Since `path_type` is later passed as the `type` argument to
  `cortex.freesurfer.get_paths`, and `get_paths` silently returns `None` for any
  unrecognized `type` value (see `freesurfer/get_paths.md`'s Issues), the subsequent
  `if do_import_subject:` branch's `os.path.exists(other)` call would receive `other=None`
  and raise `TypeError` rather than proceeding as intended. Flagged as a likely real bug,
  not fixed here — see `_notes.md`.
- **No mention this opens Blender interactively** and requires the user to manually save
  and close it before the function continues (blocking on `blender.fs_cut_open`).

## Fixed documentation

### Summary
Initializes an interface to cut the segmented surface for flatmapping. This function
creates or opens a blend file in your filestore which allows surfaces to be cut along
hand-defined seams. Blender will automatically open the file. After edits are made,
remember to save the file, then exit Blender.

The surface will be automatically extracted from blender then run through the
`mris_flatten` command in freesurfer (or SLIM, or blender, depending on `flatten_with`).
The flatmap will be imported once that command finishes if `do_import_subject` is `True`
(default value).

### Parameters
- **cx_subject** : str
    Name of the subject to edit (pycortex subject ID)
- **hemi** : str
    Which hemisphere to flatten. Should be "lh" or "rh"
- **name** : str, optional
    String name of the current flatten attempt. Defaults to "flatten"
- **fs_subject** : str
    Name of Freesurfer subject (if different from pycortex subject). `None` defaults to
    `cx_subject`.
- **data** : Dataview or list of Dataview
    A data view object or list of data view objects to display on the surface as a cutting
    guide.
- **freesurfer_subject_dir** : str
    Name of Freesurfer subject directory. `None` defaults to `SUBJECTS_DIR` environment
    variable.
- **flatten_with** : {'freesurfer', 'SLIM', 'blender'}, default `'freesurfer'`
    'freesurfer' uses freesurfer's `mris_flatten` function to flatten the cut surface.
    'SLIM' uses the SLIM algorithm, which takes much less time but tends to leave more
    distortions in the flatmap. SLIM is an optional dependency, and must be installed to
    work; clone the code
    (https://github.com/MichaelRabinovich/Scalable-Locally-Injective-Mappings) to your
    computer and set the slim dependency path in your pycortex config file to point to
    `</path/to/your/slim/install>/ReweightedARAP`. **`flatten_with="SLIM"` currently
    appears to trigger a code bug on the import step — see Issues.**
- **method** : str
    Method to use for UV unwrap. When using Blender, it must be present (enforced via
    `assert method is not None`) and can be one of 'CONFORMAL', 'ANGLE_BASED',
    'MINIMUM_STRETCH'.
- **do_import_subject** : bool
    Set option to automatically import flatmaps when both are completed (if set to false,
    you must import later with `cortex.freesurfer.import_flat()`).
- **blender_path** : str
    Path to blender executable. If None, defaults to path specified in pycortex config
    file.
- **recache** : boolean
    Whether or not to recache intermediate files. Takes longer this way, potentially
    resolves some errors. Useful if you've made changes to the alignment.
- **auto_overwrite** : bool
    Whether to overwrite existing flatmaps. If True, the flatmap will be overwritten
    without asking for confirmation.
- **\*\*kwargs**
    Forwarded to `cortex.freesurfer.flatten` (if `flatten_with="freesurfer"`, e.g.
    `save_every`) or `flatten_slim` (if `flatten_with="SLIM"`).

### Returns
`None`. Also returns early (`None`) if the flattening step reports it was not run/aborted
(e.g. `freesurfer.flatten`'s interactive confirmation was declined).

### Raises
- `ValueError` — fiducial and inflated vertex counts don't match for `fs_subject`/`hemi`
  (re-import needed); `flatten_with` isn't one of `'freesurfer'`, `'SLIM'`, `'blender'`.
- `AssertionError` — `flatten_with="blender"` and `method` is `None`.

### Notes
- **Opens Blender interactively** (`blender.fs_cut_open`) and blocks until the user saves
  and closes it.
- **Requires FreeSurfer** (`mris_flatten`, if `flatten_with="freesurfer"`), **Blender**
  (always, for the cutting step itself, plus for `flatten_with="blender"`'s UV unwrap),
  and, for `flatten_with="SLIM"`, a separately-installed SLIM dependency configured via
  `options.cfg`'s `[dependency_paths] slim` key.
- Writes/reuses a cached `.blend` file per `(cx_subject, hemi, name)` under the subject's
  anatomicals path.

### Example
```python
import cortex

# Requires FreeSurfer + Blender installed. Opens Blender interactively; blocks until
# the cut-surface .blend file is saved and closed, then runs mris_flatten.
cortex.segment.cut_surface("S1", "lh", name="flatten_v1")
```

## Confidence / open questions
- The `"slip"`/`"slim"` typo and its downstream `TypeError` consequence is inferred by
  static reading of `segment.py:294` combined with `cortex.freesurfer.get_paths`'s
  silent-`None`-return behavior for unrecognized `type` values — not confirmed by actually
  running `cut_surface(..., flatten_with="SLIM")` with a working SLIM install in this
  pass.
- Did not run Blender/FreeSurfer/SLIM in this pass.
- **Recommendation for maintainers:** fix the `"slip"` → `"slim"` typo at
  `segment.py:294`; add Returns/Raises; enumerate the `**kwargs` forwarding targets.
