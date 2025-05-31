"""Get references to the dynamically linked libraries."""

import ctypes
import os
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent
search_dirs = ["bin", "lib"]
try_exts = ["", ".so", ".dll", ".dylib", ".bundle"]

c_ldpc = None

for subdir in search_dirs:
    # Build the candidate base path (without extension)
    base_path = ROOT_DIR / subdir / "c_ldpc"

    for ext in try_exts:
        candidate = base_path.with_suffix(ext)
        if candidate.exists():
            try:
                c_ldpc = ctypes.CDLL(str(candidate))
                print(f"Loaded {candidate} successfully.")
            except Exception as e:
                print(f"Attempted to load {candidate}: {e}")
            break  # stop trying extensions for this subdir

    if c_ldpc is not None:
        break  # library was loaded (or at least found); stop searching other subdirs

if c_ldpc is None:
    raise RuntimeError(
        f"Could not find or load the 'c_ldpc' dynamic library in either {ROOT_DIR / 'bin'} or {ROOT_DIR / 'lib'} directories with extensions {try_exts}."
    )

# shorthand
c_double_p = ctypes.POINTER(ctypes.c_double)
c_int32_p = ctypes.POINTER(ctypes.c_int32)

# sumprod
c_ldpc.sumprod.argtypes = [
    c_double_p,  #  double *ch
    c_int32_p,  #  int32_t *vdeg
    c_int32_p,  #  int32_t *cdeg
    c_int32_p,  #  int32_t *intrlv
    ctypes.c_int32,  #  int32_t Nv
    ctypes.c_int32,  #  int32_t Nc
    ctypes.c_int32,  #  int32_t Nmsg
    c_double_p,  #  double *app
]
c_ldpc.sumprod.restype = ctypes.c_int

# sumprod2  (same signature as sumprod)
c_ldpc.sumprod2.argtypes = c_ldpc.sumprod.argtypes
c_ldpc.sumprod2.restype = ctypes.c_int

# minsum  (extra double correction_factor)
c_ldpc.minsum.argtypes = c_ldpc.sumprod.argtypes + [ctypes.c_double]
c_ldpc.minsum.restype = ctypes.c_int

# Lxor
c_ldpc.Lxor.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
c_ldpc.Lxor.restype = ctypes.c_double

# Lxfb
c_ldpc.Lxfb.argtypes = [c_double_p, ctypes.c_long, ctypes.c_int]
c_ldpc.Lxfb.restype = ctypes.c_double
