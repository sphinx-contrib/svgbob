# `sphinxcontrib.svgbob` [![Stars](https://img.shields.io/github/stars/althonos/sphinxcontrib.svgbob.svg?style=social&maxAge=3600&label=Star)](https://github.com/althonos/sphinxcontrib.svgbob/stargazers)

*A Sphinx extension to render ASCII diagrams into SVG using [Svgbob](https://github.com/ivanceras/svgbob).*

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square&maxAge=2678400)](https://choosealicense.com/licenses/mit/)
[![Source](https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=2678400&style=flat-square)](https://github.com/althonos/sphinxcontrib.svgbob/)
[![GitHub issues](https://img.shields.io/github/issues/althonos/sphinxcontrib.svgbob.svg?style=flat-square&maxAge=600)](https://github.com/althonos/sphinxcontrib.svgbob/issues)

## 🗺️ Overview

To include diagrams into Sphinx documentation, diagrams are commonly described
with a dedicated markup language, and converted into an image by Sphinx when
the documentation is built. However, this reduces the legibility of the
documentation source for readers that are not browsing the HTML version.

[Svgbob](https://github.com/ivanceras/svgbob) is a diagramming model implemented
in Rust that can convert ASCII diagrams. Using it allows you to:

* Keep a textual version of the diagram in your documentation, so that it remains legible.
* Render a nicer version as SVG for HTML or PDF renderings of the documentation.

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

When Sphinx (and `autodoc`) render the docstring of this function, you'll get
the following HTML output:

![example1.html.png](https://raw.githubusercontent.com/althonos/sphinxcontrib-svgbob/master/static/example1.html.png)

And yet, the `help(hamming)` will still look nice:

![example1.console.png](https://raw.githubusercontent.com/althonos/sphinxcontrib-svgbob/master/static/example1.console.png)
