import shutil
import subprocess
from pathlib import Path

# python compiler_setting/create_exe.py

compiler = input("cx_Freeze or Nuitka [c/n]: ")

if compiler not in ["c", "n"]:
    exit()

Path("compiler_setting/temp").mkdir()
for dir_name in ["Fonts", "README"]:
    shutil.copytree(dir_name, f"compiler_setting/temp/{dir_name}")

if compiler == "c":
    Path("compiler_setting/temp").rename("compiler_setting/cx_Freeze")

    shutil.move("compiler_setting/setup.py", ".")
    subprocess.run([".venv/Scripts/python.exe", "setup.py", "build"])
    shutil.move("setup.py", "compiler_setting")

    for dir_name in Path("build/exe.win-amd64-3.10").iterdir():
        shutil.move(dir_name, "compiler_setting/cx_Freeze")

    shutil.rmtree("build")

elif compiler == "n":
    Path("compiler_setting/temp").rename("compiler_setting/Nuitka")

    subprocess.run([
        ".venv/Scripts/python.exe", "-m", "nuitka", "--mingw64", "--follow-imports",
        "--onefile", "--plugin-enable=tk-inter", "--windows-disable-console",
        "--windows-icon-from-ico=compiler_setting/icon.ico", "app.py",
    ])

    shutil.move("app.exe", "compiler_setting/Nuitka")

    for dir_name in ["app.build", "app.dist", "app.onefile-build"]:
        shutil.rmtree(dir_name)
