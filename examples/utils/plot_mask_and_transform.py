# -*- coding: utf-8 -*-
"""
=======================================
From voxels to a Volume: masks and xfms
=======================================

If you are coming from standard fMRI analysis, ``cortex.Volume`` can feel
like a black box: you hand it a *1D* array of numbers and a subject/transform
name, and a cortical surface pops out. This example opens that box up by
walking through the two pieces that make it possible -- the **transform**
(:doc:`/transforms`) and the **mask** (:ref:`database-masks`) -- using the
same functional volume the transform itself was aligned to as a reference,
so you can see exactly which voxels end up feeding the surface.

The four steps below mirror what you'd normally do by hand when you get a
new subject/transform pair and want to understand what you're working with:
look at the transform, look at the mask, look at the two of them together,
and only then trust that squeezing your data through the mask does the
right thing.
"""

import numpy as np
import matplotlib.pyplot as plt

import cortex

# We use the "S1" example subject and its "fullhead" transform, since both
# ship with pycortex's test filestore -- the same pair used by the other
# examples in this folder (e.g. plot_mosaic.py), so nothing needs to be
# downloaded to run this script.
subject = "S1"
xfmname = "fullhead"

###############################################################################
# 1. The transform
# -----------------
# A transform record does not contain "a" matrix, it contains *two*
# representations of the same alignment, plus the reference volume they were
# both computed from. ``xfmtype`` picks which representation you get back:
#
# - ``"magnet"`` is the affine in the scanner's physical coordinates, exactly
#   as it would appear in the reference volume's Nifti header
#   (``nibabel``'s ``.affine``). This is the space alignment tools work in,
#   because it's anchored to physical space rather than to any one file's
#   voxel indexing.
# - ``"coord"`` is the same alignment, but expressed directly as voxel
#   *indices* into the reference volume. This is what pycortex actually uses
#   internally to decide "which voxel does this surface point fall into",
#   since it avoids a physical-coordinate round trip on every lookup -- and
#   it's the representation masks (below) are defined in.
#
# Both are derived from each other via the reference image's own affine when
# the transform is first saved (see ``cortex.db.save_xfm``), so which one you
# ask for should depend on what you're about to do with it: hand it to an
# alignment/plotting tool that expects physical coordinates ("magnet"), or
# index directly into the functional volume ("coord").
xfm = cortex.db.get_xfm(subject, xfmname, xfmtype="magnet")

print("magnet-space affine (fiducial -> scanner coordinates of the epi):")
print(xfm.xfm)

# The reference is stored as a nibabel image -- the actual functional volume
# this transform was aligned to. Its shape is what everything else in this
# example (masks, and any data you plot) has to match.
reference = xfm.reference
print("\nreference functional volume shape (x, y, z):", reference.shape)

###############################################################################
# 2. The mask
# -----------
# pycortex operates on triangular mesh surfaces, but your data almost always
# starts out as a 3D functional volume -- not every voxel in that volume is
# useful, since plenty of it is skull, white matter, or empty space around
# the head. A **mask** is a boolean volume, the same shape as the reference,
# that says "keep this voxel" / "drop this voxel". Getting a mask is what
# turns a 3D volume-shaped problem into the 1D "one value per selected
# voxel" arrays that ``cortex.Volume`` expects for masked data.
#
# ``'thick'`` and ``'thin'`` are the two masks pycortex defines by default
# for every transform, selecting voxels within 8mm / 2mm of the fiducial
# surface respectively. The first time you ask for a mask it is computed
# from the surfaces and cached in the filestore, so this call may take a
# moment the first time it's run for a given subject/transform.
thick_mask = cortex.db.get_mask(subject, xfmname, "thick")

# Note that get_mask() already returns the mask transposed into the same
# (z, y, x) axis order as reference.get_fdata().T below -- pycortex is
# internally consistent about this ordering, so the two line up directly
# without any extra transposing on our part.
print("\nmask shape:", thick_mask.shape)
print("reference volume shape, transposed to match:", reference.get_fdata().T.shape)
print("number of voxels selected by the 'thick' mask:", thick_mask.sum(), "/", thick_mask.size)

###############################################################################
# 3. Seeing the mask and the reference together
# -----------------------------------------------
# ``thick_mask`` on its own is just a wall of ``True``/``False`` -- it only
# means something once you see *where* those voxels sit relative to the
# actual functional volume. ``cortex.mosaic`` (used with ``show=False`` so it
# hands back an image array instead of immediately plotting) tiles all
# slices of a 3D volume into one 2D image, which is a convenient way to look
# at a whole volume, and its mask, at a glance.
reference_volume = reference.get_fdata().T

ref_mosaic, (nwide, ntall) = cortex.mosaic(reference_volume, show=False)
mask_mosaic, _ = cortex.mosaic(thick_mask.astype(float), show=False)

fig, ax = plt.subplots(figsize=(8, 8))
# Background: every slice of the raw functional reference, in grayscale.
ax.imshow(ref_mosaic, cmap="gray")
# Foreground: only the voxels selected by the mask, everything else made
# transparent via a masked array, so you can see the mask sitting directly
# on top of the anatomy it was computed from.
ax.imshow(np.ma.masked_where(mask_mosaic == 0, mask_mosaic), cmap="autumn", alpha=0.6)
ax.axis("off")
ax.set_title("'thick' mask (orange) over the reference epi, all slices")
plt.show()

###############################################################################
# 4. From masked voxels to a cortex.Volume
# -------------------------------------------
# This is the step the mask actually exists for: pycortex's ``Volume`` object
# accepts data as a flat 1D array with exactly one value per ``True`` voxel
# in a mask, and stitches it back into 3D using the mask before mapping it
# onto the cortical surface for display. So a real analysis pipeline would
# put its statistic (betas, r2, t-values, ...) in this same 1D shape, one
# entry per masked voxel, in the same voxel order as ``thick_mask``.
#
# Here we stand in for "real" data with random noise, just to demonstrate
# the plumbing -- one random value per voxel that survived the mask, nothing
# more.
fake_data = np.random.randn(thick_mask.sum())

# Passing mask=thick_mask explicitly (rather than just letting Volume guess
# a mask from the data's length) is the same thing that happens implicitly
# whenever you pass a 1D array to Volume: it's finding/loading exactly this
# mask under the hood to know how to unfold your 1D array back into the 3D
# volume before resampling it onto the surface.
vol = cortex.Volume(
    fake_data, subject, xfmname, mask=thick_mask,
    cmap="RdBu_r", vmin=-3, vmax=3,
)

cortex.quickshow(vol, with_curvature=True, with_colorbar=True)
plt.show()

###############################################################################
# From here, swapping ``fake_data`` for a real 1D statistic computed on the
# same masked voxels (e.g. from ``mask.sum()``-length model weights or
# scores) is the whole recipe for getting volumetric fMRI results onto a
# pycortex flatmap or 3D surface.
