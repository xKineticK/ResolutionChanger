# Resolution Changer

# Resolution Changer

Una aplicación para cambiar la resolución de pantalla con funcionalidades especiales para gaming.

Una aplicación para cambiar la res## 🔨 Desarrollo

## ✨ Características

### Requisitos

- 🎮 Cambio rápido de resolución con presets comunes- Python 3.11+

- 📺 Soporte especial para resoluciones 4:3 (ideal para gaming retro)- PyQt6

- 🚀 Opción de configuración automática 4:3 al iniciar- PyInstaller (para builds)

- 🎯 Integración con Steam para manejo automático de juegos- NSIS (para instaladores)

- 💾 Configuración persistente de preferencias

- 🎨 Interfaz moderna con PyQt6### Configurar Entorno de Desarrollo

```powershell

## 🔧 Tecnologías# Crear entorno virtual

python -m venv .venv

- **Python 3.11+** - Lenguaje de programación.venv\Scripts\activate

- **PyQt6** - Framework de interfaz gráfica

- **PyInstaller** - Empaquetado de ejecutables# Instalar dependencias

- **NSIS** - Creación de instaladores profesionalespip install -r requirements.txt

```

## 🏗️ Arquitectura

### Ejecutar en Modo Desarrollo

El proyecto utiliza el patrón MVP (Model-View-Presenter):```powershell

python run.py

``````

src/

├── models/          # Lógica de datos y configuración### Crear Build de Distribución

├── views/           # Interfaces de usuario```powershell

├── presenters/      # Lógica de presentación y coordinaciónpython build.py

└── services/        # Servicios externos (Steam, Windows API)```

```

Esto creará:

## 🚀 Instalación y Uso- `dist/ResolutionChanger-Safe.exe` - Ejecutable optimizado

- `ResolutionChanger-Safe-Setup.exe` - Instalador profesional

### Opción 1: Instalador (Recomendado)

1. Descargar `ResolutionChanger-Safe-Setup.exe`## 🔍 Estructura del Proyecto

2. Ejecutar el instalador como administrador

3. Seguir las instrucciones en pantalla```

ResolutionChanger/

### Opción 2: Ejecutable Portátil├── src/                     # Código fuente principal

1. Descargar `ResolutionChanger-Safe.exe`│   ├── models/             

2. Ejecutar directamente (requiere permisos de administrador)│   ├── views/              

│   ├── presenters/         

### Opción 3: Desde Código Fuente│   └── services/           

```powershell├── resources/              # Recursos (iconos, configuraciones)

# Clonar repositorio├── config/                 # Archivos de configuración

git clone https://github.com/tuusuario/ResolutionChanger.git├── games/                  # Módulos específicos de juegos

cd ResolutionChanger├── run.py                  # Punto de entrada principal

├── build.py                # Script de construcción

# Crear entorno virtual├── ResolutionChanger-Safe.spec  # Configuración PyInstaller

python -m venv .venv├── installer-safe.nsi      # Script instalador NSIS

.venv\Scripts\activate├── requirements.txt        # Dependencias Python

├── version_info_enhanced.txt # Metadatos del ejecutable

# Instalar dependencias└── README.md              # Este archivo

pip install -r requirements.txt```con funcionalidades especiales para gaming.



# Ejecutar aplicación## ✨ Características

python run.py

```- 🎮 Cambio rápido de resolución con presets comunes

- 📺 Soporte especial para resoluciones 4:3 (ideal para gaming retro)

## 🔨 Desarrollo- 🚀 Opción de configuración automática 4:3 al iniciar

- 🎯 Integración con Steam para manejo automático de juegos

### Requisitos- 💾 Configuración persistente de preferencias

- Python 3.11+- 🎨 Interfaz moderna con PyQt6

- PyQt6## 🔧 Tecnologías

- PyInstaller (para builds)

- NSIS (para instaladores)- **Python 3.11+** - Lenguaje de programación

- **PyQt6** - Framework de interfaz gráfica

### Configurar Entorno de Desarrollo- **PyInstaller** - Empaquetado de ejecutables

```powershell- **NSIS** - Creación de instaladores profesionales

# Crear entorno virtual

python -m venv .venv## 🏗️ Arquitectura

.venv\Scripts\activate

El proyecto utiliza el patrón MVP (Model-View-Presenter):

# Instalar dependencias

pip install -r requirements.txt```

```src/

├── models/          # Lógica de datos y configuración

### Ejecutar en Modo Desarrollo├── views/           # Interfaces de usuario

```powershell├── presenters/      # Lógica de presentación y coordinación

python run.py└── services/        # Servicios externos (Steam, Windows API)

``````



### Crear Build de Distribución## 🚀 Instalación y Uso

```powershell

python build.py### Opción 1: Instalador (Recomendado)

```1. Descargar `ResolutionChanger-Safe-Setup.exe`

2. Ejecutar el instalador como administrador

Esto creará:3. Seguir las instrucciones en pantalla

- `dist/ResolutionChanger-Safe.exe` - Ejecutable optimizado

- `ResolutionChanger-Safe-Setup.exe` - Instalador profesional### Opción 2: Ejecutable Portátil

1. Descargar `ResolutionChanger-Safe.exe`

## 🔍 Estructura del Proyecto2. Ejecutar directamente (requiere permisos de administrador)



```### Opción 3: Desde Código Fuente

