import os

import setuptools
import setuptools_rust

setuptools.setup(
    rust_extensions=[
        setuptools_rust.RustExtension(
            "sphinxcontrib.svgbob._svgbob",
            path=os.path.join("sphinxcontrib", "svgbob", "_svgbob", "Cargo.toml"),
            binding=setuptools_rust.Binding.PyO3,
            strip=setuptools_rust.Strip.Debug,
            features=["extension-module"],
        )
    ],
)
