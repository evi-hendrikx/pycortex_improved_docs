# cortex.freesurfer.import_flat

## Current signature (from source)
```python
def import_flat(fs_subject, patch, hemis=['lh', 'rh'], cx_subject=None,
                flat_type='freesurfer', auto_overwrite=False,
                freesurfer_subject_dir=None, clean=True):
```
Note: `hemis=['lh', 'rh']` is a mutable default argument (not currently mutated in the
function body, so not an active bug — see `_notes.md`).

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:266-296](cortex/freesurfer.py#L266-L296)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.import_flat.html

## Issues with current documentation
- **`Returns` section header is present but empty.** The function always returns `None`.
- **No Raises section.**
- **`auto_overwrite` is not documented as a parameter at all**, despite being a real,
  named parameter that skips the interactive confirmation prompt entirely when `True`.
- **`clean`'s docstring is accurate but doesn't explain what "disconnected polys" are or
  why they occur** (a poor surface cut leaving stray, disconnected mesh fragments) —
  minor, but the underlying helper (`_remove_disconnected_polys`) itself documents this
  better than `import_flat` does.
- **No explicit type note for `flat_type='slim'`'s dependency** on
  `cortex.formats.read_obj` and a differently-located file (`get_paths(..., type='slim')`)
  compared to the `'freesurfer'`/`'blender'` paths.

## Fixed documentation

### Summary
Imports a flat brain from freesurfer. NOTE: This will delete the overlays.svg file for
this subject, since THE FLATMAPS WILL CHANGE, as well as all cached information (e.g. old
flatmap boundaries, roi svg intermediate renders, etc).

### Parameters
- **fs_subject** : str
    Freesurfer subject name
- **patch** : str
    Name of flat.patch.3d file; e.g., "flattenv01"
- **hemis** : list
    List of hemispheres to import. Defaults to both hemispheres.
- **cx_subject** : str
    Pycortex subject name
- **flat_type** : str
    Type of flatmap to import. Defaults to 'freesurfer'. Can be 'freesurfer', 'slim', or
    'blender'.
- **auto_overwrite** : bool, optional
    If `True`, skip the interactive confirmation prompt and proceed directly with
    overwriting/deleting. Default `False`.
- **freesurfer_subject_dir** : str
    directory for freesurfer subjects. None defaults to environment variable
    $SUBJECTS_DIR
- **clean** : bool
    If True, the flat surface is cleaned to remove the disconnected polys.

### Returns
`None`. Also returns early (`None`, nothing written) if the interactive confirmation
prompt is declined and `auto_overwrite=False`.

### Raises
Propagates errors from the underlying surface-file parsing (`get_surf`/`parse_patch`/
`cortex.formats.read_obj`) if the expected patch/flat files aren't found.

### Notes
- **Destructive**: deletes the subject's `overlays.svg` file and clears the pycortex cache
  for `cx_subject` (`database.db.clear_cache`), since imported flatmaps change flatmap
  geometry that cached ROI/flatmap renders depended on.
- **Blocks on an interactive `input()` confirmation** unless `auto_overwrite=True`.
- No FreeSurfer command execution here (pure file I/O), but expects the referenced patch
  files to already exist (produced by `cortex.freesurfer.flatten` or Blender cuts).

### Example
```python
import cortex.freesurfer as fs

# Skips the confirmation prompt; overwrites flat surfaces for both hemispheres of "S1".
fs.import_flat("S1", "flattenv01", auto_overwrite=True)
```

## Confidence / open questions
- **Recommendation for maintainers:** fill in the empty `Returns` section; document
  `auto_overwrite`; avoid the mutable default argument `hemis=['lh', 'rh']`.
