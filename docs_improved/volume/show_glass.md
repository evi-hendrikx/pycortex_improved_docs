# cortex.volume.show_glass

## Current signature (from source)
```python
def show_glass(dataview, pad=10):
```

## Where this is documented today
- Source docstring: `'''Create a classic "glass brain" view of the data, with the
  outline'''` (one line). [cortex/volume.py:195-209](cortex/volume.py#L195-L209)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.volume.show_glass.html

## Issues with current documentation
- **The docstring gives no indication that this function is broken and unconditionally
  fails on every call**, for two independent reasons:
  1. It references a bare name `subject` (`volume.py:198`: `nib = db.get_anat(subject,
     'fiducial')`) that is **not** a parameter of `show_glass` (the actual parameter is
     `dataview`, whose `.subject` attribute is never extracted) — this raises `NameError:
     name 'subject' is not defined` on the very first line of the function body.
  2. Even if that were fixed, the function ends with an unconditional `raise
     NotImplementedError` (`volume.py:209`), preceded by a comment: `"this requires a lot
     of logic to put the image into a canonical orientation, too much work for something
     we'll never use"` — i.e. the original author explicitly abandoned finishing this
     function.
- Also, `db.get_anat(subject, 'fiducial')` uses `'fiducial'` as an anatomical `type` —
  but `Database.get_anat`'s `type` parameter is meant to name a function in `cortex.anat`
  (`'raw'`, `'raw_wm'`, `'brainmask'`, `'whitematter'`); `'fiducial'` is not a valid
  option there either (fiducial is a *surface* type, not an anatomical-volume type) — a
  second, independent problem with the (dead, unreachable) code, on top of the `NameError`.
- **`pad` parameter is accepted but never used anywhere in the function body** — dead
  parameter.

## Fixed documentation

### Summary
**Not implemented — currently raises `NameError` immediately, and would raise
`NotImplementedError` even if that were fixed.** Intended to create a classic "glass
brain" (transparent, outline-only) view of volumetric data, but the implementation is
both incomplete and contains an unrelated bug (an undefined variable reference)
predating the point where it gives up.

### Parameters
- **dataview** : (intended) `cortex.Dataview`
    (Documented for completeness — not actually usable; see Raises. Note the function
    never actually reads `dataview` — it references an undefined `subject` name instead,
    which is an independent bug from the deliberate `NotImplementedError`.)
- **pad** : int, optional
    (Accepted but never used anywhere in the function body — dead parameter.) Default 10.

### Returns
N/A — never returns; always raises.

### Raises
- `NameError` — **always**, immediately: `db.get_anat(subject, 'fiducial')` references a
  bare name `subject` that is never defined (the function's actual parameter is
  `dataview`; its `.subject` attribute is never accessed).
- `NotImplementedError` — would also be raised (if the `NameError` above were fixed),
  unconditionally, per the author's own comment abandoning the canonical-orientation
  logic as "too much work for something we'll never use."
- Additionally, even past both of the above, `'fiducial'` is not a valid `type` for
  `Database.get_anat` (which expects an anatomical-volume type name from `cortex.anat`,
  not a surface type) — a third, independent problem in the unreachable code.

### Notes
- **Do not use — confirmed broken by inspection**, not merely undocumented.
- No working alternative for a "glass brain" view currently exists in pycortex, as far as
  this docs project's source review found.

### Example
```python
import cortex

vol = cortex.Volume.random("S1", "fullhead")
try:
    cortex.volume.show_glass(vol)
except NameError:
    print("show_glass is currently broken (undefined 'subject' reference); do not use.")
```

## Confidence / open questions
- All three issues (undefined `subject`, unconditional `NotImplementedError`, invalid
  `'fiducial'` anat type) are confirmed by direct static reading of `volume.py:195-209`
  and cross-reading `Database.get_anat`'s implementation — not confirmed by execution
  (the `NameError` would trigger immediately if run, which is consistent with this
  reading, but a live pycortex install with a subject wasn't exercised in this pass).
- **Recommendation for maintainers:** this function needs a real implementation, not a
  documentation fix — consider removing it from the public API until it's finished, since
  it currently cannot do anything useful and its docstring gives no warning of that.
