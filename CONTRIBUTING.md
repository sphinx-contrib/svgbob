# Contributing to `sphinxcontrib-svgbob`

For bug fixes or new features, please file an issue before submitting a
pull request. If the change isn't trivial, it may be best to wait for
feedback.

## Rule 0: Don't be an asshole.

[I didn't make that one up](https://en.wikipedia.org/wiki/The_No_Asshole_Rule),
so let's try to make the Internet a better place . This can start right here
in our day-to-day interactions while we build code.

## Setting up a local repository

You can just clone the repository without needing any extra setup to get a
local copy of the code:

```console
$ git clone https://github.com/althonos/sphinxcontrib-svgbob
```

## Running tests

Tests are written as usual Python unit tests with the `unittest` module of
the standard library. Running them requires the extension to be built
locally:

```console
$ python setup.py build_ext --inplace
$ python -m unittest discover -vv
```

## Coding guidelines

This project targets Python 3.6 or later.

Python objects should be typed where applicable; the exception is the Rust
compatibility layer, where it's acceptable that the `to_svg` is not typed.

### Interfacing with Rust

This project uses Rust and [`pyo3`](https://pyo3.rs) to interface with the
`svgbob` code. You'll need a Rust compiler on your system to compile the
extension if you are going to tinker with the code, even if you only intend
to edit the Python part of the code.

If you're unfamiliar with Rust, check the [*Get Started*](https://www.rust-lang.org/learn/get-started)
page of the Rust documentation on how to get a local toolchain.
