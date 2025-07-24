# Montana County Map Generator - Build Instructions

This document explains how to build the executable (.exe) file for the Montana County Distribution Map Generator.

## Prerequisites

1. **Python 3.8+** installed
2. **PyInstaller** installed: `pip install pyinstaller`
3. **All dependencies** installed: `pip install -r requirements.txt`

## Build Options

### Option 1: Using the Spec File (Recommended)
```bash
pyinstaller GUI_MAP_Generator.spec
```

### Option 2: Using the Batch Script (Windows)
```bash
build_exe.bat
```

### Option 3: Using the PowerShell Script (Windows)
```powershell
.\build_exe.ps1
```

### Option 4: Direct PyInstaller Command
```bash
pyinstaller --clean --noconfirm --onefile --windowed --icon=app_icon.ico --name="Montana_County_Map_Generator" --add-data="MontanaCounties_shp;MontanaCounties_shp" --add-data="shapefiles;shapefiles" --add-data="app_icon.ico;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --hidden-import=pandas --hidden-import=geopandas --hidden-import=matplotlib --hidden-import=matplotlib.pyplot --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=numpy --hidden-import=shapely --hidden-import=pyproj --hidden-import=fiona --hidden-import=pyogrio --hidden-import=pathlib --hidden-import=datetime --exclude-module=test --exclude-module=tests --exclude-module=unittest --exclude-module=pytest --exclude-module=doctest --exclude-module=IPython --exclude-module=jupyter --exclude-module=notebook --exclude-module=sphinx --exclude-module=pydoc --exclude-module=setuptools --exclude-module=distutils --exclude-module=pip --exclude-module=wheel --exclude-module=virtualenv --exclude-module=venv --optimize=0 GUI_MAP_Generator.py
```

## Build Features

### ✅ No Console Window
- Uses `--windowed` flag to prevent console window from appearing

### ✅ Professional Icons
- Application icon in taskbar, file explorer, and application windows
- Uses `app_icon.ico` for consistent branding

### ✅ Optimized Size
- `--onefile`: Creates a single executable file
- `--optimize=0`: No bytecode optimization (prevents docstring errors)
- Excludes unnecessary modules (tests, documentation, etc.)

### ✅ Complete Dependencies
- Includes all required data files (shapefiles, icons)
- Hidden imports for all necessary modules
- Proper handling of geopandas and matplotlib dependencies

### ✅ Professional Metadata
- Version information embedded in executable
- Company name, description, and copyright information
- Proper file properties in Windows

## Output

The build process creates:
- **Executable**: `dist/Montana_County_Map_Generator.exe`
- **Size**: Typically 50-100 MB (depending on dependencies)
- **Compatibility**: Windows 10/11 (64-bit)

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **PyInstaller Not Found**
   ```bash
   pip install pyinstaller
   ```

3. **Large File Size**
   - This is normal for applications with scientific libraries
   - The executable includes Python runtime and all dependencies

4. **Antivirus False Positives**
   - Some antivirus software may flag PyInstaller executables
   - Add the executable to your antivirus whitelist

### Performance Tips

1. **Use SSD**: Building on an SSD is significantly faster
2. **Close Other Applications**: Free up RAM during build
3. **Clean Builds**: Delete `dist` and `build` folders before rebuilding

## Distribution

The generated executable is self-contained and can be distributed to users without requiring Python installation. Users only need to:

1. Download the `.exe` file
2. Run it directly (no installation required)
3. The application will create maps in their Downloads folder

## File Structure After Build

```
dist/
└── Montana_County_Map_Generator.exe  # Your executable
```

The executable contains all necessary files embedded within it, making distribution simple and reliable. 