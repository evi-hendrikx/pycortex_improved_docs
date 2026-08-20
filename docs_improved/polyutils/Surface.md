# cortex.polyutils.Surface

## Current signature (from source)
```python
class Surface(exact_geodesic.ExactGeodesicMixin, subsurface.SubsurfaceMixin):
    def __init__(self, pts, polys):
```
`Surface` is a large class (~30 public methods/properties across
`cortex/polyutils/surface.py`, plus two mixins: `ExactGeodesicMixin` in `exact_geodesic.py`
and `SubsurfaceMixin` in `subsurface.py`). This file covers the full public interface;
private (`_`-prefixed) helpers and trivial dunders are omitted per project scope.

## Where this is documented today
- Source docstring (class + `__init__`): [cortex/polyutils/surface.py:22-43](cortex/polyutils/surface.py#L22-L43)
- Per-method docstrings scattered throughout `surface.py`, `exact_geodesic.py`,
  `subsurface.py` — see per-method notes below for gaps.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.polyutils.Surface.html

## Issues with current documentation
- **This class is, overall, one of the better-documented in pycortex** (most
  numerically-heavy methods have full NumPy-style docstrings with math references), but
  coverage is inconsistent:
  - **`boundary_vertices`, `edge_lengths`, `iter_surfedges_weighted` have only informal,
    non-NumPy-style docstrings** (no `Returns` section, algorithm described in prose
    comments).
  - **`iter_surfedges`, `get_graph`, `weighted_distance_graph`, `extract_geodesic_chunk`,
    `polyhedra`, `patches` have minimal or no docstrings.**
  - **`edge_collapse` raises `NotImplementedError` on its first line** — dead/unfinished
    code (see `_notes.md`).
  - **`extract_chunk`'s one-line docstring says "for testing purposes"** but doesn't
    document its parameters, return value, or that `seed=None` picks a random start
    vertex.
- **No Raises sections anywhere** in the class.
- **No Examples section** for the class as a whole.
- **`SubsurfaceMixin` methods are individually reasonably documented (informal NumPy-ish
  style)**, but the mixin's own class docstring — which explains the actual motivation
  (performance) for using subsurfaces at all — isn't cross-referenced from any of
  `Surface`'s own docs, so a reader browsing `Surface`'s method list wouldn't easily
  discover why `get_geodesic_patch` (subsurface-based) differs from `geodesic_distance`
  (full-surface).
- **`exact_geodesic_distance`/`call_vtp_geodesic` require a separately-compiled external
  VTP executable** configured via `options.cfg`'s `[geodesic] vtp_path` — this hard
  external dependency is documented reasonably well in `call_vtp_geodesic`'s own
  docstring, but has no `Returns` section, and the dependency isn't mentioned in
  `exact_geodesic_distance`'s (the more commonly called) docstring at all.

## Fixed documentation

### Summary
Represents a single cortical hemisphere surface (white matter, pial, fiducial, inflated,
flattened, etc.) and implements a large set of geometric/analytical operations on it:
curvature, smoothing, gradients, geodesic distance, mesh interpolation, subsurface
extraction, and more.

### Parameters (`__init__`)
- **pts** : 2D ndarray, shape (total_verts, 3)
    Location of each vertex in space (mm). Order is x, y, z.
- **polys** : 2D ndarray, shape (total_polys, 3)
    Indices of the vertices in each triangle in the surface.

### Public methods and properties

**Basic geometry** (all memoized properties, i.e. computed once and cached):
- **`.ppts`** : ndarray, shape (n_faces, 3, 3) — 3D matrix of points in each face: n faces
  x 3 points per face x 3 coords per point.
- **`.connected`** : sparse matrix — vertex-face associations.
- **`.adj`** : sparse matrix — vertex adjacency matrix.
- **`.face_normals`** : ndarray, shape (n_faces, 3) — normal vector for each face.
- **`.vertex_normals`** : ndarray, shape (n_verts, 3) — normal vector for each vertex
  (average of neighboring face normals).
- **`.face_areas`** : ndarray, shape (n_faces,) — area of each face.
- **`.cotangent_weights`** : ndarray, shape (3, n_faces) — cotangent of the angle opposite
  each vertex in each face.
- **`.avg_edge_length`** : float — average length of all edges in the surface.
- **`.edge_lengths`** : ndarray, shape (3 * n_faces,) — vector of edge lengths (same
  iteration order as `iter_surfedges`; border edges appear once, non-border edges twice).
- **`.boundary_vertices`** : ndarray of bool, shape (n_verts,) — mask of boundary
  (border) vertices, found via the standard "edges appearing in exactly 1 face are
  border edges" rule.
- **`.graph`** : `networkx.Graph` — undirected graph representing this surface's edges.
- **`.get_graph()`** — returns `.graph` (a plain method wrapper, no added behavior).
- **`.weighted_distance_graph`** : `networkx.Graph` — like `.graph`, but with edges
  weighted by 3D edge length.
- **`.iter_surfedges`** : generator of (int, int) — yields each triangle's three edges as
  vertex-index pairs.
- **`.iter_surfedges_weighted`** : generator of (int, int, float) — like
  `iter_surfedges`, with edge lengths attached (same iteration order as `.edge_lengths`).

**Curvature and Laplace-Beltrami operator:**
- **`.laplace_operator`** (property) → `(B, D, W, V)` sparse matrices
    Laplace-Beltrami operator for this surface — a sparse adjacency matrix with edge
    weights determined by the cotangents of the angles opposite each edge. `D` is the
    lumped mass matrix, `W` the weighted adjacency matrix, `V` a diagonal normalizing
    matrix (stiffness matrix = `V - W`; full LB operator = `D⁻¹(V - W)`); `B` is the FEM
    mass matrix. See Reuter et al., 2009, "Discrete Laplace-Beltrami operators for shape
    analysis and segmentation."
- **`.mean_curvature()`** → ndarray, shape (n_verts,)
    Compute mean curvature using the Laplace-Beltrami operator. Negative = folded inward
    (sulcus), positive = folded outward (gyrus). Noisy — consider smoothing with
    `.smooth()`.
- **`.smooth(scalars, factor=1.0, iterations=1)`** → ndarray, shape (n_verts,)
    Smooth a vertex-wise function across the surface using mean curvature flow. `factor`
    controls smoothing strength; `iterations` repeats the process.

**Gradients and interpolation:**
- **`.surface_gradient(scalars, at_verts=True)`** → ndarray, shape (n_verts, 3) or
  (n_faces, 3)
    Gradient of a per-vertex function, evaluated at vertices (default) or faces.
- **`.create_biharmonic_solver(boundary_verts, clip_D=0.1)`** → `(lhs, D, Dinv, lhsfac,
  notboundary)`
    Set up the biharmonic equation with Dirichlet boundary conditions and precompute its
    Cholesky (or LU) factorization, for solving smooth interpolation problems with fixed
    boundary values.
- **`.interp(verts, vals)`** → ndarray, shape (n_verts, dimensions)
    Interpolate a function given at knot points `verts` (with values `vals`) across the
    whole surface using biharmonic interpolation. For repeated interpolation with the same
    knot points, precompute via the private `_create_interp` instead (documented as an
    optimization tip in `.interp`'s own docstring, though `_create_interp` itself is
    private and not separately documented here per project scope).

**Geodesic distance:**
- **`.approx_geodesic_distance(verts, m=0.1)`** → ndarray, shape (n_verts,)
    Fast but inaccurate approximate geodesic distance from every vertex to the closest
    vertex in `verts`, via Varadhan's heat-kernel formula. Use with care.
- **`.geodesic_distance(verts, m=1.0, fem=False)`** → ndarray, shape (n_verts,)
    Minimum mesh geodesic distance from every vertex to the closest vertex in `verts`,
    via the heat method (Crane et al., 2012). Caches sparse LU factorizations, so repeated
    calls (even with different `verts`) are fast after the first. Time is independent of
    `len(verts)`.
- **`.geodesic_path(a, b, max_len=1000, d=None, **kwargs)`** → list of int
    Greedy shortest path (by geodesic distance) from vertex `a` to vertex `b`. `**kwargs`
    forwarded to `geodesic_distance`. Can get stuck in loops for some meshes — bounded by
    `max_len`.
- **`.exact_geodesic_distance(vertex)`** (from `ExactGeodesicMixin`) → ndarray, shape
  (n_verts,)
    Exact (not heat-approximated) geodesic distance from `vertex` (or the minimum over a
    list of vertices), via an externally-compiled VTP executable. Requires
    `options.cfg`'s `[geodesic] vtp_path` to be set to a compiled VTP binary; raises
    `ExactGeodesicException` if unset/missing/the binary fails.

**Subsurfaces** (from `SubsurfaceMixin` — see `subsurface.py`'s module docstring: these
trade a small per-call setup cost for much faster repeated operations on a bounded region
of cortex, compared to running the full-surface equivalents):
- **`.create_subsurface(vertex_mask=None, polygon_mask=None)`** → `Surface`
    Create a new `Surface` restricted to a vertex or polygon mask (specify one; the final
    vertex set is always derived from the polygon mask, to avoid dangling vertices).
- **`.get_connected_vertices(vertex, mask, old_version=False)`** → ndarray of bool
    Vertices connected to `vertex` (breadth-first) that satisfy `mask`.
- **`.get_euclidean_ball(xyz, radius)`** → ndarray of bool
    Vertices within Euclidean distance `radius` of the 3D point `xyz`.
- **`.get_euclidean_patch(vertex, radius, old_version=False)`** → dict with `'vertex_mask'`
    Connected vertices within Euclidean distance `radius` of `vertex`.
- **`.get_geodesic_patch(vertex, radius, attempts=5, m=1.0, old_version=False)`**
    Vertices within geodesic distance `radius` of `vertex`, using a subsurface for speed.
- **`.get_geodesic_patches(radius, seeds=None, n_random_seeds=None, output='dense')`**
    Batch version of `get_geodesic_patch` over multiple seed vertices.
- **`.get_geodesic_strip_patch(v0, v1, radius, room_factor=2, method='bb', ...)`**
    Extract a patch forming a "strip" between two vertices, within a geodesic radius.
- **`.get_strip_coordinates(v0, v1, geodesic_path=None, distance_algorithm='softmax')`**
    Compute per-vertex coordinates along a strip between `v0` and `v1`.
- **`.lift_subsurface_data(data, vertex_mask=None)`**
    Map data computed on a subsurface back onto the full surface's vertex indexing.
- **`.furthest_border_points`** (property)
    Points on the subsurface's border that are geodesically furthest apart.
- **`.plot_subsurface_rotating_gif(...)`**
    Render a rotating GIF visualization of a subsurface. **Requires Mayavi/matplotlib
    animation support** (GUI/rendering dependency).

**Mesh extraction / miscellaneous:**
- **`.extract_chunk(nfaces=100, seed=None, auxpts=None)`** → `(pts, polys)` or
  `(pts, aux, polys)`
    Extract a small chunk of the surface via breadth-first search, for testing purposes.
    `seed=None` picks a random starting vertex.
- **`.extract_geodesic_chunk(origin, radius)`** → `(pts, polys)`
    Extract the sub-mesh within geodesic `radius` of `origin`.
- **`.polyhedra(wm)`** → generator
    Iterates through the polyhedra that make up the closest volume to each vertex (used
    for volume-fraction-style computations between two surfaces, e.g. white matter and
    pial).
- **`.patches(auxpts=None, n=1)`** → generator
    Iterates through small local patches around each vertex (`n=1`: full 1-ring faces;
    `n=0.5`: half-edge patches; raises `ValueError` for other `n`).
- **`.edge_collapse(p1, p2, target)`** — **Not implemented.** Raises `NotImplementedError`
  unconditionally; dead/unfinished code (see `_notes.md`).

### Returns
See per-method entries above.

### Raises
- `Exception` — `create_subsurface` if neither `vertex_mask` nor `polygon_mask` given.
- `ValueError` — `patches` with `n` not in `{1, 0.5}`.
- `ExactGeodesicException` — `exact_geodesic_distance`/`call_vtp_geodesic` if the VTP
  executable isn't configured, doesn't exist, or fails.
- `NotImplementedError` — `edge_collapse` (unconditional).

### Notes
- Most geometric properties are memoized (`@_memo`) — computed once per `Surface`
  instance and cached; mutating `.pts`/`.polys` after first access will **not**
  automatically invalidate the cache.
- `geodesic_distance`/`approx_geodesic_distance` cache sparse factorizations on the
  instance (`self._rlfac_solvers`, `self._nLC_solvers`), keyed by the `m` parameter —
  repeated calls with the same `m` are much faster after the first.
- `exact_geodesic_distance` requires a separately-compiled external VTP executable
  (not bundled with pycortex) configured via `options.cfg`.
- `SubsurfaceMixin` methods trade setup cost for speed on bounded regions — see the
  mixin's own module docstring in `cortex/polyutils/subsurface.py` for rough benchmark
  numbers (full-surface `geodesic_distance`: ~10s startup, ~200ms per call; subsurface:
  ~40-200ms startup depending on radius).
- No FreeSurfer/FSL dependency for most of the class; `plot_subsurface_rotating_gif`
  requires a plotting/animation backend.

### Example
```python
import cortex

subject = "S1"
pts, polys = cortex.db.get_surf(subject, "fiducial", merge=True)
surf = cortex.polyutils.Surface(pts, polys)

curv = surf.mean_curvature()
smoothed_curv = surf.smooth(curv, factor=1.0, iterations=2)

# Geodesic distance from a seed vertex to every other vertex:
dist = surf.geodesic_distance([0])

# A small local patch around a vertex, for fast repeated operations:
patch = surf.get_geodesic_patch(vertex=0, radius=15)
```

## Confidence / open questions
- Did not exercise `exact_geodesic_distance`/`plot_subsurface_rotating_gif` (external VTP
  binary / GUI rendering dependencies) in this pass.
- The `SubsurfaceMixin` method summaries above were drawn from each method's own (already
  reasonably complete) docstring; not all edge cases in the more algorithmically complex
  ones (`get_geodesic_strip_patch`, `get_strip_coordinates`) were independently verified.
- **Recommendation for maintainers:** either implement or remove `edge_collapse`; add
  proper NumPy-style docstrings (with Returns) to `boundary_vertices`, `edge_lengths`,
  `iter_surfedges_weighted`, `polyhedra`, `patches`; cross-reference `SubsurfaceMixin`'s
  performance rationale from `Surface`'s own class docstring.
