import hashlib
import os
import pathlib
import typing

from docutils.nodes import image, SkipNode

from sphinx.transforms import SphinxTransform
from sphinx.locale import __

from ._svgbob import to_svg
from .node import svgbob



class SvgbobToImageTransform(SphinxTransform):
    default_priority = 10

    def apply(self, **kwargs: typing.Any) -> None:
        source = os.path.dirname(self.document["source"])
        for node in self.document.traverse(svgbob):
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

        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        with open(outfile, mode="w") as f:
            f.write(to_svg(node["code"], **options))

        return outfile
