# cortex.freesurfer.parse_curv

## Current signature (from source)
```python
def parse_curv(filename):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:467-472](cortex/freesurfer.py#L467-L472)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.parse_curv.html

## Issues with current documentation
- **No docstring content, Parameters, Returns, or Raises at all.**
- **The fixed 15-byte header skip (`fp.seek(15)`) is unexplained** — assumes the "new"
  FreeSurfer curv file format's fixed-size header; no comment or docs justify the magic
  number.
- **No mention of what "curv" data represents** (per-vertex scalar values — curvature,
  but also sulcal depth/thickness, since `import_subj` reuses this same parser for `sulc`
  and `thickness` files too).

## Fixed documentation

### Summary
Parse a FreeSurfer binary curvature-format file (e.g. `lh.curv`, but also used for
`sulc`/`thickness` files, which share the same on-disk format) into a per-vertex array.

### Parameters
- **filename** : str
    Path to a FreeSurfer binary curv-format file.

### Returns
- **values** : ndarray, shape (n_vertices,), dtype float32
    Per-vertex scalar values (sign/meaning depends on the source file — curvature, sulcal
    depth, or thickness).

### Raises
- `FileNotFoundError` — `filename` doesn't exist.

### Notes
- Skips a fixed 15-byte header (the "new" FreeSurfer curv-file format's magic number +
  vertex/face counts), then reads the remainder as big-endian `float32`, byte-swapped to
  native order.
- `cortex.freesurfer.import_subj` calls this for `curv`, `sulc`, and `thickness` files
  alike, then negates the result (`-lh`, `-rh`) before saving — the sign convention used
  internally by pycortex is therefore flipped relative to the raw FreeSurfer file.

### Example
```python
import cortex.freesurfer as fs

curv = fs.parse_curv("/path/to/SUBJECTS_DIR/S1/surf/lh.curv")
print(curv.shape, curv.dtype)
```

## Confidence / open questions
- **Recommendation for maintainers:** add a docstring; document the fixed 15-byte header
  assumption (and what happens if an "old"-format curv file, which uses a different
  header, is passed — not handled here).
