Masks
=====

A :term:`mask` selects the voxels of a functional volume that lie near the
cortex, for one subject and :doc:`transform <transforms>`. Modeling only
those voxels is much cheaper than modeling the whole volume. A mask is a
boolean ``(z, y, x)`` array on the transform's reference grid, cached in the
transform's directory as ``mask_{type}.nii.gz``.

For a worked example of what a mask looks like against its reference volume,
and how it turns a 1D array of per-voxel values into a :class:`cortex.Volume`,
see :ref:`sphx_glr_auto_examples_utils_plot_mask_and_transform.py`.


Mask types
----------

The simplest mask would take the voxel nearest each surface vertex, but
pycortex's :term:`pixel-wise sampling` can read voxels that no vertex falls
in. All mask types are therefore computed from the distance between voxels
and the surface:

* ``'nearest'``: only voxels overlapping the fiducial surface itself. The
  most conservative option.
* ``'thin'``: voxels within 2 mm of the fiducial surface.
* ``'cortical'``: voxels whose centers fall inside the cortical ribbon,
  between the white matter and pial surfaces (requires both surfaces). This
  is the most anatomically precise mask, but can be too restrictive:
  functional data rarely aligns with the anatomy closely enough for every
  true cortical voxel to fall inside the ribbon.
* ``'line_nearest'``: any voxel with any part intersecting the cortical
  ribbon. A more liberal counterpart to ``'cortical'``.
* ``'thick'``: voxels within 8 mm of the fiducial surface. This is the
  default, because EPI scans are distorted by field inhomogeneity and never
  perfectly co-register with the anatomical scan, so a generous margin makes
  it less likely that true cortical signal is excluded. It also keeps a fair
  amount of white matter and skull; switching to ``'thin'`` is a reasonable
  way to cut down the number of voxels once you trust the alignment.

For selecting voxels inside surface ROIs rather than by distance to the
surface, see :func:`cortex.utils.get_roi_masks`.


Getting a mask
--------------

::

    import cortex
    mask = cortex.db.get_mask('S1', 'fullhead', 'thick')

The first time a mask type is requested, ``get_mask`` generates it with
:func:`cortex.utils.get_cortical_mask` and saves it in the transform's
directory; later calls read the saved file. Because a mask is computed from
the alignment, ``cortex.db.save_xfm`` refuses to change a transform that
already has masks.


.. _masked-data:

Using masked data
-----------------

Masked data holds only the voxels inside a mask, in the mask's voxel order::

    mask = cortex.db.get_mask('S1', 'fullhead', 'thick')
    masked = data[mask]            # 1D, one value per voxel in the mask
    vol = cortex.Volume(masked, 'S1', 'fullhead')

:class:`cortex.Volume` accepts 1D masked data, or 2D ``(t, v)`` for a time
series. It finds the mask by looking for a saved mask of this transform with
the same number of voxels. If there is none, pass ``mask=``, either the
boolean array or the name of a mask type. Unmasking only works with exactly
the mask the data was made with, which is why custom masks are best saved
in the database.


Saving a custom mask
--------------------

::

    import cortex
    cortex.db.save_mask(subject, xfmname, masktype, mask)

``mask`` must have the shape of the transform's reference volume. The mask
is saved as ``mask_{masktype}.nii.gz``; ``save_mask`` refuses to overwrite
an existing mask of the same type.
