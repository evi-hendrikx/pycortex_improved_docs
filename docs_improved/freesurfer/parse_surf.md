# cortex.freesurfer.parse_surf

## Current signature (from source)
```python
def parse_surf(filename):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:408-421](cortex/freesurfer.py#L408-L421)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.parse_surf.html
  (renders no description).

## Issues with current documentation
- **No docstring content at all.**
- **No Parameters/Returns/Raises sections.**
- **Prints the file's comment line to stdout as a side effect** (`print(comment)`) — not
  documented, and easy to be surprised by if calling this in a loop over many files.
- **No mention of the binary format being parsed** (FreeSurfer's big-endian triangle-surface
  file format, `.white`/`.pial`/`.smoothwm`/etc.) or of the sibling writer function
  `write_surf`.

## Fixed documentation

### Summary
Parse a FreeSurfer binary surface file (e.g. `lh.white`, `rh.pial`) into vertex
coordinates and triangle indices.

### Parameters
- **filename** : str
    Path to a FreeSurfer binary surface file.

### Returns
- **pts** : ndarray, shape (n_vertices, 3)
    Vertex coordinates.
- **polys** : ndarray, shape (n_faces, 3)
    Triangle vertex-index triples.

### Raises
- `FileNotFoundError` — `filename` doesn't exist.
- `struct.error` — the file doesn't match the expected FreeSurfer binary surface format.

### Notes
- Prints the file's embedded comment/header line to stdout as a side effect.
- Counterpart writer: `cortex.freesurfer.write_surf`.
- Uses big-endian byte order (FreeSurfer's on-disk convention), byte-swapped into the
  platform's native order on read.

### Example
```python
import cortex.freesurfer as fs

pts, polys = fs.parse_surf("/path/to/SUBJECTS_DIR/S1/surf/lh.white")
print(pts.shape, polys.shape)
```

## Confidence / open questions
- **Recommendation for maintainers:** add a docstring (currently entirely empty); consider
  making the comment-printing opt-in rather than unconditional.
