from cx_Freeze import setup, Executable

from source.path import path_image, path_assets

setup(
    name='Bataille Navale',
    description='Bataille Navale',
    author='Raphaël & Léo',
    version='1',

    options={
        "build_exe": {
            "include_files": [path_assets],
        }
    },

    packages=['source'],

    executables=[
        Executable(
            "main.pyw",
            icon=path_image / "icon/icon.ico",
            base="win32gui",
            target_name="Bataille Navale.exe",
            shortcut_name="Bataille Navale",
            shortcut_dir="DesktopFolder"
        )
    ],
)
