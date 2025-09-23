# logic.py
import subprocess
import win32api
import win32con
import pywintypes
import psutil
import threading
import time
import winreg
from loggingLib import printInfo, printWarning, printError
from games.steam import *
from resolutions import ResolutionManager  # Asegúrate de que esta línea importe correctamente tu clase ResolutionManager

original_width = win32api.GetSystemMetrics(0)
original_height = win32api.GetSystemMetrics(1)
process = None

# Eliminar el diccionario resolutions del final del archivo ya que ahora está manejado por ResolutionManager
# Mantener solo estas líneas para la gestión de resoluciones:
resolution_manager = ResolutionManager()
resolutions = resolution_manager.get_all_resolutions()

# Asegúrate de que estas variables estén disponibles para importar
__all__ = ['resolutions', 'info', 'open_game_in_steam', 'resolution_manager']

def change_resolution(selected_resolution):
    # Obtener las resoluciones actualizadas
    resolutions = resolution_manager.get_all_resolutions()
    if selected_resolution not in resolutions:
        printError(f"Resolución no válida: {selected_resolution}")
        return
        
    selectedRes = resolutions[selected_resolution]
    if selectedRes != (original_width, original_height):
        printInfo(f"Cambiando resolución a {selectedRes[0]}x{selectedRes[1]}")
        devmode = pywintypes.DEVMODEType()
        devmode.PelsWidth = selectedRes[0]
        devmode.PelsHeight = selectedRes[1]
        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
        win32api.ChangeDisplaySettings(devmode, 0)
    else:
        printInfo("La resolución ya está establecida. No se realiza cambio.")

def restore_resolution(width, height):
    printInfo(f"Restaurando resolución original a {width}x{height}")
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)

def get_running_app_id():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Valve\\Steam")
        value, _ = winreg.QueryValueEx(key, "RunningAppID")
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return 0

def monitor_game_via_registry(target_game_name, target_game_id):
    printInfo(f"Waiting for game {target_game_name} to start...")
    time.sleep(2)  # Espera inicial para evitar problemas de sincronización
    while True:
        running_id = get_running_app_id()
        if int(running_id) == int(target_game_id):
            printInfo(f"Running {target_game_name}. Waiting to exit to restore resolution.")
            break
        time.sleep(1)

    while True:
        running_id = get_running_app_id()
        if int(running_id) != int(target_game_id):
            printInfo(f"Game {target_game_name} has exited. Restoring resolution.")
            break
        time.sleep(2)

    restore_resolution(original_width, original_height)

def open_game_in_steam(steam_path, game_var, resolution_var, games):
    selected_game_name = game_var
    if steam_path:
        game_id = None
        for game in games:
            if game.name == selected_game_name:
                game_id = game.id
                break

        if game_id is not None:
            change_resolution(resolution_var)
            printInfo(f"Abriendo juego {selected_game_name} con ID {game_id}")
            subprocess.Popen([steam_path, f'steam://rungameid/{game_id}'])
            hilo = threading.Thread(target=monitor_game_via_registry, args=(selected_game_name, game_id), daemon=True)
            hilo.start()
        else:
            printError("No se encontró el juego seleccionado en la lista de juegos.")
    else:
        printError("La ruta de Steam no está configurada.")

def get_aspect_ratio():
    ratio = round(original_width / original_height, 2)
    match ratio:
        case 1.78: return "16:9"
        case 1.6: return "16:10"
        case 1.33: return "4:3"
        case _: return ""

def get_recommended_resolution(aspect_ratio):
    if aspect_ratio == "4:3": return "You are already on 4:3"
    if aspect_ratio == "16:9" and original_width == 1920: return "1280x960"
    if aspect_ratio == "16:9" and original_width == 2560: return "1600x1200"
    if aspect_ratio == "16:9" and original_width == 3840: return "2880x2160"
    return ""


info = {
    "Resolution": f"{original_width}x{original_height}",
    "Aspect ratio": get_aspect_ratio(),
    "4:3 Resolution": get_recommended_resolution(get_aspect_ratio())
}
