Static flatmaps
===============

``cortex.quickflat`` draws data on a subject's flatmap with matplotlib, for
figures and image files. It uses the same :term:`pixel-wise sampling` as
the :doc:`WebGL viewer <webgl>`, and needs the subject to have a
``flat`` surface (see :doc:`flattening`).


Making a figure
---------------

``cortex.quickshow`` is an alias for :func:`cortex.quickflat.make_figure`::

    import cortex
    import matplotlib.pyplot as plt

    volume = cortex.Volume.random("S1", "fullhead")
    fig = cortex.quickshow(volume, with_curvature=True)
    plt.show()

It takes any :doc:`dataview <dataset>` (``Volume``, ``Vertex``, their 2D
and RGB versions, or a ``(data, subject, xfmname)`` tuple) and returns a
matplotlib ``Figure``. The colormap and its range come from the dataview's
``cmap``, ``vmin`` and ``vmax``. Pass ``fig=`` an existing figure or axes
to draw into it, e.g. to combine several flatmaps in one figure.

See :ref:`sphx_glr_auto_examples_quickflat_plot_make_figure.py`.


Layers
------

The flatmap is built from image layers drawn on top of each other. Each is
switched on with a keyword argument:

.. list-table::
   :header-rows: 1
   :widths: 30 12 58

   * - Keyword
     - Default
     - Layer
   * - ``with_curvature``
     - ``False``
     - Gray curvature shading behind the data. Style with
       ``curvature_brightness``, ``curvature_contrast`` and
       ``curvature_threshold`` (defaults in the ``[curvature]`` section of
       ``options.cfg``).
   * - ``with_rois``
     - ``True``
     - ROI outlines from the subject's ``overlays.svg`` (see :doc:`rois`).
       ``roi_list`` selects which ones.
   * - ``with_sulci``
     - ``False``
     - Sulcus outlines from ``overlays.svg``. ``sulci_list`` selects which
       ones.
   * - ``with_labels``
     - ``True``
     - Labels on the ROIs and sulci.
   * - ``with_colorbar``
     - ``True``
     - A colorbar, or a 2D colormap square for 2D dataviews. Place it with
       ``colorbar_location`` (``'left'``, ``'center'``, ``'right'`` or a
       ``(left, bottom, width, height)`` tuple).
   * - ``with_dropout``
     - ``False``
     - Crosshatching over regions with low EPI signal, estimated from the
       transform's reference image (``True``, or a number for the exponent
       of :func:`cortex.utils.get_dropout`). ``extra_hatch`` adds a hatch
       layer from your own data.
   * - ``cutout``
     - ``None``
     - Clip the flatmap to one region, a sub-layer of the ``cutouts`` layer
       in ``overlays.svg``.

ROI and sulcus lines and labels are styled with ``linewidth``,
``linecolor``, ``roifill``, ``shadow``, ``labelsize`` and ``labelcolor``;
their defaults are in the ``[rois_paths]``, ``[rois_labels]``,
``[sulci_paths]`` and ``[sulci_labels]`` sections of ``options.cfg``.

The ROI, sulcus and cutout layers are rendered from ``overlays.svg`` with
`Inkscape <https://inkscape.org/>`_. Without Inkscape installed, pass
``with_rois=False`` (see :doc:`install`).

For full control, turn layers off in ``make_figure`` and add them yourself
with the functions in ``cortex.quickflat.composite`` (``add_rois``,
``add_sulci``, ``add_curvature``, ``add_hatch``, ``add_colorbar``, …),
each with its own styling options.

See the examples for
:ref:`ROIs <sphx_glr_auto_examples_quickflat_plot_rois.py>`,
:ref:`sulci <sphx_glr_auto_examples_quickflat_plot_sulci.py>`,
:ref:`dropout <sphx_glr_auto_examples_quickflat_plot_dropout.py>`,
:ref:`cutouts <sphx_glr_auto_examples_quickflat_plot_cutouts.py>`,
:ref:`zooming to one ROI <sphx_glr_auto_examples_quickflat_plot_zoom_to_roi.py>`
and :ref:`advanced compositing
<sphx_glr_auto_examples_quickflat_plot_advanced_compositing.py>`.


Saving to a file
----------------

* :func:`cortex.quickflat.make_png` saves the figure as a PNG. It takes
  the same keywords as ``make_figure``, plus ``bgcolor`` (transparent by
  default). See :ref:`sphx_glr_auto_examples_quickflat_plot_make_png.py`.
* :func:`cortex.quickflat.make_svg` saves an SVG with the data (and
  curvature) as an embedded image and the ROIs as editable vector paths,
  for finishing a figure in a vector editor. See
  :ref:`sphx_glr_auto_examples_quickflat_plot_make_svg.py`.
* :func:`cortex.quickflat.make_gif` makes an animated GIF with one flatmap
  per frame, e.g. to flip between two maps. See
  :ref:`sphx_glr_auto_examples_quickflat_plot_make_gif.py`.

::

    cortex.quickflat.make_png("flatmap.png", volume, with_curvature=True)
    cortex.quickflat.make_svg("flatmap.svg", volume)


Resolution and sampling
-----------------------

``height`` sets the image height in pixels (default 1024); the width
follows from the flatmap's aspect ratio.

For volume data, each pixel samples the volume at ``thick`` points (default
32) between the white matter and pial surfaces and averages them; with
``thick=1`` it samples once, at ``depth`` (0 = white matter, 1 = pial,
default 0.5). ``sampler`` sets how the volume is interpolated
(``'nearest'`` by default, or e.g. ``'trilinear'``). NaN values are left
out of the average unless ``nanmean=False``; see
:ref:`sphx_glr_auto_examples_quickflat_plot_thickness_nanmean.py`.


Caching
-------

The first flatmap for a subject, transform, height and sampler is slow:
pycortex computes which voxels each pixel samples and saves that in the
subject's cache. Later flatmaps with the same settings reuse it.

This cache is **not** updated when a transform changes. After re-aligning a
transform under the same name, pass ``recache=True`` once (or clear the
cache with ``cortex.db.clear_cache(subject)``); otherwise the flatmap still
samples the old alignment.
