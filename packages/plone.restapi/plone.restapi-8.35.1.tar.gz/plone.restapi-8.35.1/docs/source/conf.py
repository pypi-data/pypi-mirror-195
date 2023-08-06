# plone.restapi documentation build configuration file, created by
# sphinx-quickstart on Mon Apr 28 13:04:12 2014.
#
# This file is execfile()d with the current directory set to its containing
# dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath("."))
import os
import sys
import datetime

sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

# General information about the project.
project = "plone.restapi"
thisyear = datetime.datetime.now().year
copyright = "2014-%s, Plone Foundation" % thisyear

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# TODO: There must be a way to import this from `setup.py` so we don't have to
# update it manually for each release.
version = "8.24.2.dev0"
release = version

# -- General configuration ----------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom ones.
extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinxcontrib.httpdomain",
    "sphinxcontrib.httpexample",
]


def patch_pygments_to_highlight_jsonschema():
    """Append "application/json+schema" to the list of mimetypes the
    Pygments JSON lexer is registered to handle.
    """
    try:
        from pygments.lexers._mapping import LEXERS

        mod, lexer_name, aliases, filenames, mimetypes = LEXERS["JsonLexer"]
        mimetypes = mimetypes + ("application/json+schema",)
        LEXERS["JsonLexer"] = (mod, lexer_name, aliases, filenames, mimetypes)
    except:
        # Be defensive (don't fail a docs build if this doesn't work)
        pass


# The suffix of source filenames.
# source_suffix = ".rst"
source_suffix = {
    ".md": "markdown",
    ".rst": "reStructuredText",
}


# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ""
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = "%B %d, %Y"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = ["*ideas/*"]

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, "()" will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# Options for the linkcheck builder
# Ignore localhost
linkcheck_ignore = [
    r"https://coveralls.io/repos/github/plone/plone.restapi/badge.svg\?branch=master",  # plone.restapi
    r"https://github.com/plone/plone.restapi/blob/dde57b88e0f1b5f5e9f04e6a21865bc0dde55b1c/src/plone/restapi/services/content/add.py#L35-L61",  # plone.restapi
]


# -- Intersphinx configuration ----------------------------------

# This extension can generate automatic links to the documentation of objects
# in other projects. Usage is simple: whenever Sphinx encounters a
# cross-reference that has no matching target in the current documentation set,
# it looks for targets in the documentation sets configured in
# intersphinx_mapping. A reference like :py:class:`zipfile.ZipFile` can then
# linkto the Python documentation for the ZipFile class, without you having to
# specify where it is located exactly.
#
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
#
intersphinx_mapping = {
    "plone": ("https://6.docs.plone.org/", None),
    "python": ("https://docs.python.org/3/", None),
    "training": ("https://training.plone.org/5/", None),
}


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://plonerestapi.readthedocs.org/"
ogp_description_length = 200
ogp_image = "https://6.docs.plone.org/_static/Plone_logo_square.png"
ogp_site_name = "plone.restapi Documentation"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]


# -- sphinx_copybutton -----------------------
copybutton_prompt_text = r"^ {0,2}\d{1,3}"
copybutton_prompt_is_regexp = True


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_book_theme"

html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"

html_css_files = ["custom.css", ("print.css", {"media": "print"})]

# See http://sphinx-doc.org/ext/todo.html#confval-todo_include_todos
todo_include_todos = True

html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/plone/plone.restapi",
    "repository_branch": "master",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "extra_navbar": """
    <p class="ploneorglink">
        <a href="https://plone.org">
            <img src="/_static/logo.svg" alt="plone.org" /> plone.org</a>
    </p>""",
    "extra_footer": """<p>The text and illustrations in this website are licensed by the Plone Foundation under a Creative Commons Attribution 4.0 International license. Plone and the Plone® logo are registered trademarks of the Plone Foundation, registered in the United States and other countries. For guidelines on the permitted uses of the Plone trademarks, see <a href="https://plone.org/foundation/logo">https://plone.org/foundation/logo</a>. All other trademarks are owned by their respective owners.</p>
    <p><a href="https://www.netlify.com">
  <img src="https://www.netlify.com/img/global/badges/netlify-color-bg.svg" alt="Deploys by Netlify" />
</a></p>""",
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "%(project)s v%(release)s" % {"project": project, "release": release}

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_extra_path = [
    # "robots.txt",
]

# If not "", a "Last updated on:" timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = "%b %d, %Y"

# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# Announce that we have an opensearch plugin
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch
html_use_opensearch = "https://plonerestapi.readthedocs.org/"


# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://plonerestapi.readthedocs.org/"


# -- Options for HTML help output -------------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "plonerestapidoc"


# -- Options for myST markdown conversion to html -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "deflist",  # You will be able to utilise definition lists
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "linkify",  # Identify “bare” web URLs and add hyperlinks.
    "colon_fence",  # You can also use ::: delimiters to denote code fences,\
    #  instead of ```.
    "substitution",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2
]

myst_substitutions = {
    "postman_basic_auth": "![](../_static/img/postman_basic_auth.png)",
    "postman_headers": "![](../_static/img/postman_headers.png)",
    "postman_request": "![](../_static/img/postman_request.png)",
    "postman_response": "![](../_static/img/postman_response.png)",
    "postman_retain_headers": "![](../_static/img/postman_retain_headers.png)",
    "fawrench": '<span class="fa fa-wrench" style="font-size: 1.6em;"></span>',
}

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    # The paper size ("letterpaper" or "a4paper").
    # "papersize": "letterpaper",
    # The font size ("10pt", "11pt" or "12pt").
    # "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    # "preamble": "",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    (
        "index",
        "plonerestapi.tex",
        "plone.restapi Documentation",
        "Plone Foundation",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", "plonerestapi", "plone.restapi Documentation", ["Plone Foundation"], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "plonerestapi",
        "plone.restapi Documentation",
        "Plone Foundation",
        "plonerestapi",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: "footnote", "no", or "inline".
# texinfo_show_urls = "footnote"

suppress_warnings = ["image.nonlocal_uri"]

patch_pygments_to_highlight_jsonschema()
