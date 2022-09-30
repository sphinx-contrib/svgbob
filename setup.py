#!/usr/bin/env python3

import configparser
import os
import shutil
import subprocess
import sys
import urllib.request

import setuptools
import setuptools_rust
from distutils.errors import DistutilsPlatformError
from distutils.log import INFO
from setuptools.command.sdist import sdist as _sdist
from setuptools_rust.build import build_rust as _build_rust

try:
    from setuptools_rust.rustc_info import get_rust_version
except ImportError:
    from setuptools_rust.utils import get_rust_version


class vendor(setuptools.Command):

    description = "vendor Rust dependencies into a local folder"
    user_options = [
        ("vendor-dir=", "d", "the path where to vendor the Rust crates")
    ]

    def initialize_options(self):
        self.vendor_dir = None

    def finalize_options(self):
        if self.vendor_dir is None:
            self.vendor_dir = "crates"

    def run(self):
        # make sure rust is available
        _build_cmd = self.get_finalized_command("build_rust")
        rustc = get_rust_version()
        if rustc is None:
            _build_cmd.setup_temp_rustc_unix(toolchain="stable", profile="minimal")
        # vendor crates
        path = next(ext.path for ext in self.distribution.rust_extensions)
        proc = subprocess.run(["cargo", "vendor", self.vendor_dir, "--manifest-path", path])
        proc.check_returncode()
        # write the cargo config file
        self.mkpath(".cargo")
        with open(os.path.join(".cargo", "config.toml"), "w") as f:
            f.write(
                """
                [source.crates-io]
                replace-with = "vendored-sources"

                [source.vendored-sources]
                directory = "{}"
                """.format(self.vendor_dir)
            )



class sdist(_sdist):
    """A `sdist` that generates a `pyproject.toml` on the fly.
    """

    def run(self):
        # build `pyproject.toml` from `setup.cfg`
        c = configparser.ConfigParser()
        c.add_section("build-system")
        c.set("build-system", "requires", str(self.distribution.setup_requires))
        c.set("build-system", 'build-backend', '"setuptools.build_meta"')
        with open("pyproject.toml", "w") as pyproject:
            c.write(pyproject)
        # run the rest of the packaging
        _sdist.run(self)


class build_rust(_build_rust):

    def run(self):
        try:
            rustc = get_rust_version()
        except DistutilsPlatformError:
            rustc = None
        if rustc is not None:
            nightly = rustc.prerelease is not None and "nightly" in rustc.prerelease
        else:
            if sys.platform in ("linux", "darwin"):
                self.setup_temp_rustc_unix(toolchain="nightly", profile="minimal")
                nightly = True
            else:
                nightly = False

        if self.inplace:
            self.extensions[0].strip = setuptools_rust.Strip.No
        if nightly:
            self.extensions[0].features = (*self.extensions[0].features, "nightly")

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
    cmdclass=dict(build_rust=build_rust, sdist=sdist, vendor=vendor),
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
