# Cross-cutting notes — pycortex API documentation improvement project

This file collects patterns and issues that repeat across many functions, discrepancies
between the scope list and actual source, a running progress checklist, and possible code
bugs noticed while writing documentation (not fixed, per project scope — this is a
docs-only project; see the design doc for constraints).

Repo: `pycortex_improved_docs` fork of gallantlab/pycortex, branch as checked out at the
start of this project (see `git log -1` at time of writing — HEAD was
`537f05e Bump JamesIves/github-pages-deploy-action from 4.8.0 to 4.9.0 (#671)`, version
string `1.3.0.dev0` per `cortex/version.py`).

## Progress checklist (by module, per the scope list in the design doc)

- [x] `cortex.quickflat` — make_figure, make_png, make_svg
- [x] `cortex.webgl` — show, make_static
- [x] `cortex.dataset` — Volume, Volume2D, VolumeRGB, Vertex, Vertex2D, VertexRGB, Dataset
- [x] `cortex.align` — manual, automatic, autotweak
- [x] `cortex.anat` — brainmask, whitematter, voxelize
- [x] `cortex.database` — Database
- [x] `cortex.freesurfer` — get_paths, autorecon, flatten, import_subj, import_flat,
      show_surf, make_fiducial, parse_surf, parse_curv, parse_patch, get_surf, get_curv,
      write_dot, read_dot, write_decimated, SpringLayout, stretch_mwall
- [ ] `cortex.anat` — brainmask, whitematter, voxelize
- [ ] `cortex.database` — Database
- [ ] `cortex.freesurfer` — get_paths, autorecon, flatten, import_subj, import_flat,
      show_surf, make_fiducial, parse_surf, parse_curv, parse_patch, get_surf, get_curv,
      write_dot, read_dot, write_decimated, SpringLayout, stretch_mwall
- [ ] `cortex.mapper` — Mapper, get_mapper
- [ ] `cortex.mni` — compute_mni_transform, transform_to_mni, transform_surface_to_mni,
      transform_mni_to_subject
- [ ] `cortex.polyutils` — Surface, Distortion
- [ ] `cortex.segment` — init_subject, fix_wm, fix_pia, cut_surface
- [ ] `cortex.surfinfo` — curvature, distortion, thickness, tissots_indicatrix, flat_border
- [ ] `cortex.utils` — add_roi, anat2epispace, get_aseg_mask, get_cmap, get_cortical_mask,
      get_ctmmap, get_ctmpack, get_dropout, get_hemi_masks, get_roi_mask, get_roi_masks,
      get_roi_verts, get_vox_dist, make_movie, vertex_to_voxel
- [ ] `cortex.volume` — unmask, mosaic, epi2anatspace, anat2epispace, epi2anatspace_fsl,
      anat2epispace_fsl, show_slice, show_mip, show_glass
- [ ] `cortex.xfm` — Transform

## Discrepancies vs. the scope list (found while reading source)

### cortex.quickflat
- `make_gif`, `show` (a thin `make_figure` wrapper), and `make_movie` (raises
  `NotImplementedError` unconditionally — dead code, see below) exist as public functions in
  `cortex/quickflat/view.py` but are **not** in the scope list. Not documented in this pass
  (out of scope); flagging here per the design doc's instruction to note discrepancies.
  `cortex.quickflat.utils` and `cortex.quickflat.composite` additionally define several
  public-looking `add_*` compositing functions (`add_curvature`, `add_data`, `add_rois`,
  `add_sulci`, `add_hatch`, `add_colorbar`, `add_colorbar_2d`, `add_custom`,
  `add_connected_vertices`, `add_cutout`) that are the real implementation behind
  `make_figure`'s `with_*` flags. These aren't in the scope list either (they live in
  submodules of `quickflat`, not `quickflat` itself, and aren't re-exported at the
  `cortex.quickflat` package level) but they were read in full to document `make_figure`'s
  effective kwargs chain accurately.

