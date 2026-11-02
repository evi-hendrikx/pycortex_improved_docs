Aligning functional data
========================

A functional (EPI) scan and the anatomical scan used to build a subject's
surfaces are almost never acquired with the subject in exactly the same
position, and EPI sequences (optimized for T2* contrast) suffer larger and
different geometric distortions than the T1 anatomical. Before functional
data can be put on the surface, pycortex needs a :term:`transform <xfm /
transform>` that maps one onto the other (see :doc:`transforms` for what it
stores). The alignment is limited to a **rigid-body** transform (6 degrees
of freedom: translation and rotation): the two scans are of the same
physical brain, so more freedom would only let the alignment silently
absorb segmentation or acquisition problems.

Start with **automatic** alignment, which is fast and usually gets most of
the way. Then check it, and correct it if needed, with **manual**
alignment: a registration algorithm optimizes a global metric that doesn't
know which regions matter for your analysis, and can fail on partial-volume
acquisitions or unusual contrast.

The examples below use subject ``S1``, a new transform named
``example-transform``, and a reference image ``ref-image.nii.gz`` from the
functional run, in any format nibabel reads. This is usually the temporal
mean image.

Automatic Alignment
-------------------

Call ``cortex.align.automatic`` to align the brain automatically::

	cortex.align.automatic('S1', 'example-transform', './ref-image.nii.gz')

This creates the transform in the filestore, as ``S1/transforms/example-transform/`` (see :doc:`transforms`), and should be the first step for any alignment.

As of pycortex 1.2.8, this uses FreeSurfer's ``mri_coreg`` (for an initial
coarse alignment) followed by ``bbregister`` (boundary-based registration)
by default — you'll see a ``UserWarning`` reminding you of this every time
you call it. If you specifically want the older FSL-based BBR alignment
instead, call ``cortex.align.automatic_fsl`` with the same arguments.

``cortex.align.automatic`` accepts a few more arguments worth knowing about:

* ``init``: how to get the initial, coarse alignment that ``bbregister``
  then refines. Defaults to ``"coreg"`` (FreeSurfer's ``mri_coreg``, best
  in most cases); ``"fsl"`` uses FSL's FLIRT instead, ``"header"`` assumes
  the reference and anatomical are already close (e.g. acquired in the
  same session), and a path to an existing DAT/LTA transform can also be
  passed directly.
* ``epi_mask``: pass ``True`` if the reference wasn't distortion-corrected,
  to mask out areas with spatial distortion during registration.
* ``reference_contrast``: ``"t2"`` (default, for BOLD — gray matter
  brighter than white matter) or ``"t1"`` (white matter brighter than gray
  matter).
* ``intermediate``: a path to a whole-brain image acquired in the same
  session, useful when ``reference`` itself has a small field of view.

When it finishes, ``cortex.align.automatic`` prints a "mincost" quality
score (0 to 1, lower is better; values under ~0.5 indicate a good
registration) — but treat that as a sanity check, not a substitute for
looking at the result yourself in the :ref:`manual aligner <manual-alignment>`.

Both ``cortex.align.automatic`` and ``cortex.align.automatic_fsl`` accept a
``noclean`` argument (``bool``, default ``False``). Intermediate files
generated during alignment are written to ``/tmp`` and deleted once
alignment finishes; pass ``noclean=True`` to keep them there instead
(useful for debugging), in which case the function returns the temp
directory's path.

Automatically Tweaking Alignments
---------------------------------
In theory, a pre-existing alignment can be tweaked automatically.
Like ``cortex.align.automatic_fsl``, this is done via FSL BBR.
In practice, the search range is too big to be reliably useful, and tweaking should usually be done using manual alignment instead — the function's own docstring calls it "probably not very useful."
::

    cortex.align.autotweak('S1', 'example-transform')

.. _manual-alignment:

Manual Alignment
-----------------

Automatic alignment typically gets you most of the way to a good
alignment, but rarely all the way — the remainder needs a person looking
at the actual images. The current, recommended manual aligner is
``cortex.align.manual``, which opens FreeSurfer's **FreeView** with the
reference image and the subject's white-matter and pial surface contours
overlaid on top of it::

	cortex.align.manual('S1', 'example-transform')

This requires FreeSurfer to be installed with ``freeview`` and
``lta_convert`` on your ``PATH``, and ``$SUBJECTS_DIR`` set correctly in
your environment (pycortex shells out to ``freeview`` directly, using
``$SUBJECTS_DIR`` to find the subject's ``orig.mgz`` and surface files).

By default, the white-matter surface is outlined in yellow and the pial
surface in blue (``wm_color`` / ``pial_color`` arguments — check the
colors actually shown in your FreeView window rather than assuming, since
this function's own docstring lists different defaults than its code
currently uses). ``wm_surface`` selects which FreeSurfer white-matter
surface file to use for the outline (``'white'`` by default, or
``'smoothwm'``).

Use FreeView's own tools to nudge the registration until the surface
contours hug the reference image's gray/white matter boundary. When
you're done, **save the registration** — FreeView will want to write it
somewhere in a temporary ``fsalign_...`` directory pycortex just created;
save it there under the name pycortex tells you to use (``register.lta``
by default, the ``output_name`` argument) and then close FreeView.
Pycortex then converts that file and saves the result into the database
as a new transform.

A few other arguments:

* ``inspect_only=True`` opens the current alignment for viewing only —
  closing FreeView won't overwrite anything, useful for just checking an
  existing transform.
* ``noclean=True`` keeps pycortex's temporary working directory instead of
  deleting it when FreeView closes (and returns its path) — useful for
  debugging if the save doesn't go as expected.
* ``reference`` only needs to be supplied when creating a transform from
  scratch; to re-open and adjust an existing transform, leave it out and
  the transform's stored reference image will be reused.

.. note::

   ``cortex.align.fs_manual`` is a deprecated alias kept only for backward
   compatibility — it just calls ``cortex.align.manual`` and will be
   removed in a future release. Use ``cortex.align.manual`` directly.

Tips for aligning the brain
~~~~~~~~~~~~~~~~~~~~~~~~~~~
* The really deep sulci work great as landmarks to align stuff up.
* To check how well the brain is aligned, make a flatmap out of the
  reference image itself using the new transform. Since the reference
  image is a real EPI volume, adjacent voxels should have similar
  intensities — a good alignment carries that smoothness onto the
  flatmap as a smooth gradient across the cortical surface. A bad
  alignment instead samples the reference at the wrong locations, so
  neighbouring surface vertices end up pulling from unrelated voxels and
  the flatmap looks patchy/speckled instead::

    vol = cortex.Volume('./ref-image.nii.gz', 'S1', 'example-transform')
    cortex.quickshow(vol)

  Smooth gradient across the brain → good alignment. A lot of voxels
  starkly different from their neighbours → revisit the alignment (see
  :ref:`manual alignment <manual-alignment>` above).

  See :ref:`sphx_glr_auto_examples_utils_plot_check_alignment.py` for a
  runnable version of this check (against the bundled ``S1`` subject's
  already-good ``fullhead`` transform, so you can see what "smooth
  gradient" actually looks like before judging one of your own).
