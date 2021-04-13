from hashlib import sha1
from typing import Any, Dict, List, Optional

from docutils.nodes import Element, General, Inline, Node
from docutils.parsers.rst import directives
from sphinx.builders import Builder
from sphinx.errors import SphinxError
from sphinx.ext.graphviz import align_spec, figure_wrapper
from sphinx.locale import __
from sphinx.util.docutils import SphinxDirective
from sphinx.util.i18n import search_image_for_language

from .node import svgbob


class SvgbobError(SphinxError):
    category = "Svgbob error"


class SvgbobDirective(SphinxDirective):
    """Directive to convert ASCII diagrams to SVG with Svgbob.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = False

    option_spec = {
        "font-size": int,
        "font-family": directives.unchanged,
        "fill-color": directives.unchanged,
        "background-color": directives.unchanged,
        "stroke-color": directives.unchanged,
        "stroke-width": float,
        "scale": float,
    }

    def run(self) -> List[Node]:
        document = self.state.document
        source: str = "\n".join(self.content)

        node = svgbob()
        node["code"] = source
        node["options"] = self.options.copy()

        classes = ["svgbob"]
        node["classes"] = classes + self.options.get("class", [])
        if "align" in self.options:
            node["align"] = self.options["align"]

        return [node]

        # if "caption" not in self.options:
        #     self.add_name(node)
        #     return [node]
        # else:
        #     node["caption"] = self.options["caption"]
        #     figure = figure_wrapper(self, node, node["caption"])
        #     figure["classes"] = classes
        #     self.add_name(figure)
        #     return [figure]
