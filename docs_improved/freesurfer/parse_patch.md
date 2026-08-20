# cortex.freesurfer.parse_patch

## Current signature (from source)
```python
def parse_patch(filename):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:475-484](cortex/freesurfer.py#L475-L484)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.parse_patch.html

## Issues with current documentation
- **No docstring content, Parameters, Returns, or Raises at all.**
- **The returned structured array's field meanings are undocumented**, in particular the
  sign convention on `vert` (positive = interior vertex index+1, negative = boundary/edge
  vertex index+1, per its use in `get_surf`: `verts = patch[patch['vert'] > 0]['vert'] - 1`,
  `edges = -patch[patch['vert'] < 0]['vert'] - 1`) — this convention is only discoverable
  by reading `get_surf`'s body, not from `parse_patch` itself.
- **No mention that patch files only include a subset of the full surface's vertices**
  (a "patch" is a cut-out region, not the whole mesh) and that `x`/`y`/`z` here are the
  patch's own (typically 2D-flattened) coordinates, not necessarily the original 3D
  surface coordinates.

## Fixed documentation

### Summary
Parse a FreeSurfer binary patch file (e.g. a `.flat.patch.3d` output of `mris_flatten`, or
an input patch for flattening) into a structured array of per-vertex patch data.

### Parameters
- **filename** : str
    Path to a FreeSurfer binary patch file.

### Returns
- **data** : structured ndarray, shape (n_patch_vertices,), dtype
  `[('vert', '>i4'), ('x', '>f4'), ('y', '>f4'), ('z', '>f4')]`
    One entry per vertex included in the patch. `vert` is a signed 1-based index into the
    *original* full surface's vertex array: positive values mark interior patch vertices
    (`vert - 1` gives the 0-based index), negative values mark boundary/edge vertices
    (`-vert - 1` gives the 0-based index) — see `cortex.freesurfer.get_surf` for how this
    is consumed. `x`, `y`, `z` are the vertex's coordinates within the patch (for a flat
    patch, typically a 2D layout with `z` near 0).

### Raises
- `FileNotFoundError` — `filename` doesn't exist.
- `AssertionError` — the number of parsed vertex records doesn't match the header's
  declared vertex count.

### Notes
- A "patch" contains only a subset of a full surface's vertices (the cut/flattened
  region), not the whole mesh.
- Counterpart writer: `cortex.freesurfer.write_patch` (note: not a perfect round-trip
  inverse — `write_patch` takes a different, simpler `edges` argument rather than the
  signed-index convention this function's output uses).

### Example
```python
import cortex.freesurfer as fs

patch = fs.parse_patch("/path/to/SUBJECTS_DIR/S1/surf/lh.flattenv01.flat.patch.3d")
print(patch.dtype.names)  # ('vert', 'x', 'y', 'z')
```

## Confidence / open questions
- The sign convention on `vert` was reconstructed from its downstream usage in
  `cortex.freesurfer.get_surf` (`freesurfer.py:503-504`), not from any docs on
  `parse_patch` itself — confirmed by static reading, not execution.
- **Recommendation for maintainers:** add a docstring documenting the structured dtype and
  sign convention directly on `parse_patch`, rather than leaving it only inferable from
  `get_surf`'s body.
