import vdf
import requests
import time
import os

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


def load_games():
    games = []

    try:
        with open(r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf", encoding='utf-8') as f:
            data = vdf.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo libraryfolders.vdf")
        return games

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
                        name = get_game_name(appid)
                        game = SteamGame(appid, name)
                        games.append(game)
                    except Exception as e:
                        print(f"⚠️ Error leyendo {filename}: {e}")
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
