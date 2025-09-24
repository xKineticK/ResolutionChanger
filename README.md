# Resolution Changer# Resolution Changer



Una aplicación para cambiar la resolución de pantalla con funcionalidades especiales para gaming.# Resolution Changer



## ✨ CaracterísticasUna aplicación para cambiar la resolución de pantalla con funcionalidades especiales para gaming.



- 🎮 Cambio rápido de resolución con presets comunesUna aplicación para cambiar la res## 🔨 Desarrollo

- 📺 Soporte especial para resoluciones 4:3 (ideal para gaming retro)

- 🚀 Opción de configuración automática 4:3 al iniciar## ✨ Características

- 🎯 Integración con Steam para manejo automático de juegos

- 💾 Configuración persistente de preferencias### Requisitos

- 🎨 Interfaz moderna con PyQt6

- 🎮 Cambio rápido de resolución con presets comunes- Python 3.11+

## 🔧 Tecnologías

- 📺 Soporte especial para resoluciones 4:3 (ideal para gaming retro)- PyQt6

- **Python 3.11+** - Lenguaje de programación

- **PyQt6** - Framework de interfaz gráfica- 🚀 Opción de configuración automática 4:3 al iniciar- PyInstaller (para builds)

- **PyInstaller** - Empaquetado de ejecutables

- **NSIS** - Creación de instaladores profesionales- 🎯 Integración con Steam para manejo automático de juegos- NSIS (para instaladores)



## 🏗️ Arquitectura- 💾 Configuración persistente de preferencias



El proyecto utiliza el patrón MVP (Model-View-Presenter):- 🎨 Interfaz moderna con PyQt6### Configurar Entorno de Desarrollo



``````powershell

src/

├── models/          # Lógica de datos y configuración## 🔧 Tecnologías# Crear entorno virtual

├── views/           # Interfaces de usuario

├── presenters/      # Lógica de presentación y coordinaciónpython -m venv .venv

└── services/        # Servicios externos (Steam, Windows API)

```- **Python 3.11+** - Lenguaje de programación.venv\Scripts\activate



## 🚀 Instalación y Uso- **PyQt6** - Framework de interfaz gráfica



### Opción 1: Instalador (Recomendado)- **PyInstaller** - Empaquetado de ejecutables# Instalar dependencias

1. Descargar `ResolutionChanger-Safe-Setup.exe`

2. Ejecutar el instalador como administrador- **NSIS** - Creación de instaladores profesionalespip install -r requirements.txt

3. Seguir las instrucciones en pantalla

```

### Opción 2: Ejecutable Portátil

1. Descargar `ResolutionChanger-Safe.exe`## 🏗️ Arquitectura

2. Ejecutar directamente (requiere permisos de administrador)

### Ejecutar en Modo Desarrollo

### Opción 3: Desde Código Fuente

```powershellEl proyecto utiliza el patrón MVP (Model-View-Presenter):```powershell

# Clonar repositorio

git clone https://github.com/xKineticK/ResolutionChanger.gitpython run.py

cd ResolutionChanger

``````

# Crear entorno virtual

python -m venv .venvsrc/

.venv\Scripts\activate

├── models/          # Lógica de datos y configuración### Crear Build de Distribución

# Instalar dependencias

pip install -r requirements.txt├── views/           # Interfaces de usuario```powershell



# Ejecutar aplicación├── presenters/      # Lógica de presentación y coordinaciónpython build.py

python run.py

```└── services/        # Servicios externos (Steam, Windows API)```



## 🔨 Desarrollo```



### RequisitosEsto creará:

- Python 3.11+

- PyQt6## 🚀 Instalación y Uso- `dist/ResolutionChanger-Safe.exe` - Ejecutable optimizado

- PyInstaller (para builds)

- NSIS (para instaladores)- `ResolutionChanger-Safe-Setup.exe` - Instalador profesional



### Configurar Entorno de Desarrollo### Opción 1: Instalador (Recomendado)

```powershell

# Crear entorno virtual1. Descargar `ResolutionChanger-Safe-Setup.exe`## 🔍 Estructura del Proyecto

python -m venv .venv

.venv\Scripts\activate2. Ejecutar el instalador como administrador



# Instalar dependencias3. Seguir las instrucciones en pantalla```

pip install -r requirements.txt

```ResolutionChanger/



### Ejecutar en Modo Desarrollo### Opción 2: Ejecutable Portátil├── src/                     # Código fuente principal

```powershell

python run.py1. Descargar `ResolutionChanger-Safe.exe`│   ├── models/             

```

2. Ejecutar directamente (requiere permisos de administrador)│   ├── views/              

### Crear Build de Distribución

```powershell│   ├── presenters/         

python build.py

```### Opción 3: Desde Código Fuente│   └── services/           



Esto creará:```powershell├── resources/              # Recursos (iconos, configuraciones)

