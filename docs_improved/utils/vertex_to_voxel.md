# cortex.utils.vertex_to_voxel

## Current signature (from source)
```python
def vertex_to_voxel(subject):  # Am I deprecated in favor of mappers??? Maybe?
```

## Where this is documented today
- Source docstring: [cortex/utils.py:946-955](cortex/utils.py#L946-L955) — `Parameters`
  has a description, `Returns` section header present but empty; no summary line at all
  (docstring opens directly with `Parameters`).
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.vertex_to_voxel.html

## Issues with current documentation
- **No summary/description line at all** — the docstring jumps straight into
  `Parameters` with no sentence describing what the function actually computes.
- **`Returns` section header present but empty.**
- **The function's own inline comment says `# Am I deprecated in favor of mappers???
  Maybe?`** — a genuine, unresolved uncertainty left by the original author about whether
  this function should be considered legacy/superseded by `cortex.mapper`. This is
  valuable context that isn't surfaced anywhere in the actual docstring.
- **No Raises section.**
- **Uses `"identity"` as a hard-coded transform name** internally
  (`get_vox_dist(subject, "identity", ...)`) — i.e. this operates in the subject's native
  anatomical grid, not any particular functional space; not stated.

## Fixed documentation

### Summary
For each anatomical-space voxel, finds the index of the nearest vertex on any of the
fiducial, white-matter, or pial surfaces (whichever is geometrically closest), within a
maximum search distance of the subject's maximum cortical thickness. **Author's own
in-source comment flags uncertainty about whether this is superseded by
`cortex.mapper`** — see Notes.

### Parameters
- **subject** : str
    Name of subject

### Returns
- **all_verts** : ndarray (z, y, x)
    Array with the same shape as the subject's native anatomical grid (`"identity"`
    transform space), containing for each voxel the index of the nearest vertex across
    the fiducial, white-matter, and pial surfaces (whichever is closest). Voxels farther
    than the subject's max cortical thickness from all three surfaces get an out-of-range
    sentinel index (from the underlying `get_vox_dist`'s `max_dist`-bounded KD-tree
    query — see `get_vox_dist.md`).

### Raises
Propagates errors from `cortex.database.Database.get_surfinfo`/`get_vox_dist` if
`subject`'s surfaces/thickness info aren't available.

### Notes
- Always operates against the `"identity"` transform (native anatomical grid) — not
  parameterized by `xfmname`.
- **The function's own source comment questions whether it's deprecated in favor of
  `cortex.mapper`** — this uncertainty is unresolved in the codebase; treat this function
  as possibly-legacy and consider whether a `Mapper`-based approach better suits your use
  case.
- No FreeSurfer/FSL/GUI dependency at call time.

### Example
```python
import cortex

nearest_vertex_per_voxel = cortex.utils.vertex_to_voxel("S1")
```

## Confidence / open questions
- Could not determine from source/tests whether `cortex.mapper`-based approaches are, in
  fact, meant to fully replace this function — the ambiguity is the original author's own,
  left unresolved in a code comment, not something resolvable from static reading alone.
- **Recommendation for maintainers:** resolve the deprecation question left in the
  in-source comment (either deprecate formally, with a pointer to a `Mapper`-based
  replacement, or remove the comment if the function is still the right tool); add a
  summary line and complete the `Returns` section.
