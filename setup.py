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
        # 1) run your Zig build
        subprocess.run(["zig", "build"], check=True)
        # 2) copy the resulting shared libs into build_lib/ldpc_jossy/
        if not os.path.exists(ZIG_BUILD_DIR):
            raise FileNotFoundError(f"{ZIG_BUILD_DIR} not found")
        target_pkg_dir = os.path.join(self.build_lib, PACKAGE_NAME)
        for item in os.listdir(ZIG_BUILD_DIR):
            src = os.path.join(ZIG_BUILD_DIR, item)
            dst = os.path.join(target_pkg_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
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
    version="0.1.7",
    packages=find_packages(),
    ext_modules=[dummy_ext],  # ← this makes build_ext run
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
)
