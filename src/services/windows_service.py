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
            devmode = pywintypes.DEVMODEType()
            devmode.PelsWidth = width
            devmode.PelsHeight = height
            devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
            win32api.ChangeDisplaySettings(devmode, 0)
            return True
        except Exception:
            return False

    def restore_original_resolution(self) -> bool:
        """Restaura la resolución original"""
        width, height = self.original_resolution
        return self.change_resolution(width, height)

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