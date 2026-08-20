# cortex.freesurfer.write_decimated

## Current signature (from source)
```python
def write_decimated(path, pts, polys):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:996-1012](cortex/freesurfer.py#L996-L1012)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.write_decimated.html

## Issues with current documentation
- **No docstring content, Parameters, Returns, or Raises at all.**
- **Likely broken in Python 3 due to a text/binary file-mode mismatch.** The final block
  opens `path+'.full.patch.3d'` in text mode (`open(..., 'w')`) but then writes `bytes`
  objects to it (`fp.write(struct.pack(...))`, `fp.write(data.tobytes())`) —
  `struct.pack`/`ndarray.tobytes` both return `bytes`, and writing `bytes` to a text-mode
  file object raises `TypeError: write() argument must be str, not bytes` in Python 3. This
  looks like a real bug (the file should be opened as `'wb'`, matching every other binary
  writer in this module, e.g. `write_surf`/`write_patch`). Flagged, not fixed — see
  `_notes.md`.
- **No mention that this writes two files**, not one (`<path>.smoothwm` via `write_surf`,
  and `<path>.full.patch.3d`).
- **`decimate` (from `cortex.polyutils`) is the actual mesh-simplification step** — its
  parameters/algorithm aren't surfaced here at all, since `write_decimated` calls it with
  no tunable arguments exposed.

## Fixed documentation

### Summary
Decimate (simplify) a surface mesh and write it out in FreeSurfer surface + patch format,
for use as a coarser starting point (e.g. for spring-relaxation-based flattening or
smoothing).

### Parameters
- **path** : str
    Base output path (without extension). Two files are written:
    `<path>.smoothwm` (the decimated surface, FreeSurfer binary format) and
    `<path>.full.patch.3d` (a patch file marking boundary vs. interior vertices).
- **pts** : ndarray, shape (n_vertices, 3)
    Input vertex coordinates.
- **polys** : ndarray, shape (n_faces, 3)
    Input triangle vertex-index triples.

### Returns
`None`. Writes `<path>.smoothwm` and `<path>.full.patch.3d` as side effects.

### Raises
- `TypeError` — **as currently written, this function raises `TypeError` on Python 3**
  when writing the `.full.patch.3d` file, because it's opened in text mode (`'w'`) but
  written with `bytes` data. See Issues; this appears to be a real, unfixed bug rather than
  intended behavior.

### Notes
- Uses `cortex.polyutils.decimate` (mesh simplification) and
  `cortex.polyutils.boundary_edges` (to mark patch boundary vertices) internally, with no
  tunable parameters exposed by `write_decimated` itself.
- **As currently written, likely fails outright on Python 3** — see Raises/Issues.

### Example
```python
import cortex.freesurfer as fs

# NOTE: as of current pycortex source, the .full.patch.3d write step is expected to
# raise TypeError on Python 3 due to a text/binary file-mode mismatch (see Issues).
fs.write_decimated("/tmp/decimated_lh", pts, polys)
```

## Confidence / open questions
- The text/binary mode mismatch is confirmed by direct reading of
  `freesurfer.py:1009-1012` (`open(path+'.full.patch.3d', 'w')` followed by `fp.write()`
  calls on `bytes` values), not by running the code in this pass.
- **Recommendation for maintainers:** change `open(path+'.full.patch.3d', 'w')` to
  `'wb'`; add a docstring covering both output files.
