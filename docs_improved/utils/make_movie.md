# cortex.utils.make_movie

## Current signature (from source)
```python
def make_movie(stim, outfile, fps=15, size="640x480"):
```
Note: not to be confused with `cortex.quickflat.view.make_movie` (an unrelated, unfinished
function that `raise NotImplementedError`s immediately — see `_notes.md`) or
`cortex.webgl.view.JSMixer.makeMovie`/`.make_movie_views` (WebGL viewer camera-animation
recorders — see `webgl/show.md`). Three same/similar-named, functionally unrelated
"make movie" functions exist across pycortex.

## Where this is documented today
- Source docstring: [cortex/utils.py:919-939](cortex/utils.py#L919-L939) — `stim`,
  `outfile` have no descriptions; `Returns` section present but empty.
- Online API page: https://gallantlab.org/pycortex/generated/cortex.utils.make_movie.html

## Issues with current documentation
- **`stim` and `outfile` parameters have no description text at all** in the `Parameters`
  section.
- **`Returns` section header is present but empty** — the function returns `None` always.
- **No Raises section** — `subprocess.call`'s return code is not checked; a failed
  `ffmpeg` call fails silently (no exception, no output file, no error message).
- **`outfile`'s extension handling is a gotcha**: the actual output filename is
  `"{outfile}.ogv"` — an `.ogv` suffix is always appended, even if `outfile` already ends
  in `.ogv` or another extension (producing e.g. `movie.mp4.ogv` if you pass
  `outfile="movie.mp4"`). Not documented.
- **Name collision with two other, unrelated "make movie" functions** in pycortex (see
  the note at the top of this file) — not cross-referenced anywhere.

## Fixed documentation

### Summary
Makes an .ogv movie. A simple wrapper for ffmpeg. Calls:
`"ffmpeg -r {fps} -i {infile} -b 4800k -g 30 -s {size} -vcodec libtheora {outfile}.ogv"`

### Parameters
- **stim** : str
    Path to the input image sequence or video (passed as ffmpeg's `-i` argument, e.g. a
    printf-style pattern like `frame%04d.png` for an image sequence).
- **outfile** : str
    Base output path (without extension) — the actual output file will be
    `"{outfile}.ogv"` (an `.ogv` suffix is always appended, even if `outfile` already has
    an extension).
- **fps** : float
    refresh rate of the stimulus
- **size** : str
    resolution of the movie out

### Returns
`None`. Writes `"{outfile}.ogv"` as a side effect (if `ffmpeg` succeeds — see Raises).

### Raises
No explicit exceptions — `subprocess.call`'s return code is not checked, so a failed
`ffmpeg` invocation (e.g. `ffmpeg` not installed, invalid `stim` path) fails silently with
no output file and no error.

### Notes
- **Requires `ffmpeg`** on `PATH`, with `libtheora` codec support.
- Output filename always gets `.ogv` appended to `outfile` verbatim — pre-strip any
  extension from `outfile` yourself if you want a clean result.
- Not to be confused with `cortex.quickflat.view.make_movie` (unimplemented,
  `NotImplementedError`) or the `JSMixer.makeMovie`/`.make_movie_views` methods returned
  by `cortex.webgl.show` (WebGL camera-animation recorders) — three differently-scoped
  "make movie" functions exist in pycortex.

### Example
```python
import cortex

cortex.utils.make_movie("frames/frame%04d.png", "output_movie", fps=30, size="1280x720")
# Writes: output_movie.ogv
```

## Confidence / open questions
- Did not run `ffmpeg` in this pass.
- **Recommendation for maintainers:** fill in `stim`/`outfile` descriptions and the empty
  `Returns` section; check `subprocess.call`'s return code; consider using
  `os.path.splitext` to avoid double extensions; disambiguate the name collision with the
  other two "make movie" functions.
