import vdf
import requests
import time
import os

class SteamGames:
    def __init__(self):
        self.games = []  # lista de dicts con id, name y exe_path

    def load_games(self):
        try:
            with open(r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf", encoding='utf-8') as f:
                data = vdf.load(f)
        except FileNotFoundError:
            print("❌ No se encontró el archivo libraryfolders.vdf")
            return

        libraries = data.get('libraryfolders', {})

        for entry in libraries.values():
            if isinstance(entry, dict) and "path" in entry:
                library_path = entry["path"]
                manifest_dir = os.path.join(library_path, "steamapps")

                for filename in os.listdir(manifest_dir):
                    if filename.startswith("appmanifest") and filename.endswith(".acf"):
                        manifest_path = os.path.join(manifest_dir, filename)
                        try:
                            with open(manifest_path, encoding='utf-8') as f:
                                manifest = vdf.load(f)
                            appid = manifest['AppState']['appid']
                            install_dir = manifest['AppState'].get('installdir')
                            full_path = os.path.join(library_path, "steamapps", "common", install_dir)

                            name = self.get_game_name(appid)

                            self.games.append({
                                "id": appid,
                                "name": name,
                                "path": full_path
                            })
                        except Exception as e:
                            print(f"⚠️ Error leyendo {filename}: {e}")

    def get_game_name(self, appid):
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
        finally:
            time.sleep(0.2)


def main():
    print("🟡 Cargando juegos de Steam...")
    steam_games = SteamGames()
    steam_games.load_games()
    print("✅ Juegos cargados correctamente.\n")

    for game in steam_games.games:
        print(f"{game['id']}: {game['name']} | Ruta: {game['path']}")


if __name__ == "__main__":
    main()
