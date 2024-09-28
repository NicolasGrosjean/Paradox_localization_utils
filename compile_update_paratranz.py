from cx_Freeze import setup, Executable

build_exe_options = {"build_exe": "update_paratranz/dist", "packages": ["requests"], "excludes": ["tkinter"]}

setup(
    name="update_paratranz",
    version="1.1",
    description="Update translation on Paratranz",
    options={"build_exe": build_exe_options},
    executables=[Executable("paradox_localization_utils/update_paratranz.py")],
)
