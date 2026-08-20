# cortex.segment.fix_wm

## Current signature (from source)
```python
def fix_wm(subject):
```

## Where this is documented today
- Source docstring: [cortex/segment.py:505-523](cortex/segment.py#L505-L523)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.segment.fix_wm.html

## Issues with current documentation
- **No Returns section** — returns `None` always.
- **No Raises section.**
- **Deprecation notice is only a runtime warning, not in the docstring text**, and — more
  importantly — **references a function, `rerun_recon()`, that does not exist anywhere in
  the pycortex codebase.** The warning says: *"We recommend using edit_segmentation() and
  rerun_recon() instead of fix_wm() and fix_pia()."* `edit_segmentation` does exist (in
  this same module, not in the scope list for this docs project), but a repo-wide search
  finds no `rerun_recon` function defined anywhere — this deprecation guidance points
  users to a function that doesn't exist. Flagged as a likely doc/code bug, not fixed here
  — see `_notes.md`.
- **No mention of the required tools** (FreeSurfer's `tkmedit`, Mayavi) or that this opens
  multiple blocking interactive GUI windows and an `input()` prompt.

## Fixed documentation

### Summary
Initializes an interface to make white matter edits to the surface. This will open two
windows -- a tkmedit window that makes the actual edits, as well as a mayavi window to
display the surface. Clicking on the mayavi window will drop markers which can be loaded
using the "Goto Save Point" button in tkmedit.

If you wish to load the other hemisphere, simply close the mayavi window and the other
hemisphere will pop up. Mayavi will stop popping up once the tkmedit window is closed.

Once the tkmedit window is closed, a variety of autorecon options are available. When
autorecon finishes, the new surfaces are immediately imported into the pycortex database.

**Deprecated** — see Notes.

### Parameters
- **subject** : str
    Name of the subject to edit

### Returns
`None`.

### Raises
Propagates `subprocess.CalledProcessError` from the underlying `cortex.freesurfer.autorecon`
call if the user chooses to run one, and any error from
`cortex.freesurfer.import_subj` at the end.

### Notes
- **Deprecated at runtime** (`DeprecationWarning`-style message), recommending
  `edit_segmentation()` and a `rerun_recon()` function instead — **`rerun_recon()` does
  not currently exist in pycortex** (see Issues); treat this deprecation guidance as only
  partially actionable until that's resolved upstream.
- **Requires FreeSurfer** (`tkmedit`) **and Mayavi** (GUI dependencies) and blocks on
  multiple interactive windows plus a terminal `input()` prompt choosing among
  autorecon-wm / autorecon-cp / do nothing.
- Re-imports the subject into pycortex (`cortex.freesurfer.import_subj`) automatically
  after autorecon finishes (unless "do nothing" is chosen).

### Example
```python
import cortex

# Deprecated. Requires FreeSurfer + Mayavi installed and a display.
# Opens tkmedit + Mayavi windows, then prompts interactively in the terminal.
cortex.segment.fix_wm("S1")
```

## Confidence / open questions
- The claim that `rerun_recon` doesn't exist is based on a repo-wide grep for
  `def rerun_recon` across `cortex/`, which returned no matches.
- Did not run `tkmedit`/Mayavi in this pass.
- **Recommendation for maintainers:** either implement `rerun_recon()` or update the
  deprecation message to point to an actually-existing replacement; add Returns/Raises.
