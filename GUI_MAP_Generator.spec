# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all necessary data files
datas = [
    ('MontanaCounties_shp', 'MontanaCounties_shp'),
    ('shapefiles', 'shapefiles'),
    ('app_icon.ico', '.'),
]

# Add geopandas data files
try:
    import geopandas
    geopandas_data = collect_data_files('geopandas')
    datas.extend(geopandas_data)
except ImportError:
    pass

# Add matplotlib data files
try:
    import matplotlib
    matplotlib_data = collect_data_files('matplotlib')
    datas.extend(matplotlib_data)
except ImportError:
    pass

# Collect hidden imports
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'pandas',
    'geopandas',
    'matplotlib',
    'matplotlib.pyplot',
    'matplotlib.backends.backend_tkagg',
    'numpy',
    'shapely',
    'pyproj',
    'fiona',
    'pyogrio',
    'pathlib',
    'datetime',
    'os',
    'sys',
]

# Add geopandas hidden imports
try:
    geopandas_hidden = collect_submodules('geopandas')
    hiddenimports.extend(geopandas_hidden)
except ImportError:
    pass

# Add matplotlib hidden imports
try:
    matplotlib_hidden = collect_submodules('matplotlib')
    hiddenimports.extend(matplotlib_hidden)
except ImportError:
    pass

a = Analysis(
    ['GUI_MAP_Generator.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'test',
        'tests',
        'unittest',
        'pytest',
        'doctest',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'pydoc',
        'setuptools',
        'distutils',
        'pip',
        'wheel',
        'virtualenv',
        'venv',
    ],
    noarchive=False,
    optimize=0,  # Changed from 2 to 0 to fix docstring issue
)

pyz = PYZ(a.pure, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Montana_County_Map_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Changed from True to False to avoid issues
    upx=True,    # Use UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # Application icon
    version_file='version_info.txt',
    uac_admin=False,
    uac_uiaccess=False,
)
