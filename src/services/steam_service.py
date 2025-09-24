import vdf
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
from src.models.game_model import Game

class SteamService:
    def __init__(self):
        self.default_steam_path = "C:/Program Files (x86)/Steam/steam.exe"

    def _get_game_name(self, appid: str) -> str:
        """Obtiene el nombre del juego desde la API de Steam"""
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data[str(appid)]["success"]:
                return data[str(appid)]["data"]["name"]
        except requests.RequestException:
            pass
        return "Unknown"

    def _process_manifest(self, manifest_path: str) -> Optional[Game]:
        """Procesa un archivo manifest de Steam"""
        try:
            with open(manifest_path, encoding='utf-8') as f:
                manifest = vdf.load(f)
            appid = manifest['AppState']['appid']
            name = self._get_game_name(appid)
            return Game(appid, name)
        except Exception:
            return None

    def load_games(self) -> List[Game]:
        """Carga todos los juegos instalados de Steam"""
        games = []
        manifest_paths = []

        try:
            with open(r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf", encoding='utf-8') as f:
                data = vdf.load(f)
        except FileNotFoundError:
            return games

        # Recolectar rutas de manifiestos
        libraries = data.get('libraryfolders', {})
        for entry in libraries.values():
            if isinstance(entry, dict) and "path" in entry:
                library_path = entry["path"]
                manifest_dir = os.path.join(library_path, "steamapps")
                
                try:
                    for filename in os.listdir(manifest_dir):
                        if filename.startswith("appmanifest") and filename.endswith(".acf"):
                            manifest_paths.append(os.path.join(manifest_dir, filename))
                except Exception:
                    continue

        # Procesar manifiestos en paralelo
        with ThreadPoolExecutor(max_workers=30) as executor:
            future_to_manifest = {
                executor.submit(self._process_manifest, manifest_path): manifest_path 
                for manifest_path in manifest_paths
            }
            
            for future in as_completed(future_to_manifest):
                game = future.result()
                if game:
                    games.append(game)

        return games

    def launch_game(self, steam_path: str, game_id: str) -> None:
        """Lanza un juego de Steam"""
        import subprocess
        steam_path = steam_path or self.default_steam_path
        subprocess.Popen([steam_path, f'steam://rungameid/{game_id}'])