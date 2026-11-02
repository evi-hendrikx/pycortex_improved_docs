Importing from other software
=============================

Every route into pycortex ends at the same place: a subject in the
:doc:`filestore <database>` with surfaces and at least one transform (see
:ref:`minimal-filestore-contents`). This page covers how to get there from
the software you used to build the surfaces.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - You have...
     - Start at...
   * - A FreeSurfer subject (``recon-all``)
     - :ref:`import-freesurfer`
   * - fMRIPrep output
     - :ref:`import-fmriprep`
   * - HCP data (CIFTI, fs_LR 32k)
     - :ref:`import-hcp`
   * - Data already on fsaverage
     - :ref:`import-fsaverage`
   * - Surfaces from any other tool (GIFTI or a mesh you can read)
     - :ref:`import-gifti`
   * - AFNI / SUMA
     - :ref:`import-afni`
   * - BrainVoyager
     - :ref:`import-brainvoyager`
   * - A registration matrix from FSL, SPM, AFNI, ...
     - :ref:`import-transforms`


.. _import-freesurfer:

FreeSurfer
----------

To build and edit the surfaces with FreeSurfer first, see
:doc:`segmentation_guide`. For the transform, compute one with
:doc:`align` or convert an existing ``register.dat`` (see
:ref:`import-transforms`).

.. _database-freesurfer-import:

Importing a subject
~~~~~~~~~~~~~~~~~~~

The usual way to create a subject in the pycortex database is to import one that has
already been segmented with Freesurfer_::

    import cortex
    cortex.freesurfer.import_subj(freesurfer_subject, pycortex_subject=None,
                                  freesurfer_subject_dir=None,
                                  whitematter_surf='smoothwm',
                                  autoflatten=True)

This reads from the Freesurfer subject directory,
``$SUBJECTS_DIR/{freesurfer_subject}/``, and writes into the pycortex filestore entry
for the subject, ``{filestore}/{pycortex_subject}/``. Only the files listed below are
copied over. Note that ``import_subj`` overwrites any pre-existing pycortex subject
of the same name, including all blender cuts, masks and transforms, and deletes all
cached files for that subject.

Anatomical volumes are converted with ``mri_convert``:

======================  =============================  ==========================
Freesurfer file         pycortex file                  Contents
======================  =============================  ==========================
``mri/T1.mgz``          ``anatomicals/raw.nii.gz``     T1-weighted anatomical
``mri/aseg.mgz``        ``anatomicals/aseg.nii.gz``    Automatic segmentation
``mri/wm.mgz``          ``anatomicals/raw_wm.nii.gz``  White matter segmentation
======================  =============================  ==========================

Surfaces are imported for both hemispheres (``lh`` and ``rh``) and are converted with
``mris_convert --to-scanner``, so that they are stored in the same coordinate system
as the anatomical volumes rather than in the Freesurfer TKR coordinate system (whose
center is set to FOV/2). As a consequence, the imported surfaces will look misaligned
with the anatomical volumes if you load them in ``freeview``, which expects TKR
coordinates. This is expected: the surfaces in the pycortex database are only meant to
be used by pycortex.

==========================  =============================  ======================
Freesurfer file             pycortex file                  Contents
==========================  =============================  ======================
``surf/?h.smoothwm``        ``surfaces/wm_?h.gii``         White matter surface
``surf/?h.pial``            ``surfaces/pia_?h.gii``        Pial surface
``surf/?h.inflated``        ``surfaces/inflated_?h.gii``   Inflated surface
==========================  =============================  ======================

The surface imported as ``wm`` is whichever surface is named by the
``whitematter_surf`` argument, so the first row above is really
``surf/?h.{whitematter_surf}``. It defaults to ``smoothwm``, but that surface is
smoothed and may not be appropriate for every use; ``white`` is a good alternative.

Surface info files hold one value per vertex. Both hemispheres are stored together in
a single ``.npz`` file, under the keys ``left`` and ``right``. Note that the values are
stored **negated** with respect to the Freesurfer values.

