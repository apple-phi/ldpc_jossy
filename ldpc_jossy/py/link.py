"""Get references to the dynamically linked libraries."""

import ctypes
import os
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent

p = ROOT_DIR / "bin" / "c_ldpc"

try_exts = ["", ".so", ".dll", ".dylib"]
for ext in try_exts:
    if os.path.exists(p.with_suffix(ext)):
        p = p.with_suffix(ext)
        break

c_ldpc = ctypes.CDLL(str(p))

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
