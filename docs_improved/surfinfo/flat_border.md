# cortex.surfinfo.flat_border

## Current signature (from source)
```python
def flat_border(outfile, subject):
```

## Where this is documented today
- Source docstring: none. [cortex/surfinfo.py:155-221](cortex/surfinfo.py#L155-L221)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.surfinfo.flat_border.html
  (no docstring content beyond the bare signature).

## Issues with current documentation
- **No docstring at all.**
- **Appears to be currently broken (unconditionally) — likely `NameError`.** The function
  references a bare name `height` (`surfinfo.py:204`: `aspect = (height /
  (flatpts.max(0) - flatpts.min(0))[1])`) that is not a parameter of `flat_border`, not
  assigned anywhere earlier in the function, not imported, and not a module-level global
  in `cortex/surfinfo.py`. As written, **every call to this function should raise
  `NameError: name 'height' is not defined`.** This looks like leftover/incomplete code —
  possibly intended to be a parameter (mirroring `height` in `cortex.quickflat`'s
  functions) that was never added to the signature. Flagged, not fixed — see `_notes.md`.
- **Also likely broken on modern NetworkX**: `fog.degree().items()`
  (`surfinfo.py:183`) uses the NetworkX 1.x `Graph.degree()` API, which returned a dict
  supporting `.items()`; in NetworkX >= 2.0, `.degree()` returns a `DegreeView` which does
  **not** support `.items()` (iterate it directly instead, as `(node, degree)` pairs) —
  this would raise `AttributeError` on any current NetworkX version, in addition to (and
  independently of) the `NameError` above.
- **Not documented as the auto-generation target of `cortex.db.get_surfinfo(subject,
  type="flat_border")`.**
- Several variables (`ismwalls`, `lines`, saved to `outfile`) have no explanation of their
  meaning/format.

## Fixed documentation

### Summary
Intended to compute the flatmap's boundary/cut-edge lines (distinguishing medial-wall
boundary segments from other cut edges) and save them for use as an overlay reference.
**As currently written in this version of pycortex, this function is broken and will raise
an exception on any call** — see Issues.

### Parameters
- **outfile** : str
    Path where the border-line data would be saved (if the function worked).
- **subject** : str
    Subject in the pycortex database for whom the flatmap border would be computed.

### Returns
`None` (intended). Would write `outfile` as an `.npz` with `lines` (a list of per-boundary-
segment 2D point arrays) and `ismwalls` (a parallel list of booleans marking which segments
are medial-wall boundary vs. other cut edges), if the function ran successfully.

### Raises
- `NameError` — **always**, currently, at `aspect = (height / ...)`: `height` is
  referenced but never defined anywhere in scope (see Issues).
- `AttributeError` — would also occur (masked by the `NameError` above, since it happens
  earlier in the function) on any NetworkX version >= 2.0, from `fog.degree().items()`.

### Notes
- **This function currently cannot run to completion** — flagged as a likely real code
  bug, not a documentation gap, per project scope (not fixed here).
- Would require `networkx` (imported lazily) if the `NameError` were fixed.
- No FreeSurfer/FSL/GUI dependency otherwise.
- Normally would be invoked indirectly via `cortex.db.get_surfinfo(subject,
  type="flat_border")` — that call will currently fail with the errors above.

### Example
```python
import cortex

# NOTE: as of the current pycortex source, this call is expected to raise
# NameError: name 'height' is not defined (see Issues). Included here to
# document the intended call signature, not as a working example.
cortex.surfinfo.flat_border("s1_flat_border.npz", "S1")
```

## Confidence / open questions
- The `NameError` is confirmed by static reading of `surfinfo.py:204` — `height` does not
  appear as a parameter, local assignment, import, or module-level name anywhere in
  `cortex/surfinfo.py`. Not independently confirmed by running the function (which would
  itself confirm the `NameError` immediately, but a live pycortex install with a subject
  wasn't available in this pass).
- The NetworkX `.degree().items()` issue is a well-known 1.x→2.x breaking change,
  confirmed by static reading, not execution — and is masked by the earlier `NameError` in
  current control flow, so wouldn't be hit until the first bug is fixed.
- **Recommendation for maintainers:** this function needs an actual code fix, not just
  documentation — define/parameterize `height`, and update the NetworkX `.degree()` usage
  to the modern API. Until fixed, consider either removing it from the public API or
  marking it clearly broken in the source itself.
