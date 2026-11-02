Setting up a subject
====================

Pycortex needs a triangular mesh of each subject's cortical surface before
it can put any functional data on a flatmap or in the WebGL viewer — see
:doc:`overview` for how this surface fits into the rest of the pipeline.
That mesh has to come from somewhere: it's derived from a segmentation of
the subject's own anatomical MRI, identifying the boundary between white
matter and gray matter, and between gray matter and dura/CSF.

This is done per-subject, not with a generic template (e.g. ``fsaverage``),
because individual cortical folding patterns vary substantially between
people; averaging surfaces across subjects would blur exactly the
fine-grained spatial detail pixel-wise sampling (:doc:`overview`) is
designed to preserve. The undistorted mesh reconstructed at this boundary
is called the :term:`fiducial surface`, and every other surface pycortex
uses (:term:`inflated <inflated surface>`, :term:`flat <flat surface /
flatmap>`) is a deformation of it that must keep the same vertex count and
correspondence, since that's what lets data plotted on one surface line up
with the same data on another.

If you already have surfaces from FreeSurfer, fMRIPrep, HCP or another
tool, start at :doc:`importing_other_software`. Building a subject from
scratch has these phases:

**1. Segmentation**

FreeSurfer will automatically discern where white matter and gray matter are in the brain. The software is good but not perfect, so you will need to look through its results and fine-tune the surfaces it generates so we can generate a 3D model of the brain. See :doc:`segmentation_guide`.

Once the segmentation is done, import the subject into pycortex with ``cortex.freesurfer.import_subj``. See :ref:`database-freesurfer-import`.


**2. Cutting and flattening**

The surface is cut open and flattened, either automatically or by hand in Blender. See :doc:`flattening`.


**3. Aligning functional data**

Compute a transform from each functional scan to the anatomy with :doc:`align`. See :doc:`transforms` for what a transform stores and :doc:`masks` for selecting the voxels near the cortex.


**4. Labeling ROIs**

Here you will project functional data (semantic betas or localizer data, as well as retinotopic) onto the flatmaps, allowing you to label Regions of Interest on the brain - areas responsive to faces, scenes, or whatever else we're analyzing. See :doc:`rois`.
