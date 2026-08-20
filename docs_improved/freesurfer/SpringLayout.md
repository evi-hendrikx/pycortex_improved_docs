# cortex.freesurfer.SpringLayout

## Current signature (from source)
```python
class SpringLayout(object):
    def __init__(self, pts, polys, dpts=None, pins=None, stepsize=1, neighborhood=0):
```

## Where this is documented today
- Source docstring: class and `__init__` both empty (`"""\n    """`).
  [cortex/freesurfer.py:1015-1102](cortex/freesurfer.py#L1015-L1102)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.SpringLayout.html

## Issues with current documentation
- **No docstring content anywhere in the class** — not on the class itself, `__init__`,
  or any of `step`, `run`, `view_step`.
- **No explanation of the physical model**: this implements a simple spring-relaxation
  layout — each vertex is pulled toward/away from its mesh neighbors to match target
  (rest-length) distances taken from `dpts`, iteratively, with optionally-pinned vertices
  held fixed. None of this is stated anywhere.
- **`pins` parameter's type/semantics are unclear from the signature alone** — accepts a
  list/set/ndarray of vertex indices to hold fixed (never moved by `.step()`); passing
  anything else (e.g. `None`, the default) means no vertices are pinned.
- **`neighborhood` is undocumented** — expands each vertex's neighbor set by this many
  additional hops (0 = direct mesh neighbors only), trading accuracy for smoother
  convergence.
- **`_estatic` (an electrostatic-repulsion term) is defined but never called** from
  `step()` (`step()`'s commented-out `+ self._estatic(i)` — dead code, and also would be
  broken since it uses `self.kdt`, which is set up as a comment (`#self.kdt =
  cKDTree(...)`) and never actually assigned anywhere in the class). Flagged as dead code
  in `_notes.md`.
- **`view_step` requires Mayavi** (GUI dependency), not mentioned.
- **No Returns documented for `.step()`**, which returns a `(dict, move)` tuple.

## Fixed documentation

### Summary
Iterative spring-relaxation mesh layout: repeatedly nudges each (non-pinned) vertex toward
satisfying target edge lengths (from a reference point set `dpts`), useful for smoothing or
relaxing a mesh (e.g. after cutting/flattening) toward more uniform edge lengths.

### Parameters (`__init__`)
- **pts** : ndarray, shape (n_vertices, 3)
    Initial (mutable, will be moved by `.step()`) vertex positions.
- **polys** : ndarray, shape (n_faces, 3)
    Triangle vertex-index triples, used to derive each vertex's mesh neighbors.
- **dpts** : ndarray, shape (n_vertices, 3), optional
    Reference point set used to compute each edge's target ("rest") length. `None`
    defaults to `pts` itself (i.e. relax `pts` toward preserving its own initial edge
    lengths).
- **pins** : list, set, or ndarray of int, optional
    Vertex indices to hold fixed — never moved by `.step()`. `None` pins nothing.
- **stepsize** : float, optional
    Scale factor applied to each computed spring force per step. Default `1`.
- **neighborhood** : int, optional
    Number of additional graph hops to expand each vertex's neighbor set by (0 = direct
    mesh neighbors only). Default `0`.

### Public methods and properties
- **`.pts`** (attribute) : ndarray, shape (n_vertices, 3) — current (mutated in place by
  `.step()`) vertex positions.
- **`.step()`** → `(dict, ndarray)`
    Perform one relaxation iteration, mutating `.pts` in place for non-pinned vertices.
    Returns `(dict(x=..., y=..., z=...), move)` — a dict of the new coordinate arrays
    (convenient for some plotting APIs) and the per-vertex displacement applied this step.
- **`.run(n=1000)`**
    Call `.step()` `n` times in a loop, printing the iteration number each time.
- **`.view_step()`**
    Advance one step and update a live Mayavi wireframe visualization (creates the
    figure on first call). **Requires Mayavi** (GUI dependency).

### Returns
See `.step()` above; `__init__`/`run`/`view_step` return `None`.

### Raises
Not validated — passing mismatched-shape `pts`/`polys`/`dpts`, or out-of-range `pins`
indices, will surface as low-level `numpy`/indexing errors rather than a clear message.

### Notes
- No FreeSurfer command dependency — pure Python/NumPy mesh relaxation.
- `view_step()` requires Mayavi installed and a display.
- An electrostatic-repulsion term (`_estatic`) is defined on the class but is dead code —
  never called from `.step()`, and would itself fail if called (relies on `self.kdt`,
  which is never actually assigned — only referenced in a comment). See `_notes.md`.
- Used internally by `cortex.freesurfer.stretch_mwall`.

### Example
```python
import cortex.freesurfer as fs

layout = fs.SpringLayout(pts, polys, pins=[0, 1, 2])
for _ in range(100):
    layout.step()
relaxed_pts = layout.pts
```

## Confidence / open questions
- The claim that `_estatic`/`self.kdt` is dead/broken code is based on static reading
  (`freesurfer.py:1049,1078-1083,1086-1087`), not execution.
- **Recommendation for maintainers:** add docstrings throughout; either wire up or remove
  the dead `_estatic`/`self.kdt` electrostatic-repulsion code path.
