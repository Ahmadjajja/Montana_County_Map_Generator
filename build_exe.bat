@echo off
echo ========================================
echo Montana County Map Generator - Build Script
echo ========================================
echo.

echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo Cleaned!

echo.
echo Building executable with PyInstaller...
echo This may take several minutes...
echo.

pyinstaller --clean ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --icon=app_icon.ico ^
    --name="Montana_County_Map_Generator" ^
    --add-data="MontanaCounties_shp;MontanaCounties_shp" ^
    --add-data="shapefiles;shapefiles" ^
    --add-data="app_icon.ico;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=pandas ^
    --hidden-import=geopandas ^
    --hidden-import=matplotlib ^
    --hidden-import=matplotlib.pyplot ^
    --hidden-import=matplotlib.backends.backend_tkagg ^
    --hidden-import=numpy ^
    --hidden-import=shapely ^
    --hidden-import=pyproj ^
    --hidden-import=fiona ^
    --hidden-import=pyogrio ^
    --hidden-import=pathlib ^
    --hidden-import=datetime ^
    --exclude-module=test ^
    --exclude-module=tests ^
    --exclude-module=unittest ^
    --exclude-module=pytest ^
    --exclude-module=doctest ^
    --exclude-module=IPython ^
    --exclude-module=jupyter ^
    --exclude-module=notebook ^
    --exclude-module=sphinx ^
    --exclude-module=pydoc ^
    --exclude-module=setuptools ^
    --exclude-module=distutils ^
    --exclude-module=pip ^
    --exclude-module=wheel ^
    --exclude-module=virtualenv ^
    --exclude-module=venv ^
    --optimize=0 ^
    --upx-dir=upx ^
    GUI_MAP_Generator.py

echo.
echo ========================================
echo Build completed!
echo ========================================
echo.
echo Executable location: dist\Montana_County_Map_Generator.exe
echo.
echo Press any key to exit...
pause > nul 