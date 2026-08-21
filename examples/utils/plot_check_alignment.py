# -*- coding: utf-8 -*-
"""
=================================
Sanity-checking an alignment
=================================

Once you've computed a transform (see :doc:`/align`), how do you actually
tell whether it's any good, short of squinting at FreeView? A quick,
concrete check: run the transform's own EPI reference volume through
itself and look at the result on the flatmap. Since real EPI data varies
smoothly from one voxel to its neighbours, a good alignment carries that
smoothness onto the surface as a smooth gradient. A bad alignment instead
samples the reference volume at the wrong voxel for many neighbouring
surface points, so the flatmap comes out patchy/speckled instead --
neighbouring vertices end up pulling values from spatially unrelated
voxels.

This example runs that check against the bundled ``S1`` subject's
``fullhead`` transform, so there's nothing to align and nothing to
download -- it's meant to show you what the check itself looks like, not
to compute a new alignment (for that, see :doc:`/align`).
"""

import matplotlib.pyplot as plt

import cortex

subject = "S1"
xfmname = "fullhead"

###############################################################################
# Load the transform and pull out its stored reference volume -- the actual
# functional (EPI) scan this transform was computed against, saved
# alongside it precisely to make this kind of check possible (see
# :doc:`/database`).
xfm = cortex.db.get_xfm(subject, xfmname, xfmtype="coord")

# nibabel images are indexed (x, y, z); cortex.Volume expects 3D data as
# (z, y, x), the same convention get_mask() already returns -- so
# transpose before handing it to Volume.
reference_volume = xfm.reference.get_fdata().T

###############################################################################
# Feed the reference volume straight back through its own transform and
# look at the resulting flatmap.
volume = cortex.Volume(reference_volume, subject, xfmname, cmap="gray")

cortex.quickshow(volume, with_curvature=True, with_colorbar=True)
plt.show()

###############################################################################
# What to look for
# -----------------
# ``S1``'s ``fullhead`` transform is a real, previously-verified alignment,
# so this should render as a smooth gradient across the cortex -- lighter
# where the EPI signal was brighter, darker where it wasn't, with no sharp
# pixel-to-pixel noise. If you run this same check on a transform of your
# own and instead see fine-grained speckling (neighbouring patches of the
# flatmap jumping between unrelated intensities), that's the flatmap
# equivalent of the surface contours not hugging the anatomy in FreeView --
# time to revisit the alignment, manually if necessary (see the
# :ref:`manual alignment <manual-alignment>` section of :doc:`/align`).
