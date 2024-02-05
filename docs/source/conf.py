project = 'File Processing'
project_copyright = '2024, hc-sc-ocdo-bdpd'
author = 'hc-sc-ocdo-bdpd'


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx_inline_tabs",
    "myst_parser"
]

templates_path = ['_templates']
exclude_patterns = []


html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['css/fonts.css']
html_title = "File Processing"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#702963",
        "color-brand-content": "#702963",
    },
    "dark_css_variables": {
        "color-brand-primary": "#D7BFDC",
        "color-brand-content": "#D7BFDC",
        "color-background-primary": "#242424"
    },
}