ResolutionChanger/```powershell

├── src/                     # Código fuente principal# Clonar repositorio

│   ├── models/             git clone https://github.com/tuusuario/ResolutionChanger.git

│   ├── views/              cd ResolutionChanger

│   ├── presenters/         

│   └── services/           # Crear entorno virtual

├── resources/              # Recursos (iconos, configuraciones)python -m venv .venv

├── config/                 # Archivos de configuración.venv\Scripts\activate

├── games/                  # Módulos específicos de juegos

├── run.py                  # Punto de entrada principal# Instalar dependencias

├── build.py                # Script de construcciónpip install -r requirements.txt

├── ResolutionChanger-Safe.spec  # Configuración PyInstaller

├── installer-safe.nsi      # Script instalador NSIS# Ejecutar aplicación

├── requirements.txt        # Dependencias Pythonpython run.py

├── version_info_enhanced.txt # Metadatos del ejecutable```

└── README.md              # Este archivo

```### For Developers



## ⚠️ Consideraciones de Antivirus#### Build the Project

```bash

El ejecutable está optimizado para minimizar falsas detecciones de antivirus:# Install dependencies

pip install -r requirements.txt

- **UPX deshabilitado** - Sin compresión adicional

- **Módulos excluidos** - Se excluyen módulos que pueden ser marcados como sospechosos# Build professional executable

- **Metadatos completos** - Información detallada del archivopython build_clean.py

- **Firma digital** - (Opcional) Para mayor confianza```



Si tu antivirus detecta el archivo:#### Create Installer

1. Añadir excepción para la carpeta de instalación```bash

2. Reportar falso positivo al proveedor del antivirus# After building, create professional installer

3. Usar el código fuente para ejecutar directamente"C:\Program Files (x86)\NSIS\makensis.exe" installer-professional.nsi

```

## 📝 Licencia

## � Project Structure

Este proyecto es de código abierto. Consulta el archivo LICENSE para más detalles.

```

## 🤝 ContribucionesResolutionChanger/

├── src/                          # Source code (MVP architecture)

Las contribuciones son bienvenidas. Por favor:│   ├── models/                   # Data models

│   ├── views/                    # UI components

1. Fork del proyecto│   ├── presenters/              # Business logic

2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)│   ├── services/                # External services

3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)│   └── utils/                   # Utilities and config management

4. Push a la rama (`git push origin feature/AmazingFeature`)├── resources/                   # Images and assets

5. Abrir Pull Request├── config/                      # Default configuration files

├── run.py                       # Application entry point

## 🐛 Reportar Problemas├── build_clean.py              # Professional build script

├── installer-professional.nsi  # NSIS installer script

Si encuentras algún problema:└── version_info.txt            # Windows version info

```

1. Revisar issues existentes

2. Crear nuevo issue con:## 🛠️ Development Tools

   - Descripción detallada del problema

   - Pasos para reproducir| File | Purpose |

   - Sistema operativo y versión|------|---------|

   - Logs de error (si aplica)| `build_clean.py` | Creates professional single-file executable |

| `installer-professional.nsi` | Creates Windows installer |

## 📋 Changelog| `version_info.txt` | Windows executable version information |

| `requirements.txt` | Python dependencies |

### v1.0.0 (Actual)

- ✅ Implementación MVP completa## 📦 Distribution Files

- ✅ Funcionalidad 4:3 con auto-startup

- ✅ Integración Steam- **`dist/ResolutionChanger.exe`** - Single executable file

- ✅ Instalador profesional- **`ResolutionChanger-Professional-Setup.exe`** - Windows installer

- ✅ Optimización anti-antivirus

- ✅ Configuración persistente## 🏗️ Architecture



## 🔮 RoadmapThe project follows MVP (Model-View-Presenter) architecture:



- [ ] Soporte para múltiples monitores- **Models**: Data structures and business entities

- [ ] Perfiles de resolución personalizados- **Views**: PyQt6 UI components and windows

- [ ] Integración con más plataformas de gaming- **Presenters**: Bridge between views and models, handles business logic

- [ ] Modo oscuro/claro- **Services**: External API integrations (Steam, Windows API)

- [ ] Notificaciones del sistema- **Utils**: Configuration management, logging, utilities
- Custom resolution support
- Automatic resolution restoration
- Real-time logging
- 4:3 aspect ratio calculation
- Auto 4:3 on startup option
- Configuration persistence in AppData

## 🚀 Installation

### Option 1: Download Pre-built Executable
1. Download the latest release from the [Releases](https://github.com/xKineticK/ResolutionChanger/releases) page
2. Choose between:
   - **Installer**: `ResolutionChanger-Setup.exe` - Full installation with Start Menu shortcuts
   - **Portable**: `ResolutionChanger_Portable.zip` - No installation required
3. Launch Resolution Changer from the Start Menu, Desktop shortcut, or directly from the portable folder

### Option 2: Build from Source

#### Requirements
- Python 3.11 or above
- Steam installed
- Windows operating system

#### Quick Build (Windows)
```batch
# Clone the repository
git clone https://github.com/xKineticK/ResolutionChanger.git
cd ResolutionChanger

# Run the quick build script
build.bat
```

#### Manual Build

1. Clone the repository:
```bash
git clone https://github.com/xKineticK/ResolutionChanger.git
cd ResolutionChanger
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## ▶️ Usage

Run the application:
```bash
python run.py
```

## 🏗️ Project Structure

```
ResolutionChanger/
├── src/
│   ├── models/          # Data and business logic
│   ├── views/           # UI components
│   ├── presenters/      # Application logic
│   ├── services/        # External services integration
│   └── utils/           # Utility functions and classes
├── config/             # Configuration files
├── resources/          # Application resources
└── tests/             # Unit tests
```

## 🛠️ Development

This project follows the MVP (Model-View-Presenter) architecture pattern:

- **Models**: Handle data and business logic
- **Views**: Handle user interface
- **Presenters**: Handle application logic and user input
- **Services**: Handle external integrations
- **Utils**: Common utilities and helpers

## 💡 Credits

Developed by xKineticK with ♥ and a little bit of madness for aspect ratio.
