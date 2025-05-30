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
