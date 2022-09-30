import typing

from sphinx.application import Sphinx

from .directive import SvgbobDirective
from .transform import SvgbobToImageTransform


__version__ = "0.2.0"


def setup(app: Sphinx) -> typing.Dict[str, typing.Any]:
    app.add_directive("svgbob", SvgbobDirective)
    app.add_transform(SvgbobToImageTransform)
    return {
        "version": __version__,
        "parallel_read_safe": True
    }
