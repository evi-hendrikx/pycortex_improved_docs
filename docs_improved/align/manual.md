# cortex.align.manual

## Current signature (from source)
```python
def manual(
    subject,
    xfmname,
    output_name="register.lta",
    wm_color="yellow",
    pial_color="blue",
    wm_surface='white',
    noclean=False,
    reference=None,
    inspect_only=False,
):
```

## Where this is documented today
- Source docstring: [cortex/align.py:111-165](cortex/align.py#L111-L165)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.align.manual.html

## Issues with current documentation
- **Docstring/code drift on default colors.** The docstring says `wm_color : str | "blue"`
  (implying default `"blue"`) and `pial_color : str | "red"` (implying default `"red"`) —
  but the actual signature defaults are `wm_color="yellow"`, `pial_color="blue"`. This is a
  direct, confirmed mismatch between documented and actual defaults.
  is `wm_color="yellow"`, `pial_color="blue"` — do not trust the docstring's stated
  defaults.
- **`wm_surface` is completely undocumented in the `Parameters` section's usual place** —
  its entry appears, but *after* the `Returns`-adjacent block in a way that's easy to miss
  (it's the last parameter listed, out of declaration order relative to the signature) and
  its description ("name for white matter surface to use. 'white' or 'smoothwm'") doesn't
  explain what visually differs between the two options.
- **No mention of the required environment.** This function shells out to the FreeSurfer
  `freeview` GUI and `lta_convert` CLI tool (via `subprocess.call(cmd, shell=True)`) and
  relies on the `$SUBJECTS_DIR` environment variable already being set correctly (baked
  directly into the shell command string) — none of this is stated. A user without
  FreeSurfer installed/configured will get an opaque non-zero exit code raising
  `IOError("Problem with FreeView!")` with no further explanation.
- **`Returns` section says "Nothing unless noclean is true"** but doesn't say what is
  returned when it *is* true (the path to the temp cache directory, as a `str`) — should be
  stated as an explicit type.
- **No Raises section** despite several explicit `raise` statements with different
  triggers: `ValueError` (masks already cached and `inspect_only=False`, or a `reference`
  is given for an existing transform without masks/no `inspect_only`), `IOError` (FreeView
  or `lta_convert` returns non-zero).
- **Precondition on `reference`'s interaction with existing/new transforms is confusing in
  prose**: reading the source, the actual rule is: if `xfmname` already exists in the
  database, `reference` **must** be left `None` (passing a real path raises `ValueError`
  refusing to overwrite); if `xfmname` does **not** yet exist, `reference` must be given
  (implicitly — if left `None` in that branch, the function prints "Transform does not
  exist!" and then still proceeds to try to use `sub_xfm`, which won't be defined,
  producing an `UnboundLocalError` rather than a clean early exit — this looks like an
  actual bug, not fully caught by the `try/except IOError`, since it only catches during the
  initial `db.get_xfm` lookup, not the later `if reference is None:` branch's fallback
  behavior).
- **No Examples section**, unsurprising given this launches an interactive GUI, but a
  pseudo-runnable walkthrough (what to actually do inside FreeView, where to save the
  output) is missing.
- **The "IMPORTANT" note about where the `.lta` file must be saved is present but buried in
  prose** rather than being a clearly marked warning — a user who saves the file to the
  wrong location will get an unhelpful failure from `lta_convert`.

## Fixed documentation

### Summary
Opens FreeSurfer's FreeView GUI for manually aligning/adjusting a functional volume to a
subject's cortical surface, then saves the result as a pycortex transform.

### Parameters
- **subject** : str
    Subject identifier; must exist in the pycortex database and be a valid FreeSurfer
    subject under `$SUBJECTS_DIR`.
- **xfmname** : str
    Name of the transform to create (requires `reference`) or modify (requires
    `reference=None`).
- **output_name** : str, default `"register.lta"`
    Filename FreeView must save the registration under.
- **wm_color** : str, default `"yellow"`
    Color of the white matter surface outline in FreeView. (Docstring previously said
    `"blue"` — see Issues.)
- **pial_color** : str, default `"blue"`
    Color of the pial surface outline. (Docstring previously said `"red"` — see Issues.)
- **wm_surface** : {'white', 'smoothwm'}, default `'white'`
    Which white matter surface to display/edit against.
- **noclean** : bool, default `False`
    If `True`, don't delete the temp working directory; return its path instead of `None`.
- **reference** : str, optional
    Path to the functional reference volume. Required for a brand-new transform; must be
    `None` when modifying an existing one (raises `ValueError` otherwise).
- **inspect_only** : bool, default `False`
    If `True`, open for viewing only — nothing is saved on close.

### Returns
- `None`, unless `noclean=True`, in which case the `str` path to the (not-deleted)
  temporary FreeView working directory is returned.

### Raises
- `ValueError` — a `reference` is given for an already-existing `xfmname`; masks are
  already cached for `xfmname` and `inspect_only=False` (must delete cached masks by hand
  first, or pass `inspect_only=True` to just view).
- `IOError` — the `freeview` process or `lta_convert` conversion step exits with a non-zero
  status (commonly: FreeSurfer/`freeview`/`lta_convert` not installed or not on `PATH`, or
  `$SUBJECTS_DIR` not set/incorrect).
- `UnboundLocalError` (likely unintended) — if `xfmname` does not yet exist **and**
  `reference` is left `None`: the function only prints `"Transform does not exist!"` and
  then falls through to code that assumes a previously-loaded `sub_xfm` object, which was
  never assigned on this path. Treat "must supply `reference` for a brand-new transform" as
  a hard requirement even though it isn't enforced with a clean error message (see
  `_notes.md`).

### Notes
- **Requires a working FreeSurfer installation** (`freeview`, `lta_convert` on `PATH`) with
  `$SUBJECTS_DIR` set to the directory containing `subject`'s FreeSurfer output, and
  requires an interactive display (opens a GUI window) — cannot be run headless.
- Not runnable in a typical automated/CI/notebook context; intended for interactive manual
  alignment work at a workstation with FreeSurfer + a display.
- The registration produced inside FreeView **must be saved, from within FreeView itself,**
  to the exact path printed by this function (`<tempdir>/<output_name>`) — pycortex has no
  way to detect the save otherwise.
- On success, saves a new/updated `'coord'`-type transform for `(subject, xfmname)` into the
  pycortex database via `cortex.database.Database.save_xfm`.
- Deprecated sibling: `cortex.align.fs_manual` is a deprecated alias for this exact
  function (kept for backward compatibility, emits `DeprecationWarning`).
- Distinct, separately-deprecated function: `cortex.align.mayavi_manual` is the *old*
  (Mayavi-based, not FreeView-based) manual aligner GUI, superseded by this function — also
  emits `DeprecationWarning` and requires Mayavi rather than FreeSurfer.

### Example
```python
import cortex

# Manually align a new functional reference volume to subject S1's cortical surface,
# creating a new transform named "manual_example".
# This opens the FreeView GUI -- interactive step required.
#
# In FreeView: adjust the overlaid wm/pial surface contours to match the anatomy in
# the reference volume, then save the registration via FreeView's own File > Save
# Registration As... dialog, to the exact path printed to the console by this call.
cortex.align.manual(
    "S1",
    "manual_example",
    reference="/path/to/functional_reference.nii.gz",
)

# To re-open and tweak an existing transform later (no `reference` needed/allowed):
cortex.align.manual("S1", "manual_example")

# To just view an existing transform without risk of modifying it:
cortex.align.manual("S1", "manual_example", inspect_only=True)
```

## Confidence / open questions
- The `UnboundLocalError` scenario (brand-new `xfmname` with `reference=None`) is inferred
  from static control-flow reading of `align.py:174-196`, not confirmed by execution
  (would require a FreeSurfer environment to trigger safely).
- Could not run FreeView/FreeSurfer in this pass to confirm the exact end-to-end behavior;
  all "Notes" about GUI mechanics are read from source comments/print statements, not
  observed directly.
- **Recommendation for maintainers:** fix the `wm_color`/`pial_color` docstring defaults to
  match the signature; add an explicit, early, clear error (rather than an
  `UnboundLocalError`) when `reference is None` and `xfmname` doesn't yet exist; add
  Returns/Raises sections; note the FreeSurfer/GUI/`$SUBJECTS_DIR` requirements explicitly
  near the top of the docstring rather than only implied by the body.
