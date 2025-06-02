# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import pyproj
from pathlib import Path

block_cipher = None

# Get paths
shapefile_dir = os.path.abspath('MontanaCounties_shp')
pyproj_data_dir = os.path.abspath(pyproj.datadir.get_data_dir())

# Collect all data files
datas = []

# Add shapefile components
for f in os.listdir(shapefile_dir):
    if f.endswith(('.shp', '.dbf', '.shx', '.prj')):
        source = os.path.join(shapefile_dir, f)
        dest = os.path.join('MontanaCounties_shp', f)
        datas.append((source, os.path.dirname(dest)))

# Add pyproj data directory
datas.append((pyproj_data_dir, 'pyproj/data'))

# Add icon file
datas.append(('app_icon.ico', '.'))

a = Analysis(
    ['GUI_MAP_Generator.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pandas',
        'geopandas',
        'matplotlib',
        'tkinter',
        'numpy',
        'shapely',
        'fiona',
        'pyproj',
        'rtree',
        'shapely.geometry',
        'pyproj.datadir',
        'geopandas.datasets',
        'fiona._shim',
        'fiona.schema',
        'matplotlib.backends.backend_tkagg'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Montana Bee Map Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Changed to False to hide the console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
    version='file_version_info.txt',
) 