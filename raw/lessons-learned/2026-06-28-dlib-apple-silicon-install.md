---
Source: Session reflection
Collected: 2026-06-28
Published: 2026-06-28
---

# dlib installation on Apple Silicon macOS

## Problem
`pip install dlib` (and by extension `pip install face-recognition`) fails to build from source on Apple Silicon Macs with a compiler error:

```
dlib/external/libpng/arm/../pngpriv.h:527:16: fatal error: 'fp.h' file not found
```

dlib bundles its own libpng, and that libpng's ARM code includes `<fp.h>` — an old Apple Carbon/Math header removed from modern macOS arm64 SDKs (macOS 12+). The pip-distributed source tarball has not been patched for this. The error is silent about the root cause; you just see a CMake build failure after a long compile.

Secondary issues that compound it:
- Python 3.13 has no prebuilt dlib wheel, so pip always falls back to source compilation, hitting this error every time.
- `conda install -c conda-forge dlib` in the base conda env fails with `RemoveError: 'setuptools' is a dependency of conda and cannot be removed` because the transaction conflicts with conda's own runtime dependencies.
- `face_recognition_models` (a dependency of `face-recognition`) calls `from pkg_resources import resource_filename`, which breaks on setuptools >= 71 where `pkg_resources` was removed as a top-level importable module.

## Fix

```bash
# 1. Create a fresh env with Python 3.11 (has no dlib wheel gap)
conda create -n <env> python=3.11 -y

# 2. Install dlib from conda-forge (pre-patched binary, no source compile)
conda run -n <env> conda install -c conda-forge dlib -y

# 3. Now pip install face-recognition (skips dlib, it's already there)
conda run -n <env> pip install face-recognition

# 4. Restore pkg_resources removed in setuptools >= 71
conda run -n <env> pip install "setuptools<71"
```

## Why it works
- conda-forge's dlib package ships a patched binary that removes the `fp.h` dependency.
- A non-base env has no conda self-dependency constraints, so the setuptools version conflict doesn't block the transaction.
- Python 3.11 is the last version with reliable dlib wheels on PyPI (though conda-forge is still the safer path regardless).

## Key rule
On Apple Silicon, never use `pip install dlib` directly. Always use `conda install -c conda-forge dlib` in a dedicated env first, then pip install downstream packages.
