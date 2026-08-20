# cortex.freesurfer.stretch_mwall

## Current signature (from source)
```python
def stretch_mwall(pts, polys, mwall):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:1104-1114](cortex/freesurfer.py#L1104-L1114)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.stretch_mwall.html

## Issues with current documentation
- **No docstring content, Parameters, Returns, or Raises at all.**
- **Mutates `pts` in place** (`pts[mwall, 0] = ...`, etc.) while *also* returning a new
  `SpringLayout` object wrapping that same, now-mutated `pts` — the in-place mutation is a
  significant, undocumented side effect (a caller who expected a pure function and reused
  the original `pts` array afterward will see it altered). The mutation projects the
  vertex indices `mwall` (medial wall) onto a circle around their centroid, in the y-z
  plane, before handing them off to a `SpringLayout` for relaxation (with the `mwall`
  vertices pinned).
- **No explanation of what a "medial wall" is** or why stretching it onto a circle is a
  useful preprocessing step (it's the region with no real cortical data, typically
  collapsed/degenerate in flattened surfaces — pushing it out to a ring gives the relaxation
  a well-defined, non-degenerate boundary to pin against).

## Fixed documentation

### Summary
Push a surface's medial-wall vertices out onto a circle (in the y-z plane, centered on
their own centroid), then return a `SpringLayout` (with those vertices pinned) ready to
relax the rest of the mesh around this fixed boundary — a preprocessing step used before
mesh relaxation/flattening around the medial wall.

### Parameters
- **pts** : ndarray, shape (n_vertices, 3)
    Vertex coordinates. **Mutated in place** for the rows indexed by `mwall` (see Notes).
- **polys** : ndarray, shape (n_faces, 3)
    Triangle vertex-index triples.
- **mwall** : array-like of int or bool
    Indices (or boolean mask) selecting the medial-wall vertices to stretch onto a circle.

### Returns
- **layout** : `cortex.freesurfer.SpringLayout`
    A spring-relaxation layout initialized with the mesh (post-mutation `pts` as both the
    live and reference point set) and `mwall` vertices pinned in their new
    circle-projected positions.

### Raises
Not validated — an empty or out-of-range `mwall` will surface as a low-level `numpy`
indexing/shape error.

### Notes
- **Mutates `pts` in place** for the medial-wall rows — not a pure function. Pass a copy
  if you need to preserve the original coordinates.
- The "medial wall" is the region of a cortical surface with no meaningful cortical data
  (the cut edge between hemispheres); pushing it onto a well-defined circle gives mesh
  relaxation (via `SpringLayout`) a stable, non-degenerate boundary to pin against.

### Example
```python
import cortex.freesurfer as fs

# mwall: boolean array or index list marking medial-wall vertices
layout = fs.stretch_mwall(pts, polys, mwall)
for _ in range(200):
    layout.step()
relaxed_pts = layout.pts
```

## Confidence / open questions
- The in-place mutation is confirmed by static reading (`freesurfer.py:1107-1113`
  assigns directly into `pts[mwall, ...]`), not by execution.
- **Recommendation for maintainers:** add a docstring; consider returning a new array
  instead of mutating `pts` in place, or at least documenting the mutation explicitly.
