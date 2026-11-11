<p align="center">
  <h1 align="center">Etebase - Encrypt Everything</h1>
</p>

> [!NOTE]
> **This is an independent fork** of [etebase-py](https://github.com/etesync/etebase-py), the original
> project of the EteSync authors. This fork is not affiliated with, endorsed by or supported by EteSync or
> Etebase in any way. The history of the original project is kept as it is, with its authors, and the
> changes of this fork follow it. Like the original, it's licensed under the [BSD-3-Clause](./LICENSE) license.

A Python library for Etebase

This package is implemented in Rust and exposes a Python API for people to use.

![GitHub tag](https://img.shields.io/github/tag/nikossvnk/etebase-py.svg)
[![PyPI](https://img.shields.io/pypi/v/etebase.svg)](https://pypi.python.org/pypi/etebase/)
[![Build Status](https://github.com/nikossvnk/etebase-py/actions/workflows/check.yml/badge.svg)](https://github.com/nikossvnk/etebase-py/actions)

# Documentation

The Python API, with its types, is described in [`etebase/etebase_python.pyi`](./etebase/etebase_python.pyi).

# Build

## Install deps

```
pip install maturin
```

## Build

```
maturin build --release
```

The extension is built against the Python stable ABI (abi3), so the resulting wheel works on Python 3.9 and newer.

For development, `maturin develop` builds and installs the package into the current virtualenv.
