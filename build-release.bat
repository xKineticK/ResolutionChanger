@echo off
echo ================================
echo  Resolution Changer - Build Release
echo ================================
echo.

:: Limpiar dist anterior
echo [1/4] Cleaning previous builds...
del /Q "dist\*.exe" 2>nul

:: Generar ejecutables
echo [2/4] Building executables...
call .venv\Scripts\python.exe -m PyInstaller ResolutionChanger-Safe.spec --clean
if %errorlevel% neq 0 goto error

:: Generar instalador oficial
echo [3/4] Building official installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer-online.nsi
if %errorlevel% neq 0 goto error

:: Mostrar resultado final
echo [4/4] Release files ready:
echo.
for %%f in (dist\ResolutionChanger*.exe) do (
    echo   %%~nxf (%%~zf bytes)
)

echo.
echo ================================
echo ✅ RELEASE BUILD COMPLETED!
echo ================================
echo.
echo Ready for GitHub Release:
echo   📦 ResolutionChanger.exe (Official Installer)
echo   💾 ResolutionChanger-Portable.exe (Portable Version)
echo.
goto end

:error
echo ❌ Build failed!
exit /b 1

:end