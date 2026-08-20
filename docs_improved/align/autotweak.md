# cortex.align.autotweak

## Current signature (from source)
```python
def autotweak(subject, xfmname):
```

## Where this is documented today
- Source docstring: [cortex/align.py:469-480](cortex/align.py#L469-L480)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.align.autotweak.html

## Issues with current documentation
- **The docstring itself already admits the function is of dubious value**: "Ideally this
  function should actually use a limited search range, but it doesn't. It's probably not
  very useful." This is honest and useful context, but it's the *only* substantive content
  in the docstring — there's no `Returns`, `Raises`, or explanation of what it actually does
  mechanically or what "tweak" means concretely (re-runs FSL BBR from the current transform
  as its initialization, producing a *new*, separately-named transform).
- **No mention that the result is saved under a different, auto-generated name**
  (`xfmname + "_auto"`), **not** overwriting the input `xfmname` — a user could easily
  assume this modifies `xfmname` in place given the name "tweak."
- **No Returns section** — the function implicitly returns `None` always (no `noclean`
  parameter exists here, unlike its siblings `automatic`/`automatic_fsl`/`manual`, so
  there's no path to a returned temp-dir string at all — the `finally: shutil.rmtree(cache)`
  always runs unconditionally).
- **No Raises section** — `IOError` is raised if the FLIRT BBR subprocess call fails.
- **Requires a `'magnet'`-type transform to already exist** for `(subject, xfmname)`
  (`db.get_xfm(subject, xfmname, xfmtype='magnet')`) — this is a specific, undocumented
  precondition; transforms saved as `'coord'` type only (the norm for `automatic`/`manual`)
  are not what's being read here, and this distinction between `'magnet'` and `'coord'`
  transform representations is not explained anywhere in this function's docs (see
  `cortex.xfm.Transform` for the underlying representations).
- **No mention of required environment** (FSL's FLIRT, same as `automatic_fsl`).
- **No Examples section.**

## Fixed documentation

### Summary
Re-runs FSL's boundary-based registration (FLIRT BBR), initialized from an existing
`'magnet'`-type transform, to produce a refined alignment — saved as a **new** transform
named `<xfmname>_auto` (the original `xfmname` transform is left untouched). Per the
source docstring's own caveat, this doesn't restrict the search range as originally
intended and "is probably not very useful" — consider `cortex.align.automatic_fsl` or
`cortex.align.automatic` instead for most use cases.

### Parameters
- **subject** : str
    Subject identifier; must exist in the pycortex database.
- **xfmname** : str
    Name of an **existing** transform to use as the initialization for BBR refinement.
    Must have been saved with `xfmtype='magnet'` (raises an error via
    `cortex.database.Database.get_xfm` otherwise/if missing).

### Returns
`None`.

### Raises
- `IOError` — the underlying FLIRT BBR subprocess call fails (non-zero exit).
- Whatever `cortex.database.Database.get_xfm(subject, xfmname, xfmtype='magnet')` raises if
  no such magnet-type transform exists (see `cortex.database.Database`).

### Notes
- **Requires a working FSL installation** (FLIRT on `PATH`, respecting the
  `[basic] fsl_prefix` config option) — same external dependency as `automatic_fsl`.
- Saves its result as a **new** transform, `<subject>, <xfmname>_auto`, of type `'coord'` —
  does not modify or overwrite the input `xfmname` transform.
- Always cleans up its temporary working directory (no `noclean` escape hatch, unlike
  `automatic`/`automatic_fsl`/`manual`).
- Per the pycortex source's own docstring: likely not very useful in its current form
  (doesn't limit the BBR search range as intended). Prefer `cortex.align.automatic` or
  `cortex.align.automatic_fsl` for a fresh alignment.

### Example
```python
import cortex

# Requires an existing 'magnet'-type transform "S1"/"initial_xfm" in the pycortex
# database, and a working FSL installation.
cortex.align.autotweak("S1", "initial_xfm")
# Result is saved as a NEW transform: ("S1", "initial_xfm_auto")

# Inspect the result:
cortex.align.manual("S1", "initial_xfm_auto", inspect_only=True)
```

## Confidence / open questions
- Could not verify at runtime what error type/message results from calling
  `db.get_xfm(subject, xfmname, xfmtype='magnet')` when no such transform exists — not
  independently traced into `cortex.database.Database.get_xfm`'s implementation in this
  file (documented separately under the `cortex.database` module).
- **Recommendation for maintainers:** given the docstring already flags this function as
  "probably not very useful," consider either fixing the intended limited-search-range
  behavior, or deprecating/removing it in favor of `automatic`/`automatic_fsl`; at minimum,
  document the `_auto`-suffix output naming and the `'magnet'`-type transform precondition.
