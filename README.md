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

# Install

The package is called `ciphwren-etebase`, so that it doesn't clash with EteSync's `etebase` on PyPI, and it's
still imported as `etebase`. It isn't on PyPI: each [release](https://github.com/nikossvnk/etebase-py/releases)
has wheels for Linux (x86_64, aarch64), macOS (x86_64, arm64) and Windows (x86_64), for Python 3.9 and newer,
and pip picks the right one from the release page:

```
pip install ciphwren-etebase==0.33.0 --find-links https://github.com/nikossvnk/etebase-py/releases/expanded_assets/v0.33.0
```

In a `requirements.txt`, put the `--find-links …` line above `ciphwren-etebase==0.33.0`.

Uninstall EteSync's `etebase` first if it's installed: both provide the `etebase` module.

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
