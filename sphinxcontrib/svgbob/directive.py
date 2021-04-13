import typing

import sphinx.errors
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.ext.graphviz import align_spec
from sphinx.util.docutils import SphinxDirective

from .node import svgbob


class SvgbobError(sphinx.errors.SphinxError):
    category = "Svgbob error"


class SvgbobDirective(SphinxDirective):
    """Sphinx directive to convert ASCII diagrams to Svgbob nodes.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 3
    final_argument_whitespace = False

    option_spec = {
        # Svgbob options
        "font-size": int,
        "font-family": directives.unchanged,
        "fill-color": directives.unchanged,
        "background-color": directives.unchanged,
        "stroke-color": directives.unchanged,
        "stroke-width": float,
        "scale": float,
        # HTML options
        "align": align_spec,
        "class": directives.class_option,
    }

    def run(self) -> typing.List[Node]:
        document = self.state.document
        source: str = "\n".join(self.content)
        nodes: typing.List[Node] = []

        node = svgbob()
        node["code"] = source
        node["options"] = self.options.copy()

        classes = ["svgbob"]
        node["classes"] = classes + self.options.get("class", [])
        if "align" in self.options:
            node["align"] = self.options["align"]

        self.add_name(node)
        nodes.append(node)
        return nodes
