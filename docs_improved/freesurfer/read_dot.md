# cortex.freesurfer.read_dot

## Current signature (from source)
```python
def read_dot(fname, pts):
```

## Where this is documented today
- Source docstring: empty (`"""\n    """`).
  [cortex/freesurfer.py:977-993](cortex/freesurfer.py#L977-L993)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.read_dot.html

## Issues with current documentation
- **No docstring content, Parameters, Returns, or Raises at all.**
- **Extremely fragile, hand-rolled parsing** — skips exactly 4 fixed header lines, then
  parses subsequent lines with a hard-coded regex and a `while el[1] != '--'` loop assuming
  a very specific GraphViz output layout (one node-position line per vertex, ending as soon
  as an edge line, marked by `'--'` in the second whitespace-split token, is seen). This
  format assumption is not documented anywhere and will silently break (produce wrong
  data or raise an unrelated exception like `IndexError`) if fed `.dot` output that doesn't
  match this exact structure (e.g. output from a different GraphViz version/tool than
  whatever produced the original test data).
- **`pts` parameter's purpose is non-obvious**: only used to size the output array
  (`len(pts)`), not to constrain/validate which node IDs are expected.

## Fixed documentation

### Summary
Parse 2D node positions back out of a GraphViz-processed `.dot` file (as written by
`cortex.freesurfer.write_dot` and laid out by an external tool like `neato`), using a
narrow, format-specific parser.

### Parameters
- **fname** : str
    Path to a GraphViz-laid-out `.dot` file (e.g. `neato -Tdot ... -o fname`).
- **pts** : array-like
    Only used for its length — determines the size of the returned `(len(pts), 2)` array.
    Node IDs found in the file are used directly as row indices, so `fname` must reference
    node IDs in `range(len(pts))`.

### Returns
- **data** : ndarray, shape (len(pts), 2)
    2D `(x, y)` layout position for each node ID found in the file; rows for node IDs not
    present in the file remain `0`.

### Raises
- `FileNotFoundError` — `fname` doesn't exist.
- `IndexError`/`ValueError` (likely, unhandled) — the file doesn't exactly match the
  narrow line-format this parser expects (see Issues) — e.g. output from a different
  GraphViz version, or a `.dot` file not laid out by a compatible tool.

### Notes
- **Extremely format-fragile** — designed for one specific GraphViz `.dot` output layout;
  not a general-purpose `.dot` parser. See Issues.
- Counterpart writer: `cortex.freesurfer.write_dot` (note: `write_dot` itself is likely
  broken on modern NetworkX — see `write_dot.md`).

### Example
```python
import cortex.freesurfer as fs

# Assumes surface.dot was laid out externally, e.g.:
#   neato -Tdot surface.dot -o surface_laidout.dot
positions = fs.read_dot("surface_laidout.dot", pts)
```

## Confidence / open questions
- Did not test this parser against real GraphViz output in this pass — the fragility
  assessment is based on static reading of the fixed-line-skip/regex logic
  (`freesurfer.py:977-993`).
- **Recommendation for maintainers:** add a docstring; consider using a real `.dot` parser
  library instead of hand-rolled line skipping/regex, or at minimum document the exact
  expected input format/GraphViz version this was written against.
