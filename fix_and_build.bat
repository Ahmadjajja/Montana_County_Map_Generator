@echo off
echo ========================================
echo Fixing and Rebuilding Montana County Map Generator
echo ========================================
echo.

echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo Cleaned!

echo.
echo Building with fixed settings (no optimization to avoid docstring error)...
echo.

pyinstaller GUI_MAP_Generator.spec

echo.
echo ========================================
echo Build completed!
echo ========================================
echo.
echo The executable should now work without the docstring error.
echo Location: dist\Montana_County_Map_Generator.exe
echo.
pause 