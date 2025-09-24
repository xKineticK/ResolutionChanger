# Resolution Changer

Una aplicación para cambiar la resolución de pantalla con funcionalidades especiales para gaming.

##  Características

-  Cambio rápido de resolución con presets comunes
-  Soporte especial para resoluciones 4:3 (ideal para gaming retro)
-  Opción de configuración automática 4:3 al iniciar
-  Integración con Steam para manejo automático de juegos
-  Configuración persistente de preferencias
-  Interfaz moderna con PyQt6

##  Tecnologías

- **Python 3.11+** - Lenguaje de programación
- **PyQt6** - Framework de interfaz gráfica
- **PyInstaller** - Empaquetado de ejecutables
- **NSIS** - Creación de instaladores profesionales

##  Arquitectura

El proyecto utiliza el patrón MVP (Model-View-Presenter):

```
src/
 models/          # Lógica de datos y configuración
 views/           # Interfaces de usuario
 presenters/      # Lógica de presentación y coordinación
 services/        # Servicios externos (Steam, Windows API)
```

##  Instalación y Uso

### Opción 1: Instalador (Recomendado)
1. Descargar ResolutionChanger-Safe-Setup.exe
2. Ejecutar el instalador como administrador
3. Seguir las instrucciones en pantalla

### Opción 2: Ejecutable Portátil
1. Descargar ResolutionChanger-Safe.exe
2. Ejecutar directamente (requiere permisos de administrador)

### Opción 3: Desde Código Fuente
```powershell
# Clonar repositorio
git clone https://github.com/xKineticK/ResolutionChanger.git
cd ResolutionChanger

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python run.py
```

##  Desarrollo

### Requisitos
- Python 3.11+
- PyQt6
- PyInstaller (para builds)
- NSIS (para instaladores)

### Configurar Entorno de Desarrollo
```powershell
# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar en Modo Desarrollo
```powershell
python run.py
```

### Crear Build de Distribución
```powershell
python build.py
```

Esto creará:
- dist/ResolutionChanger-Safe.exe - Ejecutable optimizado
- ResolutionChanger-Safe-Setup.exe - Instalador profesional

##  Consideraciones de Antivirus

El ejecutable está optimizado para minimizar falsas detecciones de antivirus:

- **UPX deshabilitado** - Sin compresión adicional
- **Módulos excluidos** - Se excluyen módulos que pueden ser marcados como sospechosos
- **Metadatos completos** - Información detallada del archivo

Si tu antivirus detecta el archivo:
1. Añadir excepción para la carpeta de instalación
2. Reportar falso positivo al proveedor del antivirus
3. Usar el código fuente para ejecutar directamente

##  Licencia

Este proyecto es de código abierto. Consulta el archivo LICENSE para más detalles.

##  Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork del proyecto
2. Crear rama para tu feature
3. Commit de cambios
4. Push a la rama
5. Abrir Pull Request

##  Changelog

### v1.0.0 (Actual)
-  Implementación MVP completa
-  Funcionalidad 4:3 con auto-startup
-  Integración Steam
-  Instalador profesional
-  Optimización anti-antivirus
-  Configuración persistente
