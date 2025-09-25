import win32api
import win32con
import pywintypes
import winreg
from typing import Tuple, Optional

class WindowsService:
    def __init__(self):
        self.original_resolution = self._get_current_resolution()

    def _get_current_resolution(self) -> Tuple[int, int]:
        """Obtiene la resolución actual del sistema"""
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        return (width, height)

    def change_resolution(self, width: int, height: int) -> bool:
        """Cambia la resolución del sistema"""
        try:
            from ..utils.logger import log_info, log_error
            
            # Verificar si la resolución ya es la actual
            current_width, current_height = self._get_current_resolution()
            if current_width == width and current_height == height:
                log_info(f"Resolution {width}x{height} is already active")
                return True
            
            # Método 1: Configuración básica
            log_info(f"Trying basic resolution change to {width}x{height}")
            devmode = pywintypes.DEVMODEType()
            devmode.PelsWidth = width
            devmode.PelsHeight = height
            devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
            
            result = win32api.ChangeDisplaySettings(devmode, 0)
            if result == win32con.DISP_CHANGE_SUCCESSFUL:
                log_info("Basic resolution change successful")
                return True
            
            # Método 2: Con configuración completa
            log_info(f"Trying enhanced resolution change to {width}x{height}")
            devmode = pywintypes.DEVMODEType()
            devmode.PelsWidth = width
            devmode.PelsHeight = height
            devmode.BitsPerPel = 32
            devmode.DisplayFrequency = 60
            devmode.Fields = (win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT | 
                             win32con.DM_BITSPERPEL | win32con.DM_DISPLAYFREQUENCY)
            
            result = win32api.ChangeDisplaySettings(devmode, 0)
            if result == win32con.DISP_CHANGE_SUCCESSFUL:
                log_info("Enhanced resolution change successful")
                return True
            
            # Método 3: Con registro permanente
            log_info(f"Trying permanent resolution change to {width}x{height}")
            result = win32api.ChangeDisplaySettings(devmode, win32con.CDS_UPDATEREGISTRY)
            if result == win32con.DISP_CHANGE_SUCCESSFUL:
                log_info("Permanent resolution change successful")
                return True
            
            # Reportar el error específico
            error_messages = {
                win32con.DISP_CHANGE_BADMODE: "The graphics mode is not supported",
                win32con.DISP_CHANGE_BADFLAGS: "An invalid set of flags was passed",
                win32con.DISP_CHANGE_BADPARAM: "An invalid parameter was passed",
                win32con.DISP_CHANGE_FAILED: "The display driver failed the specified graphics mode",
                win32con.DISP_CHANGE_NOTUPDATED: "Unable to write settings to the registry",
                win32con.DISP_CHANGE_RESTART: "The computer must be restarted for the graphics mode to work"
            }
            
            error_msg = error_messages.get(result, f"Unknown error code: {result}")
            log_error(f"Resolution change failed: {error_msg}")
            
            return False
                
        except Exception as e:
            try:
                from ..utils.logger import log_error
                log_error(f"Exception during resolution change to {width}x{height}: {str(e)}")
            except:
                pass
            return False

    def restore_original_resolution(self) -> bool:
        """Restaura la resolución original"""
        width, height = self.original_resolution
        return self.change_resolution(width, height)
    
    def verify_resolution_change(self, expected_width: int, expected_height: int) -> bool:
        """Verifica si la resolución cambió correctamente"""
        import time
        time.sleep(0.5)  # Esperar un momento para que el cambio tome efecto
        current_width, current_height = self._get_current_resolution()
        return current_width == expected_width and current_height == expected_height
    
    def get_available_resolutions(self) -> list:
        """Obtiene las resoluciones disponibles en el sistema"""
        resolutions = set()
        try:
            i = 0
            while True:
                try:
                    devmode = win32api.EnumDisplaySettings(None, i)
                    width = devmode.PelsWidth
                    height = devmode.PelsHeight
                    if width >= 800 and height >= 600:  # Filtrar resoluciones muy pequeñas
                        resolutions.add((width, height))
                    i += 1
                except:
                    break
            
            # Convertir a lista ordenada
            return sorted(list(resolutions), key=lambda x: (x[0], x[1]))
            
        except Exception as e:
            try:
                from ..utils.logger import log_error
                log_error(f"Failed to enumerate display settings: {str(e)}")
            except:
                pass
            return []
    
    def is_resolution_supported(self, width: int, height: int) -> bool:
        """Verifica si una resolución está soportada por el sistema"""
        available = self.get_available_resolutions()
        return (width, height) in available

    def get_running_game_id(self) -> Optional[str]:
        """Obtiene el ID del juego en ejecución desde el registro de Steam"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Valve\\Steam")
            value, _ = winreg.QueryValueEx(key, "RunningAppID")
            winreg.CloseKey(key)
            return str(value) if value != 0 else None
        except FileNotFoundError:
            return None

    def get_display_info(self) -> dict:
        """Obtiene información del display"""
        width, height = self.original_resolution
        ratio = round(width / height, 2)
        
        aspect_ratio = {
            1.78: "16:9",
            1.6: "16:10",
            1.33: "4:3"
        }.get(ratio, "Unknown")

        return {
            "Resolution": f"{width}x{height}",
            "Aspect ratio": aspect_ratio,
            "Original resolution": f"{width}x{height}"
        }