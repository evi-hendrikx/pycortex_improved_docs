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

---
*Table is appended module-by-module as work progresses — see `_notes.md` for the checklist
of remaining modules.*
