# Sphinx configuration for documenting cube.py
# This is the main configuration file for Sphinx.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

project = 'twisty'
author = 'bfxdev'
release = '2025'

extensions = [
    'myst_parser',
    'autodoc2',
    'sphinx_rtd_theme',
]

# See https://myst-parser.readthedocs.io/en/v0.13.3/using/syntax-optional.html
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# autodoc2 config
autodoc2_packages = [
    "../cube.py",
]
autodoc2_render_plugin = "myst"
autodoc2_output_dir = "api"

#html_theme = 'alabaster'
#html_theme = 'classic'
html_theme = 'sphinx_rtd_theme'

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]
