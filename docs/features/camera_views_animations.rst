Camera views and animations
===========================

The WebGL viewer's camera views and animation panel. Views are stored in the
subject's ``views`` directory; see :doc:`/database`.


Default views
~~~~~~~~~~~~~

Every subject is offered a standard set of views whether or not anything has been saved for it, so a freshly imported subject already has the usual orientations one click away under **camera > views**:

=========================  ====================================================
View                       Shows
=========================  ====================================================
``dorsal``                 From above, frontal lobe towards the top of the
                           image, the subject's right on the right.
``ventral``                From below, frontal lobe towards the top.
``lateral_left``           From the left, brain upright.
``lateral_right``          From the right, brain upright.
``*_inflated``             The same four angles on the inflated surface.
``flat``                   The flattened surface. Omitted for a subject with
                           no flat surface, which also puts the ``_inflated``
                           views at full inflation rather than half.
=========================  ====================================================

They are built from the same tables ``cortex.export.save_views`` uses for :func:`save_3d_views`, and can be inspected from python::

    from cortex.export.save_views import default_subject_views
    default_subject_views()["dorsal"]

Each view but ``flat`` also fixes the camera's aim and distance, so clicking it returns exactly the same scene every time, ready to render the same images again. The camera aims at the middle of the surface the view shows, from the distance at which that brain fills 85% of a 4:3 frame (``FRAMING_FILL`` and ``FRAMING_ASPECT`` in ``cortex.export.save_views``); in a wider window there is simply more room either side. Brains differ in size, and an inflated surface in shape, so this is fitted to each subject's own surfaces — as the viewer lays them out — the first time a viewer opens that subject, and cached as ``default_view_framing.json`` in its cache directory; the cache is refitted when a surface file changes. Pass the subject to see the framed views::

    default_subject_views(subject="S1")["dorsal"]

**A view saved in the filestore under one of these names replaces the default.** So if a subject's anatomy wants a different angle, or you prefer a different framing, save your own view under that name and it is used instead — for that subject only, leaving every other default in place::

    viewer.save_view(subject, "dorsal", is_overwrite=True)

The ``flat`` view uses the viewer's standard flatmap preset. It names no camera angle, because a flattened surface ignores one: the controls hold the camera square-on to the flatmap and discard whatever azimuth and altitude they are given (unless the surface's ``allow_tilt`` is on). Leaving them out is what keeps an animation from spinning the brain as it flattens, and from overwriting the folded angle it returns to when it unfolds again. A flat view or keyframe captured in the viewer leaves them out for the same reason.

