import vdf
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

class SteamGame:
    def __init__(self, appid, name):
        self.id = appid
        self.name = name

    def __repr__(self):
        return f"ID: {self.id}, Nombre: {self.name}"


def get_game_name(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data[str(appid)]["success"]:
            return data[str(appid)]["data"]["name"]
        else:
            return "Desconocido"
    except requests.RequestException:
        return "Error de conexión"
    # finally:
    #     time.sleep(0.2)


def process_manifest(manifest_path: str) -> SteamGame:
    """Procesa un único archivo manifest y retorna un objeto SteamGame"""
    try:
        with open(manifest_path, encoding='utf-8') as f:
            manifest = vdf.load(f)
        appid = manifest['AppState']['appid']
        name = get_game_name(appid)
        return SteamGame(appid, name)
    except Exception as e:
        print(f"⚠️ Error leyendo {os.path.basename(manifest_path)}: {e}")
        return None


def load_games() -> List[SteamGame]:
    games = []
    manifest_paths = []

    try:
        with open(r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf", encoding='utf-8') as f:
            data = vdf.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo libraryfolders.vdf")
        return games

    # Primero recolectamos todas las rutas de manifiestos
    libraries = data.get('libraryfolders', {})
    for entry in libraries.values():
        if isinstance(entry, dict) and "path" in entry:
            library_path = entry["path"]
            manifest_dir = os.path.join(library_path, "steamapps")
            
            try:
                for filename in os.listdir(manifest_dir):
                    if filename.startswith("appmanifest") and filename.endswith(".acf"):
                        manifest_paths.append(os.path.join(manifest_dir, filename))
            except Exception as e:
                print(f"⚠️ Error accediendo a {manifest_dir}: {e}")

    # Procesamos los manifiestos en paralelo
    with ThreadPoolExecutor(max_workers=30) as executor:
        future_to_manifest = {
            executor.submit(process_manifest, manifest_path): manifest_path 
            for manifest_path in manifest_paths
        }
        
        for future in as_completed(future_to_manifest):
            game = future.result()
            if game:
                games.append(game)

    return games


# def main():
#     print("🟡 Cargando juegos de Steam...")
#     games = load_games()
#     print(type(games))
#     print(f"✅ Se cargaron {len(games)} juegos.\n")

#     for game in games:
#         print(game.name)


# if __name__ == "__main__":
#     main()
