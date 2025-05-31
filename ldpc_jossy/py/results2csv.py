import os
import sys
import subprocess
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent


def main():
    exe = ROOT_DIR / "bin" / "results2csv"
    try_exts = ["", ".exe", ".bat", ".sh", ".so", ".dll", ".dylib"]
    for ext in try_exts:
        if os.path.exists(exe.with_suffix(ext)):
            exe = exe.with_suffix(ext)
            break
    else:
        sys.exit(f"Could not find results2csv executable at {exe!r}")
    # Forward all args
    # But if no argv[1] then set it to ROOT_DIR / "data" / "results.csv"
    argv = sys.argv.copy()
    if len(argv) < 2:
        argv.append(str(ROOT_DIR / "data" / "results"))  # prefix without .csv
    return subprocess.call([exe, *argv[1:]])
