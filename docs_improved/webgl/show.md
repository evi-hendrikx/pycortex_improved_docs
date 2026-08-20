# cortex.webgl.show

## Current signature (from source)
```python
def show(
    data: Union[dataset.Dataset, dataset.Dataview],
    autoclose: Optional[bool] = None,
    open_browser: Optional[bool] = None,
    port: Optional[int] = None,
    pickerfun: Optional[Callable[[tuple[int, int, int], int, str], None]] = None,
    recache: bool = False,
    template: str = "mixer.html",
    overlays_available: Optional[tuple[str, ...]] = None,
    overlays_visible: Optional[tuple[str, ...]] = ("rois", "sulci"),
    labels_visible: Optional[tuple[str, ...]] = ("rois",),
    types: Optional[tuple[str, ...]] = ("inflated",),
    overlay_file: Optional[str] = None,
    curvature_brightness: Optional[float] = None,
    curvature_contrast: Optional[float] = None,
    curvature_smoothness: Optional[float] = None,
    surface_specularity: Optional[float] = None,
    title: str = "Brain",
    layout: Optional[str] = None,
    display_url: bool = True,
    **kwargs,
):
```
Note: `layout`'s type hint (`Optional[str]`) does not match its documented/actual usage —
both the docstring and `make_static`'s equivalent parameter describe/use it as
`None or list of (int, int)`, not `str`. This looks like a copy-paste type-hint error.

Also available as `cortex.webshow` (aliased at package import time in `cortex/__init__.py`:
`from cortex.webgl import show as webshow`), and pycortex additionally exposes
`cortex.quickshow = cortex.quickflat.make_figure` — not the same function, don't confuse
the two "quick"/"web" show aliases.

