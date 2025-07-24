@echo off
echo Building Montana County Map Generator...
echo.

pyinstaller --clean --noconfirm --onefile --windowed --icon=app_icon.ico --name="Montana_County_Map_Generator" --add-data="MontanaCounties_shp;MontanaCounties_shp" --add-data="shapefiles;shapefiles" --add-data="app_icon.ico;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --hidden-import=pandas --hidden-import=geopandas --hidden-import=matplotlib --hidden-import=matplotlib.pyplot --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=numpy --hidden-import=shapely --hidden-import=pyproj --hidden-import=fiona --hidden-import=pyogrio --hidden-import=pathlib --hidden-import=datetime --exclude-module=test --exclude-module=tests --exclude-module=unittest --exclude-module=pytest --exclude-module=doctest --exclude-module=IPython --exclude-module=jupyter --exclude-module=notebook --exclude-module=sphinx --exclude-module=pydoc --exclude-module=setuptools --exclude-module=distutils --exclude-module=pip --exclude-module=wheel --exclude-module=virtualenv --exclude-module=venv --optimize=0 GUI_MAP_Generator.py

echo.
echo Build completed! Check dist/Montana_County_Map_Generator.exe
pause 