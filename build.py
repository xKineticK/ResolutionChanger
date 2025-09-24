#!/usr/bin/env python3#!/usr/bin/env python3#!/usr/bin/env python3

"""

Build script para Resolution Changer""""""

Crea ejecutable optimizado y instalador profesional

"""Build script para Resolution ChangerScript de construcción para Resolution Changer



import osCrea ejecutable optimizado y instalador profesionalCrea un ejecutable usando PyInstaller

import shutil

import subprocess""""""

import sys

from pathlib import Path



def clean_build():import osimport os

    """Limpia directorios de construcción"""

    dirs_to_clean = ['build', '__pycache__']import shutilimport shutil

    

    for dir_name in dirs_to_clean:import subprocessimport subprocess

        if os.path.exists(dir_name):

            print(f"🧹 Limpiando: {dir_name}")import sysimport sys

            shutil.rmtree(dir_name)

from pathlib import Pathfrom pathlib import Path

def check_environment():

    """Verifica el entorno de desarrollo"""

    python_exe = sys.executable

    venv_python = ".venv/Scripts/python.exe"def clean_build():def clean_build():

    

    if os.path.exists(venv_python):    """Limpia directorios de construcción"""    """Limpia directorios de construcción anteriores"""

        python_exe = os.path.abspath(venv_python)

        print(f"✅ Usando entorno virtual: {python_exe}")    dirs_to_clean = ['build', '__pycache__']    dirs_to_clean = ['build', 'dist', '__pycache__']

    else:

        print("⚠️  No se encontró entorno virtual")        

    

    # Verificar dependencias    for dir_name in dirs_to_clean:    for dir_name in dirs_to_clean:

    try:

        result = subprocess.run([python_exe, "-c", "import PyQt6; print(f'PyQt6: OK')"],         if os.path.exists(dir_name):        if os.path.exists(dir_name):

                              capture_output=True, text=True)

        if result.returncode == 0:            print(f"🧹 Limpiando: {dir_name}")            print(f"Limpiando directorio: {dir_name}")

            print("✅ PyQt6: OK")

        else:            shutil.rmtree(dir_name)            shutil.rmtree(dir_name)

            print("❌ PyQt6 no encontrado")

            return False    

    except Exception as e:

        print(f"❌ Error verificando PyQt6: {e}")def check_environment():    # Limpiar archivos .pyc

        return False

        """Verifica el entorno de desarrollo"""    for root, dirs, files in os.walk('.'):

    return python_exe

    python_exe = sys.executable        for file in files:

def build_executable(python_exe):

    """Construye el ejecutable optimizado"""    venv_python = ".venv/Scripts/python.exe"            if file.endswith('.pyc'):

    print("🔨 Construyendo ejecutable...")

                        os.remove(os.path.join(root, file))

    cmd = [

        python_exe, "-m", "PyInstaller",    if os.path.exists(venv_python):

        "--clean",

        "--noconfirm",        python_exe = os.path.abspath(venv_python)def check_requirements():

        "ResolutionChanger-Safe.spec"

    ]        print(f"✅ Usando entorno virtual: {python_exe}")    """Verifica que PyInstaller esté instalado"""

    

    try:    else:    # Usar el ejecutable Python del entorno virtual si existe

        subprocess.check_call(cmd)

                print("⚠️  No se encontró entorno virtual")    python_exe = sys.executable

        # Renombrar el resultado

        if os.path.exists("dist/ResolutionChanger.exe"):        venv_python = ".venv/Scripts/python.exe"

            if os.path.exists("dist/ResolutionChanger-Safe.exe"):

                os.remove("dist/ResolutionChanger-Safe.exe")    # Verificar dependencias    if os.path.exists(venv_python):

            os.rename("dist/ResolutionChanger.exe", "dist/ResolutionChanger-Safe.exe")

            try:        python_exe = os.path.abspath(venv_python)

        print("✅ Ejecutable creado: dist/ResolutionChanger-Safe.exe")

        return True        result = subprocess.run([python_exe, "-c", "import PyQt6; print(f'PyQt6: OK')"],         print(f"Usando Python del entorno virtual: {python_exe}")

        

    except subprocess.CalledProcessError as e:                              capture_output=True, text=True)    

        print(f"❌ Error construyendo ejecutable: {e}")

        return False        if result.returncode == 0:    try:



