"""Get references to the dynamically linked libraries."""

import ctypes
import os
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent

ext = "so" if os.name != "nt" else "dll"

c_ldpc = ctypes.CDLL(str(ROOT_DIR / "bin" / f"c_ldpc.{ext}"))
