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

---
*Table is appended module-by-module as work progresses — see `_notes.md` for the checklist
of remaining modules.*
