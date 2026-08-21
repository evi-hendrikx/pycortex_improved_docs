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
<database-masks>` in :doc:`database` for how these ROI SVGs sit alongside
the rest of a subject's stored data. From the drawn outline, pycortex can
derive both a volumetric mask (for restricting analyses to voxels inside
an ROI) and a set of surface vertex indices (for surface-based analyses),
so the same hand-drawn boundary works for either representation.

Using ROIs
----------

pycortex supports a method of defining surface ROIs using Inkscape. The ROIs are rendered as surface textures in the viewers, and roi masks can be extracted using helper functions.

For the vertex-index side, see
:ref:`sphx_glr_auto_examples_utils_plot_get_roi_vertices.py`. For the
volumetric-mask side, see
:ref:`sphx_glr_auto_examples_utils_plot_roi_voxel_mask.py` (a
probabilistic mask, values 0-1) and
:ref:`sphx_glr_auto_examples_utils_plot_roi_voxel_index_volume.py` (which
voxels fall in which ROI).

.. seealso::

   To draw ROIs and sulci interactively in the WebGL viewer (without Inkscape), see
   :doc:`In-browser ROI and sulcus drawing <roidraw>`.
