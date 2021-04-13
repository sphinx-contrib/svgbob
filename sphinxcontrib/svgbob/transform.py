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

            out = self.render(node)
            img["uri"] = os.path.relpath(out, source)

            node.replace_self(img)

    def render(self, node: svgbob, prefix: str = "svgbob") -> pathlib.Path:
        builder = self.app.builder

        hash = hashlib.sha1(node["code"].encode()).hexdigest()
        fname = "{}-{}.svg".format(prefix, hash)
        outfn = pathlib.Path(builder.outdir).joinpath(builder.imagedir, fname)

        if outfn.is_file():
            return outfn

        outfn.parent.mkdir(parents=True, exist_ok=True)

        with outfn.open(mode="w") as f:
            f.write(to_svg(node["code"]))

        # response = requests.post(kroki_url, json=payload, stream=True)
        # response.raise_for_status()
        # with outfn.open(mode="wb") as f:
        #     for chunk in response.iter_content(chunk_size=128):
        #         f.write(chunk)

        return outfn


        # try:
        #     out = render_kroki(
        #         builder, diagram_type, diagram_source, output_format, prefix
        #     )
        # except KrokiError as exc:
        #     logger.warning(
        #         __("kroki %s diagram (%s) with code %r: %s"),
        #         diagram_type,
        #         output_format,
        #         diagram_source,
        #         exc,
        #     )
        #     raise SkipNode from exc
        #
        # return out
#
#
#
# def render_kroki(
#     builder: Builder,
#     diagram_type: str,
#     diagram_source: str,
#     output_format: str,
#     prefix: str = "kroki",
# ) -> Path:
#     kroki_url: str = builder.config.kroki_url
#     payload: Dict[str, str] = {
#         "diagram_source": diagram_source,
#         "diagram_type": diagram_type,
#         "output_format": output_format,
#     }
#
#     hashkey = (str(kroki_url) + str(payload)).encode()
#     fname = "%s-%s.%s" % (prefix, sha1(hashkey).hexdigest(), output_format)
#     outfn = Path(builder.outdir).joinpath(builder.imagedir, fname)
#
#     if outfn.is_file():
#         return outfn
#
#     try:
#         outfn.parent.mkdir(parents=True, exist_ok=True)
#
#         response = requests.post(kroki_url, json=payload, stream=True)
#         response.raise_for_status()
#         with outfn.open(mode="wb") as f:
#             for chunk in response.iter_content(chunk_size=128):
#                 f.write(chunk)
#
#         return outfn
#     except requests.exceptions.RequestException as e:
#         raise KrokiError(__("kroki did not produce a diagram")) from e
#     except IOError as e:
#         raise KrokiError(
#             __("Unable to write diagram to file %r") % outfn
#         ) from e
