# Index — pycortex API documentation improvement

One row per function/class covered. Status column summarizes the single biggest issue found
(see each linked file's "Issues with current documentation" section for full detail). See
`_notes.md` for cross-cutting patterns, scope discrepancies, and maintainer recommendations.

**Legend:** 🔴 significant gaps (missing kwargs chain, broken parameter, major drift) ·
🟡 moderate gaps (missing Returns/Raises/Examples, minor drift) · 🟢 no major issues found

| Module | Function/Class | File | Status |
|---|---|---|---|
| quickflat | make_figure | [quickflat/make_figure.md](quickflat/make_figure.md) | 🔴 `shadow` kwarg is broken (raises `KeyError`); `with_borders` is a no-op; docstring omits `with_borders`, `with_connected_vertices`, `roi_list`; no Returns/Raises/Examples |
| quickflat | make_png | [quickflat/make_png.md](quickflat/make_png.md) | 🔴 undocumented full `**kwargs` forwarding to `make_figure`; `thick` documented as own param but only works via kwargs; no Returns/Raises/Examples |
| quickflat | make_svg | [quickflat/make_svg.md](quickflat/make_svg.md) | 🔴 undocumented `**kwargs` forwarding to `make_flatmap_image`/`get_flatcache` (smaller, different surface than `make_png`); `with_dropout` silently drops numeric power arg; no Returns/Raises/Examples |
| webgl | make_static | [webgl/make_static.md](webgl/make_static.md) | 🔴 no Returns/Raises/Examples; side effects (files written) understated; `**kwargs`→template forwarding unenumerated |
| webgl | show | [webgl/show.md](webgl/show.md) | 🔴 no Returns section despite a major behavioral fork (returns a scriptable `JSMixer` client only if `open_browser` is effectively True, else `None`); `layout` type hint wrong (`str` vs list of tuple); `autoclose`/`open_browser` "Default True" wording misleading (actually config-driven) |
| dataset | Volume | [dataset/Volume.md](dataset/Volume.md) | 🔴 multiple-inheritance hides most public API (`.map`, `.masked[...]`, `.raw`, `.copy`, operators) from `Volume`'s own docstring; `Dataview.raw`/`get_cmapdict` have zero docstrings |
| dataset | Vertex | [dataset/Vertex.md](dataset/Vertex.md) | 🔴 `Vertex.map` and `Volume.map` share a name but do unrelated things; `Vertex.map`'s own Parameters section omits `surface_type`/`hemi`/`fs_subj`/`**kwargs` |
| dataset | Volume2D | [dataset/Volume2D.md](dataset/Volume2D.md) | 🔴 `vmin`/`vmax`/`vmin2`/`vmax2` docstrings are literal `"TODO:WHAT"` placeholders; 2D `cmap` is an image file, not a matplotlib colormap (undocumented) |
| dataset | Vertex2D | [dataset/Vertex2D.md](dataset/Vertex2D.md) | 🔴 same `"TODO:WHAT"` placeholder issue as Volume2D; `.vertices` undocumented |
| dataset | VolumeRGB | [dataset/VolumeRGB.md](dataset/VolumeRGB.md) | 🔴 undocumented "fast path vs. remap path" fork that silently changes numeric interpretation of input data; `state` param is a literal `"TODO"` |
| dataset | VertexRGB | [dataset/VertexRGB.md](dataset/VertexRGB.md) | 🔴 same fast/remap-path issue as VolumeRGB; `.left`/`.right` return colors not channel values (undocumented, differs from plain Vertex) |
| dataset | Dataset | [dataset/Dataset.md](dataset/Dataset.md) | 🔴 thinnest docs in the module — almost no method has a docstring; `get_surf`/`get_xfm`/`get_mask`/`get_overlay` read packed HDF5 only, easily confused with same-named `cortex.db` methods |
| align | manual | [align/manual.md](align/manual.md) | 🔴 docstring/code drift on `wm_color`/`pial_color` defaults ("blue"/"red" documented vs. actual "yellow"/"blue"); missing-`reference`-on-new-transform path likely raises `UnboundLocalError` |
| align | automatic | [align/automatic.md](align/automatic.md) | 🟡 one of the better-documented functions found so far (correct Returns); missing Raises, FreeSurfer dependency, and mincost-diagnostic caveat |
| align | autotweak | [align/autotweak.md](align/autotweak.md) | 🟡 docstring is honest about low usefulness but omits that output is saved as a new `<xfmname>_auto` transform, not overwriting the input |
| anat | brainmask | [anat/brainmask.md](anat/brainmask.md) | 🔴 no docstring at all; FSL dependency and `AssertionError` failure mode undocumented |
| anat | whitematter | [anat/whitematter.md](anat/whitematter.md) | 🔴 no docstring; undocumented 3-tier fallback chain (voxelize → FreeSurfer raw_wm → FSL fast) with varying external-tool requirements |
| anat | voxelize | [anat/voxelize.md](anat/voxelize.md) | 🔴 one-line docstring hardcodes "whitematter" though `surf` is configurable; returned array is transposed relative to the saved file (undocumented) |
| database | Database | [database/Database.md](database/Database.md) | 🔴 `save_view`'s docstring describes `get_view`'s behavior (backwards); `get_anat`'s docstring is truncated mid-sentence; `get_overlay` has a self-admitted broken code path in a comment; several methods (`get_overlay`, `save_mask`, `get_mask`, `get_cache`, `make_subj`) have no docstring at all |
| freesurfer | get_paths | [freesurfer/get_paths.md](freesurfer/get_paths.md) | 🟡 `type='slim'` undocumented; returns an unfilled `{name}` template string (undocumented) |
| freesurfer | autorecon | [freesurfer/autorecon.md](freesurfer/autorecon.md) | 🔴 `parallel`/`n_cores` undocumented; blocking interactive confirmation prompt not mentioned |
| freesurfer | flatten | [freesurfer/flatten.md](freesurfer/flatten.md) | 🟡 empty Returns section; interactive prompt undocumented |
| freesurfer | import_subj | [freesurfer/import_subj.md](freesurfer/import_subj.md) | 🔴 re-initializes the global `cortex.db` singleton (undocumented, can cause stale-reference bugs) |
| freesurfer | import_flat | [freesurfer/import_flat.md](freesurfer/import_flat.md) | 🔴 `auto_overwrite` param entirely undocumented; empty Returns section; mutable default arg |
| freesurfer | show_surf | [freesurfer/show_surf.md](freesurfer/show_surf.md) | 🔴 deprecated ("probably broken") only via runtime warning, not docstring; most params blank; Mayavi/GUI dependency unstated |
| freesurfer | make_fiducial | [freesurfer/make_fiducial.md](freesurfer/make_fiducial.md) | 🔴 one-line docstring; hard-codes `smoothwm`; writes into FreeSurfer dir not pycortex db (undocumented) |
| freesurfer | parse_surf | [freesurfer/parse_surf.md](freesurfer/parse_surf.md) | 🔴 no docstring at all |
| freesurfer | parse_curv | [freesurfer/parse_curv.md](freesurfer/parse_curv.md) | 🔴 no docstring at all |
| freesurfer | parse_patch | [freesurfer/parse_patch.md](freesurfer/parse_patch.md) | 🔴 no docstring; structured-array field sign convention only inferable from a different function's body |
| freesurfer | get_surf | [freesurfer/get_surf.md](freesurfer/get_surf.md) | 🔴 one-line docstring; name collides with two unrelated `get_surf` functions elsewhere in pycortex; 3rd return value's meaning depends on `type` |
| freesurfer | get_curv | [freesurfer/get_curv.md](freesurfer/get_curv.md) | 🟡 no Returns section; non-`'wm'` type requires a pre-existing file, not generated |
| freesurfer | write_dot | [freesurfer/write_dot.md](freesurfer/write_dot.md) | 🔴 no docstring; likely broken on NetworkX >= 2.0 (`edges_iter` removed) |
| freesurfer | read_dot | [freesurfer/read_dot.md](freesurfer/read_dot.md) | 🔴 no docstring; extremely format-fragile hand-rolled `.dot` parser |
| freesurfer | write_decimated | [freesurfer/write_decimated.md](freesurfer/write_decimated.md) | 🔴 no docstring; likely raises `TypeError` on Python 3 (text/binary file-mode mismatch) |
| freesurfer | SpringLayout | [freesurfer/SpringLayout.md](freesurfer/SpringLayout.md) | 🔴 no docstring anywhere in class; dead/broken electrostatic-repulsion code path |
| freesurfer | stretch_mwall | [freesurfer/stretch_mwall.md](freesurfer/stretch_mwall.md) | 🔴 no docstring; mutates `pts` in place (undocumented) |

---
*Table is appended module-by-module as work progresses — see `_notes.md` for the checklist
of remaining modules.*
