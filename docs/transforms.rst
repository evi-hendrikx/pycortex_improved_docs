Transform formats
=================

Functional data, usually collected by an epi sequence, typically does not have the same scan parameters as the anatomical MPRAGE scan used to generate the surfaces. Additionally, fMRI sequences which are usually optimized for T2* have drastically different and larger distortions than a typical T1 anatomical sequence. While automatic algorithms exist to align these two scan types, they will sometimes fail spectacularly, especially if a partial volume slice prescription is necessary.

In short: the anatomical surfaces in the :doc:`database` and a given
functional scan don't start out in the same coordinate space, so pycortex
needs an explicit record of the mapping between them before it can say
"this voxel of functional data corresponds to this point on the cortical
surface." That mapping is the :term:`xfm <xfm / transform>`, created via :doc:`align`.

pycortex includes automatic and interactive tools to compute manual **affine** alignments — see :doc:`align` for current details (``cortex.align.manual`` currently opens FreeSurfer's FreeView). 
Alternatively, if an automatic algorithm works well enough, you can also commit your own transform to the database. Transforms in pycortex always go from **fiducial to functional** space. 
They have four variables associated:

    * **Subject** : name of the subject, must match the surfaces used to create the transform
    * **Name** : A unique identifier for this transform
    * **type** : The type of transform -- from fiducial to functional **magnet** space, or fiducial to **coord** innate space
    * **epifile** : the filename of the functional data that the fiducial is aligned to

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

Both are stored together (see :doc:`database`) precisely so that neither
has to be recomputed from the other at lookup time: ``cortex.db.save_xfm``
derives whichever of the two you didn't supply from the reference image's
own affine, so going through pycortex's own save/load path keeps them
consistent automatically. The risk is only if you hand-edit the stored
``matrices.xfm`` JSON directly instead of going through ``save_xfm`` —
then it's possible to leave **coord** and **magnet** describing two
different alignments, which would silently misalign masks, flatmaps, and
the viewer for that transform without any error being raised.

Transforms always store the epifile in order to allow visual validation of alignment using :doc:`align`.

For a runnable example that loads a transform's ``magnet`` affine and reference volume, then uses the derived ``coord``-space mask to build a :class:`cortex.Volume`, see :ref:`sphx_glr_auto_examples_utils_plot_mask_and_transform.py`.
