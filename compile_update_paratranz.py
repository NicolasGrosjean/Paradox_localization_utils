import sys
from cx_Freeze import setup, Executable

build_exe_options = {"build_exe": "dist", "packages": ["requests"], "excludes": ["tkinter"]}
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="update_paratranz",
    version="0.1",
    description="Update translation on Paratranz",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/update_paratranz.py", base=base)],
)

