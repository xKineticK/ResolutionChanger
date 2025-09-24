import threading
import time
from typing import Optional
from src.models.game_model import GameModel
from src.models.resolution_model import ResolutionModel
from src.services.steam_service import SteamService
from src.services.windows_service import WindowsService
from src.utils.config import ConfigManager

class MainPresenter:
    def __init__(self, view, game_model: GameModel, resolution_model: ResolutionModel):
        self.view = view
        self.game_model = game_model
        self.resolution_model = resolution_model
        self.steam_service = SteamService()
        self.windows_service = WindowsService()
        self.config_manager = ConfigManager()
        
        # Conectar señales de la vista
        self.view.resolution_changed.connect(self.on_resolution_change)
        self.view.game_selected.connect(self.on_game_select)
        self.view.play_clicked.connect(self.on_play_game)
        self.view.aspect_ratio_clicked.connect(self.calculate_4_3_resolution)
        self.view.auto_4_3_changed.connect(self.on_auto_4_3_change)
        
        # Inicialización
        self.load_initial_data()

    def load_initial_data(self) -> None:
        """Carga los datos iniciales"""
        # Cargar juegos
        games = self.steam_service.load_games()
        self.game_model.set_games(games)
        self.view.update_game_list([game.name for game in games])
        
        # Cargar resoluciones
        resolutions = self.resolution_model.get_all_resolutions()
        self.view.update_resolution_list(list(resolutions.keys()))
        
        # Cargar información del sistema
        system_info = self.windows_service.get_display_info()
        self.view.update_system_info(system_info)
        
        # Cargar configuración de 4:3 automático
        auto_4_3 = self.config_manager.get("auto_4_3")
        self.view.set_auto_4_3(auto_4_3)
        
        # Si está activado el 4:3 automático, calcular resolución 4:3
        if auto_4_3:
            self.calculate_4_3_resolution()

    def on_resolution_change(self, resolution_str: str) -> None:
        """Maneja el cambio de resolución seleccionada"""
        resolution = self.resolution_model.get_resolution(resolution_str)
        if resolution:
            self.view.log_info(f"Selected resolution: {resolution_str}")

    def on_game_select(self, game_name: str) -> None:
        """Maneja la selección de juego"""
        game = self.game_model.select_game(game_name)
        if game:
            self.view.log_info(f"Selected game: {game_name}")

    def on_play_game(self) -> None:
        """Maneja el inicio del juego"""
        game = self.game_model.get_selected_game()
        if not game:
            self.view.show_error("Please select a game first")
            return

        resolution = self.view.get_current_resolution()
        if not resolution:
            self.view.show_error("Please select a resolution")
            return

        steam_path = self.view.get_steam_path()
        if not steam_path:
            self.view.show_error("Please set Steam path first")
            return

        # Cambiar resolución y lanzar juego
        res_tuple = self.resolution_model.get_resolution(resolution)
        if res_tuple:
            width, height = res_tuple
            if self.windows_service.change_resolution(width, height):
                self.steam_service.launch_game(steam_path, game.id)
                self._monitor_game(game)
            else:
                self.view.show_error("Failed to change resolution")

    def calculate_4_3_resolution(self) -> None:
        """Calcula y establece una resolución 4:3"""
        # Obtener la resolución actual del sistema
        current_width, current_height = self.windows_service._get_current_resolution()
        self.view.log_info(f"Current resolution: {current_width}x{current_height}")
        
        # Calcular la resolución 4:3
        width, height = self.resolution_model.calculate_4_3_resolution(current_width, current_height)
        resolution_str = f"{width}x{height}"
        self.view.log_info(f"Calculated 4:3 resolution: {resolution_str}")
        
        # Añadir la resolución si no existe
        if self.resolution_model.add_resolution(width, height):
            self.view.log_info(f"Added new resolution: {resolution_str}")
            resolutions = self.resolution_model.get_all_resolutions()
            self.view.update_resolution_list(list(resolutions.keys()))
        
        # Seleccionar la resolución
        self.view.set_current_resolution(resolution_str)
        self.view.log_info(f"Selected 4:3 resolution: {resolution_str}")

    def _monitor_game(self, game) -> None:
        """Monitorea el estado del juego y restaura la resolución cuando termina"""
        def monitor():
            self.view.log_info(f"Monitoring {game.name}...")
            while True:
                running_id = self.windows_service.get_running_game_id()
                if running_id == game.id:
                    break
                time.sleep(1)

            self.view.log_info(f"Game {game.name} is running")
            
            while True:
                running_id = self.windows_service.get_running_game_id()
                if running_id != game.id:
                    break
                time.sleep(2)

            self.windows_service.restore_original_resolution()
            self.view.log_info(f"Game {game.name} closed, resolution restored")

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def on_auto_4_3_change(self, enabled: bool) -> None:
        """Maneja cambios en la opción de 4:3 automático"""
        self.config_manager.set("auto_4_3", enabled)
        self.view.log_info(f"Auto 4:3 {'enabled' if enabled else 'disabled'}")