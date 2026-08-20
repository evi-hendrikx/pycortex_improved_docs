# cortex.webgl.make_static

## Current signature (from source)
```python
def make_static(
    outpath,
    data,
    recache=False,
    template="static.html",
    anonymize=False,
    overlays_available=None,
    overlays_visible=("rois", "sulci"),
    labels_visible=("rois",),
    types=("inflated",),
    html_embed=True,
    copy_ctmfiles=True,
    title="Brain",
    layout=None,
    overlay_file=None,
    curvature_brightness=None,
    curvature_contrast=None,
    curvature_smoothness=None,
    surface_specularity=None,
    **kwargs,
):
```

## Where this is documented today
- Source docstring: [cortex/webgl/view.py:45-143](cortex/webgl/view.py#L45-L143)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.webgl.make_static.html
  (autodoc from this docstring; flat listing truncates to
  `make_static(outpath, data[, recache, ...])`).

## Issues with current documentation
- **No Returns section** — function returns `None` (writes files to `outpath`).
- **No Raises section.**
- **No Examples section**, despite this being one of pycortex's most commonly used
  end-user functions (exporting a shareable static WebGL viewer).
- **`**kwargs` forwarding is named but not enumerated.** The docstring says "All additional
  keyword arguments are passed to the template renderer" (a Tornado `Loader.generate(...)`
  call) but doesn't say what the template (`static.html` by default) actually accepts. In
  practice the Tornado template is a Jinja/Tornado-style HTML template — any extra kwarg
  becomes a variable available inside it; passing an unsupported/misspelled kwarg does not
  error, it's simply ignored by the template unless it references that variable name. This
  "silently does nothing if unused" behavior is worth stating so users don't assume a typo
  will raise an error.
- **`data` type description is generic ("Dataset object or implicit Dataset")** without
  pointing to `cortex.dataset.normalize` (the actual coercion function used internally) or
  giving a concrete example of "a dictionary of Volume, Vertex, etc. objects."
