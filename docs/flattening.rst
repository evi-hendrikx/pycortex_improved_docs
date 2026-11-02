Cutting and flattening
======================

Pycortex needs a :term:`flat surface <flat surface / flatmap>` to make
flatmaps. A closed, curved surface like the cortex cannot be laid flat
without tearing it somewhere, the same reason no world map projection is
accurate everywhere on a sphere. So the surface is first cut along a few
anatomical seams, which keeps the distortion small and puts the seams in
visually unimportant places, and then flattened.

There are two ways to do this:

* **Automatically**, with autoflatten_. ``cortex.freesurfer.import_subj``
  does this by default; see :ref:`database-autoflatten`.
* **By hand**: you place the cuts in Blender, and pycortex flattens the cut
  surface; see :ref:`making-cuts`.

Both start from a FreeSurfer subject (see :doc:`segmentation_guide`) and
write ``surfaces/flat_lh.gii`` and ``surfaces/flat_rh.gii`` into the
pycortex subject. Both also delete the subject's ``overlays.svg`` and all of
its cached files, since the flatmaps fundamentally change.

.. _autoflatten: https://gallantlab.org/autoflatten/


.. _database-autoflatten:

Automatic flattening with autoflatten
-------------------------------------

autoflatten_ is a separate package by Matteo Visconti di Oleggio Castello
(source_). It projects a template set of cuts onto the subject's surfaces
by surface-based registration, flattens the resulting patches, and imports
the flatmaps into the pycortex database. It is an optional dependency,
installed with the ``autoflatten`` extra::

    pip install "pycortex[autoflatten]"

``import_subj`` runs it at the end of the import (see
:ref:`database-freesurfer-import`). If autoflatten_ is not installed,
``import_subj`` warns and skips this step. Flattening takes a while,
typically 15-30 minutes for both hemispheres, so you may want to skip it
and flatten the surfaces later (or by hand)::

    cortex.freesurfer.import_subj(freesurfer_subject, autoflatten=False)

You can then run the same step on its own at any time::

    cortex.freesurfer.autoflatten_subject(freesurfer_subject, pycortex_subject=None,
                                          freesurfer_subject_dir=None)

Extra command line arguments for autoflatten_ can be passed through the
``autoflatten_args`` argument of either function, for instance
``autoflatten_args=['--backend', 'freesurfer']`` to flatten with FreeSurfer's
``mris_flatten`` instead of the default JAX-accelerated backend, or
``autoflatten_args=['--overwrite']`` to redo patches that already exist.

.. _source: https://github.com/mvdoc/autoflatten


.. _making-cuts:

Cutting by hand
---------------

``cortex.segment.cut_surface`` opens the surface in Blender, where you make
the cuts, and then flattens the cut surface with one of three methods
(``flatten_with=``):

* ``'freesurfer'`` (default, recommended): FreeSurfer's ``mris_flatten``.
  Produces high-quality flatmaps with minimal distortion, but takes about 2
  hours per hemisphere.
* ``'SLIM'``: the SLIM algorithm. Very fast, but tends to leave more
  distortion. SLIM must be installed separately.
* ``'blender'``: Blender's UV unwrapping (pass ``method=`` as
  ``'CONFORMAL'``, ``'ANGLE_BASED'`` or ``'MINIMUM_STRETCH'``). Typically
  5-15 minutes per hemisphere, but may introduce more distortion than
  FreeSurfer.

You may follow the steps below or a `Python notebook
<https://colab.research.google.com/github/gallantlab/pycortex/blob/main/examples/quickstart/fmri_flattening.ipynb>`_.
To make the cuts, watch the `cutting tutorial video
<https://www.youtube.com/watch?v=D4tylQ_mMuM>`_.

Step 1: Cut the left hemisphere
*******************************

``cut_surface`` creates a Blender file with the surface and opens Blender.
Make the cuts, save the file and exit Blender; the cut surface is then
flattened.

.. code-block:: python

    import cortex

    cortex.segment.cut_surface(
        "sub-01",                   # Your subject ID
        "lh",                       # Left hemisphere
        name="flatten",             # Name for this flattening attempt
        flatten_with="freesurfer",  # Or "SLIM" or "blender"
        recache=True,               # Force recache of the subject
        do_import_subject=False,    # Don't import until both hemispheres are done
    )

Step 2: Cut the right hemisphere
********************************

.. code-block:: python

    cortex.segment.cut_surface(
        "sub-01",                   # Your subject ID
        "rh",                       # Right hemisphere
        name="flatten",             # Name for this flattening attempt
        flatten_with="freesurfer",  # Or "SLIM" or "blender"
        recache=True,               # Force recache of the subject
        auto_overwrite=True,        # Overwrite PyCortex record
        do_import_subject=True,     # Import both hemispheres when done
    )

With ``do_import_subject=True`` both flatmaps are imported into pycortex
once this finishes. If you flattened with ``do_import_subject=False``, or
flattened the patches some other way, import them with::

    cortex.freesurfer.import_flat(fs_subject, patch, hemis=['lh', 'rh'],
                                  cx_subject=None)

Step 3: Check the result
************************

Plot some data on the new flatmap::

    import cortex
    from matplotlib import pyplot as plt

    cortex.quickshow(cortex.Vertex.random("sub-01"), with_colorbar=True, recache=True)
    plt.show()
