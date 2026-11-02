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
   * - Set up a new subject from scratch
     - :doc:`subject_setup`
   * - Build and edit surfaces with FreeSurfer
     - :doc:`segmentation_guide`
   * - Cut and flatten surfaces into flatmaps
     - :doc:`flattening`
   * - Bring in surfaces, data or transforms from FreeSurfer, fMRIPrep, HCP,
       fsaverage, AFNI, BrainVoyager, FSL or SPM
     - :doc:`importing_other_software`
   * - Understand what's stored in the filestore / browse an existing
       subject's data
     - :doc:`database`
   * - Register a functional scan to a subject's anatomy
     - :doc:`align` and :doc:`transforms`
   * - Define and use regions of interest
     - :doc:`rois` (SVG/Inkscape workflow) and :doc:`roidraw` (in-browser
       drawing add-on)
   * - Render a static 2D image of data on a flatmap
     - :doc:`quickflat`
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
   database
   align
   transforms
   masks

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Visualizing data

   dataset
   quickflat
   userguide/webgl
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