def create_installer():            print("✅ PyQt6: OK")        # Verificar PyInstaller

    """Crea el instalador NSIS"""

    print("📦 Creando instalador...")        else:        result = subprocess.run([python_exe, "-c", "import PyInstaller; print(f'PyInstaller: {PyInstaller.__version__}')"], 

    

    nsis_path = "C:/Program Files (x86)/NSIS/makensis.exe"            print("❌ PyQt6 no encontrado")                              capture_output=True, text=True)

    if not os.path.exists(nsis_path):

        nsis_path = "C:/Program Files/NSIS/makensis.exe"            return False        if result.returncode == 0:

    

    if not os.path.exists(nsis_path):    except Exception as e:            print(result.stdout.strip())

        print("❌ NSIS no encontrado. Instala NSIS para crear el instalador.")

        return False        print(f"❌ Error verificando PyQt6: {e}")        else:

    

    try:        return False            print("PyInstaller no encontrado. Instalando...")

        subprocess.check_call([nsis_path, "installer-safe.nsi"])

        print("✅ Instalador creado: ResolutionChanger-Safe-Setup.exe")                subprocess.check_call([python_exe, "-m", "pip", "install", "pyinstaller"])

        return True

    except subprocess.CalledProcessError as e:    return python_exe        

        print(f"❌ Error creando instalador: {e}")

        return False        # Verificar PyQt6



