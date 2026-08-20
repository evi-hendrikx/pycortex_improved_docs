# cortex.surfinfo.thickness

## Current signature (from source)
```python
def thickness(outfile, subject):
```

## Where this is documented today
- Source docstring: [cortex/surfinfo.py:78-92](cortex/surfinfo.py#L78-L92)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.surfinfo.thickness.html

## Issues with current documentation
- **No Returns section.**
- **No Raises section.**
- **Not documented as the auto-generation target of `cortex.db.get_surfinfo(subject,
  type="thickness")`.**

## Fixed documentation

### Summary
Compute cortical thickness as the distance between corresponding pial and white matter
vertices for the given subject. Note that this is slightly different than the method used
by Freesurfer, and will yield ever-so-slightly different results.

### Parameters
- **outfile** : str
    Path where the thickness map will be saved.
- **subject** : str
    Subject in the pycortex database for whom cortical thickness will be computed.

### Returns
`None`. Writes `outfile` (an `.npz` with `left`/`right` arrays) as a side effect.

### Raises
Propagates errors from `cortex.database.Database.get_surf` if `subject`'s pial/wm surfaces
aren't available.

### Notes
- No FreeSurfer/FSL/GUI dependency; requires `subject`'s `pia` and `wm` surfaces to already
  be in the pycortex database with matching vertex counts (a mismatch will surface as a
  numpy broadcasting error, not a clear message).
- Normally invoked indirectly via `cortex.db.get_surfinfo(subject, type="thickness")`.

### Example
```python
import cortex

cortex.surfinfo.thickness("s1_thickness.npz", "S1")
```

## Confidence / open questions
- **Recommendation for maintainers:** add a Returns section and validate pial/wm vertex
  count match up front with a clear error message.
