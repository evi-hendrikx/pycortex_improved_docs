# Conceptual docs rewrite — working notes

Not published/linked from the site (no toctree entry). Internal record of
what changed and why, for whoever reviews this work.

Source design doc: `pycortex-conceptual-docs-plan.md` (repo root).
Execution plan: written to plan mode, approved before implementation
(session on 2026-08-20).

## What changed, page by page

- **`docs/overview.rst`** (new) — landing/on-ramp page. Problem statement
  paraphrased from Gao et al. 2015 (cited, not quoted at length), an ASCII
  roadmap diagram, a "which page do I need" table, and a hello-world
  example reusing the exact snippet already in `install.rst`
  (`cortex.webshow(cortex.Volume.random("S1", "fullhead"))`) rather than
  inventing a new one.
- **`docs/glossary.rst`** (new) — `.. glossary::` directive with 13 terms
  (subject, filestore, fiducial/inflated/flat surface, xfm/transform,
  xfmname, mask, pixel-wise sampling, CTM, Volume, Vertex, Dataset, ROI
  overlay, dropout). Each links back to the page that owns the full
  explanation.
- **`docs/index.rst`** — added `overview` and `glossary` to the toctree
  (overview first), added one pointer sentence near the top. Left the
  rest (citation, indices) untouched.
- **`docs/install.rst`** — one added sentence after the demo snippet
  pointing to `overview.rst` for what the API calls mean.
