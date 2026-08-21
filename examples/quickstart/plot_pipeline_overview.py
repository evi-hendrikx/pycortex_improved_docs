"""
================================================
The full pipeline: mask, Volume, flatmap, viewer
================================================

This is the runnable version of the "Phase 2" diagram on :doc:`/overview`:

    functional data + a mask -> ``cortex.Volume`` -> static flatmap /
    interactive WebGL viewer

using only the ``S1`` demo subject that ships with pycortex, so nothing
needs to be downloaded, and no FreeSurfer run is required, to run this
script.

"Phase 1" (surfaces + alignment) isn't run here because it's already done
for ``S1`` -- its surfaces and its ``fullhead`` transform are already
sitting in the filestore, which is exactly what :doc:`/segmentation_guide`
and :doc:`/align` produce for a subject of your own. If you're starting
from your own subject rather than ``S1``, that setup comes first;
everything below is what you'd run afterward, every time you have new
data to look at.

For a closer look at what a mask actually *is*, and how it turns a 3D
volume into the flat 1D array ``cortex.Volume`` expects, see
:ref:`sphx_glr_auto_examples_utils_plot_mask_and_transform.py`.
"""

import numpy as np
import matplotlib.pyplot as plt

import cortex

subject = "S1"
xfmname = "fullhead"

###############################################################################
# functional data + a mask -> cortex.Volume
# -------------------------------------------
# ``cortex.db.get_mask`` returns a boolean 3D array, the same shape as the
# functional reference this transform was aligned to, selecting the voxels
# that actually matter (i.e. sit within the cortical sheet). A real analysis
# would put its statistic (betas, t-values, ...) here, one value per masked
# voxel; we stand in with random noise just to demonstrate the plumbing.
mask = cortex.db.get_mask(subject, xfmname, "thick")
data = np.random.randn(mask.sum())
volume = cortex.Volume(
    data, subject, xfmname, mask=mask,
    cmap="RdBu_r", vmin=-3, vmax=3,
)

###############################################################################
# cortex.Volume -> a static flatmap
# ------------------------------------
# ``cortex.quickshow`` (an alias for ``cortex.quickflat.make_figure``) lays
# the whole cortex out flat in one 2D image -- see :doc:`/rois` and
# :doc:`/colormaps` for the layers (ROI outlines, curvature, colorbar, ...)
# it can add on top of this.
cortex.quickshow(volume, with_curvature=True, with_colorbar=True)
plt.show()

###############################################################################
# cortex.Volume -> an interactive WebGL viewer
# -----------------------------------------------
# ``cortex.webshow`` (an alias for ``cortex.webgl.show``) opens the same
# data in a browser-based viewer where you can drag between folded,
# inflated, and flattened views live -- see :doc:`/userguide/webgl`. It
# starts a local web server and blocks until you close it, so it is not
# actually called while this gallery page is built; run the line below
# yourself to try it:
#
#     cortex.webshow(volume)
#
# See ``retinotopy_webgl.py`` for a complete, standalone script built
# around this same call.