def main():def build_executable(python_exe):        result = subprocess.run([python_exe, "-c", "from PyQt6.QtCore import PYQT_VERSION_STR; print(f'PyQt6: {PYQT_VERSION_STR}')"], 

    """Función principal"""

    print("🚀 === Resolution Changer Build Script ===")    """Construye el ejecutable optimizado"""                              capture_output=True, text=True)

    

    # Limpiar construcciones anteriores    print("🔨 Construyendo ejecutable...")        if result.returncode == 0:

    clean_build()

                    print(result.stdout.strip())

    # Verificar entorno

    python_exe = check_environment()    cmd = [        else:

    if not python_exe:

        print("❌ Error en el entorno")        python_exe, "-m", "PyInstaller",            print("PyQt6 no encontrado. Instalando...")

        sys.exit(1)

            "--clean",            subprocess.check_call([python_exe, "-m", "pip", "install", "PyQt6"])

    # Construir ejecutable

    if not build_executable(python_exe):        "--noconfirm",        

        print("❌ Falló la construcción del ejecutable")

        sys.exit(1)        "ResolutionChanger-Safe.spec"        return True

    

    # Crear instalador    ]    except Exception as e:

    if not create_installer():

        print("⚠️  No se pudo crear el instalador (NSIS no disponible)")            print(f"Error verificando dependencias: {e}")

    

    print("\n🎉 ¡Build completado exitosamente!")    try:        return False

    print("📂 Ejecutable: dist/ResolutionChanger-Safe.exe")

    print("📦 Instalador: ResolutionChanger-Safe-Setup.exe")        subprocess.check_call(cmd)



if __name__ == "__main__":        def build_executable():

    main()
        # Renombrar el resultado    """Construye el ejecutable usando PyInstaller"""

        if os.path.exists("dist/ResolutionChanger.exe"):    print("Construyendo ejecutable...")

            if os.path.exists("dist/ResolutionChanger-Safe.exe"):    

                os.remove("dist/ResolutionChanger-Safe.exe")    # Usar el ejecutable Python del entorno virtual si existe

            os.rename("dist/ResolutionChanger.exe", "dist/ResolutionChanger-Safe.exe")    python_exe = sys.executable

            venv_python = ".venv/Scripts/python.exe"

        print("✅ Ejecutable creado: dist/ResolutionChanger-Safe.exe")    if os.path.exists(venv_python):

        return True        python_exe = os.path.abspath(venv_python)

                print(f"Usando Python del entorno virtual: {python_exe}")

    except subprocess.CalledProcessError as e:    

        print(f"❌ Error construyendo ejecutable: {e}")    # Comando PyInstaller usando el Python correcto

        return False    cmd = [

        python_exe, "-m", "PyInstaller",

def create_installer():        "--clean",

    """Crea el instalador NSIS"""        "--noconfirm",

    print("📦 Creando instalador...")        "ResolutionChanger.spec"

        ]

    nsis_path = "C:/Program Files (x86)/NSIS/makensis.exe"    

    if not os.path.exists(nsis_path):    try:

        nsis_path = "C:/Program Files/NSIS/makensis.exe"        subprocess.check_call(cmd)

            print("✅ Construcción completada exitosamente!")

    if not os.path.exists(nsis_path):        return True

        print("❌ NSIS no encontrado. Instala NSIS para crear el instalador.")    except subprocess.CalledProcessError as e:

        return False        print(f"❌ Error en la construcción: {e}")

            return False

    try:

        subprocess.check_call([nsis_path, "installer-safe.nsi"])def create_installer():

        print("✅ Instalador creado: ResolutionChanger-Safe-Setup.exe")    """Crea un instalador usando NSIS (si está disponible)"""

        return True    nsis_script = """

    except subprocess.CalledProcessError as e:; Resolution Changer Installer Script

        print(f"❌ Error creando instalador: {e}")!define APPNAME "Resolution Changer"

        return False!define COMPANYNAME "ResolutionChanger"  

!define DESCRIPTION "Change screen resolution for gaming"

def main():!define VERSIONMAJOR 1

    """Función principal"""!define VERSIONMINOR 0

    print("🚀 === Resolution Changer Build Script ===")!define VERSIONBUILD 0

    

    # Limpiar construcciones anteriores!define HELPURL "https://github.com/xKineticK/ResolutionChanger"

    clean_build()!define UPDATEURL "https://github.com/xKineticK/ResolutionChanger"

    !define ABOUTURL "https://github.com/xKineticK/ResolutionChanger"

    # Verificar entorno

    python_exe = check_environment()!define INSTALLSIZE 100000  ; Estimate in KB

    if not python_exe:

        print("❌ Error en el entorno")RequestExecutionLevel admin

        sys.exit(1)InstallDir "$PROGRAMFILES\\${COMPANYNAME}\\${APPNAME}"

    

    # Construir ejecutableName "${APPNAME}"

    if not build_executable(python_exe):Icon "resources\\images\\icon.ico"

        print("❌ Falló la construcción del ejecutable")outFile "ResolutionChanger-Setup.exe"

        sys.exit(1)

    !include LogicLib.nsh

    # Crear instalador!include MUI2.nsh

    if not create_installer():

        print("⚠️  No se pudo crear el instalador (NSIS no disponible)"); Interface Settings

    !define MUI_ABORTWARNING

    print("\n🎉 ¡Build completado exitosamente!")!define MUI_ICON "resources\\images\\icon.ico"

    print("📂 Ejecutable: dist/ResolutionChanger-Safe.exe")!define MUI_UNICON "resources\\images\\icon.ico"

    print("📦 Instalador: ResolutionChanger-Safe-Setup.exe")

; Pages

if __name__ == "__main__":!insertmacro MUI_PAGE_WELCOME

    main()!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required to install ${APPNAME}!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

; Main application files
Section "Resolution Changer (required)" SecMain
    SectionIn RO  ; Read only - required
    
    SetOutPath $INSTDIR
    File /r "dist\\ResolutionChanger\\*"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    ; Registry entries for Add/Remove programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$INSTDIR\\resources\\images\\icon.ico"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "HelpLink" "${HELPURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
    
    ; Create AppData directory for configurations
    CreateDirectory "$APPDATA\\ResolutionChanger"
    
    ; Copy default configuration files if they don't exist
    IfFileExists "$APPDATA\\ResolutionChanger\\settings.json" +2 0
        File /oname=$APPDATA\\ResolutionChanger\\settings.json "src\\config\\default_settings.json"
    
    IfFileExists "$APPDATA\\ResolutionChanger\\resolutions.json" +2 0
        File /oname=$APPDATA\\ResolutionChanger\\resolutions.json "src\\config\\resolutions.json"
SectionEnd

; Start Menu shortcuts
Section "Start Menu Shortcuts" SecStartMenu
    CreateDirectory "$SMPROGRAMS\\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\ResolutionChanger.exe" "" "$INSTDIR\\resources\\images\\icon.ico" 0 SW_SHOWNORMAL "" "${DESCRIPTION}"
    CreateShortCut "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall ${APPNAME}.lnk" "$INSTDIR\\uninstall.exe" "" "$INSTDIR\\uninstall.exe" 0 SW_SHOWNORMAL "" "Uninstall ${APPNAME}"
SectionEnd

; Desktop shortcut
Section "Desktop Shortcut" SecDesktop
    CreateShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\ResolutionChanger.exe" "" "$INSTDIR\\resources\\images\\icon.ico" 0 SW_SHOWNORMAL "" "${DESCRIPTION}"
SectionEnd

; Section descriptions
LangString DESC_SecMain ${LANG_ENGLISH} "Main application files (required)"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "Create shortcuts in Start Menu"
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create shortcut on Desktop"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller
Section "Uninstall"
    ; Remove application files
    RMDir /r "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\\${COMPANYNAME}\\Uninstall ${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\\${COMPANYNAME}"
    Delete "$DESKTOP\\${APPNAME}.lnk"
    
    ; Ask if user wants to keep configuration files
    MessageBox MB_YESNO|MB_ICONQUESTION "Do you want to keep your configuration files and settings?" IDYES KeepConfig
    RMDir /r "$APPDATA\\ResolutionChanger"
    KeepConfig:
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"
SectionEnd
"""
    
    # Escribir script NSIS
    with open("installer.nsi", "w") as f:
        f.write(nsis_script)
    
    print("Script de instalador NSIS mejorado creado: installer.nsi")
    print("Características incluidas:")
    print("  ✅ Interfaz moderna con páginas de bienvenida")
    print("  ✅ Instalación en Program Files")
    print("  ✅ Configuración en AppData (automática)")
    print("  ✅ Accesos directos opcionales (Start Menu + Desktop)")
    print("  ✅ Desinstalador que pregunta por configuración")
    print("  ✅ Registro en Add/Remove Programs")
    print("Para crear el instalador, ejecuta: makensis installer.nsi")

def main():
    """Función principal"""
    print("=== Resolution Changer Build Script ===")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("run.py"):
        print("❌ Error: Este script debe ejecutarse desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Limpiar construcciones anteriores
    clean_build()
    
    # Verificar dependencias
    if not check_requirements():
        sys.exit(1)
    
    # Construir ejecutable
    if build_executable():
        print("\n🎉 ¡Ejecutable creado exitosamente!")
        print("📁 Ubicación: dist/ResolutionChanger/ResolutionChanger.exe")
        
        # Crear script de instalador
        create_installer()
        
        print("\n📝 Próximos pasos:")
        print("1. Prueba el ejecutable en: dist/ResolutionChanger/ResolutionChanger.exe")
        print("2. Para crear un instalador, instala NSIS y ejecuta: makensis installer.nsi")
        print("3. Para crear versión portátil, ejecuta: python create_portable.py")
        
        # Preguntar si crear versión portátil
        try:
            response = input("\n¿Crear también versión portátil? (s/n): ").lower().strip()
            if response in ['s', 'si', 'y', 'yes']:
                print("\n📦 Creando versión portátil...")
                import subprocess
                subprocess.call([sys.executable, "create_portable.py"])
        except KeyboardInterrupt:
            print("\n\nOperación cancelada.")
    else:
        print("❌ Error en la construcción")
        sys.exit(1)

if __name__ == "__main__":
    main()