# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'twisty'
copyright = '2025'
author = 'bfxdev'

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx.ext.autodoc",
    "sphinxcontrib.mermaid"
]

autodoc2_packages = [
    "../cube.py",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
#html_static_path = ['_static']

# -- MyST configuration ------------------------------------------------------

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "restructuredText",
]