- **`docs/segmentation_guide.rst`** — added a "Why this exists" section
  before the existing walkthrough: individual-subject vs. `fsaverage`
  surfaces, what a fiducial surface is and why FreeSurfer is used, and
  folded the one substantive point from the orphaned `segmentation.rst`
  (mentioning Caret as an alternative segmentation/flattening tool) into
  this section, since `segmentation.rst` itself is not reachable from
  the built site. Also added one sentence in the "Making cuts" section
  explaining *why* cutting is topologically necessary before flattening
  (a closed curved surface can't be flattened without cutting — this is
  a general cartography/geometry fact, not specific to the paper or
  pycortex source, so it's not attributed to either).
- **`docs/database.rst`** — added a "Why this exists" section up top
  (why a pycortex-owned filestore instead of pointing at `SUBJECTS_DIR`,
  why surfaces must share vertex counts) and fixed a broken `:module:`
  Sphinx role (not a real role) that pointed at `svgroi.py`, replaced
  with a `:doc:` cross-link to `rois.rst` plus a plain-text mention of
  `cortex.svgroi`.
- **`docs/align.rst`** — added a "why" intro (no separate heading, per
  request — see below) on misregistration/rigid-body reasoning. Then
  found, on user request to check "all the mayavi stuff" against current
  source, that the entire "Manual Alignment" section and half of
  "Automatic Alignment" were describing an API that no longer exists this
  way. Rewrote both against `cortex/align.py` directly:
  - `cortex.align.manual` used to be the Mayavi-based aligner; it has
    been **renamed to `cortex.align.mayavi_manual`** and is now
    deprecated (raises `DeprecationWarning` on call). The name
    `cortex.align.manual` now belongs to what used to be called
    `fs_manual` — a FreeSurfer **FreeView**-based aligner. `fs_manual` is
    now just a deprecated alias for `manual`. The doc had this exactly
    backwards (said `manual` = Mayavi, `fs_manual` = FreeView
    alternative). Rewrote the "Manual Alignment" section around the
    current `cortex.align.manual` (FreeView, `wm_color`/`pial_color`/
    `wm_surface`/`inspect_only`/`noclean`/`reference` args, requires
    `$SUBJECTS_DIR` + `freeview`/`lta_convert` on PATH), and moved the
    old Mayavi screenshot walkthrough to a clearly-labeled "Legacy: the
    old Mayavi-based aligner" section at the bottom instead of deleting
    it (preserves the content per the "don't delete without preserving
    substance" constraint, since it may still be relevant to older
    installs).
  - `cortex.align.automatic` **defaulted to FSL** when the old doc was
    written; as of pycortex 1.2.8 it defaults to FreeSurfer's
    `mri_coreg` + `bbregister` instead (confirmed via the
    `warnings.warn(...)` literally inside the current function). The old
    FSL-based behavior is now a separate function, `automatic_fsl`. The
    doc's `use_fs_bbr=True` kwarg **does not exist** on current
    `automatic()` at all — removed that example, documented `init`/
    `epi_mask`/`reference_contrast`/`intermediate` instead (all read
    directly off the current signature and docstring).
  - The doc claimed `noclean` "defaults to `true`" and that setting it to
    `false` keeps temp files — backwards on both counts. Current
    signature default is `noclean=False`, and `noclean=True` is what
    keeps the files (per the docstring: "If True, intermediate files
    will not be removed"). Fixed.
  - Found and flagged (not fixed, since it's in `cortex/align.py`, out of
    this doc-only task's scope) a **source docstring bug**: `manual()`'s
    signature defaults are `wm_color="yellow", pial_color="blue"`, but
    its own docstring says the defaults are `"blue"` and `"red"`
    respectively. Documented the real (signature) defaults, and added a
    note in the rendered page telling readers to trust what FreeView
    actually shows over either written default, since the two disagree
    in the source itself.
  - `docs/transforms.rst` also referenced the old "manual aligner is
    mayavi-based" framing and linked to `docs.enthought.com/mayavi` as
    *the* alignment tool — fixed to describe both current tools
    generically and removed the now-orphaned `mayavi_` footnote target.
  - `docs/overview.rst`'s roadmap diagram listed
    `cortex.align.automatic / cortex.align.manual / cortex.align.fs_manual`
    as three meaningfully different options — fixed to
    `cortex.align.automatic (or automatic_fsl) / cortex.align.manual`,
    since `fs_manual` is just a deprecated alias, not a third option.
  - Per follow-up request, the "Legacy: the old Mayavi-based aligner"
    section (the old screenshot walkthrough I'd moved to the bottom
    rather than deleted) was removed outright instead. `align.rst` now
    only documents the current `automatic`/`automatic_fsl`/`manual` API.
    Note: `docs/aligner/*.png` (the screenshots that section used) are
    now unreferenced by any `.rst` file — left in place since deleting
    image assets wasn't requested, but flagging them as orphaned in case
    someone wants to clean them up.
  - **Not** touched: `docs/segmentation_guide.rst`'s Mayavi references
    (`cortex.segment.fix_wm`/`fix_pia` popping up a Mayavi viewer for
    voxel editing) — checked against current `cortex/segment.py`, this
    is a *different*, unrelated use of Mayavi that is still current and
    accurate as written.
- **`docs/rois.rst`** — was a 4-sentence stub; expanded with a "Why this
  exists" section (thresholded/volumetric ROIs vs. hand-drawn SVG
  boundaries on a flatmap, and why one drawing works for both a
  volumetric mask and a surface vertex set) grounded in the paper's ROI
  section and `cortex.utils.add_roi`. Kept the original short paragraph
  and the `roidraw` seealso as a second "Using ROIs" section.
- **`docs/transforms.rst`** — was a short stub; added a "Why this exists"
  intro and expanded the coord-vs-magnet explanation. **Checked against
  `cortex/database.py`'s `save_xfm`** before writing this: it turns out
  `save_xfm` automatically derives whichever of `coord`/`magnet` you
  didn't supply from the reference image's own affine, so they can't
  practically drift apart through pycortex's own API — only by
  hand-editing the stored `matrices.xfm` JSON directly. The text reflects
  that (my first draft overstated the risk; corrected it after reading
  the actual `save_xfm` implementation). Also fixed two broken `:module:`
  roles, replaced with a `:doc:` cross-link to `align.rst`.
- **`docs/colormap_rst.py` / `docs/colormaps.rst`** — see "Deviation from
  the plan doc" below. Added a "why 1D vs 2D colormaps" section (which
  colormaps in the list are 2D — the ones with `2D`/`alpha`/`covar` in
  the name — and why: `Volume2D`/`Vertex2D`/`VolumeRGB`/`VertexRGB` need
  to encode two values per point, e.g. an effect size plus a reliability/
  alpha channel, which a single 1D colormap can't do), regenerated
  `colormaps.rst` from the updated script so the committed page matches.
- **`docs/roidraw.rst`** — one added cross-link line at the top pointing
  back to `rois.rst` for the "why". No other changes — this page was
  already current and well-scoped (documents a separate add-on package,
  `pycortex-roidraw`, not part of core pycortex).
- **Not touched**: `docs/userguide/webgl.rst`, `docs/api_reference_flat.rst`,
  `docs/dataset.rst` (still commented out of the toctree — left that way;
  reactivating a possibly-stale page wasn't in scope and wasn't asked
  for), `docs/segmentation.rst` (orphaned, see below).

## Deviations from the plan doc (flagged as instructed)

1. **`docs/colormaps.rst` is not hand-written** — it's fully regenerated
   by `docs/colormap_rst.py` from `filestore/colormaps/*.png` every time
   that script runs, so editing the `.rst` directly would be silently
   overwritten on the next regeneration. Per the plan doc's own
   contingency ("if any turn out to be autogenerated, treat as read-only
   source and write improved version alongside instead, and flag the
   discrepancy"), I instead edited the generator script
   (`docs/colormap_rst.py`) to prepend the "why" section, then ran it
   once to regenerate `colormaps.rst` so the committed file reflects the
   new script. This script is a docs-build helper, not `cortex` package
   source, and running it does not change any program behavior — only
   the generated `.rst` file.
2. **`docs/segmentation.rst` (23 lines) is orphaned** — not in
   `index.rst`'s toctree and not linked from any other page, so it isn't
   part of the built/rendered site at all. It's an older, shorter draft
   covering roughly the same ground as `segmentation_guide.rst` (which is
   linked, current, and much more complete — it already documents the
   newer Blender/SLIM cutting-and-flattening workflow that
   `segmentation.rst` predates). I folded its one distinct point (Caret
   as an alternative segmentation tool) into `segmentation_guide.rst`
   rather than resurrecting the whole page, and left `segmentation.rst`
   itself untouched/unlinked per the "don't delete without preserving
   substance" constraint — its content is not lost, but the file is
   effectively dead. Flagging this rather than silently leaving a
   duplicate, undiscoverable page in the tree.
3. **No Mermaid/Graphviz diagram** — `docs/conf.py` has no diagram
   extension configured, and this is a plain `alabaster`-themed build
   with no evidence of what environment actually runs `make html` (no
   CI docs-build config found in this pass). Adding
   `sphinxcontrib-mermaid` or `sphinx.ext.graphviz` would add a new
   dependency that might not be installed wherever these docs are built,
   and Graphviz specifically needs a system binary, not just a pip
   package. Used a plain ASCII diagram in a `.. code-block:: text` block
   instead — the plan doc explicitly allows this fallback. Worth
   revisiting if the maintainers confirm Mermaid rendering is available
   in their actual build pipeline.

## Things I was not confident enough to assert as fact

- **Why `overlays.svg`/masks were specifically added "in May 2013"**
  (an existing, unverified claim already in `database.rst` before this
  rewrite) — left as-is, did not add or remove this date claim, did not
  independently verify it against git history.
- **Exact reason automatic alignment "gets you like 95% of the way"** —
  this is existing text from the original `align.rst`, not something I
  added or independently verified numerically; kept as an informal
  existing claim, not restated as a precise measured figure.
- I did **not** re-verify every image/screenshot in `align.rst`'s manual
  aligner walkthrough (mayavi GUI) against a running install — that
  section was left untouched, since it's step-by-step GUI instruction,
  not conceptual framing, and the "note" already in that file says the
  manual aligner is Ubuntu-14.04-specific/possibly broken on newer
  systems. Not in scope for this pass; flagging in case it's worth a
  separate audit.

## Local build check

Attempted `cd docs && make html`. Result: **not run to completion in this
pass** — [fill in after the build attempt below]. See the end of this
session's tool output for the actual pass/fail and any warnings surfaced,
and update this line before treating the check as done.

## Correction: removed the colormaps.rst image, found it already existed elsewhere

Per "do not put it in colormaps": removed the "A worked example" section
(image + code) I'd added to `colormap_rst.py`/`colormaps.rst`, replacing
it with a one-line pointer to `overview.rst` and the runnable
`plot_volume2D.py`/`plot_vertex2D.py` examples instead.

While doing that, found that `overview.rst` (edited elsewhere since I
last touched it) now has `docs/flatmap_comparison.png` — a proper 3-panel
"first (1D) / second (1D) / first & second jointly (2D)" comparison
figure, already embedded right in the intro. This does the same job as
the image I'd generated, better (one integrated figure vs. my separate
gif + static image), so I did not add my own image anywhere — it would
have been redundant. `docs/flatmap_2d_first_vs_second.png` (the file I
generated earlier this session) is now unreferenced by any `.rst`/`.py`
file; left it on disk rather than deleting unprompted, but it's dead and
safe to remove.

While looking at the current `overview.rst`, also fixed a real bug (not
a style choice): a dangling, grammatically incomplete sentence fragment
— "interactive 3D visualizations of fMRI data projected onto cortical
surface models. It can also generate high quality 2D flattened cortical
visualizations." — sitting on its own with no subject, clearly a
copy-paste remnant of `index.rst`'s "Pycortex is a software package for
generating beautiful interactive 3D visualizations..." with the opening
clause missing. Deleted it; the paragraph right after already covers the
same ground properly.

## New real (not reused) image: `flatmap_2d_first_vs_second.png`

(Superseded by the above — see the correction note. Kept below for the
original reasoning/verification trail.)

Per request for a 3rd image showing "first vs second" as a 2D map: this
one isn't a reused existing asset — actually ran pycortex in this
environment to generate it. Reused the same `first`/`second` random-data
pattern from `examples/quickflat/plot_make_gif.py` (same seed/vmin/vmax
convention as the `overview.rst` gif, for consistency), but instead of
two separate 1D flatmaps, built a `cortex.Volume2D(first, second, ...)`
and rendered it with `cortex.quickflat.make_png(..., with_colorbar=True)`
— i.e. one flatmap where a 2D colormap jointly encodes both values, with
a real 2D colorbar swatch in the corner. Saved as
`docs/flatmap_2d_first_vs_second.png`.

Placed it in `colormaps.rst` (via `colormap_rst.py`, since that page is
generated — added a new "A worked example" section, with the exact code
that produced the image included as a runnable snippet) rather than
`overview.rst`, since it's specifically demonstrating the 2D-colormap
concept that page's "why 1D and 2D colormaps" section already introduces
conceptually but had no concrete example for — this was flagged as a gap
in my own `_example_suggestions.md` ("no example currently builds a
`Volume2D` and shows the corresponding 2D colormap swatch from this page
side by side"), now closed.

## "What you're building toward" image + troubleshooting (grad-student audience)

Per the corrected audience calibration (see the saved memory note — PIs
handing this to grad students, not undergrads: assume standard fMRI/
neuroimaging knowledge, don't over-explain, but do lower pycortex-specific
setup friction), added two things:

- **`overview.rst`**: an early image before any prose, so a new reader
  sees a real flatmap before reading motivation text. Used
  `docs/flatmap_comparison.gif` — an existing, git-tracked, already
  git-historied asset (`git log`: "Include pre-generated gif for display
  purposes", 2019), confirmed via its origin commit and
  `examples/quickflat/plot_make_gif.py`'s own source to be
  `cortex.Volume.random("S1", ...)` — i.e. **random placeholder data**,
  not a real result. Said so explicitly in the caption rather than
  letting it look like a real finding — didn't want to imply a
  scientific result that doesn't exist. Picked this over the other
  unused candidate image (`docs/raw.png`, an older ~2013-2014 semantic-
  RGB flatmap with no git history tying it to current source, so its
  provenance/accuracy against the current `S1` demo subject couldn't be
  verified) for that reason.
- **`install.rst`**: new "Troubleshooting" section covering the concrete,
  verified pycortex-specific failure modes hit this session or found in
  `cortex/defaults.cfg`/source: `$SUBJECTS_DIR` unset (verified
  `cortex.segment.edit_segmentation` does a bare
  `os.environ["SUBJECTS_DIR"]`, i.e. `KeyError` if unset), FreeSurfer/FSL
  binaries not on `PATH`, the NeuroDebian `fsl_prefix` config option
  (grounded in `cortex/defaults.cfg`'s own comment), and the
  `[dependency_paths]` config section for Inkscape/Blender/SLIM/meshlab
  (also grounded in `defaults.cfg`, including its macOS absolute-path
  guidance) — none of which were surfaced in the docs anywhere before
  this. Deliberately did **not** add generic "how to use pip/conda/a
  terminal" content, per the grad-student calibration.

## `docs/api_reference_flat.rst` (out-of-original-scope, done on request)

Fixed the two issues from my own code-review list, on request:

- The `quickflat` section listed `add_curvature`/`add_data`/`add_rois`/
  `add_sulci`/`add_hatch`/`add_colorbar`/`add_custom`/`add_cutout`/
  `get_flatmask`/`get_flatcache` directly under `cortex.quickflat`, but
  none of those are actually attributes of `cortex.quickflat` — verified
  via `hasattr` that they live in `cortex.quickflat.composite` (the 8
  `add_*` layer functions) and `cortex.quickflat.utils` (`get_flatmask`,
  `get_flatcache`, plus `make_flatmap_image` which wasn't listed at all).
  Split the section into three (`quickflat`, `quickflat.composite`,
  `quickflat.utils`), each with its own `.. automodule::`, matching the
  existing per-module pattern already used throughout this file. Also
  added `make_gif`/`make_movie` to the top-level `quickflat` list — both
  are real top-level exports (`cortex.quickshow` etc.) that were simply
  missing from the listing entirely, not misplaced.
- Removed the deprecated `get_roi_mask` (singular) entry from the
  `utils` section, keeping `get_roi_masks` (plural, current).
- Verified every moved/added name resolves at its new documented path
  with `hasattr` before editing, then confirmed via rebuild: all ~10
  `[autosummary] failed to import cortex.quickflat.*` warnings are gone,
  and the corresponding stub pages exist under `docs/generated/`
  (e.g. `cortex.quickflat.composite.add_data.rst`).
- **Not done** (flagged in my code-review list but not requested here):
  `segment`'s listing still has deprecated `fix_wm`/`fix_pia` and is
  missing `edit_segmentation`/`run_freesurfer_recon`/`flatten_slim`;
  `align`'s listing is missing `automatic_fsl`. Same class of staleness,
  left for a follow-up request since this task was scoped to the
  quickflat/get_roi_mask items specifically.

## `examples/quickstart/plot_retinotopy_flatmap.py`

Per one of my own `_example_suggestions.md` findings, added one sentence
to this example's module docstring making explicit that `S1`'s surfaces
are already bundled with the install (linking to `overview.rst`), so the
`urlretrieve` call in the script is only fetching the retinotopy *data*,
not the subject. This is an example script docstring, not `cortex`
package source/behavior — no executable code changed.

While rebuilding to verify, found (not created by me) a new example file,
`examples/quickstart/plot_pipeline_overview.py`, with two broken `:doc:`
references (`segmentation_guide`, `align` — missing the leading `/` for
an absolute doc path from a nested example dir, same class of mistake).
This looks like the concurrent peer session's work (see "Concurrency
note" above) — possibly implementing my own suggestion of a single
whole-pipeline example. Left it alone since it wasn't part of this
request and may be actively being edited elsewhere; flagging for
follow-up.

## Rebalanced `overview.rst` toward display, not just setup

Per feedback that the roadmap diagram read as mostly about FreeSurfer/
alignment preprocessing when pycortex is really mostly about displaying
data: split "The core mental model" into an explicit "Phase 1 — one-time
setup, per subject" (FreeSurfer/import/align, unchanged content, now
visually smaller) and "Phase 2 — every time you have data to look at"
(now expanded with the actual breadth of display options grounded in
`cortex/quickflat/view.py`'s `make_figure` signature — ROI outlines,
labels, sulci, curvature, dropout, colorbar, cutouts — and
`userguide/webgl.rst`'s already-documented interactive features —
live colormap/dataset switching, in-browser ROI/sulcus drawing, saved
viewpoints, time-series playback). Reworded the section intro to say
this directly rather than leaving the reader to infer it from a
five-stage linear diagram that was 3/5 setup and 2/5 display.

Also replaced the inline "five-minute demo" code block with a "Where to
see it working" section that links to the existing snippet in
`install.rst` (not duplicated) and points more specifically into
`examples/quickstart/`, `examples/quickflat/`, `examples/datasets/`, and
`examples/webgl/` for the display-side functionality Phase 2 now
describes — all four directories confirmed to exist in `examples/`.

## Added "Phase 3 — have fun with it"

Per request, added a third, lighter-toned phase after Phase 1 (setup)
and Phase 2 (display) in "The core mental model": a short, playful list
of the more exploratory/creative corners of pycortex, each linked to a
real example script (grepped each example's own docstring title before
picking it, not guessed from filename) — animated GIFs, multi-dataset
comparison viewers, `Dataset`/`Volume` arithmetic, geodesic distance/path
tools, subsurfaces, Tissot's indicatrix (flatmap distortion
visualization), and advanced compositing control.

## Deprecation audit (full repo sweep, on request)

Grepped `cortex/` for `DeprecationWarning`/`deprecated`/`will be removed`
to find every deprecated function, then checked each reworked page's code
snippets against that list.

- **`align.rst`** — already covered above (`mayavi_manual`/`fs_manual`,
  old `automatic()` FSL default). The Mayavi section was subsequently
  removed outright per follow-up request rather than kept as a labeled
  legacy section.
- **`segmentation_guide.rst`** — found and fixed a second, separate
  deprecation: `cortex.segment.fix_wm()` / `fix_pia()` (the
  tkmedit+Mayavi voxel-editing tools used twice in this page) are
  deprecated in current source in favor of
  `cortex.segment.edit_segmentation()` + `cortex.segment.run_freesurfer_recon()`
  (a FreeView-based combined tool). Rewrote both usages accordingly.
  Deliberately did **not** invent FreeView-specific click/keyboard
  instructions to replace the old tkmedit ones (edit-voxel tool, left/
  center/right-click semantics, brush-radius menus) — those were
  tkmedit-specific and I have no verified source for FreeView's
  equivalent controls, so fabricating them would violate the "don't
  invent plausible-sounding rationale" constraint. Pointed readers to
  FreeView's own documentation instead. Also corrected the claimed
  tkmedit outline colors (yellow=main/green=original/red=pial) which was
  tkmedit-specific and doesn't apply to FreeView (FreeView, per
  `edit_segmentation`'s source, uses yellow=smoothwm, green=white,
  **blue**=pial, not red).
  - Note: the deprecation warning text in `cortex/segment.py` itself says
    to use "`edit_segmentation()` and `rerun_recon()`", but no
    `rerun_recon` function actually exists in the source — the real
    function is `run_freesurfer_recon` (aliased from
    `cortex.freesurfer.autorecon`). Used the real, working name in the
    docs and flagging the source's own warning-message typo here rather
    than silently propagating it.
- **Checked, not touched (no deprecated calls found)**: `database.rst`
  (`get_surf`, `get_xfm`, `load_xfm`, `get_mask`, `load_mask`,
  `webgl.show`), `rois.rst`/`roidraw.rst` (no direct Python calls),
  `transforms.rst`, `install.rst`, `overview.rst`, `glossary.rst`,
  `docs/dataset.rst` (`Dataset`, `Volume`, `Vertex`, `VolumeRGB`,
  `VertexRGB`, `load`, `quickshow`, etc.), `docs/userguide/webgl.rst` (no
  Python calls, just UI/keyboard-shortcut docs).
- **Out of scope but flagging**: `docs/api_reference_flat.rst` (the
  auto-generated API reference, explicitly a separate project per the
  plan doc) lists `get_roi_mask` in its function index —
  `cortex.utils.get_roi_mask` (singular) is deprecated in favor of
  `get_roi_masks` (plural) per its own `warnings.warn(...)`. Not fixed
  here since that file is autosummary-generated and out of this task's
  stated scope, but worth a heads-up for whoever picks up the API-docs
  project.
- Other deprecated functions found in the sweep
  (`cortex.surfs`, `get_roipack`, `get_roi_mask`, `db.get_coords`,
  `freesurfer.show_surf`, `blend_curvature`) are not referenced by any
  narrative doc page at all, so nothing to fix there.

## Formatting change: no "Why this exists" headings

Per request, removed the literal "Why this exists" section heading from
every page it was added to (`segmentation_guide.rst`, `database.rst`,
`align.rst`, `rois.rst`, `transforms.rst`) — the explanatory paragraphs
now flow directly under the page's main title instead of sitting under a
repeated boilerplate subheading. `colormap_rst.py`'s "Why 1D and 2D
colormaps" heading was left as-is since it's a specific, non-generic
heading, not the generic phrase that was asked to go.

## Concurrency note

Partway through this session, `docs/dataset.rst` was found modified on
disk by a concurrent Claude Code session on the same repo (not by me —
that file was never in this session's edit scope). The user confirmed
that session isn't important and to proceed regardless. Its changes
(fixing a `Volume2d` → `Volume2D` typo, documenting `VertexRGB`/
`Vertex2D`, fixing a `:method:` role) don't conflict with anything in this
plan and aren't cross-linked from any page I touched, so they were left
in place rather than reverted.

## Not done / explicitly out of scope

- No `.py` file under `cortex/` (the actual package) was modified. Only
  `docs/**` and `docs/colormap_rst.py` (a docs build helper) changed —
  confirmed via `git diff --stat -- cortex/` being empty.
- API reference regeneration/audit is a separate project per the plan
  doc; not touched here.
