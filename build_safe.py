#!/usr/bin/env python3
"""
Script de construcción mejorado con técnicas anti-antivirus
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_optimized_spec():
    """Crea un archivo .spec optimizado para reducir detecciones de antivirus"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

# Configuración optimizada para reducir falsos positivos de antivirus
block_cipher = None

# Archivos de datos necesarios
added_files = [
    ('resources', 'resources'),
    ('src/config', 'config'),
]

# Exclusiones para reducir tamaño y falsos positivos
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'cv2',
    'tensorflow',
    'torch',
    'jupyter',
    'IPython',
    'sphinx',
    'pytest',
    'setuptools',
    'distutils',
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'win32api',
        'win32con',
        'win32gui',
        'pywintypes'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ResolutionChanger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Desactivar UPX para evitar detecciones
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/images/icon.ico',
    version='version_info.txt'
)
'''
    
    with open('ResolutionChanger-Safe.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec optimizado para antivirus creado")

def create_enhanced_version_info():
    """Crea información de versión más detallada"""
    version_info = '''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [
        StringStruct('CompanyName', 'xKineticK'),
        StringStruct('FileDescription', 'Resolution Changer - Display Resolution Management Tool'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'ResolutionChanger'),
        StringStruct('LegalCopyright', '© 2025 xKineticK. All rights reserved.'),
        StringStruct('LegalTrademarks', ''),
        StringStruct('OriginalFilename', 'ResolutionChanger.exe'),
        StringStruct('ProductName', 'Resolution Changer'),
        StringStruct('ProductVersion', '1.0.0.0'),
        StringStruct('Assembly Version', '1.0.0.0'),
        StringStruct('Comments', 'Professional display resolution management utility')
        ])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info_enhanced.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✅ Información de versión mejorada creada")

def build_safe_executable():
    """Construye ejecutable con técnicas anti-detección"""
    print("🛡️ Construyendo ejecutable optimizado para antivirus...")
    
    # Usar Python del entorno virtual
    python_exe = sys.executable
    venv_python = ".venv/Scripts/python.exe"
    if os.path.exists(venv_python):
        python_exe = os.path.abspath(venv_python)
    
    # Actualizar el spec para usar version info mejorada
    with open('ResolutionChanger-Safe.spec', 'r') as f:
        content = f.read()
    
    content = content.replace("version='version_info.txt'", "version='version_info_enhanced.txt'")
    
    with open('ResolutionChanger-Safe.spec', 'w') as f:
        f.write(content)
    
    # Comando PyInstaller optimizado
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "ResolutionChanger-Safe.spec"
    ]
    
    try:
        subprocess.check_call(cmd)
        
        # Renombrar el ejecutable resultante
        if os.path.exists("dist/ResolutionChanger.exe"):
            if os.path.exists("dist/ResolutionChanger-Safe.exe"):
                os.remove("dist/ResolutionChanger-Safe.exe")
            os.rename("dist/ResolutionChanger.exe", "dist/ResolutionChanger-Safe.exe")
        
        print("✅ Ejecutable optimizado creado: dist/ResolutionChanger-Safe.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la construcción: {e}")
        return False

def main():
    """Función principal"""
    print("=== Resolution Changer - Build Optimizado para Antivirus ===")
    
    # Limpiar construcciones anteriores
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Crear configuraciones optimizadas
    create_optimized_spec()
    create_enhanced_version_info()
    
    # Construir ejecutable optimizado
    if build_safe_executable():
        print("\\n🎉 ¡Ejecutable optimizado para antivirus creado exitosamente!")
        print("📂 Archivo: dist/ResolutionChanger-Safe.exe")
        print("\\n📋 Siguientes pasos recomendados:")
        print("1. Subir ejecutable a VirusTotal para verificar detecciones")
        print("2. Reportar falsos positivos a los fabricantes de antivirus")
        print("3. Considerar firma digital para distribución profesional")
    else:
        print("\\n❌ La construcción falló")
        sys.exit(1)

if __name__ == "__main__":
    main()