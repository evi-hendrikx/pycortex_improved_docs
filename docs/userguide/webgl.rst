WebGL Viewer
============

The WebGL viewer shows data on a subject's cortical surface in a web
browser. You can drag a slider to unfold the brain from folded to inflated
to flat, which builds a sense of how the flatmap corresponds to the folded
cortex. In the viewer you can:

- adjust camera angle and zoom in real time
- toggle display of ROIs and various labels
- switch between multiple datasets
- flatten and inflate cortical surface
- play back time-series data
- create scripted animations
- select points by clicking on them
- switch between colormaps

.. seealso::

   You can draw, edit, and export ROIs directly in the WebGL viewer with the
   :doc:`pycortex-roidraw </roidraw>` add-on.


Opening a viewer
----------------

There are two kinds of viewer. A **dynamic viewer**, from
:func:`cortex.webgl.show` (alias ``cortex.webshow``), is served by your
Python process and lasts as long as it does::

    import cortex

    volume = cortex.Volume.random("S1", "fullhead")
    viewer = cortex.webshow(volume)

A **static viewer**, from :func:`cortex.webgl.make_static`, is a directory
with an ``index.html`` and the data, which you can keep, share or put on a
website::

    cortex.webgl.make_static("my_viewer", volume)

Open it through a web server, not by double-clicking ``index.html`` (the
browser refuses to load the data from ``file://`` paths). Locally,
``python -m http.server`` in that directory is enough.

Both take any :doc:`dataview </dataset>`, or a dict of named dataviews to
switch between in the viewer (with **+**/**-**). A 4D ``Volume`` or 2D
``Vertex`` is played back as a movie. Useful options:

* ``overlays_visible`` / ``labels_visible``: which overlay layers (``'rois'``,
  ``'sulci'``, …) and labels are shown at the start.
* ``types``: extra surface types to include, ``('inflated',)`` by default.
* ``recache=True``: rebuild the compressed surfaces, e.g. after changing a
  subject's surfaces or ``overlays.svg``.
* ``show`` only: ``open_browser``, ``port``, ``autoclose``, and
  ``pickerfun``, a function called with the voxel, vertex and hemisphere
  of every point you click.
* ``make_static`` only: ``anonymize=True`` renames the subject's files for
  public sharing; ``html_embed`` inlines the scripts into ``index.html``.

See :ref:`sphx_glr_auto_examples_webgl_single_dataset.py`,
:ref:`sphx_glr_auto_examples_webgl_multiple_datasets.py` and
:ref:`sphx_glr_auto_examples_webgl_static.py`.


Controlling the viewer from Python
----------------------------------

``cortex.webshow`` returns a handle to the open browser tab::

    viewer = cortex.webshow(volume)
    viewer.getImage("brain.png", size=(1920, 1080))  # screenshot
    viewer.addData(other=other_volume)                # push more data
    viewer.save_view("S1", "my_view")                 # save the camera view
    viewer.get_view("S1", "my_view")                  # and restore it

``viewer.makeMovie`` renders an animation between keyframes to PNG frames.
See :doc:`/features/camera_views_animations` for saved views and
animations.

To render images in a script without opening a browser, use
:func:`cortex.export.save_3d_views` or :func:`cortex.export.plot_panels`
with ``headless=True`` (needs Playwright); see
:ref:`sphx_glr_auto_examples_webgl_plot_panels_headless.py`.


Using the viewer
----------------

The viewer is driven with the keyboard, the mouse and the control panel.


Keyboard Shortcuts
^^^^^^^^^^^^^^^^^^

There are many keyboard shortcuts that allow for more fluid interaction with the WebGL viewer. A complete list of keyboard shortcuts can also be displayed in the viewer by pressing the **h** key.

=============   ====================================
Key             Action
=============   ====================================
f               flatten brain
i 	            inflate brain
k 	            inflate brain to surface cuts
r               fold brain into original coordinates (without moving camera)
t               reset entire view (fold brain, reset camera position, rotation, and zoom)
shift + wheel   change inflation level
p               show pial surface
u               show fiducial surface
y               show white matter surface
l               toggle labels
h               toggle keyboard shortcut overview
+/-	            switch between datasets
e               toggle X slice
d               toggle Y slice
c               toggle Z slice
q/w             switch between X slices
a/s             switch between Y slices
z/x             switch between Z slices
o               toggle data opacity
m               toggle multiple layers
alt + wheel     change cortical depth
shift + l       toggle left hemisphere
shift + r       toggle right hemisphere
shift + s       save current view as png
=============   ====================================


Mouse and Trackpad Controls
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The camera is driven directly from the 3D view.

============================   ====================================
Action                         Effect
============================   ====================================
left-click and drag            rotate the brain (pan, when flattened)
shift or middle-click + drag   pan the view
ctrl or right-click + drag     zoom in and out
scroll wheel                   zoom in and out
pinch                          zoom in and out
============================   ====================================

Pinch-to-zoom works both on laptop trackpads and on touchscreens, and zooms the
brain rather than the surrounding web page.

View Controls
^^^^^^^^^^^^^

The **Open Controls** button in the upper right corner opens a control panel for many different display options.

Camera Controls
***************

======== =====================================================
name     description
======== =====================================================
azimuth  camera rotation within the xy plane
altitude angle above the xy plane
radius   zoom level
fold     fold brain into original coordinates
reset    reset entire view (position, rotation, zoom, fold)
inflate  inflate cortical surface
flatten  flatten cortical surface
======== =====================================================


Surface Controls
****************

=================== ==================================
name                description
=================== ==================================
unfold              level of unfolding
pivot               angle between hemispheres
shift               distance between hemispheres
depth               cortical depth
bumpy_flatmap       give the flatmap relief, see below
bumpy_flatmap_scale how much to exaggerate that relief
left                toggle left hemisphere
right               toggle right hemisphere
=================== ==================================


Lighting Controls
*****************

These live in the ``lighting`` sub-menu of the surface controls.

==================== ==========================================================
name                 description
==================== ==========================================================
topleft_lighting     crossfade from the default headlight (0) to a light from
                     the upper left (1)
uniform_illumination how flat and shadowless the illumination is, 0 to 1
specularity          specular reflection level
==================== ==========================================================

See :doc:`/features/bumpy_flatmap` for how unfolding drives these,
and for the ``bumpy_flatmap`` relief.


Overlay Controls
****************

======= ===================
name 	description
======= ===================
visible toggle roi outlines
labels  toggle roi labels
======= ===================


For how the viewer renders data with :term:`pixel-wise sampling`, and the
design behind it, see the :ref:`pycortex paper <citation>`.