==========================  ================================  ==================
Freesurfer files            pycortex file                     Contents
==========================  ================================  ==================
``surf/?h.sulc``            ``surface-info/sulcaldepth.npz``  Sulcal depth
``surf/?h.thickness``       ``surface-info/thickness.npz``    Cortical thickness
``surf/?h.curv``            ``surface-info/curvature.npz``    Curvature
==========================  ================================  ==================

``import_subj`` also (re-)generates the fiducial surfaces, halfway between the white
matter and the pial surfaces, which are used for cutting and flattening. Those are
written back into the *Freesurfer* subject directory as ``surf/?h.fiducial``, not into
the pycortex filestore.

Labels and annotations are not imported; see ``cortex.freesurfer.get_label``.


Flattening the surfaces
~~~~~~~~~~~~~~~~~~~~~~~

By default, ``import_subj`` ends by cutting and flattening the surfaces with
autoflatten, which takes 15-30 minutes; pass ``autoflatten=False`` to skip
it. See :doc:`flattening` for autoflatten, cutting by hand, and importing
the resulting flatmaps.

.. _FreeSurfer: http://surfer.nmr.mgh.harvard.edu/


.. _import-fmriprep:

fMRIPrep
--------

**Surfaces.** fMRIPrep runs FreeSurfer's ``recon-all`` for you, so the
simplest route is to import its FreeSurfer subject directory (see
:ref:`import-freesurfer`)::

    import cortex
    cortex.freesurfer.import_subj(
        "sub-01",
        pycortex_subject="sub01",
        freesurfer_subject_dir="/path/to/derivatives/sourcedata/freesurfer",
    )

``cortex.fmriprep.import_subj`` copies fMRIPrep's own GIFTI surfaces,
``T1w`` and ``aseg`` instead. It only reads the legacy output layout
(``<source_dir>/fmriprep/sub-<label>/anat`` and
``<source_dir>/freesurfer/sub-<label>``, the default before fMRIPrep 21.0)
and does not create flat surfaces. See
:ref:`sphx_glr_auto_examples_import_surface_import_fmriprep.py`.

**Transform.**

* BOLD in ``T1w`` space (``--output-spaces T1w``): the BOLD and the surfaces
  already share scanner coordinates, so the transform is the identity
  matrix (see :ref:`shared-world-space`).
* BOLD in native space: fMRIPrep stores the BOLD-to-T1w registration as an
  ITK transform, which pycortex does not read. Either request ``T1w``
  outputs, or compute a transform from the native ``boldref`` with
  :doc:`align`.


.. _import-hcp:

HCP (CIFTI, fs_LR 32k)
----------------------

``cortex.hcp`` handles data on the HCP ``fs_LR`` 32k mesh without
Connectome Workbench. Download the ``32k_fs_LR`` template subject once, then
plot fs_LR data on it like any other vertex data::

    import cortex
    import cortex.hcp
    import nibabel as nib

    cortex.hcp.download_fs_lr()
    img = nib.load("data.dscalar.nii")
    lh_idx, rh_idx = cortex.hcp.get_cifti_vertex_indices(img)
    data = cortex.hcp.cifti_to_surface(img.get_fdata()[0], lh_idx, rh_idx)  # 64984 vertices
    cortex.quickshow(cortex.Vertex(data, "32k_fs_LR"))

CIFTI files only store cortical vertices outside the medial wall;
``cifti_to_surface`` fills the full surface, with NaN on the medial wall. To resample to fsaverage
instead, ``cortex.hcp.to_fsaverage("data.dscalar.nii")`` reads the CIFTI and
projects it in one step. See
:ref:`sphx_glr_auto_examples_hcp_plot_hcp_fs_lr.py`.


.. _import-fsaverage:

Data on fsaverage
-----------------

