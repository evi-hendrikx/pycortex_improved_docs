====================
Surface Segmentation
====================

Pycortex does not implement its own segmentation — that's a hard, mature
problem already solved by dedicated tools. It wraps FreeSurfer_, which
performs the segmentation and produces per-vertex-corresponding pial/white
matter surfaces automatically (imperfectly — manual correction is usually
still needed, covered below). What pycortex *does* own is everything
downstream of that: importing the result into the :doc:`database`, and
:doc:`cutting and flattening <flattening>` the surface. This page describes
how to do the segmentation using FreeSurfer.

.. _FreeSurfer: http://surfer.nmr.mgh.harvard.edu/




**Unpacking Data, Importing data, & Starting Freesurfer Unpacking Data**

If you have raw data, you want to unpack the .tar back to multiple dcm files. To do this, into terminal type:

       ``tar xvf filename.tar``


If possible, you want to proceed with MEMPRAGE RMS data.




Starting & Setting up Freesurfer
##################################


To open freesurfer:
    ``source_directory_name_here/SetUpFreeSurfer.sh``

For example:
    ``/auto/myfolder/freesurfer/SetUpFreeSurfer.sh``

Create a "subjects" directory. If a "subjects" directory doesn't exist, make one in the FreeSurfer directory. Freesurfer is finicky about directories, so this step is crucial.




Importing Data Into Freesurfer
#################################

After you've unpacked the raw data, there are 2 ways to choose from to import your data to into freesurfer:

**1. Using .dcm files:** To do this, go into the directory of the dicom files you want to use and then type:
    ``recon-all -i ./NameofFirstDicomFile.dcm -s <subject_name>``
For example:
    ``recon-all -i ./000000-01-1.dcm -s Subject``

In this case, you just give Freesurfer the name of the very first dicom file in the directory, and it will find the rest of them.

**2. Using .nii or .mgz files:** you can type:
    ``recon-all -i /name/name/name/name/name.nii -s <subject_name>``

For example:
    ``/auto/myfolder/anatomy/Subject/Subject_t1_nii -s Subject``

The '-s Subject' portion creates a folder, in this case a folder titled "Subject". The folder should be named for the subject.



Creating Pial & White Matter Surfaces
###########################################

Now that the anatomical data for your subject has been imported into Freesurfer and a new
directory has been created, you next want to run a command called autorecon1 to separate
the brain from the rest of the anatomy (eyes, muscle, etc.), and then manually check for and
correct potential errors. Next, you will need to determine the surfaces of the brain – both the
pial surface as well as the white matter. This is done using the command autorecon2.
Following this, you will manually make edits to these newly created surfaces.


Autorecon1: Separating Brain from Other Anatomy
***************************************************

The autorecon1 command motion corrects and conforms, normalizes, computes the Talairach transform, and strips the skull. Keep in mind that this command takes approximately 30-40 minutes, so make sure you're ready before running it. To use the command type:

    ``recon-all -autorecon1 -s <subject_name>``

For example:
    ``recon-all -autorecon1 -s Subject``


Manual Edits to the Anatomical
--------------------------------

At this stage, you just want to make sure that autorecon1 ran successfully and that large parts
of non-brain anatomy were not left behind. If big chunks of eye or skull were left behind, it is
good to manually delete them yourself. If autorecon1 ran successfully, you can probably skip
manual editing even if some anatomy was left behind since the next step, autorecon2, is quite
accurate at determining brain surfaces even if non-brain anatomy was left behind. However, it's good to double check that everything worked out.

To pull up the current segmentation and surfaces for manual review and
editing, use ``cortex.segment.edit_segmentation`` (the older
``cortex.segment.fix_wm``/``fix_pia`` — a Mayavi + tkmedit combination —
are deprecated in current pycortex in favor of this)::

    import cortex
    cortex.segment.edit_segmentation('Subject')

This opens FreeSurfer's **FreeView** with the subject's ``aseg.mgz``,
``brainmask.mgz``, and ``wm.mgz`` volumes loaded alongside the
white-matter (``smoothwm``, outlined in yellow) and pial (outlined in
blue) surface contours, so you can see the current segmentation and both
surfaces together and edit whichever volume needs correcting. At this
stage you're mainly looking for leftover skull or eye tissue and deleting
it. See FreeView's own documentation for its voxel-editing tools — they
differ from the older tkmedit interface these docs used to describe, and
we don't want to describe FreeView mechanics here without having verified
them directly.

When you're done and have saved your edits in FreeView, tell FreeSurfer to
regenerate the surfaces from your edited mask — ``edit_segmentation``
prints the exact command to use once you close FreeView, which will be
one of::

    cortex.segment.run_freesurfer_recon('Subject', 'wm')   # after editing wm.mgz
    cortex.segment.run_freesurfer_recon('Subject', 'pia')  # after editing brainmask.mgz



Autorecon2: Creating Surfaces
***********************************

Here, you will be creating both white and gray matter surfaces using the autorecon2
command. When the command is complete, there will be outlines on the brain indicating that
the program has determined where the pial and white matter surfaces are located. The pial
surface will be outlined in red, and the white matter surface will be outlined in both green and
yellow when it is finished running.

Type in the command:
    ``recon-all -autorecon2 -s <subject_name>``

*This will take up to 5 hours!*

|

Although at this stage Freesurfer has completed determining where the white matter and pial
surfaces are, it is not completely accurate, so next edits have to be made to correct these
mistakes. This is the most time-consuming part of the brain segmentation.

First fix big mistakes in the white matter surface. These include large swaths of gray matter
being identified as white matter when it shouldn't, and when big portions of white matter are
not labeled as white matter when they should be. The command to make these edits is the same as above::

    import cortex
    cortex.segment.edit_segmentation('Subject')

then, once you're satisfied with your edits to ``wm.mgz`` in FreeView::

    cortex.segment.run_freesurfer_recon('Subject', 'wm')

We'll look through the results of autorecon2, examining the white matter and pial surfaces as
loaded by FreeView. This can be a lengthy process; because it's an entirely nonverbal task, I recommend listening to podcasts as you go.

You want to make sure to delete voxels from ``wm.mgz`` that the white-matter outline
encompasses that it shouldn't (such as gray matter and/or leftover pieces of eye or skull),
as well as add voxels to regions that appear to have white matter but aren't included in the
outline.

Autorecon on the white matter surface (``run_freesurfer_recon(subject, 'wm')``) should take about 2-4 hours. These manual edits are an iterative process; when it's done, go back and look over the 3D surface, and make any changes that seem necessary. New spikes can appear in unexpected places, so three or four iterations may be needed, probably more if you are just starting to learn how to do it.
