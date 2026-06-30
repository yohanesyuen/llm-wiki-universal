---
type: lesson
tags: [installation, python, macos]
Title: Installing dlib on Apple Silicon macOS
Sources: Session reflection, 2026-06-28
Raw: "[../../raw/lessons-learned/2026-06-28-dlib-apple-silicon-install.md](../../raw/lessons-learned/2026-06-28-dlib-apple-silicon-install.md)"
Updated: 2026-06-28
---

# Installing dlib on Apple Silicon macOS

## Never Use `pip install dlib` Directly on Apple Silicon

`pip install dlib` (and by extension `pip install face-recognition`) fails to compile from source on Apple Silicon Macs with:

```
dlib/external/libpng/arm/../pngpriv.h:527:16: fatal error: 'fp.h' file not found
```

dlib bundles its own libpng. That libpng's ARM code includes `<fp.h>` — an old Apple Carbon/Math header removed from modern macOS arm64 SDKs (macOS 12+). The pip source tarball is unpatched. The error is silent about its root cause; you just see a CMake build failure after several minutes of compilation.

The conda-forge build of dlib ships a pre-patched binary with this dependency removed. Always install from there instead.

## Three Compounding Issues

### 1. Python 3.13 has no prebuilt dlib wheel

dlib does not publish a wheel for Python 3.13, so pip always falls back to source compilation — hitting the `fp.h` error every time. Using Python 3.11 avoids the wheel gap (and conda-forge handles the rest).

### 2. `conda install` in the base env is blocked

```
RemoveError: 'setuptools' is a dependency of conda and cannot be removed from conda's operating environment.
```

The conda-forge dlib transaction pulls in a setuptools version that conflicts with conda's own runtime dependencies. Conda refuses to break itself. A fresh non-base env has no such constraint and the install succeeds cleanly.

### 3. `pkg_resources` removed in setuptools ≥ 71

`face_recognition_models` calls `from pkg_resources import resource_filename`. setuptools dropped `pkg_resources` as a top-level importable module in version 71. Pinning to `<71` restores it.

## The Fix

```bash
# 1. Fresh env with Python 3.11
conda create -n <env> python=3.11 -y

# 2. Install dlib from conda-forge (pre-patched binary)
conda run -n <env> conda install -c conda-forge dlib -y

# 3. pip install face-recognition — dlib is already satisfied, skipped
conda run -n <env> pip install face-recognition

# 4. Pin setuptools to restore pkg_resources
conda run -n <env> pip install "setuptools<71"
```

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — general pattern of verifying system constraints before committing to a stack
