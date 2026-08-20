# cortex.freesurfer.autorecon

## Current signature (from source)
```python
def autorecon(fs_subject, type="all", parallel=True, n_cores=None):
```

## Where this is documented today
- Source docstring: [cortex/freesurfer.py:54-64](cortex/freesurfer.py#L54-L64)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.freesurfer.autorecon.html

## Issues with current documentation
- **No Returns section** — returns `None` always (or, implicitly, returns early with
  `None` if the user declines the interactive confirmation prompt for long-running steps).
- **No Raises section** — `subprocess.check_call` raises `subprocess.CalledProcessError` if
  `recon-all` exits non-zero; `KeyError` if `type` isn't one of the six recognized keys.
- **Interactive confirmation prompt is undocumented.** For `type` in `{'all', '2', 'cp',
  'wm'}`, the function calls Python's `input()` asking the user to confirm before running
  (citing an estimated duration) — this blocks waiting for terminal input and isn't
  mentioned in the docstring at all; unusable unattended for those `type` values without
  adapting the call.
- **`parallel`/`n_cores` are undocumented parameters** — not mentioned in the docstring's
  `Parameters` section at all, despite being real, named parameters that add
  `-parallel -openmp <n_cores>` to the command for `type` in `{'2', 'wm', 'all'}`.
- **No mention this requires FreeSurfer** (`recon-all` on `PATH`) and can take hours.

## Fixed documentation

### Summary
Run Freesurfer's autorecon-all command for a given freesurfer subject.

### Parameters
- **fs_subject** : string
    Freesurfer subject ID (should be a folder in your freesurfer $SUBJECTS_DIR)
- **type** : string
    Which steps of autorecon-all to perform. `{'all', '1', '2', '3', 'cp', 'wm', 'pia'}`.
- **parallel** : bool, optional
    If `True` (default) and `type` is `'2'`, `'wm'`, or `'all'`, adds FreeSurfer's
    `-parallel -openmp <n_cores>` flags to use multiple cores. No effect for other `type`
    values.
- **n_cores** : int, optional
    Number of cores to use when `parallel=True`. `None` uses
    `multiprocessing.cpu_count()`.

### Returns
`None`. Also returns `None` early, without running anything, if the user declines the
confirmation prompt shown for `type` in `{'all', '2', 'cp', 'wm'}`.

### Raises
- `KeyError` — `type` is not one of `{'all', '1', '2', '3', 'cp', 'wm', 'pia'}`.
- `subprocess.CalledProcessError` — the `recon-all` command exits with a non-zero status.

### Notes
- **Requires FreeSurfer** (`recon-all` on `PATH`) and can take hours depending on `type`
  (an estimate is printed/confirmed interactively for the longer steps: ~12h for `'all'`,
  ~6h for `'2'`, ~8h for `'cp'`, ~4h for `'wm'`).
- **Blocks on interactive `input()`** for `type` in `{'all', '2', 'cp', 'wm'}` — not usable
  unattended for those without modification.
- Runs synchronously (blocks until `recon-all` completes).

### Example
```python
import cortex.freesurfer as fs

# Prompts for confirmation given the long estimated runtime, then blocks until done.
fs.autorecon("S1", type="all", parallel=True)
```

## Confidence / open questions
- Did not run `recon-all` in this pass — behavior described from source reading only.
- **Recommendation for maintainers:** document `parallel`/`n_cores`; add a non-interactive
  override (e.g. a `confirm=False` kwarg) for scripted/automated use; add Returns/Raises.
