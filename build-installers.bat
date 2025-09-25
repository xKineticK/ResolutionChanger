@echo off
echo Building different installer versions...
echo.

:: Instalador completo (actual)
echo [1/4] Building full installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer-safe.nsi
if %errorlevel% neq 0 goto error

:: Instalador online (pequeño)
echo [2/4] Building online installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer-online.nsi
if %errorlevel% neq 0 goto error

:: Instalador mínimo
echo [3/4] Building minimal installer...
"C:\Program Files (x86)\NSIS\makensis.exe" installer-minimal.nsi
if %errorlevel% neq 0 goto error

:: Mostrar tamaños
echo [4/4] Installer sizes:
echo.
dir /B dist\*.exe | findstr -i installer > nul
if %errorlevel% equ 0 (
    for %%f in (dist\ResolutionChanger*.exe) do (
        echo %%~nxf: %%~zf bytes
    )
) else (
    for %%f in (dist\*.exe) do (
        echo %%~nxf: %%~zf bytes
    )
)

echo.
echo All installers built successfully!
goto end

:error
echo Error building installers!
exit /b 1

:end