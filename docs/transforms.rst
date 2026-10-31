Transform formats
=================

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
  representation used for :ref:`mask <database-masks>` generation and
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
* ``mask_{type}.nii.gz``: :ref:`masks <database-masks>` cached for this
  transform. ``save_xfm`` refuses to change a transform that already has
  masks, since they were computed from the old alignment.

For a runnable example that loads a transform's ``magnet`` affine and reference volume, then uses the derived ``coord``-space mask to build a :class:`cortex.Volume`, see :ref:`sphx_glr_auto_examples_utils_plot_mask_and_transform.py`.


Accessing transforms
~~~~~~~~~~~~~~~~~~~~
Similar to the surfaces, transforms can be access through two methods: direct command access, and the tab interface.

Command access looks like this::

    import cortex
    xfm = cortex.db.get_xfm('S1', 'fullhead', xfmtype='coord')

Tab complete looks like this::

    In [1]: import cortex
    In [2]: cortex.db.S1.transforms
    Out[2]: Transforms: [fullhead,retinotopy]

    In [3]: cortex.db.S1.transforms['fullhead'].coord.xfm
    Out[3]: 
     [[-0.44486981846094426,
       -0.0021363672818559996,
       -0.03721181986487324,
       46.62686084588364],
      [0.005235315303737166,
       -0.44485768384714863,
       -0.03704886912935894,
       60.165881316857195],
      [-0.02001550497747565,
       -0.020260819840215893,
       0.24044994416882276,
       12.698317611104553],
      [0.0, 0.0, 0.0, 1.0]]


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


.. _database-masks:

Masks
~~~~~
One of the fundamental reasons for carefully aligning surfaces is to allow the creation and use of cortical masks. This limits the number of voxels you need to model. Traditionally, these masks are created by selecting the set of nearest neighbor voxels for each vertex on the transformed surface. Unfortunately, pycortex's advanced per-pixel mapping precludes the use of this simple mask, since faces could potentially intersect with voxel corners which are not in this simple mask. Thus, the default masks in pycortex use a distance metric to compute mask membership.

Masks were added into pycortex in May 2013, due to previous issues with masked data and the addition of the per-pixel mapping. Masked datasets are further discussed in the datasets page.

Retrieving a mask
"""""""""""""""""
A mask is specified by three variables: **subject**, **transform**, and **mask type**. pycortex defines five named mask types, all computed by distance from the surface rather than simple nearest-neighbor voxel selection:

    * ``'nearest'`` — only voxels overlapping the fiducial surface itself. The most conservative option.
    * ``'thin'`` — voxels within 2 mm of the fiducial surface.
    * ``'cortical'`` — voxels whose centers fall inside the cortical ribbon, between the white matter and pial surfaces (requires both surfaces to be present for the subject). This is the most anatomically precise mask, but can be too restrictive: functional data rarely aligns with the anatomy closely enough for every true cortical voxel to fall inside the ribbon.
    * ``'line_nearest'`` — any voxel with any part intersecting the cortical ribbon. A more liberal counterpart to ``'cortical'``.
    * ``'thick'`` — voxels within 8 mm of the fiducial surface. This is the default, because field inhomogeneity means EPI (functional) scans are distorted and never perfectly co-register with the anatomical scan — a generous margin makes it less likely that true cortical signal gets excluded by the mask. The tradeoff is that it also keeps a fair amount of white matter and skull, so switching to ``'thin'`` after the fact is a reasonable way to cut down the number of voxels you need to model once you trust the alignment.

To retrieve the thick mask for S1 using the fullhead transform::

    import cortex
    mask = cortex.db.get_mask('S1', 'fullhead', 'thick')

The first time you load a mask, it is generated (via :func:`cortex.utils.get_cortical_mask`, which ``get_mask`` calls internally when a cached mask isn't found) and stored inside the folder for the associated transform, so later calls just read it back.

For selecting voxels that fall within functional ROIs defined in other experiments/datasets rather than by anatomical proximity, see :func:`cortex.utils.get_roi_masks`.

For a worked example of what a mask actually looks like (visualized against the reference functional volume it was computed from) and how it's used to turn a 1D array of per-voxel values into a :class:`cortex.Volume` for display, see :ref:`sphx_glr_auto_examples_utils_plot_mask_and_transform.py`.

Loading a mask
""""""""""""""
If you use a custom mask for any reason, it is highly recommended that you load it into the database for future reference. It will allow more seamless integration with ``Datasets``, and will prevent it from being lost. To add a custom mask to the database::

    import cortex
    cortex.db.load_mask(subject, xfmname, masktype, mask)
