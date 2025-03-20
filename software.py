import subprocess
import win32api
import win32con
import pywintypes
import psutil
import time
import threading
import customtkinter as ctk

# Tu código relacionado con el funcionamiento del software va aquí
original_width = win32api.GetSystemMetrics(0)
original_height = win32api.GetSystemMetrics(1)
process = None

# Clase para representar un juego


class Game:
    def __init__(self, name, id, icon, process):
        self.name = name
        self.id = id
        self.icon = icon
        self.process = process


# Función para cambiar la resolución
def change_resolution(selected_resolution):
    # Define resoluciones disponibles
    selectedRes = resolutions[selected_resolution]

    # Cambia la resolución a la nueva configuración
    if selectedRes != (original_width, original_height):
        devmode = pywintypes.DEVMODEType()
        devmode.PelsWidth = selectedRes[0]
        devmode.PelsHeight = selectedRes[1]
        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
        win32api.ChangeDisplaySettings(devmode, 0)


def restore_resolution(original_width, original_height):
    # Restaura la resolución original
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = original_width
    devmode.PelsHeight = original_height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)


def open_game_in_steam(steam_path, game_var, resolution_var):
    global process
    global game_id
    selected_game_name = game_var
    if steam_path:
        # Busca el juego seleccionado en la lista de juegos y obtén su ID
        game_id = None
        for game in games:
            if f"{game.name}" == selected_game_name:
                game_id = game.id
                process = game.process
                break

        if game_id is not None:
            change_resolution(resolution_var)
            subprocess.Popen([steam_path, f'steam://rungameid/{game_id}'])
            hilo = threading.Thread(
                target=monitor_process_by_name, args=(process,))
            hilo.start()

        else:
            print("No se encontró el juego seleccionado en la lista de juegos.")
    else:
        print("La ruta de Steam no está configurada.")


def monitor_process_by_name(process):
    time.sleep(30)
    while True:
        found = False
        for processes in psutil.process_iter(attrs=['pid', 'name']):
            if processes.info['name'] == process:
                found = True
                time.sleep(3)
                break
        if not found:
            break
    restore_resolution(original_width, original_height)


def get_aspect_ratio():
    # getcontext().prec = 2
    res = original_width / original_height
    res = round(res, 2)
    match res:
        case 1.78:
            relation_aspect = "16:9"
        case 1.6:
            relation_aspect = "16:10"
        case 1.33:
            relation_aspect = "4:3"
        case _:
            relation_aspect = ""
    return relation_aspect


def get_recomended_resolution(relation_aspect):
    if relation_aspect == "4:3":
        recommended_resolution = "You are already on 4:3"
    elif relation_aspect == "16:9" and original_width == 1920:
        recommended_resolution = "1280x960"
    elif relation_aspect == "16:9" and original_width == 2560:
        recommended_resolution = "1600x1200"
    elif relation_aspect == "16:9" and original_width == 3840:
        recommended_resolution = "2880x2160"
    else:
        recommended_resolution = ""

    return recommended_resolution


info = {
    "Resolution": f"{original_width}x{original_height}",
    "Aspect ratio": get_aspect_ratio(),
    "4:3 Resolution": get_recomended_resolution(get_aspect_ratio())
}

# Lista de juegos
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
    # Esta opción te permite ingresar una resolución personalizada
    # "Custom Resolution": (0, 0)
}
