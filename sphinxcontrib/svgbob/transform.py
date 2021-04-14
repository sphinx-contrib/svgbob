import hashlib
import os
import pathlib
import typing

import sphinx.transforms
from docutils.nodes import image, inline, generated, literal, literal_block

from ._svgbob import to_svg
from .node import svgbob


class SvgbobToImageTransform(sphinx.transforms.SphinxTransform):
    """Sphinx transform to turn Svgbob nodes into SVG images.
    """

    default_priority = 10

    def builder_supports_svg(self) -> bool:
        return 'image/svg+xml' in self.app.builder.supported_image_types

    def apply(self, **kwargs: typing.Any) -> None:
        source = os.path.dirname(self.document["source"])
        for node in self.document.traverse(svgbob):

            if self.builder_supports_svg():
                img = image()
                img["svgbob"] = node
                img["alt"] = node["code"]
                if "align" in node:
                    img["align"] = node["align"]
                if "class" in node:
                    img["class"] = node["class"]

                options = {
                    "font_size": node["options"].get("font-size"),
                    "font_family": node["options"].get("font-family"),
                    "fill_color": node["options"].get("fill-color"),
                    "background_color": node["options"].get("background-color"),
                    "stroke_color": node["options"].get("stroke-color"),
                    "stroke_width": node["options"].get("stroke-width"),
                    "scale": node["options"].get("scale"),
                }

                out = self.render(node, options)
                img["uri"] = os.path.relpath(out, source)
                node.replace_self(img)

            else:
                contents = node["code"].split("\n")
                rawnode = literal_block(node["code"], node["code"])
                node.replace_self(rawnode)

    def render(
        self,
        node: svgbob,
        options: typing.Dict[str, object],
        prefix: str = "svgbob",
    ) -> str:
        builder = self.app.builder

        hash = hashlib.sha1(node["code"].encode()).hexdigest()
        fname = "{}-{}.svg".format(prefix, hash)
        outfile = os.path.join(builder.outdir, builder.imagedir, fname)

        if not os.path.exists(outfile):
            os.makedirs(os.path.dirname(outfile), exist_ok=True)
            with open(outfile, mode="w") as f:
                f.write(to_svg(node["code"], **options)) # type: ignore

        return outfile
