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

### Para Usuarios Finales
Descarga los archivos ejecutables desde la sección [Releases](https://github.com/xKineticK/ResolutionChanger/releases):

**Opción 1: Instalador (Recomendado)**
- Descargar `ResolutionChanger-Setup.exe`
- Ejecutar como administrador
- Seguir las instrucciones

**Opción 2: Ejecutable Portátil**
- Descargar `ResolutionChanger.exe`
- Ejecutar directamente (requiere permisos de administrador)

### Para Desarrolladores
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

## 🔍 Estructura del Proyecto

```
ResolutionChanger/
├── src/                # Código fuente principal
│   ├── models/         # Lógica de datos y configuración
│   ├── views/          # Interfaces de usuario
│   ├── presenters/     # Lógica de presentación
│   └── services/       # Servicios externos (Steam, Windows API)
├── config/             # Archivos de configuración
├── resources/          # Recursos (iconos, imágenes)
├── run.py             # Punto de entrada principal
├── requirements.txt    # Dependencias Python
└── README.md          # Este archivo
```

## ⚠️ Nota sobre Antivirus

Algunos antivirus pueden marcar ejecutables de PyInstaller como falsos positivos. Si esto ocurre:
1. Añadir excepción para el archivo descargado
2. Ejecutar desde código fuente usando `python run.py`

## 📝 Licencia

Este proyecto es de código abierto bajo licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork del proyecto
2. Crear rama para tu feature
3. Commit de cambios 
4. Abrir Pull Request