### cortex.webgl
- No public functions found beyond `show` and `make_static` (matches scope list exactly).
  `cortex.webgl.serve.JSProxy`/`JSMixer` (the object returned by `show` when a browser
  client connects) has a genuinely useful public method surface (`getImage`, `makeMovie`,
  `make_movie_views`, `save_view`, `get_view`, `addData`, `_set_view`, `_capture_view`) but
  is not itself in the scope list (it's a return value of `show`, defined as a local class
  inside `show`'s body, not an importable `cortex.webgl.JSMixer`). Summarized inside
  `webgl/show.md`'s Returns section rather than given its own file, since it isn't a
  standalone documented class in the module.

### cortex.dataset
- Matches the scope list exactly (`Volume`, `Volume2D`, `VolumeRGB`, `Vertex`, `Vertex2D`,
  `VertexRGB`, `Dataset`). Additional public-ish classes exist but were intentionally
  documented *within* the scoped class's file rather than given their own file, since they
  are base classes / internal building blocks the scope list doesn't name individually:
  `cortex.dataset.braindata.BrainData`, `VolumeData`, `VertexData` (base classes for
  `Volume`/`Vertex`); `cortex.dataset.views.Dataview`, `Multiview` (`Multiview.__init__`
  unconditionally raises `NotImplementedError` — dead/unfinished code, see below);
  `cortex.dataset.view2D.Dataview2D`; `cortex.dataset.viewRGB.DataviewRGB`, `Colors`,
  `RGB2HSV`, `HSV2RGB`. `cortex.dataset.views.normalize` /
  `cortex.dataset.dataset.normalize` (two *different* module-level `normalize` functions,
  one for single views/tuples, one for whole datasets — also not in the scope list, but
  their behavior is described inline in `Dataset.md`/`Volume.md` since user-facing classes
  depend on them for input coercion) were read but not given standalone files.

### cortex.align
- `mayavi_manual` (deprecated old GUI aligner, requires Mayavi) and `fs_manual`
  (deprecated alias for `manual`), plus `automatic_fsl` (FSL-based sibling of `automatic`),
  exist in source but are **not** in the scope list. Not given standalone files (out of
  scope), but `automatic_fsl` is referenced/partially described inside `automatic.md` since
  `automatic`'s own docstring points to it as the recommended fallback.

### cortex.anat
- Matches the scope list exactly. None of the three functions have any real docstring
  (`brainmask`/`whitematter` have none at all; `voxelize` has one hardcoded line) — the
  least-documented module found so far at the per-function level (worse than `Dataset`,
  which at least had a class-level docstring).

### cortex.database
- Matches the scope list (`Database`). Several other classes live in this module
  (`SubjectDB`, `SurfaceDB`, `Surf`, `XfmDB`, `XfmSet`, `MaskSet`) that back `Database`'s
  attribute-style subject access (`db.S1.surfaces...`) — not individually scoped, not
  given their own files, but their existence is worth a mention in case maintainers want
  them documented later.

### cortex.freesurfer
- Matches the scope list exactly. Additional public functions/classes exist in source but
  are **not** in the scope list: `write_surf`, `write_patch` (writer counterparts of
  `parse_surf`/`parse_patch`), `get_label`, `mri_surf2surf`, `get_mri_surf2surf_matrix`,
  and `upsample_to_fsaverage`. Not given standalone files (out of scope), but
  `write_surf`/`write_patch` are referenced from `parse_surf.md`/`parse_patch.md` as
  counterpart writers since they're directly relevant there.
- This module has the worst docstring coverage found so far at the per-function level:
  `parse_surf`, `parse_curv`, `parse_patch`, `write_dot`, `read_dot`, `write_decimated`,
  and the entire `SpringLayout` class have **completely empty** docstrings (literally
  `"""\n    """`); `get_surf`, `make_fiducial` have only a one-line docstring each;
  `stretch_mwall` has none.
- **`cortex.freesurfer.get_surf` collides in name with two unrelated functions**:
  `cortex.database.Database.get_surf` (reads from the pycortex filestore) and
  `cortex.dataset.Dataset.get_surf` (reads from packed HDF5 contents). All three do
  related-but-different things; none cross-reference each other.

## Patterns repeated across many functions (updated as modules are covered)

- **Undocumented `**kwargs` forwarding chains** are pervasive in `cortex.quickflat`:
  `make_png` → `make_figure` (near-total kwargs surface); `make_svg` →
  `make_flatmap_image` → `get_flatcache` (a much smaller, and materially *different*,
  kwargs surface than `make_png`'s — easy to wrongly assume the two behave the same).
  Expect this pattern to recur in `cortex.webgl` (`show`/`make_static`) given pycortex's
  general design of stacking thin wrapper functions.
- **Collapsed multi-parameter docstring entries** (e.g. `make_figure`'s
  "`with_rois, with_labels, with_colorbar, with_borders, with_dropout, with_curvature, etc :
  bool, optional`") hide the fact that not all of the grouped parameters actually share the
  same type/behavior (`with_dropout` is `bool | float | Dataview`, not just `bool`;
  `with_borders` does nothing at all).
- **No `Returns` sections** on file-writing/plotting functions that return `None`, and no
  `Returns` section stating the return type even for functions that *do* return something
  useful (e.g. `make_figure` returns a `Figure` — visible only via a type hint, not prose).
- **No `Raises` sections anywhere so far.**
- **No runnable examples anywhere in `cortex.quickflat`'s docstrings.**
- **Color/appearance kwargs silently forwarded through a matplotlib-name → SVG-name
  translation layer** (`quickflat.utils._convert_svg_kwargs`), which is itself the source of
  a real bug (see below) and is never mentioned in any of the public docstrings that
  ultimately depend on it.

## Possible code issues (not fixed) — flag only, per project scope

- **`shadow` parameter is dead/broken in `cortex.quickflat`.** `make_figure`'s `shadow`
  parameter (and the corresponding parameter threaded through `composite.add_rois`,
  `composite.add_sulci`, and `composite.add_custom`) is documented as controlling "the
  standard deviation of the gaussian shadow," but `quickflat/utils.py`'s
  `_convert_svg_kwargs` — the function these `shadow` values are funneled into via
  `**kwargs` — has no `"shadow"` entry in its `svg_style_key_mapping` dict. Any call that
  passes a non-`None` `shadow` value (with `with_rois`, `with_sulci`, or `extra_disp`
  enabled) will raise `KeyError: 'shadow'`. Confirmed by static source reading
  (`cortex/quickflat/utils.py:221-255`, `cortex/quickflat/view.py:41,87-88,184-200`), not
  by execution. See `quickflat/make_figure.md` for detail.
- **`with_borders` (in `make_figure`) is accepted but has zero effect** — never read
  anywhere in `cortex/quickflat/view.py`'s `make_figure` body. Either dead/vestigial or an
  unfinished feature.
- **`make_svg`'s `with_dropout` silently ignores a numeric "power" argument** that
  `make_figure`'s analogous parameter *does* support — any truthy non-`Dataview` value falls
  through to `utils.get_dropout(subject, xfmname)` with the hard-coded default `power=20`,
  rather than using the passed-in number. Not a crash, but a silent behavioral
  inconsistency between two sibling functions that share a docstring wording
  ("bool or a `cortex.Dataview` object").
- **`cortex.quickflat.view.make_movie`** (not in scope list) begins with `raise
  NotImplementedError` before any of its ~40 lines of implementation code — fully dead code
  left in the module.
- **Mutable default argument** `layers=['rois']` in `make_svg`'s signature (Python
  anti-pattern; not currently mutated, so not an active bug, but fragile).
- **`cortex.dataset.views.Multiview.__init__` unconditionally raises
  `NotImplementedError`** on its second line, after already validating its `views` argument
  — dead/unfinished code (`cortex/dataset/views.py:338-344`), similar to
  `quickflat.view.make_movie`.
- **`_find_mask` (used by `Volume.__init__` for masked/linear data) returns the first
  matching saved mask found by `glob.glob` if multiple masks in the database happen to have
  the same voxel count** (`cortex/dataset/braindata.py:645-660`) — a potential silent
  mask-ambiguity bug, not confirmed to occur in practice with pycortex's standard example
  data.
- **`VolumeRGB`/`VertexRGB`'s `vmin`/`vmax` accept "a tuple of three floats" per the
  docstring, but the constructor does not validate tuple length** — `channel_vmins =
  [float(v) for v in vmin]` (`cortex/dataset/viewRGB.py:265`) silently produces a
  wrong-length list for a 2-tuple or 4-tuple input, which would misalign with the three
  color channels downstream rather than raising a clear error.
- **`cortex.anat.whitematter`'s bare `except:` clause** (`anat.py:45`) catches literally
  any exception (including e.g. `KeyboardInterrupt`) from the FreeSurfer-derived attempt
  before falling back to FSL — a code smell, not fixed here.
- **`cortex.anat.whitematter`'s final sanity check `assert arr.sum() >= 0`**
  (`anat.py:66`) is a tautology for a boolean/binary mask array (sum of non-negative values
  is always `>= 0`) — likely meant to check for a nonzero sum (mirroring the earlier
  all-zero check on the first `fast` attempt), but as written it can never fail.
- **`cortex.database.Database.save_view`'s docstring describes `get_view`'s behavior, not
  its own** (both share near-identical opening text; `save_view` actually captures and
  writes the *current* live view to disk, the reverse of what its docstring says) —
  `database.py:717-736` vs. `745-767`.
- **`cortex.database.Database.get_overlay` has a self-admitted broken code path**, per its
  own inline comment: `"NOTE: This try loop is broken, in that it does nothing for the
  intended use case (loading an overlay from a packed subject) - needs fixing."`
  (`database.py:354-355`).
- **`cortex.database.Database.get_anat`'s docstring is truncated mid-sentence** in both its
  `Parameters` and `Returns` sections (`database.py:200-208`).
- **`cortex.database.Database.__dir__` omits several real, callable public methods**
  (`get_paths`, `reload_subjects`, `save_mask`, `get_coords`, `get_shared_voxels`,
  `clear_cache`, `make_subj`) from its hardcoded list (`database.py:171-174`) — not a
  functional bug (the methods still work), but breaks tab-completion/introspection for
  them.
- **`cortex.freesurfer.write_dot` calls `graph.edges_iter()`**, a NetworkX API removed in
  NetworkX 2.0 (replaced by `graph.edges()`) — will raise `AttributeError` on any
  currently-maintained NetworkX version (`freesurfer.py:969`).
- **`cortex.freesurfer.write_decimated` opens its `.full.patch.3d` output in text mode
  (`'w'`) but writes `bytes`** (`struct.pack`/`ndarray.tobytes` output) to it — raises
  `TypeError` on Python 3 (`freesurfer.py:1009-1012`); should be `'wb'`, matching every
  other binary writer in the module.
- **`cortex.freesurfer.SpringLayout._estatic`** (an electrostatic-repulsion term) is dead
  code — never called from `.step()`, and would itself fail if called since it references
  `self.kdt`, which is only ever set up in a comment, never actually assigned
  (`freesurfer.py:1049,1078-1083,1086-1087`).
- **`cortex.freesurfer.stretch_mwall` mutates its `pts` argument in place** with no
  docstring warning of this (`freesurfer.py:1107-1113`).
- **`cortex.anat.voxelize` returns `vox.T` but saves the untransposed `vox`** to
  `outfile` (`anat.py:82-85`) — the in-memory return value and the on-disk file are not the
  same orientation.
- **`VolumeRGB`'s fast-path vs. remap-path fork** (whether raw R/G/B values are used
  directly, or normalized/recombined through `color_voxels`) is selected by an all-or-
  nothing conjunction of five conditions (`channel*color` all at R/G/B defaults AND `vmin`
  AND `vmax` both `None` AND `autorange == "individual"`) — not a bug, but a sharp edge:
  passing any single styling argument (even one that seems unrelated, like `autorange=
  "shared"` with default colors and no vmin/vmax) silently switches the whole class's
  numeric interpretation of the input data. Same logic duplicated in `VertexRGB`.
- **`cortex.webgl.show`'s `layout` parameter has a wrong type hint** (`Optional[str]`) that
  contradicts its own docstring and actual usage (`None or list of (int, int)`), and
  contradicts the equivalent, correctly-typed `layout` parameter in `make_static`
  (`view.py:304` vs. usage patterns matching `make_static`'s `layout=None`).
  `cortex/webgl/view.py:304`.
- **`cortex.webgl.make_static`'s `anonymize=True` path does a raw string `.replace(fname,
  newfname)` on generated JSON file contents** (`view.py:196-197`) to rename subjects inside
  the CTM metadata JSON — a plain substring replace rather than a structured JSON edit,
  which is a latent risk (not confirmed to have ever misfired) if a subject's internal name
  string happens to be a substring of unrelated JSON content.

## General recommendations for pycortex maintainers

(Running list — will be expanded as more modules are covered.)

1. Adopt a project-wide convention of documenting `**kwargs` forwarding targets explicitly
   (e.g. "Other Parameters: see `cortex.quickflat.make_figure`, forwarded via `**kwargs`")
   rather than silently inlining a subset of the target function's parameters as if they
   belonged to the wrapper.
2. Add `Returns`, `Raises`, and `Examples` sections consistently — none of the functions
   reviewed so far in `cortex.quickflat` have any of the three.
3. Fix or remove the `shadow` parameter in `cortex.quickflat` (currently broken for any
   non-`None` value).
4. Either implement or remove `with_borders` in `make_figure`.
5. Consider whether `cortex.quickflat.view.make_movie`, which is unreachable
   (`NotImplementedError` on the first line), should be removed entirely or actually
   finished.

---
*This file is updated incrementally as each module is completed — see the progress
checklist above for current status.*
