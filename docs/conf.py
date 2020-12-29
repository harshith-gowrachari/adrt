import sys
import shutil

# Project information
project = "adrt"
copyright = "2020, Karl Otness, Donsub Rim"
author = "Karl Otness, Donsub Rim"

try:
    import adrt

    version = adrt.__version__
except ImportError:
    pass

# Other configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "matplotlib.sphinxext.plot_directive",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"]
suppress_warnings = ["epub.unknown_project_files"]

# Theme
html_theme = "sphinx_rtd_theme"

# Autodoc configuration
autodoc_mock_imports = []

# Napoleon configuration
napoleon_google_docstring = False

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# Matplotlib plot directive configuration
plot_formats = [("png", 100), ("hires.png", 200)]
plot_rcparams = {
    "savefig.bbox": "tight",
}
plot_apply_rcparams = True
plot_include_source = True
plot_html_show_source_link = False
plot_pre_code = """
import numpy as np
from matplotlib import pyplot as plt
import adrt
"""


# Image converter settings
def adrt_magick_available():
    if sys.platform == "win32":
        return shutil.which("magick") is not None
    return shutil.which("convert") is not None


if adrt_magick_available():
    extensions.append("sphinx.ext.imgconverter")
