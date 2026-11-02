Transforms
==========

The anatomical surfaces in the :doc:`database` and a functional scan don't
start out in the same coordinate space. A :term:`transform <xfm / transform>`
records the mapping between them: an **affine** matrix that always goes
from the subject's **fiducial** surface space to one functional scan's space.
Each transform belongs to one subject and has a name, unique for that
subject (e.g. ``fullhead``). Compute one with :doc:`align`, or save one
from your own pipeline (see :ref:`adding-transforms`).

Two representations of the same transform are stored, and they answer two
different questions:

* **magnet** space is the transform expressed in the scanner's physical
  ("magnet isocenter") coordinates, as recorded in the Nifti header
  (``nibabel``'s ``affine``). It's the representation you'd use if you
  needed to relate this transform to another scan's own affine, since it's
  anchored to a physical frame rather than to any one file's array
  indexing.
* **coord** space is the same transform expressed directly in terms of
  voxel *indices* of the reference EPI file, so pycortex can look up "which
  voxel does this surface point fall into" without going through a
  physical-coordinate round trip for every lookup. This is the
  representation used for :doc:`mask <masks>` generation and
  other operations that need fast index lookups.

Both are stored together in the transform's ``matrices.xfm`` precisely so that neither
has to be recomputed from the other at lookup time: ``cortex.db.save_xfm``
derives whichever of the two you didn't supply from the reference image's
own affine, so going through pycortex's own save/load path keeps them
consistent automatically. The risk is only if you hand-edit the stored
``matrices.xfm`` JSON directly instead of going through ``save_xfm`` —
then it's possible to leave **coord** and **magnet** describing two
different alignments, which would silently misalign masks, flatmaps, and
the viewer for that transform without any error being raised.

Each transform lives in its own directory in the :doc:`filestore <database>`,
``{subject}/transforms/{name}/``:

* ``matrices.xfm``: a JSON file with two 4x4 matrices, under the keys
  ``magnet`` and ``coord``.
* ``reference.nii.gz``: a copy of the reference (EPI) volume the transform
  was computed against. Any image nibabel can read is accepted and converted
  to NIfTI; for a 4D image only the first volume is kept. Storing it allows
  visual validation and tweaking of the alignment using :doc:`align`.
* ``mask_{type}.nii.gz``: :doc:`masks <masks>` cached for this
  transform. ``save_xfm`` refuses to change a transform that already has
  masks, since they were computed from the old alignment.

For a runnable example that loads a transform's ``magnet`` affine and reference volume, then uses the derived ``coord``-space mask to build a :class:`cortex.Volume`, see :ref:`sphx_glr_auto_examples_utils_plot_mask_and_transform.py`.


Accessing transforms
~~~~~~~~~~~~~~~~~~~~
::

    import cortex
    xfm = cortex.db.get_xfm('S1', 'fullhead', xfmtype='coord')

This returns a :class:`cortex.xfm.Transform`; its ``.xfm`` attribute holds
the 4x4 matrix. See :ref:`database-access` for browsing transforms through
attributes and tab completion.


.. _adding-transforms:

Adding new transforms
~~~~~~~~~~~~~~~~~~~~~
The functions in :doc:`align` compute a transform and save it for you. If
you already have a 4x4 affine from elsewhere, save it with::

    import cortex
    cortex.db.save_xfm(subject, xfmname, xfm, xfmtype='magnet', reference='path_to_functional.nii')

``xfmtype`` says whether ``xfm`` is in ``'magnet'`` or ``'coord'`` space;
the other representation is derived from the reference image's affine.
``reference`` is required when creating a new transform.

FSL FLIRT and FreeSurfer registration matrices can be converted with
:meth:`cortex.xfm.Transform.from_fsl` and
:meth:`cortex.xfm.Transform.from_freesurfer`. Both return a ``coord``
transform::

    xfm = cortex.xfm.Transform.from_fsl('func2anat.mat', 'func.nii.gz', 'anat.nii.gz')
    xfm.save(subject, xfmname, 'coord')

