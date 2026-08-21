Glossary
========

Short definitions of terms used throughout the pycortex docs without
re-explaining them every time. If you're new to pycortex, read
:doc:`overview` first — it introduces most of these in context. Each entry
below links to the page that explains it in full.

.. glossary::

    subject
        A unique identifier (a string, e.g. ``"S1"``) for one person/brain in
        the pycortex :term:`filestore`. Every surface, transform, mask, and
        overlay in the database is filed under a subject name. See
        :doc:`database`.

    filestore
        The directory tree pycortex uses to store everything it knows about
        every subject — surfaces, transforms, caches, masks, overlays.
        Pycortex keeps its own filestore rather than reading a FreeSurfer
        ``SUBJECTS_DIR`` directly, because it needs several derived,
        pycortex-specific artifacts (flattened surfaces, caches, ROI
        overlays, masks) alongside the anatomical surfaces, and those don't
        belong inside FreeSurfer's own directory layout. See :doc:`database`.

    fiducial surface
        The triangular mesh representing the boundary halfway between white
        and gray matter, reconstructed from a segmented anatomical scan
        (traditionally via `marching cubes
        <https://en.wikipedia.org/wiki/Marching_cubes>`_ on the segmentation,
        though pycortex's current pipeline gets it from FreeSurfer's own
        surface reconstruction). It's the "ground truth" undistorted
        geometry that every other surface (inflated, flat) is derived from
        and must share a vertex count with. See :doc:`segmentation_guide`.

    inflated surface
        The fiducial surface with sulci and gyri smoothed out into a
        rounder shape, so that activity buried in folds becomes visible
        without cutting the surface. See :doc:`overview`.

    flat surface / flatmap
        The fiducial surface cut along a small number of anatomical seams
        and mathematically relaxed until it lies flat in 2D, so the entire
        cortex can be viewed at once with minimal size distortion. "Flatmap"
        also refers to the rendered image or view of data on this surface
        (e.g. what :func:`cortex.quickflat.make_figure` produces). See
        :doc:`segmentation_guide`.

    xfm / transform
        The affine matrix that maps coordinates from a subject's fiducial
        surface space into the voxel space of one particular functional
        (EPI) scan. A subject can have several transforms (one per
        functional session/geometry, identified by :term:`xfmname`), because
        a new functional scan is rarely acquired in exactly the same
        position as the last one. See :doc:`transforms` and :doc:`align`.

    xfmname
        The name identifying one particular :term:`xfm <xfm / transform>` for a subject (e.g.
        ``"fullhead"``), distinct from the subject name itself. Passed
        alongside ``subject`` to most pycortex functions that need to know
        which functional geometry the data lives in.

    mask
        A boolean array selecting which voxels of a functional volume count
        as "cortex" for a given subject/transform pair, used to reduce a
        full 3D/4D functional volume down to the much smaller set of voxels
        near the cortical surface. See :ref:`the Masks section <database-masks>` of :doc:`database`.

    pixel-wise sampling
        Pycortex's method of mapping functional volume data onto the
        screen: instead of the more traditional two-step process (sample
        the volume at each mesh *vertex*, then interpolate between vertices
        to fill in screen pixels), pycortex samples directly from the
        volume into each output pixel in a single pass. This avoids
        compounding interpolation error and produces much higher-fidelity
        images, especially for densely-sampled or high-resolution
        functional data (Gao et al., 2015 — see :doc:`overview`).

    CTM
        `OpenCTM <http://openctm.sourceforge.net/>`_, a compressed
        triangle-mesh file format. Pycortex caches surface geometry as CTM
        files (a "ctmpack": geometry + JSON limits + SVG overlay) so the
        WebGL viewer can load large meshes quickly in the browser. See
        :doc:`database`.

    Volume
        A :class:`cortex.Volume` object: functional data still indexed in
        3D/4D voxel space, paired with a subject, an :term:`xfmname`,
        and colormap settings. Use a ``Volume`` when your data lives on a
        voxel grid (the common case for raw or lightly-processed fMRI
        data).

    Vertex
        A :class:`cortex.Vertex` object: functional data already indexed
        per-vertex on the cortical surface mesh rather than per-voxel. Use
        a ``Vertex`` when your data was computed on the surface already
        (e.g. after `cortex.db.get_surf` mapping, or surface-based
        analyses), skipping the volume-to-surface sampling step entirely.

    Dataset
        A :class:`cortex.Dataset`: a named collection of ``Volume``/
        ``Vertex`` objects (and their 2D/RGB variants) bundled together and
        saved to a single ``.hdf`` file, so a full set of results can be
        loaded and shared as one object.

    ROI overlay
        A named region of interest, drawn as a closed path in an
        ``overlays.svg`` file (edited in Inkscape, or interactively in the
        browser via `pycortex-roidraw
        <https://github.com/gallantlab/pycortex-roidraw>`_) and stored per
        subject rather than per functional dataset. See :doc:`rois`.

    dropout
        Loss of EPI (functional) signal in a region, typically near air/
        tissue boundaries (e.g. orbitofrontal cortex, temporal poles). See
        :func:`cortex.utils.get_dropout`, which builds a ``Volume``
        highlighting these low-signal regions so they can be flagged on a
        flatmap rather than mistaken for a real absence of activity.
