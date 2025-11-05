@echo off
echo ===============================================
echo Creating executable for Quadric Surfaces...
echo ===============================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Build executable
echo Building executable...
pyinstaller --onefile --windowed --name="QuadricSurfaces" --icon=NONE quadric_surfaces.py

echo.
echo ===============================================
echo Build complete!
echo Executable location: dist\QuadricSurfaces.exe
echo ===============================================
echo.
pause
