# cortex.mni.transform_surface_to_mni

## Current signature (from source)
```python
def transform_surface_to_mni(subject, surfname):
```

## Where this is documented today
- Source docstring: [cortex/mni.py:116-132](cortex/mni.py#L116-L132)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.mni.transform_surface_to_mni.html

## Issues with current documentation
- **No Raises section.**
- **Does not call FSL directly** (unlike its three sibling functions in this module) —
  worth stating explicitly, since a reader might assume the whole module has the same FSL
  dependency; this function only needs a cached/computable MNI transform (via
  `cortex.db.get_mnixfm`, which itself may call FSL the first time, uncached).
- **Uses the fixed `default_template`'s affine** (`nibabel.load(default_template).affine`)
  rather than accepting a `template` parameter like its sibling functions — not stated as
  a deliberate difference; a reader coming from the other three functions might expect a
  `template` kwarg here too.

## Fixed documentation

### Summary
Transform the surface named `surfname` for subject called `subject` into MNI coordinates.
Returns `[(lpts, lpolys), (rpts, rpolys)]`.

### Parameters
- **subject** : str
    Subject identifier
- **surfname** : str
    Surface identifier

### Returns
- **[(mni_lpts, lpolys), (mni_rpts, rpolys)]**
    MNI-transformed surface in same format returned by `db.get_surf`.

### Raises
Propagates errors from `cortex.database.Database.get_mnixfm` (may invoke FSL the first
time, uncached), `get_xfm`, or `get_surf` if `subject`/`surfname` are invalid.

### Notes
- Unlike `compute_mni_transform`/`transform_to_mni`/`transform_mni_to_subject`, this
  function does not call FSL's `flirt` directly — it only needs the (possibly cached)
  anatomical-to-MNI transform via `cortex.db.get_mnixfm`, which may itself invoke FSL on
  first use for a given subject.
- Always uses `default_template`'s affine (not the module's other functions' `template`
  parameter) to build the MNI affine.

### Example
```python
import cortex

(mni_lpts, lpolys), (mni_rpts, rpolys) = cortex.mni.transform_surface_to_mni("S1", "fiducial")
```

## Confidence / open questions
- **Recommendation for maintainers:** add a Raises section; consider accepting a
  `template` parameter for consistency with the module's other three functions, or
  document why it's intentionally fixed here.
