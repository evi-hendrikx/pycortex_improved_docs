# Example suggestions for the conceptual docs

Not published/linked from the site (deliverable 5 of the plan doc — a
working file for whoever maintains the example gallery next, not a
rendered page). Cross-checked against `examples/` as it exists in the
repo right now, not invented from scratch.

## What's already there and where it fits (no changes suggested)

The gallery is more complete than the plan doc assumed — most of the
conceptual pages already have a matching worked example:

| Concept | Existing example |
|---|---|
| 2D colormap (`Volume2D`) | `examples/datasets/plot_volume2D.py` |
| Precomputed RGB colors (`VolumeRGB`) | `examples/datasets/plot_volumeRGB.py` |
| `Vertex` vs `Volume` | `examples/datasets/plot_vertex.py`, `plot_volume_to_vertex.py` |
| ROI → voxel mask/index | `examples/utils/plot_roi_voxel_mask.py`, `plot_roi_voxel_index_volume.py`, `plot_get_roi_vertices.py` |
| Static WebGL export | `examples/webgl/static.py`, `single_dataset.py` |
| End-to-end align → cut/flatten → visualize | `examples/quickstart/fmri_flattening.ipynb` (referenced from `segmentation_guide.rst`) |

I linked the retinotopy quickstart (`plot_retinotopy_flatmap.py`) and the
`S1` demo snippet from `overview.rst` rather than write a new "hello
world," since both are real, already-verified examples (see
`_conceptual_docs_notes.md`).

## Gaps / suggested new examples, one per reworked page

- **`overview.rst` (roadmap)** — there's no single example that shows the
  *whole* pipeline (surfaces → align → mask → Volume → flatmap/webgl) in
  one short, runnable script using only the bundled `S1` subject (no
  download, no FreeSurfer run required). `plot_retinotopy_flatmap.py`
  covers the back half (load → flatmap) but starts from a downloaded
  dataset, and the only full front-to-back walkthrough
  (`fmri_flattening.ipynb`) requires a real subject, a real BOLD file, and
  Blender. A short `examples/quickstart/plot_pipeline_overview.py` using
  `cortex.Volume.random("S1", "fullhead")` plus `cortex.db.get_mask` and
  both `quickshow` and `webshow` would give new users one script that
  maps directly onto the roadmap diagram, runnable with nothing but the
  base install.
- **`database.rst`** — the page explains `cortex.db.get_surf`,
  `get_xfm`, `get_mask`, and the tab-completion interface with inline
  snippets, but there's no example script exercising the `cortex.db.S1.*`
  tab-completion interface end-to-end. Not critical (it's an interactive/
  REPL feature, awkward as a `.py` script), but a short snippet in the
  page itself showing `get_surf` → `get_mask` → building a `Volume` from
  the mask would connect the database page more concretely to the
  `Volume`/`Vertex` glossary entries.
- **`align.rst`** — no example currently demonstrates the "check your
  alignment" tip already in the page ("make a flatmap out of the
  reference image using the transformation ... good alignment results in
  a smooth color gradient"). This is a genuinely useful, concrete
  sanity-check that's currently only described in prose. Worth a short
  example: run `cortex.align.automatic`, then `quickshow` the reference
  EPI volume itself through the new transform, so the reader can see what
  "smooth gradient = good, patchy = bad" actually looks like.
- **`rois.rst` / `roidraw.rst`** — `plot_get_roi_vertices.py` and
  `plot_roi_voxel_mask.py` cover *using* an existing ROI, but nothing
  shows the SVG-drawing side end-to-end (draw → `add_roi` → mask). That
  workflow is inherently interactive (Inkscape/browser), so a scripted
  example can't fully replace it, but a short "given an `overlays.svg`
  you already drew, here's `get_roi_verts` + `get_roi_masks` side by
  side" example would make the mask/vertex duality mentioned in
  `rois.rst`'s new "why" section concrete.
- **`transforms.rst`** — no example currently shows `coord` vs `magnet`
  space side by side, or demonstrates `cortex.db.save_xfm` deriving one
  from the other (the fact I checked against source for the "why"
  section). A short example loading a transform both ways and printing
  both matrices would make that distinction tangible rather than purely
  textual.
- **`colormaps.rst`** — ~~no example currently builds a `Volume2D` *and*
  shows the corresponding 2D colormap swatch~~ **done**: added a "A
  worked example" section with a real `Volume2D(first, second, ...)`
  flatmap (`flatmap_2d_first_vs_second.png`) and the exact code that
  generated it, right after the "why 1D vs 2D" prose. Still worth also
  cross-linking to `examples/datasets/plot_volume2D.py` for a second,
  more complete worked example — that part's still open.

## Existing examples worth double-checking / fixing

- **`examples/quickstart/plot_retinotopy_flatmap.py`** — works and is
  accurate, but never mentions that `S1` is the pycortex-*bundled* demo
  subject (it only says "S1 is the example subject that comes with
  pycortex"), so a reader doesn't realize they already have `S1`'s
  surfaces locally and don't need to import anything before running this
  — only the retinotopy *data* needs downloading. Worth one added
  sentence pointing at `overview.rst`'s glossary/`S1` mention. Not a
  correctness bug, just a missed connection to the new "why" framing.
- **`examples/quickstart/retinotopy_webgl.py`**,
  **`examples/quickstart/show_config.py`**,
  **`examples/utils/mni_to_subject.py`**,
  **`examples/utils/subject_to_mni.py`**,
  **`examples/utils/multi_panels_plots.py`** — none of these filenames
  start with `plot_`, and `docs/conf.py`'s `sphinx_gallery_conf` sets
  `'filename_pattern': '/plot_'`, which controls which example scripts
  Sphinx-Gallery actually *executes* when building the gallery. I did not
  build the full gallery in this pass to confirm the rendered output
  (see `_conceptual_docs_notes.md`), so I can't assert with certainty
  whether these show up unexecuted, execute anyway, or are silently
  skipped — but it's worth the maintainers confirming these five scripts
  render the way they're intended to (renaming to a `plot_` prefix if
  they're meant to execute and currently don't).
- **`examples/quickstart/fmri_flattening.ipynb`** — genuinely the best
  single "full pipeline" example in the repo (align → cut/flatten →
  visualize, matching the roadmap diagram closely), but it's a Colab
  notebook link inside `segmentation_guide.rst`'s prose, not part of the
  gallery, and its intro cell points at a fork
  (`dmitry-mli/pycortex/blob/blender-flattening-support/...`) rather than
  `gallantlab/pycortex`. Worth confirming that link still reflects the
  current recommended branch/location before treating it as a stable
  reference from `overview.rst` or `segmentation_guide.rst`.