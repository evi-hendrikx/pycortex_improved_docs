Pycortex Documentation
======================

.. image:: 3dhead.png
    :width: 85%
    :align: center

Pycortex is a software package for generating beautiful interactive 3D visualizations of fMRI data projected onto cortical surface models. It can also generate high quality 2D flattened cortical visualizations.

New to pycortex? Start with the :doc:`overview` page for the mental model, and the :doc:`glossary` for terms used throughout these docs.

.. _which-page:

Where do I start?
-----------------

Every page is listed in the sidebar. Where to begin depends on what you
already have:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - I have...
     - Start at...
   * - Nothing yet, and want to see pycortex work
     - :doc:`install`, then
       :ref:`sphx_glr_auto_examples_quickstart_plot_pipeline_overview.py`
       with the bundled ``S1`` subject
   * - An anatomical scan, but no surfaces
     - :doc:`subject_setup`
   * - Surfaces from FreeSurfer, fMRIPrep, HCP, fsaverage or another tool
     - :doc:`importing_other_software`
   * - A pycortex subject and functional data
     - :doc:`align`, then :doc:`dataset`
   * - Data in a ``Volume`` or ``Vertex``, ready to plot
     - :doc:`quickflat` or :doc:`webgl`
   * - A function name to look up
     - :doc:`api_reference_flat`
   * - Used pycortex before, and want to see what's new
     - The Features section in the sidebar, e.g.
       :doc:`features/camera_views_animations` and
       :doc:`features/bumpy_flatmap`


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Getting started

   overview
   install

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Setting up subjects

   subject_setup
   segmentation_guide
   importing_other_software
   flattening
   align
   transforms
   masks
   database

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Visualizing data

   dataset
   mapping
   quickflat
   webgl
   colormaps

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: ROIs

   rois
   roidraw

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Example gallery

   auto_examples/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Features

   features/camera_views_animations
   features/bumpy_flatmap

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Reference

   glossary
   api_reference_flat
   indices

.. _citation:

Citation
--------
If you use pycortex in published work, please cite the `pycortex paper <http://dx.doi.org/10.3389/fninf.2015.00023>`_:

*Gao JS, Huth AG, Lescroart MD and Gallant JL (2015) Pycortex: an interactive surface visualizer for fMRI. Front. Neuroinform. 9:23. doi: 10.3389/fninf.2015.00023*


This documentation was built for pycortex version |release|. For a list of recent changes, please see the `releases on GitHub <https://github.com/gallantlab/pycortex/releases/>`_.

This documentation is still under development. Please report errors or bugs at https://github.com/gallantlab/pycortex/issues.
