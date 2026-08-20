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
| mapper | get_mapper | [mapper/get_mapper.md](mapper/get_mapper.md) | 🔴 no docstring; `type`'s 10 valid values undocumented (bare `KeyError` otherwise); `**kwargs` forwarding/caching undocumented |
| mapper | Mapper | [mapper/Mapper.md](mapper/Mapper.md) | 🔴 `__call__` (the main usage pattern) totally undocumented and does two unrelated things depending on input type; `idxmap` dead code confirmed (always `None`) |
| mni | compute_mni_transform | [mni/compute_mni_transform.md](mni/compute_mni_transform.md) | 🟡 already well-documented (Params+Returns); missing Raises — unchecked `flirt` return code surfaces as an opaque downstream error |
| mni | transform_to_mni | [mni/transform_to_mni.md](mni/transform_to_mni.md) | 🟡 same unchecked-subprocess issue; returned image is backed by an uncleaned temp file (undocumented) |
| mni | transform_surface_to_mni | [mni/transform_surface_to_mni.md](mni/transform_surface_to_mni.md) | 🟢 no major issues; doesn't call FSL directly unlike its siblings (worth noting) |
| mni | transform_mni_to_subject | [mni/transform_mni_to_subject.md](mni/transform_mni_to_subject.md) | 🟡 `volarray` shape vs. `template` never validated up front; unchecked subprocess return code |
| polyutils | Surface | [polyutils/Surface.md](polyutils/Surface.md) | 🟡 large class, mostly well-documented; `edge_collapse` is unimplemented dead code; several methods (`boundary_vertices`, `patches`, `polyhedra`) lack Returns sections |
| polyutils | Distortion | [polyutils/Distortion.md](polyutils/Distortion.md) | 🟢 no major issues — one of the best-documented classes in the codebase |
| segment | init_subject | [segment/init_subject.md](segment/init_subject.md) | 🟡 `**kwargs` forwarding to `autorecon` unenumerated; initial `recon-all` call's return code unchecked |
| segment | cut_surface | [segment/cut_surface.md](segment/cut_surface.md) | 🔴 likely real bug — `flatten_with="SLIM"` sets `path_type="slip"` (typo), which combined with `get_paths`'s silent-`None` return likely raises `TypeError` on import |
| segment | fix_wm | [segment/fix_wm.md](segment/fix_wm.md) | 🔴 deprecation notice points to a `rerun_recon()` function that doesn't exist anywhere in pycortex |
| segment | fix_pia | [segment/fix_pia.md](segment/fix_pia.md) | 🔴 same nonexistent-`rerun_recon()` deprecation issue as `fix_wm` |
| surfinfo | curvature | [surfinfo/curvature.md](surfinfo/curvature.md) | 🟡 no Returns section; not cross-referenced to `cortex.db.get_surfinfo`, its typical entry point |
| surfinfo | distortion | [surfinfo/distortion.md](surfinfo/distortion.md) | 🟡 `dist_type` unvalidated (bare `AttributeError` for a bad value); not cross-referenced to `polyutils.Distortion` |
| surfinfo | thickness | [surfinfo/thickness.md](surfinfo/thickness.md) | 🟢 minor gaps only (no Returns section) |
| surfinfo | tissots_indicatrix | [surfinfo/tissots_indicatrix.md](surfinfo/tissots_indicatrix.md) | 🟡 non-deterministic (no seed param, undocumented); saved `centers` output field undocumented |
| surfinfo | flat_border | [surfinfo/flat_border.md](surfinfo/flat_border.md) | 🔴 currently broken — always raises `NameError` (`height` undefined); also uses removed NetworkX 1.x API |
| utils | get_ctmpack | [utils/get_ctmpack.md](utils/get_ctmpack.md) | 🟡 incomplete Returns section; no cross-reference to webgl's usage |
| utils | get_ctmmap | [utils/get_ctmmap.md](utils/get_ctmmap.md) | 🟢 already well-documented; minor gaps (kwargs enumeration, approximation caveat) |
| utils | get_cortical_mask | [utils/get_cortical_mask.md](utils/get_cortical_mask.md) | 🟡 unrecognized `type` falls through to a bare mapper `KeyError`; noisy progress printing undocumented |
| utils | get_vox_dist | [utils/get_vox_dist.md](utils/get_vox_dist.md) | 🔴 `surface` parameter entirely missing from Parameters section despite being real |
| utils | get_hemi_masks | [utils/get_hemi_masks.md](utils/get_hemi_masks.md) | 🔴 `type` param and Returns section both empty in shipped docstring |
| utils | add_roi | [utils/add_roi.md](utils/add_roi.md) | 🔴 docstring sentence cut off mid-word ("Use the **kwargs inputs to specify"); no Returns/Raises |
| utils | get_roi_verts | [utils/get_roi_verts.md](utils/get_roi_verts.md) | 🟡 medial-wall/cut vertex recovery behavior undocumented; affects what returned indices mean |
| utils | get_roi_mask | [utils/get_roi_mask.md](utils/get_roi_mask.md) | 🔴 deprecated; returns continuous-valued floats despite the name "mask" (undocumented) |
| utils | get_aseg_mask | [utils/get_aseg_mask.md](utils/get_aseg_mask.md) | 🟡 docstring cross-reference typo (`fs_aseg_mask` should be `fs_aseg_dict`) |
| utils | get_roi_masks | [utils/get_roi_masks.md](utils/get_roi_masks.md) | 🔴 likely real bug in `fail_for_missing_rois=False` fallback (`dict_keys + list` not valid in Python 3) |
| utils | get_dropout | [utils/get_dropout.md](utils/get_dropout.md) | 🟡 `power` parameter description is blank in shipped docstring |
| utils | make_movie | [utils/make_movie.md](utils/make_movie.md) | 🔴 name collides with two unrelated "make movie" functions elsewhere in pycortex; unchecked subprocess return code |
| utils | vertex_to_voxel | [utils/vertex_to_voxel.md](utils/vertex_to_voxel.md) | 🔴 no summary line at all; author's own in-source comment questions whether it's deprecated |
| utils | get_cmap | [utils/get_cmap.md](utils/get_cmap.md) | 🔴 likely breaks on Matplotlib >= 3.9 (`plt.cm.get_cmap` removed), masked by a bare `except:` into a generic, typo'd error |

---
*Table is appended module-by-module as work progresses — see `_notes.md` for the checklist
of remaining modules.*
