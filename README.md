# `sphinxcontrib-svgbob` [![Stars](https://img.shields.io/github/stars/sphinx-contrib/svgbob.svg?style=social&maxAge=3600&label=Star)](https://github.com/sphinx-contrib/svgbob/stargazers)

*A Sphinx extension to render ASCII diagrams into SVG using [Svgbob](https://github.com/ivanceras/svgbob).*


[![Actions](https://img.shields.io/github/workflow/status/sphinx-contrib/svgbob/Test?style=flat-square&maxAge=600)](https://github.com/sphinx-contrib/svgbob/actions)
[![Codecov](https://img.shields.io/codecov/c/gh/sphinx-contrib/svgbob/master.svg?style=flat-square&maxAge=600)](https://codecov.io/gh/sphinx-contrib/svgbob)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square&maxAge=2678400)](https://choosealicense.com/licenses/mit/)
[![Source](https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=2678400&style=flat-square)](https://github.com/sphinx-contrib/svgbob/)
[![PyPI](https://img.shields.io/pypi/v/sphinxcontrib-svgbob.svg?style=flat-square&maxAge=600)](https://pypi.org/project/sphinxcontrib-svgbob)
[![Wheel](https://img.shields.io/pypi/wheel/sphinxcontrib-svgbob.svg?style=flat-square&maxAge=2678400)](https://pypi.org/project/sphinxcontrib-svgbob/#files)
[![Python Versions](https://img.shields.io/pypi/pyversions/sphinxcontrib-svgbob.svg?style=flat-square&maxAge=600)](https://pypi.org/project/sphinxcontrib-svgbob/#files)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/sphinxcontrib-svgbob.svg?style=flat-square&maxAge=600)](https://pypi.org/project/sphinxcontrib-svgbob/#files)
[![Changelog](https://img.shields.io/badge/keep%20a-changelog-8A0707.svg?maxAge=2678400&style=flat-square)](https://github.com/sphinx-contrib/svgbob/blob/master/CHANGELOG.md)
[![GitHub issues](https://img.shields.io/github/issues/sphinx-contrib/svgbob.svg?style=flat-square&maxAge=600)](https://github.com/sphinx-contrib/svgbob/issues)
[![Downloads](https://img.shields.io/badge/dynamic/json?style=flat-square&color=303f9f&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fsphinxcontrib-svgbob)](https://pepy.tech/project/sphinxcontrib-svgbob)


## 🗺️ Overview

Diagrams to be included into Sphinx documentation are commonly described
with a dedicated markup language, and converted into an image by Sphinx when
the documentation is built. However, this reduces the legibility of the
documentation source for readers that are not browsing the HTML version.

[Svgbob](https://github.com/ivanceras/svgbob) is a diagramming model implemented
in Rust that can convert ASCII diagrams into SVG. Using it allows you to:

* Keep a textual version of the diagram in your documentation, so that it remains legible.
* Render a nicer version as SVG for HTML or PDF versions of the documentation.

This Sphinx extension builds Svgbob statically and lets you use it to render
ASCII diagrams within Sphinx documentation. Since it does not require any external
dependency, it's also suitable to use on [readthedocs.org](https://readthedocs.org).


## 🔧 Installing

`sphinxcontrib-svgbob` can be installed from [PyPI](https://pypi.org/project/sphinxcontrib-svgbob/),
which hosts some pre-built CPython wheels for x86-64 Linux and OSX, as well as the code required
to compile from source:
```console
$ pip install sphinxcontrib-svgbob
```

If a Rust compiler is not available, the `setup.py` script will attempt to
install a temporary copy if the package is compiled on a UNIX system. If
it doesn't work, see the
[documentation on `rust-lang.org`](https://forge.rust-lang.org/other-installation-methods.html)
to learn how to install Rust on your machine.

Then add this extension to the Sphinx extensions in your `conf.py` file to
make the `svgbob` directive available:
```python
extensions = [
    ...,
    "sphinxcontrib.svgbob",
]
```

That's it, you're all set!

## 💡 Example

Use the `svgbob` directive in a function docstring to show a diagram of what
is being computed:

```python
def hamming(x, y):
    """Compute the Hamming distance between two strings.

    Hamming distance between two strings of equal length is the number of
    positions at which the corresponding symbols are different. For instance,
    Hamming distance for a 3-bit string can be computed visually using a
    3-bit binary cube:

    .. svgbob::
       :align: center

                         110              111                          
                            *-----------*      
                           /|          /|
                          / |     011 / |     
                     010 *--+--------*  |
                         |  | 100    |  |
                         |  *--------+--* 101
                         | /         | /
                         |/          |/
                     000 *-----------*  001


    The minimum distance between any two vertices is the Hamming distance
    between the two bit vectors (e.g. 100→011 has distance 3).

    """
```

When Sphinx (and `autodoc`) renders the docstring of this function, you'll get
the following HTML page (here shown with the [Sphinx theme for readthedocs.org](https://github.com/readthedocs/sphinx_rtd_theme)):

![example1.html.png](https://raw.githubusercontent.com/sphinx-contrib/svgbob/master/static/example1.html.png)

And yet, the `help(hamming)` will still look nice and helpful:

![example1.console.png](https://raw.githubusercontent.com/sphinx-contrib/svgbob/master/static/example1.console.png)


## 🔩 Configuration

The `svgbob` directive supports the following arguments:

- `font-size` (integer): the size of the text to be rendered, defaults to *14*.
- `font-family`: the family of the font used to render the text, defaults to *monospace*.
- `fill-color` (CSS color): the color to use to fill closed shapes.
- `stroke-color` (CSS color): the color to use to paint strokes, defaults to *black*.
- `scale` (float): the SVG scale of the figure, defaults to *8.0*.
- `align` (CSS align value): the alignment of the resulting image.
- `class` (HTML class): an arbitrary class to add to the resulting HTML element.

For instance, use the following to use Arial with size 12, to render nicer
text in the diagram blocks:

```rst
.. svgbob::
   :font-family: Arial
   :font-size: 12

   +-------+       +--------+
   | Hello |------>| World! |
   +-------+       +--------+
```

![example2.svg](https://raw.githubusercontent.com/sphinx-contrib/svgbob/master/static/example2.svg)


## 💭 Feedback

### ⚠️ Issue Tracker

Found a bug ? Have an enhancement request ? Head over to the [GitHub issue
tracker](https://github.com/sphinx-contrib/svgbob/issues) if you need to report
or ask something. If you are filing in on a bug, please include as much
information as you can about the issue, and try to recreate the same bug
in a simple, easily reproducible situation.

### 🏗️ Contributing

Contributions are more than welcome! See [`CONTRIBUTING.md`](https://github.com/sphinx-contrib/svgbob/blob/master/CONTRIBUTING.md) for more details.


## 📚 Alternatives

* [`sphinxcontrib-kroki`](https://github.com/sphinx-contrib/kroki/) also lets you
  use Svgbob to convert ASCII diagrams, but it queries the
  [kroki.io](https://kroki.io/) website to do so, and does not support the
  new options from Svgbob v0.5.
* [`sphinxcontrib-aafig`](https://github.com/sphinx-contrib/aafig) uses the
  [`aafigure`](https://launchpad.net/aafigure) binary to convert ASCII diagrams.


## 🔨 Credits

`sphinxcontrib-svgbob` is developped and maintained by:
- [Martin Larralde](https://github.com/althonos)

The structure of this repository was adapted from the aforementioned
`sphinxcontrib-kroki` repository, as I had no experience setting up a
Sphinx extension otherwise.


## ⚖️ License

This library is provided under the [MIT License](https://choosealicense.com/licenses/mit/).
