Mapping volumes to the surface
==============================

You don't need to map anything to *show* volume data: the
:doc:`static flatmaps <quickflat>` and the :doc:`WebGL viewer
<userguide/webgl>` sample the volume directly for every pixel
(:term:`pixel-wise sampling`). Mapping is for when you want the values
themselves on the surface, one per vertex, e.g. for surface-based analyses,
to compare with surface data, or to move data to ``fsaverage``.

A **mapper** turns a :class:`cortex.Volume` into a :class:`cortex.Vertex`
for one subject and :doc:`transform <transforms>`::

    import cortex

    volume = cortex.Volume.random("S1", "fullhead")
    mapper = cortex.get_mapper("S1", "fullhead", "line_nearest")
    vertex = mapper(volume)

``volume.map("line_nearest")`` does the same in one step, and keeps the
volume's colormap settings. See
:ref:`sphx_glr_auto_examples_datasets_plot_volume_to_vertex.py`.


Mapper types
------------

The mapper type combines *where* each vertex samples the volume with *how*
the volume is interpolated there (``nearest``, ``trilinear`` or
``lanczos``, plus ``gaussian`` for point mappers):

* **Point** (``'nearest'``, ``'trilinear'``, ``'gaussian'``,
  ``'lanczos'``): the volume at the vertex's position on the fiducial
  surface. ``'nearest'`` is the default of ``get_mapper`` and
  ``Volume.map``.
* **Line** (``'line_nearest'``, ``'line_trilinear'``, ``'line_lanczos'``):
  the average of ``npts`` points (default 64) on the line from the vertex
  on the white matter surface to the same vertex on the pial surface. This
  uses the whole thickness of the cortex, like the flatmaps do, and is a
  good default.
* **Patch** (``'const_patch_nn'``, ``'const_patch_trilin'``,
  ``'const_patch_lanczos'``): the average over random points on the
  triangles around the vertex.

The mapper is a pair of sparse matrices, one per hemisphere
(``mapper.masks``), from voxels to vertices.


Mapping back to the volume
--------------------------

``mapper.backwards`` goes the other way, from a ``Vertex`` (or an array of
vertex values) to a ``Volume`` (or array), by solving the least-squares
inverse of the mapping::

    volume_again = mapper.backwards(vertex)


Masked data, NaNs and fsaverage
-------------------------------

``cortex.mapper.vol2surf`` maps :ref:`masked data <masked-data>` (1D, or
2D ``(n_samples, n_voxels)``) straight to an array of vertex values. It
leaves NaN voxels out of each vertex's average, where a plain mapper would
make the vertex NaN::

    from cortex.mapper import vol2surf

    # data: a (z, y, x) volume or (t, z, y, x) time series
    mask = cortex.db.get_mask("S1", "fullhead", "thick")
    vertex_values = vol2surf(data[..., mask], "S1", "fullhead")

``target_surface="fsaverage"`` (or ``"fsaverage5"``, ``"fsaverage6"``)
maps on to a FreeSurfer template surface instead; this needs FreeSurfer's
``mri_surf2surf``.


Caching
-------

Building a mapper is slow, so it is saved in the subject's cache
(e.g. ``fullhead_linenn.npz``) and reused. Unlike the flatmap cache, a mapper is
rebuilt automatically when its transform file is newer than the cache;
``recache=True`` forces a rebuild, e.g. after changing the surfaces.
