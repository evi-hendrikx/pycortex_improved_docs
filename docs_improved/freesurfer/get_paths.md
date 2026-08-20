# cortex.freesurfer.get_paths

## Current signature (from source)
```python
def get_paths(fs_subject, hemi, type="patch", freesurfer_subject_dir=None):
```

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:25-40](cortex/freesurfer.py#L25-L40)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.get_paths.html

## Issues with current documentation
- **`type` accepts a fourth value, `"slim"`, not listed in the docstring** — the
  `Parameters` section documents only `'patch'|'surf'|'curv'`, but the implementation also
  handles `type="slim"` (used by `import_flat` for `.obj`-format flat surfaces).
- **Return value is entirely undocumented** — no `Returns` section. The function returns a
  path-like *format string* containing a literal `{name}` placeholder (not a real path),
  e.g. `<dir>/surf/lh.{name}.patch.3d`, meant to be `.format(name=...)`'d by the caller.
  This "returns an unfilled template string" behavior is a real gotcha not mentioned
  anywhere.
- **Falls through to returning `None` for any other `type` value**, silently — no `else`
  clause/`ValueError` for an invalid `type`. Not documented.
- **No Raises section** — raises `KeyError` if `freesurfer_subject_dir` is `None` and the
  `SUBJECTS_DIR` environment variable isn't set.

## Fixed documentation

### Summary
Retrieve paths for all surfaces for a subject processed by freesurfer.

### Parameters
- **subject** : string
    Subject ID for freesurfer subject
- **hemi** : string ['lh'|'rh']
    Left ('lh') or right ('rh') hemisphere
- **type** : string ['patch'|'surf'|'curv'|'slim']
    Which type of files to return. (`'slim'` is accepted but not listed in the shipped
    docstring — used for `.obj`-format flat surfaces.)
- **freesurfer_subject_dir** : string | None
    Directory of freesurfer subjects. Defaults to the value for the environment variable
    'SUBJECTS_DIR' (which should be set by freesurfer).

### Returns
- **path_template** : str
    A path string containing an unfilled `{name}` placeholder, e.g.
    `<dir>/surf/lh.{name}.patch.3d`. The caller is expected to call `.format(name=...)` on
    it. Returns `None` (silently) if `type` isn't one of the four recognized values.

### Raises
- `KeyError` — if `freesurfer_subject_dir` is `None` and the `SUBJECTS_DIR` environment
  variable is not set.

### Notes
- No FreeSurfer command execution here — this is pure path-string construction, no I/O
  performed and no check that the files actually exist.

### Example
```python
import cortex.freesurfer as fs

template = fs.get_paths("S1", "lh", type="surf")
# '/path/to/SUBJECTS_DIR/S1/surf/lh.{name}'
pial_path = template.format(name="pial")
```

## Confidence / open questions
- **Recommendation for maintainers:** document `type="slim"`; add a `Returns` section
  explaining the unfilled-template-string convention; raise `ValueError` for an
  unrecognized `type` instead of silently returning `None`.
