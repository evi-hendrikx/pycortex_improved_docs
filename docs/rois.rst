Surface-defined ROIs
====================

A region of interest is usually defined one of two ways: by thresholding a
statistical map (e.g. "all voxels where this contrast is significant"), or
by hand, based on known anatomical/functional landmarks (e.g. retinotopic
visual field maps, which are identified by finding reversals in the
mapping between visual field position and cortical location). Thresholded
ROIs computed directly in volume space tend to produce noisy, spatially
discontinuous blobs that ignore the anatomy — a few stray significant
voxels here, a gap there — because the statistic doesn't know it's
supposed to respect the folded shape of the cortical sheet. And volumetric
ROIs generally don't give you an easy way to *draw* a boundary by eye based
on a spatial pattern (like a hemifield reversal), which is exactly the kind
of judgment call retinotopic mapping and similar landmark-based ROI
definitions require.

Pycortex instead defines ROIs as closed paths drawn directly on a
subject's flattened cortical surface, saved as layers in an
``overlays.svg`` file and edited with Inkscape (or, interactively in the
browser, with `pycortex-roidraw <https://github.com/gallantlab/pycortex-roidraw>`_
— see :doc:`roidraw`). Drawing on the flatmap means you're always looking
at the whole cortex at once with no folds hiding parts of the boundary you
care about, and a hand-drawn boundary respects anatomical continuity in a
way an automatic threshold can't. Because the SVG lives on the subject
(not on a particular functional dataset or transform), one ROI drawing
applies to any dataset for that subject — see :ref:`Overlays
<database-overlays>` in :doc:`database` for how these ROI SVGs sit alongside
the rest of a subject's stored data. From the drawn outline, pycortex can
derive both a volumetric mask (for restricting analyses to voxels inside
an ROI) and a set of surface vertex indices (for surface-based analyses),
so the same hand-drawn boundary works for either representation.

Where ROIs are stored
---------------------

Each subject has one ``overlays.svg``, drawn on top of the flatmap. Its
layers (Inkscape layers, i.e. SVG groups) are:

* ``rois``: a ``shapes`` sub-layer with one sub-layer per ROI, named after
  the ROI and holding its closed path(s), and a ``labels`` sub-layer.
* ``sulci``: the same structure, for sulci.
* ``cutouts``: regions for :doc:`clipping a flatmap <quickflat>`.
* ``data``: flatmap images of your data, added with ``cortex.add_roi`` as a
  guide for drawing.

Importing a new flatmap deletes ``overlays.svg`` (see :doc:`flattening`),
since the ROIs are drawn in flatmap coordinates; keep a copy of it before
you re-flatten.


Drawing ROIs in Inkscape
------------------------

Show the data you want to draw from on the flatmap, and open it in
`Inkscape <https://inkscape.org/>`_::

    import cortex

    # contrast: a (z, y, x) array, e.g. a localizer t map
    volume = cortex.Volume(contrast, "S1", "fullhead", vmin=-5, vmax=5)
    cortex.add_roi(volume, name="FFA")

``add_roi`` renders ``volume`` as a flatmap image, adds it to the ``data``
layer (hiding the images added before), creates an empty ``FFA`` sub-layer
under ``rois`` > ``shapes``, and opens ``overlays.svg`` in Inkscape. Select
the ``FFA`` layer, draw a closed path around the region, then save the file
and close Inkscape.

Call ``add_roi`` again for each contrast or ROI. ``add_path=False`` adds
only the image, without a new ROI sub-layer; ``open_inkscape=False`` adds
it without opening Inkscape.

To draw ROIs and sulci in the WebGL viewer instead, without Inkscape, see
:doc:`roidraw`.


Using ROIs
----------

**On the flatmap and in the viewer.** :doc:`Static flatmaps <quickflat>`
show ROI outlines and labels by default (``with_rois``, ``with_labels``;
``roi_list`` picks a subset), and so does the :doc:`WebGL viewer
<userguide/webgl>` (``overlays_visible``, ``labels_visible``).

**As vertices.** :func:`cortex.get_roi_verts` returns the vertex indices
inside each ROI, numbered across both hemispheres (left first)::

    verts = cortex.get_roi_verts("S1", ["FFA", "V1"])   # {"FFA": array([...]), ...}
    masks = cortex.get_roi_verts("S1", "FFA", mask=True)  # boolean, one per vertex

See :ref:`sphx_glr_auto_examples_utils_plot_get_roi_vertices.py`.

**As voxels.** :func:`cortex.get_roi_masks` returns a ``(z, y, x)`` mask per
ROI for a transform::

    masks = cortex.get_roi_masks("S1", "fullhead", roi_list=["FFA"])

``gm_sampler`` sets which voxels count as gray matter: ``'cortical'``
(default, voxel centers inside the cortical ribbon), ``'thin'`` or
``'thick'`` (the :doc:`masks <masks>` of those names), or a number, the
distance from the fiducial surface (1-3 is reasonable). ``'cortical-liberal'`` and
``'cortical-conservative'`` are mapper-based and give the fraction of each
voxel inside the ROI (0-1) unless you pass a ``threshold``.
``return_dict=False`` returns a single volume with one integer index per
ROI instead. See :ref:`sphx_glr_auto_examples_utils_plot_roi_voxel_mask.py`
and :ref:`sphx_glr_auto_examples_utils_plot_roi_voxel_index_volume.py`.
