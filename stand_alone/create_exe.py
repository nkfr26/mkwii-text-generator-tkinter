import shutil
import subprocess
from pathlib import Path


# python stand_alone/create_exe.py
compiler = input("cx_Freeze or Nuitka [c/n]: ")

if compiler not in ["c", "n"]:
    exit()

Path("stand_alone/temp").mkdir()
for dir_name in ["Fonts", "README"]:
    shutil.copytree(dir_name, f"stand_alone/temp/{dir_name}")

if compiler == "c":
    Path("stand_alone/temp").rename("stand_alone/cx_Freeze")

    shutil.move("stand_alone/setup.py", ".")
    subprocess.run([".venv/Scripts/python.exe", "setup.py", "build"])
    shutil.move("setup.py", "stand_alone")

    for dir_name in Path("build/exe.win-amd64-3.10").iterdir():
        shutil.move(dir_name, "stand_alone/cx_Freeze")

    shutil.rmtree("build")

elif compiler == "n":
    Path("stand_alone/temp").rename("stand_alone/Nuitka")

    subprocess.run([
        ".venv/Scripts/python.exe", "-m", "nuitka", "--mingw64", "--follow-imports",
        "--onefile", "--plugin-enable=tk-inter", "--windows-disable-console",
        "--windows-icon-from-ico=stand_alone/favicon.ico", "src/__main__.py",
    ])

    Path("__main__.exe").rename("MKWii Text Generator.exe")
    shutil.move("MKWii Text Generator.exe", "stand_alone/Nuitka")

    for dir_name in ["__main__.build", "__main__.dist", "__main__.onefile-build"]:
        shutil.rmtree(dir_name)
