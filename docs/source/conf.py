#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Happypanda X documentation build configuration file, created by
# sphinx-quickstart on Sat Feb 25 19:36:02 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import importlib
import inspect
import os
import sys
import sphinx_bootstrap_theme
import collections
from sphinx.util import inspect as sinspect
from sphinx_autodoc_napoleon_typehints import process_docstring
from sphinx.ext.napoleon import Config, docstring
from os.path import basename
from io import StringIO
from docutils.parsers.rst import Directive
from docutils import nodes, statemachine

sys.path.insert(0, os.path.realpath(os.path.join('..', '..')))

import happypanda
from happypanda.core import command
from happypanda.common import constants

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosectionlabel',
    'sphinxcontrib.documentedlist',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_napoleon_typehints',
    'sphinxcontrib.autoprogram'
    ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'HappyPanda X'
copyright = 'Twiddly'
author = 'Twiddly'

rst_prolog = """
.. |async command| replace:: **Async function** -- This function returns a ``command id``.
    Retrieve the value of the function with :meth:`.get_command_value`.
    See :ref:`Asynchronous Commands` for more information.

.. |python version| replace:: Python 3.6

.. |temp view| replace:: **Temporary View** -- This function puts objects in a temporary view.
    Use the returned ``view id`` with :func:`.temporary_view` to retrieve the objects.
"""

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

#
# The short X.Y version.
version = ".".join([str(x) for x in constants.version])+"#"+str(constants.build)
# The full version, including alpha/beta/rc tags.
release = ".".join([str(x) for x in constants.version])+"#"+str(constants.build)

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
todo_link_only = True

add_module_names = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

html_logo = "_static/hpx_logo.svg"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    #'analytics_code': 'UA-00000000-1',
    'navbar_site_name': "Contents",
    'navbar_pagenav': False,
    'source_link_position': "footer",
    'bootswatch_theme': "paper",
}

html_sidebars = {'**': ['localtoc.html']}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'HappyPandaXdoc'

html_use_smartypants = True
html_show_sourcelink = False

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'HappyPandaX.tex', 'HappyPanda X Documentation',
     'Twiddly', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'happypandax', 'HappyPanda X Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'HappyPandaX', 'HappyPanda X Documentation',
     author, 'HappyPandaX', 'One line description of project.',
     'Miscellaneous'),
]


class ExecDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = True

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get('tab-width', self.state.document.settings.tab_width)
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
        try:
            exec('\n'.join(self.content))
            text = sys.stdout.getvalue()
            for n, t in enumerate(reversed(text.split('\n'))):
                lines = statemachine.string2lines(t, tab_width, convert_whitespace=True)
                self.state_machine.insert_input(lines,
                                                self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1 + n))
            return []
        except Exception:
            return [nodes.error(None, nodes.paragraph(text = "Unable to execute python code at %s:%d:" % (basename(source), self.lineno)), nodes.paragraph(text = str(sys.exc_info()[1])))]
        finally:
            sys.stdout = oldStdout

def setup(app):
    app.add_directive('exec', ExecDirective)

def autosummary_doc(module):
    """
    Recursive autosummary that retrieves classes and functions from given module
    """

    print(f".. currentmodule:: {module}")

    s = f"""
    .. autosummary::
        :nosignatures:

    """
    sum_str = inspect.cleandoc(s)

    mod = importlib.import_module(module) 
    for name, obj in inspect.getmembers(mod, inspect.isclass) + inspect.getmembers(mod, inspect.isfunction):
        if not obj.__name__.startswith('_') and obj.__module__ == mod.__name__:
            sum_str += f"   {name}\n"

    print(sum_str)

def command_doc(module):
    """
    Document command classes
    """

    mod = importlib.import_module(module)

    print(".. automodule:: {}".format(module))

    config =  Config()
    cls_str = """.. py:function:: {}{}
    {}

        .. rubric:: Available entries:

    {}  

        .. rubric:: Available events:

    {}

    """

    cmd_str = """.. py:function:: {}{}
    {}
    """

    cls_str = inspect.cleandoc(cls_str)
    cmd_str = inspect.cleandoc(cmd_str)

    def indent_text(txt, num=4):
        return "\n".join((num * " ") + i for i in txt)

    def doc_process(docstr, obj, retval=True, indent=4,
                        config=config, docstring=docstring,
                        inspect=inspect, process_docstring=process_docstring,
                        indent_text=indent_text):
        docstr = docstring.GoogleDocstring(inspect.cleandoc(docstr), config, obj=obj)
        docslines = str(docstr).splitlines()
        process_docstring(None, '', '', obj, config, docslines)
        if docslines:
            r = docslines.pop(0)
            # put rtype last
            if retval:
                docslines.append(r)

        # indent
        if indent:
            docstr = indent_text(docslines, indent)
        else:
            docstr = "\n".join(docslines)
        return docstr

    try:
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if not obj.__name__.startswith('_') and obj.__module__ == mod.__name__ and issubclass(obj, command.CoreCommand):
                if getattr(obj, 'main', False):
                    objfunc = obj.main
                else:
                    objfunc = obj.__init__


                sig = sinspect.Signature(objfunc, bound_method=True)
                obj._get_commands()
                entries = []
                events = []
                e_objfunc = None
                for x, e in sorted(obj._entries.items()):
                    esig = sinspect.Signature(objfunc)
                    esig.signature = e.signature

                    ex_local = {'happypanda': happypanda, 'collections': collections}
                    ex_local.update(mod.__dict__)
                    ex_local.update(globals())
                    exec("def e_objfunc{}:None".format(esig.signature), ex_local, ex_local)
                    e_objfunc = ex_local['e_objfunc']

                    entries.append("    - {}".format(cmd_str.format(x, esig.format_args(), str(doc_process(e.__doc__, e_objfunc, False, indent=8)))))

                for x, e in sorted(obj._events.items()):

                    esig = sinspect.Signature(objfunc)
                    esig.signature = e.signature

                    ex_local = {'happypanda': happypanda, 'collections': collections}
                    ex_local.update(mod.__dict__)
                    ex_local.update(globals())
                    exec("def e_objfunc{}:None".format(esig.signature), ex_local, ex_local)
                    e_objfunc = ex_local['e_objfunc']

                    events.append("    - {}".format(cmd_str.format(x, esig.format_args(), str(doc_process(e.__doc__, e_objfunc, False, indent=8)))))

                retval = sig.signature.return_annotation
                sig.signature = sig.signature.replace(return_annotation=inspect.Signature.empty)


                docstr = doc_process(obj.__doc__, objfunc)

                print(cls_str.format(name, sig.format_args(), str(docstr), '\n'.join(entries), '\n'.join(events)))
    except Exception:
        w = """
        .. error::
            {}
        """.format(module)
        print(inspect.cleandoc(w))