- `dist/ResolutionChanger-Safe.exe` - Ejecutable optimizado

- `ResolutionChanger-Safe-Setup.exe` - Instalador profesional# Clonar repositorio├── config/                 # Archivos de configuración



## 🔍 Estructura del Proyectogit clone https://github.com/tuusuario/ResolutionChanger.git├── games/                  # Módulos específicos de juegos



```cd ResolutionChanger├── run.py                  # Punto de entrada principal

ResolutionChanger/

├── src/                     # Código fuente principal├── build.py                # Script de construcción

│   ├── models/             

│   ├── views/              # Crear entorno virtual├── ResolutionChanger-Safe.spec  # Configuración PyInstaller

│   ├── presenters/         

│   └── services/           python -m venv .venv├── installer-safe.nsi      # Script instalador NSIS

├── resources/              # Recursos (iconos, configuraciones)

├── config/                 # Archivos de configuración.venv\Scripts\activate├── requirements.txt        # Dependencias Python

├── games/                  # Módulos específicos de juegos

├── run.py                  # Punto de entrada principal├── version_info_enhanced.txt # Metadatos del ejecutable

├── build.py                # Script de construcción

├── ResolutionChanger-Safe.spec  # Configuración PyInstaller# Instalar dependencias└── README.md              # Este archivo

├── installer-safe.nsi      # Script instalador NSIS

├── requirements.txt        # Dependencias Pythonpip install -r requirements.txt```con funcionalidades especiales para gaming.

├── version_info_enhanced.txt # Metadatos del ejecutable

└── README.md              # Este archivo

```

# Ejecutar aplicación## ✨ Características

## ⚠️ Consideraciones de Antivirus

python run.py

El ejecutable está optimizado para minimizar falsas detecciones de antivirus:

```- 🎮 Cambio rápido de resolución con presets comunes

- **UPX deshabilitado** - Sin compresión adicional

- **Módulos excluidos** - Se excluyen módulos que pueden ser marcados como sospechosos- 📺 Soporte especial para resoluciones 4:3 (ideal para gaming retro)

- **Metadatos completos** - Información detallada del archivo

- **Firma digital** - (Opcional) Para mayor confianza## 🔨 Desarrollo- 🚀 Opción de configuración automática 4:3 al iniciar



Si tu antivirus detecta el archivo:- 🎯 Integración con Steam para manejo automático de juegos

1. Añadir excepción para la carpeta de instalación

2. Reportar falso positivo al proveedor del antivirus### Requisitos- 💾 Configuración persistente de preferencias

3. Usar el código fuente para ejecutar directamente

- Python 3.11+- 🎨 Interfaz moderna con PyQt6

## 📝 Licencia

- PyQt6## 🔧 Tecnologías

Este proyecto es de código abierto. Consulta el archivo LICENSE para más detalles.

- PyInstaller (para builds)

## 🤝 Contribuciones

- NSIS (para instaladores)- **Python 3.11+** - Lenguaje de programación

Las contribuciones son bienvenidas. Por favor:

- **PyQt6** - Framework de interfaz gráfica

1. Fork del proyecto

2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)### Configurar Entorno de Desarrollo- **PyInstaller** - Empaquetado de ejecutables

3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)

4. Push a la rama (`git push origin feature/AmazingFeature`)```powershell- **NSIS** - Creación de instaladores profesionales

5. Abrir Pull Request

# Crear entorno virtual

## 🐛 Reportar Problemas

python -m venv .venv## 🏗️ Arquitectura

Si encuentras algún problema:

.venv\Scripts\activate

1. Revisar issues existentes

2. Crear nuevo issue con:El proyecto utiliza el patrón MVP (Model-View-Presenter):

   - Descripción detallada del problema

   - Pasos para reproducir# Instalar dependencias

   - Sistema operativo y versión

   - Logs de error (si aplica)pip install -r requirements.txt```



## 📋 Changelog```src/



### v1.0.0 (Actual)├── models/          # Lógica de datos y configuración

- ✅ Implementación MVP completa

- ✅ Funcionalidad 4:3 con auto-startup### Ejecutar en Modo Desarrollo├── views/           # Interfaces de usuario

- ✅ Integración Steam

- ✅ Instalador profesional```powershell├── presenters/      # Lógica de presentación y coordinación

- ✅ Optimización anti-antivirus

- ✅ Configuración persistentepython run.py└── services/        # Servicios externos (Steam, Windows API)



## 🔮 Roadmap``````



- [ ] Soporte para múltiples monitores

- [ ] Perfiles de resolución personalizados

- [ ] Integración con más plataformas de gaming### Crear Build de Distribución## 🚀 Instalación y Uso

- [ ] Modo oscuro/claro

- [ ] Notificaciones del sistema```powershell

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
