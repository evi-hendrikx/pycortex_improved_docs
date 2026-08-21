"""
This will make the colormaps.rst file for the docs page.
"""
import os

path_to_colormaps = "../filestore/colormaps/"
all_colormaps = os.listdir(path_to_colormaps)
all_colormaps.sort()
all_paths = [os.path.join(path_to_colormaps, f) for f in all_colormaps]
all_names = [f[:-4] for f in all_colormaps]

rst_lines = ["Colormaps\n",
             "=========\n",
             "\n",
             "Why 1D and 2D colormaps\n",
             "-----------------------\n",
             "\n",
             "A standard (1D) colormap maps a single value per vertex/voxel to a color,\n"
             "which is all you need for a single data array wrapped in :class:`cortex.Volume`\n"
             "or :class:`cortex.Vertex`. Sometimes, though, you want to show two related\n"
             "quantities on the same flatmap at once -- for example, an effect size *and*\n"
             "a measure of how reliable it is at each point, so weakly-supported values can\n"
             "be visually de-emphasized rather than shown with the same confidence as strong\n"
             "ones. A single 1D colormap can't encode two independent quantities in one\n"
             "color, so pycortex also supports 2D colormaps, which map a *pair* of values\n"
             "(e.g. one axis for the main value, one for its alpha/opacity or a covariate)\n"
             "to a single color. These are used together with :class:`cortex.Volume2D` /\n"
             ":class:`cortex.Vertex2D` (two related scalar fields) or :class:`cortex.VolumeRGB`\n"
             "/ :class:`cortex.VertexRGB` (precomputed RGB(A) colors, no colormap needed).\n"
             "Below, colormaps with '2D', 'alpha', or 'covar' in the name are 2D colormaps\n"
             "(shown as a 2D swatch); the rest are standard 1D colormaps (shown as a bar).\n"
             "See the demo on :doc:`overview` for a worked example, and\n"
             ":ref:`sphx_glr_auto_examples_datasets_plot_volume2D.py` /\n"
             ":ref:`sphx_glr_auto_examples_datasets_plot_vertex2D.py` for complete,\n"
             "runnable ones.\n"
             "\n"
             "There are a number of colormaps available in pycortex.\n"
             "A full list of those that can be used are below.\n"
             "\n"]

rst_file = open("colormaps.rst", "w")
for l in rst_lines:
    rst_file.write(l)

path_template = ".. image:: {path}\n"
width = "   :width: 200px\n"
height_1d = "   :height: 25px\n"
height_2d = "   :height: 200px\n"

for path, name in zip(all_paths, all_names):
    rst_file.write(name)
    rst_file.write("\n\n")
    rst_file.write(path_template.format(path=path))
    if ("2D" in name) or ("covar" in name) or ("alpha" in name):
        rst_file.write(height_2d)
    else:
        rst_file.write(height_1d)
    rst_file.write(width)
    rst_file.write("\n\n")

rst_file.close()
