# cortex.freesurfer.write_dot

## Current signature (from source)
```python
def write_dot(fname, pts, polys, name="test"):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:954-974](cortex/freesurfer.py#L954-L974)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.write_dot.html

## Issues with current documentation
- **No docstring content, Parameters, Returns, or Raises at all.**
- **Likely broken on modern NetworkX.** The function calls `graph.edges_iter()`
  (`freesurfer.py:969`), an API removed from NetworkX in the 2.0 release (replaced by
  `graph.edges()`, which returns an iterable directly). With any NetworkX >= 2.0 installed,
  this raises `AttributeError: 'Graph' object has no attribute 'edges_iter'`. Flagged as a
  likely code bug, not fixed here — see `_notes.md`.
- **No mention of the required `networkx` dependency** (imported lazily inside the
  function, not a hard pycortex dependency).
- **`.dot` output format and its purpose (feeding into GraphViz's `neato`/similar for a
  spring-layout-style 2D graph drawing) aren't explained.**

## Fixed documentation

### Summary
Write a surface mesh's edge graph to a GraphViz `.dot` file, with edge weights set to
3D edge length — intended as input to a force-directed layout tool (e.g. GraphViz's
`neato`) to produce a 2D graph layout.

### Parameters
- **fname** : str
    Output `.dot` file path.
- **pts** : ndarray, shape (n_vertices, 3)
    Vertex coordinates.
- **polys** : ndarray, shape (n_faces, 3)
    Triangle vertex-index triples.
- **name** : str, optional
    Name to give the graph in the `.dot` file header. Default `"test"`.

### Returns
`None`. Writes `fname` as a side effect.

### Raises
- `AttributeError` — with NetworkX >= 2.0 installed, `graph.edges_iter()` no longer
  exists; this function will fail on any modern NetworkX version (see Issues).
- `ImportError` — `networkx` is not installed.

### Notes
- **Likely broken on any currently-maintained NetworkX version** — see Issues/`_notes.md`.
- Counterpart reader: `cortex.freesurfer.read_dot`.

### Example
```python
import cortex.freesurfer as fs

# NOTE: as of current pycortex source, this call is expected to fail with
# AttributeError on NetworkX >= 2.0 (uses the removed graph.edges_iter() API).
fs.write_dot("surface.dot", pts, polys, name="my_surface")
```

## Confidence / open questions
- The `edges_iter` API removal is a well-known NetworkX 1.x → 2.x breaking change;
  confirmed by static reading of the source (`freesurfer.py:969`), not by installing and
  running against a live NetworkX version in this pass.
- **Recommendation for maintainers:** update to `graph.edges()` (NetworkX >= 2.0 API); add
  a docstring; consider pinning/checking the networkx version this function actually
  supports.
