# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os, shutil, sys, glob, ast


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


def exclude_builtin_methods(arr):
    return [item for item in arr if '__' not in item]


def exclude_private_methods(arr):
    return [item for item in arr if not item.startswith('_')]


def write_class_methods_to_rst(file_dir=None, write_dir=None, file_name=None,):

    with open(file_dir + '\\' + file_name) as file:
        node = ast.parse(file.read())

    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

    class_method_dict = {
        class_.name: {
            'MethodsStr': [n.name for n in class_.body if isinstance(n, ast.FunctionDef)],
        } for class_ in classes
    }

    if not os.path.exists(write_dir):
        os.makedirs(write_dir)
    os.chdir(write_dir)

    for key, val in class_method_dict.items():
        raw_methods = class_method_dict[key]['MethodsStr']
        filtered_methods = exclude_builtin_methods(raw_methods)
        filtered_methods = exclude_private_methods(filtered_methods)

        for method in filtered_methods:
            method_w = '.'.join([key.lower(), key, method])
            with open(method_w + '.rst', 'w', encoding='utf-8') as fout:
                content = ".. _%s:\n" \
                          "\n" \
                          "%s\n" \
                          "=====================================\n" \
                          "\n" \
                          ".. automethod:: %s" % ('.'.join(method_w.split('.')[1:]), '.'.join(method_w.split('.')[2:]), method_w)

                fout.write(content)
                print('   ~' + method_w)

        class_method_dict[key] = filtered_methods

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html
#sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))

sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'gascompressibility\\pseudocritical')))
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'gascompressibility\\z_correlation')))

#sys.path.insert(0, os.path.abspath(os.path.join('..')))

copy_misc_to_static()

# auto-generation codes
# GasComressibility-py/docs> sphinx-apidoc -f -o ./source ../gascompressibility/pseudocritical


# sphinx-apidoc -f -o ./source ../src


# sphinx-apidoc -SPHINX_APIDOC_OPTIONS ['members', 'undoc-members']  -o ./source ../src

# -- Project information -----------------------------------------------------

project = 'GasCompressibility-py'
copyright = '2023, Eric Kim'
author = 'Eric Kim'

# The full version, including alpha/beta/rc tags
release = ''


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
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
#    'numpydoc',
#    'sphinx_automodapi.automodapi',
    'myst_parser',  # git install myst_parser
    'sphinx_design',
    'sphinx_disqus.disqus',
]
myst_enable_extensions = ["colon_fence"]
autosectionlabel_prefix_document = True
disqus_shortname = 'GasCompressibiltiyFactor-py'

################## Run "html make" with True once, and then change to False and run again ########################

generate_rsts = False

try:
    curdir = os.getcwd()
    os.chdir("..")
    shutil.rmtree(os.getcwd() + '\\build\\html')
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
    print('\\build\\html remove succeeded')
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
except:
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
    print('\\build\\html remove FAILED')
    print('+++++++++++++++++++++++++++++++++++++++++++++++')

if generate_rsts:
    autosummary_generate = True

    try:
        shutil.rmtree(os.getcwd() + '\\source\\functions')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
        print('\\source\\functions remove succeeded')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
    except:
        print(os.getcwd())
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
        print('\\source\\functions remove FAILED')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')

else:
    autosummary_generate = False

    try:
        shutil.rmtree(os.getcwd() + '\\source\\functions')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
        print('\\source\\functions remove succeeded')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
    except:
        print(os.getcwd())
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
        print('\\source\\functions remove FAILED')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')

    filedir = "C:\\Users\\EricKim\\Documents\\GasCompressibiltiyFactor-py\\gascompressibility\\pseudocritical"
    writedir = "C:\\Users\\EricKim\\Documents\\GasCompressibiltiyFactor-py\\docs\\source\\functions"

    write_class_methods_to_rst(file_dir=filedir, write_dir=writedir, file_name='Piper.py')
    write_class_methods_to_rst(file_dir=filedir, write_dir=writedir, file_name='Sutton.py')

    #replace_line(w_detect='__init__', w_replace='', f_loc="..\\source\\functions")
    #replace_line(w_detect='.. autosummary::', w_replace='   .. autosummary::\n      :nosignatures:\n',
    #             f_loc="..\\source\\functions")




#################################################################################

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
html_css_files = [
    'custom.css',
]



from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary import get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr
import re



#############################################

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

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


html_theme_options = {
   "pygment_light_style": "tango",
   "pygment_dark_style": "monokai",
    "show_nav_level": 4,
    "navigation_depth": 4
}

intersphinx_mapping = {
    'python': ('http://docs.python.org/2', None),
    'numpy': ('http://docs.scipy.org/doc/numpy', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('http://matplotlib.org/stable', None)
}

#############################

add_module_names = False

from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary import get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr
import re
"""
from sphinx.ext.autosummary.generate import AutosummaryRenderer


def smart_fullname(fullname):
    parts = fullname.split(".")
    print('-------------------')
    print(parts)
    return ".".join(parts[1:])


def fixed_init(self, app, template_dir=None):
    print('=====================')
    AutosummaryRenderer.__old_init__(self, app, template_dir)
    self.env.filters["smart_fullname"] = smart_fullname


AutosummaryRenderer.__old_init__ = AutosummaryRenderer.__init__
AutosummaryRenderer.__init__ = fixed_init
"""
