from PyInstaller.building.api import *
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

# Get the base path
base_path = os.path.abspath(os.path.dirname('__file__'))

# Define paths
shapefile_dir = os.path.join(base_path, 'MontanaCounties_shp')

a = Analysis(
    ['GUI_MAP_Generator.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        (shapefile_dir, 'MontanaCounties_shp'),  # Include shapefile directory
    ],
    hiddenimports=[
        'pandas',
        'geopandas',
        'matplotlib',
        'tkinter',
        'numpy',
        'shapely',
        'fiona',
        'pyproj'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Montana_Bee_Map_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # You can add an icon file here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Montana_Bee_Map_Generator'
) 