Bumpy flatmap
=============

The ``bumpy_flatmap`` surface control in the :doc:`/userguide/webgl` gives
the flatmap relief.

Unfolding towards a flatmap drives illumination to fully uniform and
specularity to zero, since a flat sheet has no shape for directional lighting to
reveal. Turning on ``bumpy_flatmap`` gives the flatmap real relief again:
unfolding then drives top-left lighting to 1 instead, which is the direction
that reads as shaded relief. Like ``pivot``, the sliders move to show the values
in effect and can still be dragged afterwards; the next change to ``unfold`` or
``bumpy_flatmap`` drives them back from the configured defaults.

The relief is the shape a slab of cortex would take if it were peeled off the
white matter and laid flat: thicker where the pia carries more area than the
white matter beneath it, which is over a gyral crown, and thinner in a sulcal
fundus. See :class:`cortex.polyutils.FlatSlab` for the quantity and
:mod:`cortex.polyutils.bumpy` for why it is that one. It costs a few seconds
per hemisphere and is cached in the subject's database entry like any other
surface info.

``bumpy_flatmap_scale`` exaggerates the relief, and is a slider in the surface
controls as well as a setting. At 1.0 the bumps are at their true scale, which
for a 2-5 mm slab is subtle next to a whole flatmap, so the default exaggerates
somewhat; larger values make the folding easier still to read. The relief is
purely vertical, so this is vertical exaggeration as on a topographic map and
turning it up does not move anything sideways relative to the data drawn
underneath. The shading follows, since a height
field scaled by *s* has a normal whose in-plane components scale by *s* and
whose out-of-plane component does not. The slider starts wherever the
configuration file put it, and runs from 0 to five times true scale -- or to
twice the configured value if that is already higher. It does nothing while
``bumpy_flatmap`` is off, since there is no relief to scale. Being a display
setting, it does not invalidate the cached geometry, so it can be dragged
around freely.

The relief appears over the second half of the unfold, between the inflated
surface and the flatmap, and the anatomical and inflated surfaces are untouched
by it. The offsets are in the flatmap's own coordinates, which have no meaning
on a folded surface.
