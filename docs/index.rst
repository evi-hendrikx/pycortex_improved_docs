Pycortex Documentation
======================

.. image:: 3dhead.png
    :width: 85%
    :align: center

Pycortex is a software package for generating beautiful interactive 3D visualizations of fMRI data projected onto cortical surface models. It can also generate high quality 2D flattened cortical visualizations.

New to pycortex? Start with the :doc:`overview` page for the mental model, and the :doc:`glossary` for terms used throughout these docs.

.. _which-page:

Which page do I need?
---------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - I want to...
     - Go to...
   * - Understand pycortex's vocabulary before reading further
     - :doc:`glossary`
   * - Turn a FreeSurfer subject into pycortex surfaces (segmentation,
       cutting, flattening)
     - :doc:`segmentation_guide`
   * - Understand what's stored in the filestore / browse an existing
       subject's data
     - :doc:`database`
   * - Register a functional scan to a subject's anatomy
     - :doc:`align` and :doc:`transforms`
   * - Define and use regions of interest
     - :doc:`rois` (SVG/Inkscape workflow) and :doc:`roidraw` (in-browser
       drawing add-on)
   * - Render a static 2D image of data on a flatmap
     - :doc:`api_reference_flat` (``cortex.quickflat``) and the
       :doc:`auto_examples/index`
   * - Get an interactive 3D/flat viewer
     - :doc:`userguide/webgl`
   * - Pick colors for 1D or 2D data
     - :doc:`colormaps`
   * - See real, runnable end-to-end code
     - :doc:`auto_examples/index`
   * - Try optional extras and new additions
     - The Features section in the sidebar, e.g.
       :doc:`features/camera_views_animations` and
       :doc:`features/bumpy_flatmap`


.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Getting started

   overview
   install

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Setting up subjects

   segmentation_guide
   database
   align
   transforms

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Visualizing data

   dataset
   colormaps
   userguide/webgl

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: ROIs

   rois
   roidraw

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Example gallery

   auto_examples/index

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Features

   features/camera_views_animations
   features/bumpy_flatmap

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Reference

   glossary
   api_reference_flat
   indices

Citation
--------
If you use pycortex in published work, please cite the `pycortex paper <http://dx.doi.org/10.3389/fninf.2015.00023>`_:

*Gao JS, Huth AG, Lescroart MD and Gallant JL (2015) Pycortex: an interactive surface visualizer for fMRI. Front. Neuroinform. 9:23. doi: 10.3389/fninf.2015.00023*


For a list of recent changes, please see the `releases on GitHub <https://github.com/gallantlab/pycortex/releases/>`_.

This documentation is still under development. Please report errors or bugs at https://github.com/gallantlab/pycortex/issues.
