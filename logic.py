# logic.py
import subprocess
import win32api
import win32con
import pywintypes
import psutil
import threading
import time
from loggingLib import printInfo, printWarning, printError

original_width = win32api.GetSystemMetrics(0)
original_height = win32api.GetSystemMetrics(1)
process = None

game_id = None

class Game:
    def __init__(self, name, id, icon, process):
        self.name = name
        self.id = id
        self.icon = icon
        self.process = process

def change_resolution(selected_resolution):
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

def open_game_in_steam(steam_path, game_var, resolution_var):
    global process
    global game_id
    selected_game_name = game_var
    if steam_path:
        game_id = None
        for game in games:
            if game.name == selected_game_name:
                game_id = game.id
                process = game.process
                break

        if game_id is not None:
            change_resolution(resolution_var)
            printInfo(f"Abriendo juego {selected_game_name} con ID {game_id}")
            subprocess.Popen([steam_path, f'steam://rungameid/{game_id}'])
            hilo = threading.Thread(target=monitor_process_by_name, args=(process,), daemon=True)
            hilo.start()
        else:
            printError("No se encontró el juego seleccionado en la lista de juegos.")
    else:
        printError("La ruta de Steam no está configurada.")

def monitor_process_by_name(process):
    printInfo(f"Esperando que se inicie el proceso: {process}")
    while True:
        if any(proc.info['name'] == process for proc in psutil.process_iter(attrs=['name'])):
            printInfo(f"{process} detectado, esperando que finalice...")
            break
        time.sleep(1)

    while True:
        if not any(proc.info['name'] == process for proc in psutil.process_iter(attrs=['name'])):
            printInfo(f"Proceso {process} finalizado")
            break
        time.sleep(2)

    restore_resolution(original_width, original_height)

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

games = [
    Game("Counter-Strike 2", 730, "icon_cs2.png", "cs2.exe"),
    Game("Rust", 252490, "icon_rust.png", "RustClient.exe"),
    Game("PUBG", 578080, "icon_pubg.png", "TslGame.exe")
]

resolutions = {
    "3840x2160": (3840, 2160),
    "2560x1440": (2560, 1440),
    "1920x1080": (1920, 1080),
    "1920x1060": (1920, 1060),
    "1600x1200": (1600, 1200),
    "1280x1024": (1280, 1024),
    "1280x960": (1280, 960)
}