## Where this is documented today
- Source docstring: [cortex/webgl/view.py:286-386](cortex/webgl/view.py#L286-L386)
- Online API page: https://gallantlab.org/pycortex/generated/cortex.webgl.show.html
  (autodoc from this docstring; flat listing truncates to
  `show(data[, autoclose, open_browser, ...])`).

## Issues with current documentation
- **No Returns section**, despite the return value being one of the more important and
  non-obvious things about this function: when `open_browser=True` (the effective default),
  `show` returns a live `JSMixer` proxy object (a `serve.JSProxy` subclass) that lets you
  script the running viewer from Python (`_set_view`, `getImage`, `makeMovie`,
  `make_movie_views`, `save_view`, `get_view`, `addData`, and attribute access into
  `view_props`). When `open_browser=False` and `display_url=False`, the function implicitly
  returns `None` (falls through with no `return` statement) — **without a client, there is
  no way to programmatically drive that viewer instance** from the same process, which is a
  significant, undocumented behavioral fork.
- **`layout` type hint is wrong** (`Optional[str]` vs. the documented/actual `None or list
  of (int, int)`).
- **No Raises section.**
- **No Examples section** in the docstring itself (a usage example only appears buried
  inside the *inner* `makeMovie`/`make_movie_views` methods' docstrings, not at the `show`
  level where a first-time user would look).
- **`port` behavior partially undocumented**: "a random port will be selected from the range
  1024-65536" is stated, but not that `show` prints the actual chosen/used port
  (`"Started server on port %d"`) to stdout — useful to know since the caller often doesn't
  set `port` explicitly and needs to discover which one was used.
- **`autoclose`'s "Default True" is misleading.** The docstring says "Default True," but the
  actual default is `None`, which is then resolved from the `[webshow] autoclose` key in
  `options.cfg` (falling back to `'true'` only if that config key itself is absent). If a
  user's local `options.cfg` sets `autoclose = false`, the real default the user experiences
  is `False`, not `True` — the docstring should say "defaults to the `[webshow] autoclose`
  config value (`true` if unset)," not flatly "Default True." Same issue for
  `open_browser` ("Default True" vs. actual default `None` → config-resolved).
- **`**kwargs` forwarding is stated ("passed to the template renderer") but not enumerated**,
  same issue as `make_static`; additionally, `show`'s internal `MixerHandler.get()` already
  passes `data`, `colormaps`, `default_cmap`, `python_interface=True`, `leapmotion=True`,
  `layout`, `subjects`, `viewopts`, `title` to the template — passing any of those names via
  `**kwargs` raises `TypeError: generate() got multiple values for keyword argument ...`,
  exactly as with `make_static`.
- **`pickerfun`'s call signature is described but its interaction with the running server
  is not.** The docstring says pickerfun is "called whenever a location on the surface is
  clicked," but doesn't mention this happens via an HTTP GET request handled inside the
  same Python process (a `PickerHandler` Tornado handler), so `pickerfun` executes
  synchronously on the server's event loop thread when a click happens in the browser — a
  slow `pickerfun` will block the viewer's server. Also undocumented: `PickerHandler`
  returns HTTP 400 (with no call to `pickerfun`) if the click event is missing/malformed
  `voxel`/`vertex`/`hemi` query parameters, so `pickerfun` is not guaranteed to be called on
  every click.
- **Process/thread/server lifecycle is entirely undocumented.** `show` starts a background
  Tornado web server (`server.start()`) inside the current Python process and keeps it
  running (unless `autoclose` closes it once all clients disconnect); the function itself
  returns quickly (non-blocking) rather than blocking for the life of the server. Nothing in
  the docstring states this, which matters for e.g. script vs. notebook usage, or for
  running `show` many times in a loop (each call starts a *new* server on a new port; old
  servers are not automatically stopped).
- **Duplicated wording with `make_static`** for `overlays_available`, `overlays_visible`,
  `labels_visible`, `types`, `overlay_file`, `curvature_*`, `surface_specularity`, `title`
  (see `make_static.md`); worth keeping in sync/de-duplicating if fixed upstream.

## Fixed documentation

### Summary
Creates a webGL MRI viewer that is dynamically served by a tornado server running inside
the current python process. Returns a proxy object that can script the live browser view.

### Parameters
- **data** : Dataset object or implicit Dataset
    Dataset object containing all the data you wish to plot. Can be any type of implicit
    dataset, such as a single Volume, Vertex, etc. object or a dictionary of such objects.
- **autoclose** : bool, optional
    If `True`, the tornado server will automatically be destroyed when the last web client
    has disconnected. If `False`, the server will stay open, allowing more connections.
    `None` (its actual default) resolves to `[webshow] autoclose` in `options.cfg`, itself
    `true` if unset — the docstring's "Default True" wording is only accurate when that
    config key is absent (see Issues).
- **open_browser** : bool, optional
    If `True`, uses the webbrowser library to open the viewer in the default local browser,
    and returns a connected client (see Returns). `None` resolves to `[webshow]
    open_browser` in `options.cfg` the same way as `autoclose`.
- **port** : int or None, optional
    The port that will be used by the server. If `None`, a random port will be selected
    from the range 1024-65536.
- **pickerfun** : function or None, optional
    Should be a function that takes three arguments, a 3-D voxel vector, a vertex index,
    and the hemisphere ("left" or "right"). Is called whenever a location on the surface is
    clicked in the viewer.
- **recache** : bool, optional
    Force recreation of CTM and SVG files for surfaces. Default `False`
- **template** : string, optional
    Name of template HTML file. Default `'mixer.html'`
- **overlays_available**, **overlays_visible**, **labels_visible**, **types**,
  **overlay_file** : optional
    Same as in `cortex.webgl.make_static`.
- **curvature_brightness**, **curvature_contrast**, **curvature_smoothness**,
  **surface_specularity** : float or None, optional
    Same as in `make_static`; `None` uses the value specified in the config file.
- **title** : str, optional
    The title that is displayed on the viewer website when it is loaded in a browser.
- **layout** : None or list of (int, int), optional
    The layout of the viewer subwindows for showing multiple subjects. Default `None`.
    (Signature type hint currently says `str` — believed to be an error, see Issues.)
- **display_url** : bool, optional
    If `True` and `open_browser=False`, display an IPython widget with a URL link to
    access the viewer. Set `False` to suppress this. Default `True`.
- **\*\*kwargs**
    All additional keyword arguments are passed to the template renderer. Same caveats as
    `make_static` — unrecognized kwargs are ignored by the template; a name collision with
    an internally-set variable raises `TypeError`.

### Returns
- If `open_browser` is (effectively) `True`: a **`JSMixer`** instance (a
  `cortex.webgl.serve.JSProxy` subclass) representing a live, connected handle to the
  browser viewer, with `.server` set to the running `WebApp`/Tornado server. Useful public
  methods/attributes on this object include:
  - `view_props` (property) — list of settable view-parameter names (camera, per-subject
    surface, curvature settings).
  - `_set_view(**kwargs)` — set one or more view parameters on the live viewer (low-level).
  - `_capture_view(frame_time=None)` — read back the current view parameters as a `dict`.
  - `getImage(filename, size=(1920, 1080))` — save the currently displayed view to a PNG.
  - `makeMovie(animation, filename="brainmovie%07d.png", offset=0, fps=30,
    size=(1920, 1080), interpolation="linear")` / `make_movie_views(...)` — render a
    sequence of PNG frames interpolating between keyframe view states.
  - `save_view(subject, name, is_overwrite=False)` / `get_view(subject, name)` — persist or
    reload a named camera view to/from the pycortex database (equivalent to
    `cortex.db.save_view`/`cortex.db.get_view`).
  - `addData(**kwargs)` — push additional data (constructed as a `Dataset(**kwargs)`) into
    the already-running viewer without restarting it.
  - Arbitrary attribute access/calls (e.g. `client.ui.set(...)`) proxy through to the
    browser's JavaScript `window.viewer` object via `serve.JSProxy` — see
    `cortex/webgl/serve.py` for the underlying RPC mechanism (out of scope for this file;
    not in the documented function/class list).
- If `open_browser` is `False`: **`None`** (implicit — there is no `return` statement on
  this path). The server is still running in the background; you must navigate to the
  printed/displayed URL manually, and there is no returned handle to script it
  programmatically from this call.

### Raises
- `TypeError` — if a `**kwargs` entry collides with an internally-set template variable
  (see Parameters).
- Any exception from `cortex.utils.get_ctmpack` (missing subject/surfaces) as in
  `make_static`.
- Errors from binding the Tornado server to `port`, if an explicit `port` is already in use
  (propagates from the underlying `tornado`/socket layer — not caught).

### Notes
- **Side effect: starts a background web server** in the current process that keeps running
  after `show` returns (non-blocking call). Repeated calls to `show` each start an
  independent new server on a new (or explicitly given) port; nothing stops previously
  started servers automatically except `autoclose` (which only stops a server once *its own*
  last client disconnects).
- **No FreeSurfer/FSL dependency**, but requires the subject(s) in `data` to already exist in
  the pycortex database with the requested `types` of surfaces, and requires a
  WebGL-capable browser to actually view the result.
- `pickerfun` runs synchronously on the server thread — keep it fast, or offload heavy work
  elsewhere (e.g. queue it) to avoid blocking the viewer's responsiveness.
- Typically used interactively (a script, a notebook, or the Python REPL) rather than inside
  automated pipelines, given it opens a live server and (usually) a browser window.

### Example
```python
import numpy as np
import cortex

subject = "S1"
xfm = "fullhead"
volume_shape = cortex.db.get_xfm(subject, xfm).shape
data = np.random.randn(*volume_shape)
vol = cortex.Volume(data, subject, xfm, vmin=-2, vmax=2, cmap='RdBu_r')

# Opens a browser window and returns a scriptable client handle.
client = cortex.webgl.show(vol, title="Example live viewer")

# Save the current view as a PNG once the browser has connected and rendered:
# client.getImage("current_view.png")

# Headless / no-auto-browser usage (e.g. on a remote server):
# cortex.webgl.show(vol, open_browser=False, display_url=True)
# -> prints/displays a URL to open manually; no client proxy is returned in this mode.
```

## Confidence / open questions
- Could not confirm at runtime that `open_browser=False, display_url=False` truly returns
  `None` with no other side effect beyond starting the server (confirmed only by static
  reading of the `if open_browser: ... elif display_url: ...` branches at
  `view.py:947-957`, which fall through with no final `return` in the `else` case).
- The `layout: Optional[str]` type-hint mismatch is a direct read of the signature vs. the
  docstring/usage; not independently verified against the JS template's actual parsing of
  `layout`.
- The description of `JSMixer`'s public methods is accurate to the source but the full
  `serve.JSProxy` RPC mechanism it relies on (in `cortex/webgl/serve.py`) was not
  independently documented — that module/class is not in the requested scope list.
- **Recommendation for maintainers:** add a proper `Returns` section describing the
  `open_browser=True` vs. `False` fork explicitly (this is the single most consequential
  undocumented behavior found in this function); fix the `layout` type hint; correct the
  `autoclose`/`open_browser` "Default True" wording to reflect the actual config-driven
  default; add at least one runnable example.
