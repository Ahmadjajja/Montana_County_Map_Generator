# Montana County Map Generator - Build Script (PowerShell)
# This script creates an optimized executable with proper icons and metadata

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Montana County Map Generator - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
try {
    $pyinstallerVersion = pyinstaller --version
    Write-Host "✓ PyInstaller found: $pyinstallerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ PyInstaller not found. Please install it with: pip install pyinstaller" -ForegroundColor Red
    exit 1
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "__pycache__") { Remove-Item "__pycache__" -Recurse -Force }
Write-Host "✓ Cleaned previous builds" -ForegroundColor Green

Write-Host ""
Write-Host "Building executable with PyInstaller..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

# Build command with all optimizations
$buildArgs = @(
    "--clean",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--icon=app_icon.ico",
    "--name=Montana_County_Map_Generator",
    "--add-data=MontanaCounties_shp;MontanaCounties_shp",
    "--add-data=shapefiles;shapefiles",
    "--add-data=app_icon.ico;.",
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.filedialog",
    "--hidden-import=tkinter.messagebox",
    "--hidden-import=pandas",
    "--hidden-import=geopandas",
    "--hidden-import=matplotlib",
    "--hidden-import=matplotlib.pyplot",
    "--hidden-import=matplotlib.backends.backend_tkagg",
    "--hidden-import=numpy",
    "--hidden-import=shapely",
    "--hidden-import=pyproj",
    "--hidden-import=fiona",
    "--hidden-import=pyogrio",
    "--hidden-import=pathlib",
    "--hidden-import=datetime",
    "--exclude-module=test",
    "--exclude-module=tests",
    "--exclude-module=unittest",
    "--exclude-module=pytest",
    "--exclude-module=doctest",
    "--exclude-module=IPython",
    "--exclude-module=jupyter",
    "--exclude-module=notebook",
    "--exclude-module=sphinx",
    "--exclude-module=pydoc",
    "--exclude-module=setuptools",
    "--exclude-module=distutils",
    "--exclude-module=pip",
    "--exclude-module=wheel",
    "--exclude-module=virtualenv",
    "--exclude-module=venv",
    "--optimize=0",
    "GUI_MAP_Generator.py"
)

# Run PyInstaller
try {
    & pyinstaller @buildArgs
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "✓ Build completed successfully!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        
        $exePath = "dist\Montana_County_Map_Generator.exe"
        if (Test-Path $exePath) {
            $fileSize = [math]::Round((Get-Item $exePath).Length / 1MB, 2)
            Write-Host "Executable location: $exePath" -ForegroundColor Cyan
            Write-Host "File size: $fileSize MB" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "✓ Ready to distribute!" -ForegroundColor Green
        } else {
            Write-Host "✗ Executable not found at expected location" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ Build failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Error during build: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 