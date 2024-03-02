import sys

from cx_Freeze import Executable, setup


# python setup.py build
# Dependencies are automatically detected, but it might need fine tuning.

build_options = {"packages": [], "excludes": []}

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        "src/__main__.py", base=base,
        target_name="MKWii Text Generator",
        icon="stand_alone/favicon.ico"
    )
]

setup(
    name="mkwii-text-generator-tkinter",
    version="1.3", description="",
    options={"build_exe": build_options},
    executables=executables
)
