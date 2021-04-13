#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import urllib.request
from distutils.errors import DistutilsPlatformError

import setuptools
import setuptools_rust
from setuptools_rust.build import build_rust as _build_rust
from setuptools_rust.utils import get_rust_version


class build_rust(_build_rust):

    def run(self):
        try:
            rustc = get_rust_version()
            nightly = rustc.prerelease is not None and "nightly" in rustc.prerelease
        except DistutilsPlatformError:
            if sys.platform in ("linux", "darwin"):
                self.setup_temp_rustc_unix(toolchain="nightly", profile="minimal")
                nightly = True
            else:
                nightly = False

        if self.inplace:
            self.extensions[0].strip = setuptools_rust.Strip.No
        if nightly:
            self.extensions[0].features.append("nightly")

        _build_rust.run(self)


    def setup_temp_rustc_unix(self, toolchain, profile):
        rustup_sh = os.path.join(self.build_temp, "rustup.sh")
        os.environ["CARGO_HOME"] = os.path.join(self.build_temp, "cargo")
        os.environ["RUSTUP_HOME"] = os.path.join(self.build_temp, "rustup")

        self.mkpath(os.environ["CARGO_HOME"])
        self.mkpath(os.environ["RUSTUP_HOME"])

        self.announce("downloading rustup.sh install script", level=INFO)
        with urllib.request.urlopen("https://sh.rustup.rs") as res:
            with open(rustup_sh, "wb") as dst:
                shutil.copyfileobj(res, dst)

        self.announce("installing Rust compiler to {}".format(self.build_temp), level=INFO)
        subprocess.call([
            "/bin/sh",
            rustup_sh,
            "-y",
            "--default-toolchain",
            toolchain,
            "--profile",
            profile,
            "--no-modify-path"
        ])

        self.announce("updating $PATH variable to use local Rust compiler", level=INFO)
        os.environ["PATH"] = ":".join([
            os.path.abspath(os.path.join(os.environ["CARGO_HOME"], "bin")),
            os.environ["PATH"]
        ])



setuptools.setup(
    cmdclass=dict(build_rust=build_rust),
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