It carries no zoom of its own either. Clicking it in the browser frames the flatmap the way ``quickflat`` frames the image it writes — the camera looks at the middle of the flatmap from the distance at which the field of view spans it — so that rendered at the pixel size quickflat uses, the frame is the png ``cortex.quickflat.make_png`` writes, same position and same scale. (The perspective camera is no obstacle: a plane square-on to it projects as a uniform scaling, which is all quickflat's mapping of the flat surface onto the bounds of the image amounts to.)

That framing is applied on request, never behind your back. Setting the flat view from python with ``_set_view`` leaves the camera where it is, so :func:`cortex.export.save_3d_views` and anything else driving the viewer render exactly as they always did; ask for it with ``handle.fit_flat_view()``, and ``getImage`` then re-frames it for the image it is about to write, whatever the shape of the window. In the animation panel, tick **match quickflat size** in the render form: the size fields are filled with the subject's quickflat size and flat keyframes are framed for it, including any already laid down. Type another size over it and flat keyframes are framed for that one instead.

A view saved in the filestore under the name ``flat`` replaces all of this, framing included, since a saved view records the camera distance it was saved with.

The camera keeps two targets — the point it orbits and looks at — one for the folded brain and one for the flatmap, and moves between them as the surface unfolds. Views store them separately, as ``camera.target`` (folded) and ``camera.flat_target``, so an animation from a folded pose into the flat view leaves the folded target where it was, and unfolding again returns the brain exactly to its starting place. The flat target starts at the middle of the flatmap, so flattening lands centred without the flat view naming one. A flat view saved before ``camera.flat_target`` existed stores its flat target as ``camera.target``, and is still read that way: a flat view that carries ``camera.target`` but no ``camera.flat_target`` sets the flat target.

Saved views in the browser
~~~~~~~~~~~~~~~~~~~~~~~~~~

Every view stored for the subject(s) a viewer displays is loaded when the viewer starts, and appears as a button under **camera > views** in the browser controls. Clicking one applies it. This works in static viewers made with ``cortex.webgl.make_static`` as well.

The **save view** button in the same menu captures the current view under a name you choose. These stay in the browser rather than being written to the filestore, so that you can experiment freely; retrieve them from python with::

    new_views = viewer.retrieve_new_views()

which returns a dict mapping each name to a dict of view parameters, in the same format as ``viewer._capture_view()``. To keep them, write them into the subject's ``views`` directory::

    viewer.save_new_views()

This returns a dict mapping each name to the file it was written to. Pass ``subject`` to store them under a subject other than the first one displayed, ``names`` to save only some of them, and ``is_overwrite=True`` to replace views already stored under the same name. A view that has been stored is no longer "new": it moves into the **camera > views** menu of the running viewer and stops being returned by ``retrieve_new_views``, so calling ``save_new_views`` twice will not rewrite the same files.

Animations
~~~~~~~~~~

The **create animation** button opens a panel for building an animation out of keyframes. Set the current frame with the slider (frames that already hold a keyframe are marked with a yellow dot), pose the brain, and press **add keyframe**; the values in between are interpolated. **play animation** previews the result at the chosen frame rate, and **render animation** writes one PNG per frame.

Smoothing
^^^^^^^^^

The **smoothing** dropdown sets how the curve through the keyframes is shaped. Each keyframe carries its own setting, which describes both how the animation arrives at it and how it leaves, so the motion between two keyframes depends on the pair at either end. The dropdown always shows the setting of the keyframe under the playhead; when there is no keyframe there it shows the one new keyframes will be given.

Eight options are available:

=========================  ====================================================
Option                     Behaviour
=========================  ====================================================
bezier (smooth)            Default. A cubic Bezier with automatically placed
                           control points. Velocity carries smoothly through
                           the keyframe and the brain never swings past the
                           pose you set.
cubic hermite (smooth)     As above, using the tangents directly rather than
                           control points. Very nearly the same curve.
linear                     Straight lines between keyframes, which is what the
                           panel did before smoothing was added. The motion
                           changes direction abruptly at each keyframe.
bezier in, hold            Arrive smoothly, then freeze on this pose until the
                           next keyframe.
hermite in, hold           As above, arriving along a Hermite tangent.
linear in, hold            Arrive in a straight line, then freeze.
linear in, bezier out      Arrive in a straight line and leave along it, easing
                           out with a Bezier. May swing past the next pose.
linear in, hermite out     As above with a Hermite. May swing past the next
                           pose.
=========================  ====================================================

The two "smooth" options and the three holds stay within the poses you set. The two "linear in" options carry the incoming speed out of the keyframe and so can overshoot, which is useful for a sense of momentum and unhelpful if you need the camera to stop exactly where you put it.

The same eight modes are available when rendering from python, either for a whole animation::

    viewer.make_movie_views(animation, interpolation="Bezier")

or per keyframe, by giving a keyframe its own ``interpolation`` key — which is what the panel does. The browser and ``cortex.webgl.interpolation`` share their arithmetic, so a movie rendered from python matches the preview played in the viewer. The older whole-animation easings ``"linear"``, ``"smoothstep"`` and ``"smootherstep"`` still work, but ease each pair of keyframes separately and cannot be combined with per-keyframe modes.

**render animation** builds the movie in the browser and downloads it as one file, the way **Save image** does — so it lands on the computer running the browser, wherever that browser saves downloads, and the server writes nothing. It works in static viewers made with :func:`cortex.webgl.make_static` too. Choose the format in the render form:

* **PNG frames (.zip)** — one lossless PNG per frame, transparent outside the brain, named after the animation's frame numbers inside a folder named after the movie (``brainmovie/brainmovie_00000.png``, …). These are the frames to use when they must match a flatmap from ``cortex.quickflat.make_png``. A zip holds at most 65,535 frames and 4 GiB; render a shorter range of frames if a movie is larger than that.
* **MP4 video** — H.264, encoded by the browser itself (WebCodecs). It is lossy and has no transparency, so frames are laid on black, as the viewer shows them. Browsers only offer video encoding in a secure context — a viewer opened on ``localhost``, over ``https``, or from a local file — so the option is unavailable when a viewer is reached over plain http from another machine. The largest size depends on the browser's encoder, and a size it cannot encode is refused before rendering starts; an odd width or height gets one extra row or column of black, since H.264 needs even dimensions.
