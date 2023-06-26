# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os, shutil, sys, glob


def replace_line(w_detect=None, w_replace=None, f_loc=None, f_extension='*.rst'):

    init_dir = os.getcwd()
    os.chdir(f_loc)

    rsts = glob.glob(f_extension)

    content_old = []
    for rst in rsts:
        with open(rst, 'r', encoding='utf-8') as filein:
            for line in filein.readlines():
                if w_detect in line:
                    line = w_replace
                content_old.append(line)
        content_new = ''.join(content_old)

        with open(rst, 'w', encoding='utf-8') as fileout:
            fileout.write(content_new)
    os.chdir(init_dir)


def copy_misc_to_static():

    curdir = os.getcwd()
    newdir = curdir + '/_static'
    os.chdir("..")
    os.chdir("../misc")
    misc_dir = os.getcwd()
    shutil.copytree(misc_dir, newdir, dirs_exist_ok=True)
    os.chdir(curdir)


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# https://stackoverflow.com/questions/53668052/sphinx-cannot-find-my-python-files-says-no-module-named
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))

copy_misc_to_static()

# auto-generation codes
# GasComressibility-py/docs> sphinx-apidoc -f -o ./source ../src
# sphinx-apidoc -SPHINX_APIDOC_OPTIONS ['members', 'undoc-members']  -o ./source ../src

# -- Project information -----------------------------------------------------

project = 'GasCompressibility-py'
copyright = '2023, Eric Kim'
author = 'Eric Kim'

# The full version, including alpha/beta/rc tags
release = '0.1.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',  # adds [source] link next to each methods
    'sphinx.ext.autosummary',
#    'numpydoc',
#    'sphinx_automodapi.automodapi',
    'myst_parser',  # git install myst_parser
]

# Autosummary article:
# https://stackoverflow.com/questions/2701998/automatically-document-all-modules-recursively-with-sphinx-autodoc/62613202#62613202
# https://romanvm.pythonanywhere.com/post/autodocumenting-your-python-code-sphinx-part-ii-6/


################## Run "html make" with True once, and then change to False and run again ########################

generate_rsts = False
autosummary_generate = False

try:
    curdir = os.getcwd()
    os.chdir("..")
    shutil.rmtree(os.getcwd() + '\\build\\html')
except:
    pass

if generate_rsts:
    autosummary_generate = True

    try:
        shutil.rmtree(os.getcwd() + '\\docs\\source\\functions')
    except:
        pass
else:
    autosummary_generate = False
    #replace_line(w_detect='__init__', w_replace='', f_loc="..\\source\\functions")
    #replace_line(w_detect='.. autosummary::', w_replace='   .. autosummary::\n      :nosignatures:\n',
    #             f_loc="..\\source\\functions")




#################################################################################

#autoclass_content = "class"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']



from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary import get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr
import re



#############################################

source_suffix = ['.rst', '.md']

# http://www.pythondoc.com/sphinx/ext/math.html

latex_engine = 'xelatex'
latex_elements = {
    'fontpkg': r'''
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex',
}
latex_show_urls = 'footnote'


#############################




