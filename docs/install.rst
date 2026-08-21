Installation
============

To install the stable release version of pycortex, do the following::

    # First, install some required dependencies
    pip install -U setuptools wheel numpy cython
    # Install the latest release of pycortex from pip
    pip install -U pycortex


If you wish to install the development version of pycortex, you can install it directly from Github.

To do so, replace the second install line above with the following::

    # Install development version of pycortex from github
    pip install -U git+https://github.com/gallantlab/pycortex.git

Optional Dependencies
---------------------
For some functionality, you will also need to install Inkscape_, using whatever method is appropriate for your system.

On Mac OS X you will also need to enable access to Inkscape on the command line, see these instructions_.

.. _Inkscape: https://inkscape.org/en/
.. _instructions: http://wiki.inkscape.org/wiki/index.php/Mac_OS_X#Inkscape_command_line

Demo
----
To test if your install went well, you can run the pycortex demo.

Pycortex is best used with IPython_

If you do not already have IPython, you can install it by running::

    pip install ipython

To run the pycortex demo, using IPython, run::

    $ ipython
    In [1]: import cortex
    In [2]: cortex.webshow(cortex.Volume.random("S1", "fullhead"))

If everything went well, this should pop up a web browser window with a demo subject.

For an explanation of what ``Volume``, ``webshow``, and the ``"fullhead"`` transform name mean, and where to go next, see :doc:`overview`.

.. _IPython: http://www.ipython.org/

Basic Configuration
-------------------
Pycortex will automatically create a database filestore when it is first installed. In Linux, this filestore is located at :file:`/usr/local/share/pycortex/`. On first import, it will also create a configuration file in your user directory which allows you to specify additional options, including alternate filestore locations. In Linux, this user configuration file is located in :file:`~/.config/pycortex/options.cfg`.

You can check the location of the filestore after installing by running::

    import cortex
    cortex.database.default_filestore

And you can check the location of the config file by running::

    import cortex
    cortex.options.usercfg

If you want to move the filestore, you need to update the config file::

   [basic]
   filestore=/abs/path/to/filestore

Troubleshooting
----------------

pycortex itself is pure Python, but several features shell out to
external neuroimaging tools it doesn't bundle — FreeSurfer, FSL, Blender,
Inkscape. Most install problems people actually hit are one of these:

* ``KeyError: 'SUBJECTS_DIR'`` (or a FreeSurfer command failing oddly) —
  FreeSurfer-backed functions like :doc:`segmentation_guide`'s
  ``cortex.segment.edit_segmentation`` and :doc:`align`'s
  ``cortex.align.manual``/``automatic`` read the ``$SUBJECTS_DIR``
  environment variable directly (the same variable FreeSurfer itself
  uses); if it isn't exported in the shell you launched Python from,
  these fail. Set it the same way you would for any FreeSurfer command
  (``export SUBJECTS_DIR=/path/to/freesurfer/subjects``) before starting
  Python/IPython.
* ``bbregister``/``mri_coreg``/``freeview``/``lta_convert``/``flirt`` not
  found — these are FreeSurfer and FSL commands, not pycortex code; make
  sure both are installed and on your ``PATH`` (``which bbregister``,
  ``which flirt``) in the same shell you launch Python from.
* FSL commands found, but automatic alignment (``cortex.align.automatic_fsl``
  / ``autotweak``) still fails — if FSL was installed via NeuroDebian,
  its binaries may be named e.g. ``fsl5.0-flirt`` instead of ``flirt``.
  Set ``fsl_prefix`` in your ``options.cfg``'s ``[basic]`` section (e.g.
  ``fsl_prefix = fsl5.0-``) to match.
* Inkscape/Blender/SLIM/meshlab "not found" even though they're
  installed — pycortex looks for these under the plain command names
  (``inkscape``, ``blender``) by default, configurable in
  ``options.cfg``'s ``[dependency_paths]`` section. On macOS in
  particular, these are usually not on ``PATH`` by default and need the
  full path to the app's binary, e.g.
  ``blender = /Applications/Blender/blender.app/Contents/MacOS/blender``.
* Data/subject not showing up in ``cortex.db`` — usually means it's in a
  different filestore than the one pycortex is currently pointed at;
  double check the location printed by
  ``cortex.database.default_filestore`` above against where you expect
  your data to be.