Many pipelines (fMRIPrep's ``fsaverage`` output spaces, group analyses) put
data on FreeSurfer's template surface. Download the template subject once
and plot the data directly, no transform needed::

    cortex.download_subject("fsaverage")
    cortex.quickshow(cortex.Vertex(data, "fsaverage"))

Data on the lower-resolution ``fsaverage5`` or ``fsaverage6`` meshes must be
upsampled first with ``cortex.freesurfer.upsample_to_fsaverage``. See
:ref:`sphx_glr_auto_examples_fsaverage_upsample_to_fsaverage.py`.


.. _import-gifti:

Surfaces from any other tool
----------------------------

pycortex doesn't check where surfaces came from. Any tool that produces
white-matter and pial meshes with matching vertices works: create the
subject and write each surface into it as GIFTI::

    import cortex
    import os

    cortex.db.make_subj("sub01")
    surf_dir = os.path.join(cortex.db.filestore, "sub01", "surfaces")
    for hemi, (pts, polys) in [("lh", lh_wm), ("rh", rh_wm)]:
        cortex.formats.write_gii(os.path.join(surf_dir, f"wm_{hemi}.gii"), pts, polys)
    # repeat for "pia" and, for the 3D viewer, "inflated"
    cortex.db.reload_subjects()

* Coordinates must be scanner (world) coordinates in millimetres, matching
  the anatomical volume, not a tool's internal space.
* If no ``fiducial`` surface is stored, pycortex uses the average of ``wm``
  and ``pia``.
* Flatmaps need a ``flat`` surface; see :doc:`flattening`.
* Copy the anatomical to ``anatomicals/raw.nii.gz``.


.. _import-afni:

AFNI / SUMA
-----------

* **Surfaces**: SUMA builds on FreeSurfer surfaces (``@SUMA_Make_Spec_FS``),
  so import that FreeSurfer subject directory with
  ``cortex.freesurfer.import_subj``.

.. # TODO what if SUMA without FreeSurfer

* **Volume data**: ``nibabel`` reads BRIK/HEAD directly; pass the array to
  :class:`cortex.Volume` as usual.
* **Transform**: AFNI matrices (``3dAllineate``, ``@auto_tlrc``) are in
  DICOM (LPS) coordinates; flip them to RAS before saving them (see
  :ref:`import-transforms`), or compute a new one with :doc:`align`.


.. _import-brainvoyager:

BrainVoyager
------------

* **Surfaces**: read ``.srf`` meshes with `bvbabel
  <https://github.com/ofgulban/bvbabel>`_, convert the vertices from
  BrainVoyager's internal coordinates to scanner coordinates, then write
  them as described in :ref:`import-gifti`::

      import bvbabel
      header, mesh = bvbabel.srf.read_srf("sub01_LH_WM.srf")
      pts, polys = mesh["vertices"], mesh["faces"]

* **Volume data**: ``bvbabel`` also reads VMR/VTC files.
* **Transform**: convert the ``.trf`` matrix to a 4x4 RAS affine (see
  :ref:`import-transforms`), or compute a new one with :doc:`align`.


.. _import-transforms:

Transforms from other software
------------------------------

Any 4x4 affine can be saved with ``cortex.db.save_xfm`` (see
:ref:`adding-transforms`). pycortex converts two formats for you:

* FSL FLIRT: :meth:`cortex.xfm.Transform.from_fsl`
* FreeSurfer ``register.dat`` / ``bbregister``:
  :meth:`cortex.xfm.Transform.from_freesurfer`

``cortex.mni`` computes and applies transforms to MNI space with FSL
(``compute_mni_transform``, ``transform_to_mni``).


.. _shared-world-space:

Functional data already in anatomical space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your pipeline left the functional data in the same scanner coordinates
as the anatomical (fMRIPrep ``T1w`` outputs, SPM *Coregister: Estimate*,
which rewrites the functional header), the ``magnet`` transform is the
identity. Save it with the functional image as reference::

    import numpy as np
    cortex.db.save_xfm("sub01", "T1w", np.eye(4), xfmtype="magnet",
                       reference="sub-01_task-x_space-T1w_boldref.nii.gz")

The built-in ``"identity"`` transform is different: it is for data on the
anatomical's own voxel grid (``anatomicals/raw.nii.gz``).
