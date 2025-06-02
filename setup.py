# -*- coding: utf-8 -*-
import sys
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.develop import develop as _develop
import subprocess, os, shutil

PACKAGE_NAME = "ldpc_jossy"
ZIG_BUILD_DIR = "zig-out"

# Declare a dummy extension so that build_ext always runs,
# even on Windows
dummy_ext = Extension(f"{PACKAGE_NAME}._dummy", sources=[])


class ZigBuildExt(_build_ext):
    def run(self):
        # 1) platform-agnostic compile step        # a. If you have Zig installed already, you can use it directly.
        if exe := shutil.which("zig"):
            print("[ZigBuildExt] Building via Zig CLI found at:", exe)
            try:
                subprocess.run([exe, "build"], check=True, stdout=sys.stdout, stderr=sys.stderr)
            except subprocess.CalledProcessError:
                print("[ZigBuildExt] Zig CLI build failed.")
                print("[ZigBuildExt] Falling back to PyPI ziglang package.")
                subprocess.run([sys.executable, "-m", "ziglang", "build"], check=True, stdout=sys.stdout, stderr=sys.stderr)
        else:
            print("[ZigBuildExt] Building via PyPI ziglang.")
            subprocess.run([sys.executable, "-m", "ziglang", "build"], check=True, stdout=sys.stdout, stderr=sys.stderr)

        # 2) copy the resulting shared libs into build_lib/ldpc_jossy/
        if not os.path.exists(ZIG_BUILD_DIR):
            raise FileNotFoundError(f"{ZIG_BUILD_DIR} not found")

        target_pkg_dir = os.path.join(self.build_lib, PACKAGE_NAME)
        print(
            f"[ZigBuildExt] Ensuring target package directory exists: {target_pkg_dir}"
        )
        os.makedirs(target_pkg_dir, exist_ok=True)

        print(f"[ZigBuildExt] Listing contents of ZIG_BUILD_DIR: {ZIG_BUILD_DIR}")
        for item in os.listdir(ZIG_BUILD_DIR):
            src = os.path.join(ZIG_BUILD_DIR, item)
            dst = os.path.join(target_pkg_dir, item)

            if os.path.isdir(src):
                print(f"[ZigBuildExt] Copying directory: {src} to {dst}")
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                print(f"[ZigBuildExt] Copying file:      {src} to {dst}")
                shutil.copy2(src, dst)

        # 3) now run the super method, which will pick up our dummy_ext
        super().run()

    def build_extension(self, ext):
        # NB: <-- this override is the magic wand.
        # By not calling into the CCompiler at all,
        # setuptools never invokes MSVC (or gcc, etc.).
        # We leave this as a no-op.
        return


class ZigDevelop(_develop):
    def run(self):
        # force our build_ext (and the Zig copy) before symlinking
        self.run_command("build_ext")
        super().run()


setup(
    name=PACKAGE_NAME,
    version="0.1.8",
    packages=[*find_packages(), "ldpc_jossy.data"],
    ext_modules=[dummy_ext],  # this makes build_ext run
    cmdclass={
        "build_ext": ZigBuildExt,
        "develop": ZigDevelop,
    },
    include_package_data=True,
    package_data={PACKAGE_NAME: ["*.so", "*.dll", "*.dylib", "bin/*", "data/*"]},
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "ldpc-test = ldpc_jossy.py.test_ldpc:main",
            "ldpc-awgn = ldpc_jossy.py.ldpc_awgn:main",
            "ldpc-results2csv = ldpc_jossy.py.results2csv:main",
            "ldpc-dispres = ldpc_jossy.py.disp_res:noop",
        ],
    },
    install_requires=["numpy", "matplotlib", "pytest"],
)
