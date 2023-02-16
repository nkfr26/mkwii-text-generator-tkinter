import sys

from cx_Freeze import Executable, setup

# python setup.py build
# Dependencies are automatically detected, but it might need fine tuning.

build_options = {"packages": [], "excludes": []}

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        "app.py", base=base,
        target_name="MKWii Text Generator",
        icon="icon.ico",
    )
]

setup(
    name="mkwii-text-generator-tkinter",
    version="1.2", description="",
    options={"build_exe": build_options},
    executables=executables,
)