- **No mention that a real web server is required to *view* the output** except implicitly
  via `show`'s docs — actually, this notice **is** present in `make_static`'s own `Notes`
  section already ("You will need a real web server to view this, since `file://` paths
  don't handle xsrf correctly"), so this one is in decent shape; flagged here only because
  it's not cross-referenced from `cortex.webgl.show`, which is the more commonly used
  sibling function and where users are more likely to look first for "how do I share this."
- **`overlays_available`/`overlays_visible`/`labels_visible`/`types` are duplicated
  verbatim between `make_static` and `show`** (same wording, same defaults) with no
  cross-reference; if pycortex maintainers update one docstring's wording in the future it's
  easy for the two to drift.
- **Side effects are under-stated.** The function: creates `outpath` (and an `outpath/data`
  subdirectory) on disk if missing; calls `cortex.utils.get_ctmpack` (which itself may
  generate/cache `.ctm`/`.json`/`.svg` geometry files per subject, and can be slow the first
  time or with `recache=True`); copies/renames those files into `outpath`; writes one PNG
  per data frame into `outpath/data/`; optionally copies stimulus files referenced in
  `Dataview.attrs['stim']` into `outpath/stim/`; and writes `outpath/index.html` (with all
  JS/CSS resources inlined if `html_embed=True`, which can produce a very large HTML file).
  None of this is mentioned explicitly.
- **`anonymize`'s actual behavior is under-explained.** The docstring says "rename CTM and
  SVG files generically, for public distribution" but doesn't mention that subject names are
  replaced with `S0`, `S1`, ... (sorted alphabetically by original subject name) in both the
  output filenames and inside the generated `.json` metadata content (via a raw string
  `.replace()` on the file contents) — worth knowing since a subject name that happens to be
  a substring of something else in that JSON could theoretically get corrupted by the naive
  replace (see `_notes.md`).
- **`layout` type in the docstring ("None or list of (int, int)") doesn't match `show`'s own
  docstring for the same-purpose parameter** (`show` describes it as `None or list of (int,
  int), optional` too, but neither describes what the numbers mean — no explanation of
  what a "subwindow layout" tuple actually specifies, e.g. rows/cols or pixel offsets).

## Fixed documentation

### Summary
Creates a static webGL MRI viewer on disk so it can be shared or hosted, as opposed to
`cortex.webgl.show`, which serves an equivalent viewer from a live Python process.

### Parameters
- **outpath** : string
    The directory where the static viewer will be saved. Will be created if it
    doesn't already exist.
- **data** : Dataset object or implicit Dataset
    Dataset object containing all the data you wish to plot. Can be any type
    of implicit dataset, such as a single Volume, Vertex, etc. object or a
    dictionary of Volume, Vertex, etc. objects.
- **recache** : bool, optional
    Force recreation of CTM and SVG files for surfaces. Default `False`
- **template** : string, optional
    Name of template HTML file. Default `'static.html'`
- **anonymize** : bool, optional
    Whether to rename CTM and SVG files generically, for public distribution. Default
    `False`.
- **overlays_available** : tuple, optional
    Overlays available in the viewer. If `None`, all overlay layers of the svg file will
    be potentially available in the viewer.
- **overlays_visible** : tuple, optional
    The listed overlay layers will be set visible by default. Default `('rois', 'sulci')`.
- **labels_visible** : tuple, optional
    Labels for the listed layers will be set visible by default. Default `('rois',)`.
- **types** : tuple, optional
    Types of surfaces to include in addition to the original (fiducial, pial, and white
    matter) and flat surfaces. Default `('inflated',)`.
- **html_embed** : bool, optional
    Whether to embed the webgl resources in the html output. Default `True`. If `False`,
    the webgl resources must be served by your web server.
- **copy_ctmfiles** : bool, optional
    Whether to copy the CTM files to the static directory. Default `True`. Set `False` to
    avoid duplicating files when the same CTM data is used in many static views (the
    datastore cache must then be served with your web server).
- **title** : str, optional
    The title that is displayed on the viewer website when it is loaded in a browser.
- **layout** : None or list of (int, int)
    The layout of the viewer subwindows for showing multiple subjects, passed to the
    template generator. Default `None`, corresponding to no subwindows.
- **overlay_file** : str or None, optional
    Custom overlays.svg file to use instead of the default one for this subject.
    Default `None`.
- **curvature_brightness**, **curvature_contrast**, **curvature_smoothness**,
  **surface_specularity** : float or None, optional
    Brightness/contrast/smoothness of curvature overlay, and specularity of surfaces.
    Default `None`, which uses the value specified in the config file.
- **\*\*kwargs**
    All additional keyword arguments are passed to the template renderer. Unrecognized
    kwargs are silently ignored by the template; colliding with an internally-set name
    (`data`, `colormaps`, `layout`, `subjects`, `viewopts`, `title`, ...) raises
    `TypeError`.

### Returns
`None`. Writes the static viewer (`index.html` plus supporting `data/`, `stim/`, and mesh
files) to `outpath` as a side effect.

### Raises
- `TypeError` — if a kwarg in `**kwargs` collides with one of the template variables the
  function itself already sets (`data`, `colormaps`, `default_cmap`, `python_interface`,
  `leapmotion`, `layout`, `subjects`, `viewopts`, `title`).
- Any exception from `cortex.utils.get_ctmpack` (e.g. missing subject in the pycortex
  database, missing flat/inflated surfaces) or from file I/O in `outpath` (e.g. permission
  errors).

### Notes
- **Requires a real web server to view the output** — opening the generated `index.html`
  directly via a `file://` URL will not work correctly (WebGL/XSRF restrictions); serve
  `outpath` with any static file server (e.g. `python -m http.server`) or upload it to a
  web host.
- **Side effects**: creates `outpath` and `outpath/data` (and `outpath/stim` if stimulus
  files are referenced); generates/caches CTM mesh files per subject (slow on first call or
  with `recache=True`); writes one PNG per data frame; writes `index.html`.
- No FreeSurfer/FSL dependency; requires the subject(s) in `data` to already exist in the
  pycortex database with the requested surface `types` available.
- `html_embed=True` can produce very large single HTML files for high-resolution data or
  many timepoints; `html_embed=False` + `copy_ctmfiles=False` is more efficient for
  publishing many related static views.

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
volume_shape = cortex.db.get_xfm(subject, xfm).shape
data = np.random.randn(*volume_shape)
vol = cortex.Volume(data, subject, xfm, vmin=-2, vmax=2, cmap='RdBu_r')

cortex.webgl.make_static(
    outpath="./static_viewer",
    data=vol,
    title="Example static viewer",
)
# Then, from a terminal in ./static_viewer:
#   python -m http.server 8080
# and open http://localhost:8080/index.html in a browser.
```

## Confidence / open questions
- Could not verify the exact runtime rendering behavior of the Tornado HTML templates
  (`static.html`, etc.) beyond reading their use of the passed-in template variables — full
  verification would require actually opening the generated page in a WebGL-capable
  browser, which wasn't done in this pass.
- The claim that `anonymize`'s content `.replace()` could corrupt JSON if a subject name is
  a substring of other JSON content is a theoretical read of `view.py:190-198`
  (`ofh.write(jsoncontents.replace(fname, newfname))`), not something observed to actually
  happen — flagged as a possible-but-unconfirmed edge case in `_notes.md`.
- **Recommendation for maintainers:** add Returns/Raises/Examples; document the actual
  template-kwarg collision behavior; state explicitly (in the docstring, not just as an
  aside) which files/directories get written; consider factoring the `curvature_*`/
  `surface_specularity`/`overlays_*` parameter docs into a single shared docstring fragment
  since they are copy-pasted identically between `make_static` and `show`.
