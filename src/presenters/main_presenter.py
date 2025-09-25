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
        self.view.custom_resolution_requested.connect(self.on_custom_resolution_request)
        self.view.remember_last_changed.connect(self.on_remember_last_change)
        
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
        
        # Mostrar resoluciones disponibles del sistema
        available_resolutions = self.windows_service.get_available_resolutions()
        if available_resolutions:
            self.view.log_info(f"System supports {len(available_resolutions)} resolutions")
        
        # Cargar configuración de 4:3 automático
        auto_4_3 = self.config_manager.get("auto_4_3")
        if auto_4_3 is None:
            auto_4_3 = False
        self.view.set_auto_4_3(auto_4_3)
        
        # Cargar configuración de recordar última resolución
        remember_last = self.config_manager.get("remember_last_resolution")
        if remember_last is None:
            remember_last = False
        self.view.set_remember_last(remember_last)
        
        # Cargar última resolución si está habilitado
        if remember_last:
            last_resolution = self.config_manager.get("last_resolution")
            if last_resolution:
                # Verificar que la resolución existe en el modelo
                if self.resolution_model.get_resolution(last_resolution):
                    self.view.set_current_resolution(last_resolution)
                    self.view.log_info(f"Restored last resolution: {last_resolution}")
        
        # Si está activado el 4:3 automático y NO está recordar última, calcular resolución 4:3
        elif auto_4_3:
            self.calculate_4_3_resolution()

    def on_resolution_change(self, resolution_str: str) -> None:
        """Maneja el cambio de resolución seleccionada"""
        resolution = self.resolution_model.get_resolution(resolution_str)
        if resolution:
            self.view.log_info(f"Selected resolution: {resolution_str}")
            
            # Guardar como última resolución si está habilitado
            remember_last = self.config_manager.get("remember_last_resolution")
            if remember_last:
                self.config_manager.set("last_resolution", resolution_str)

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
            
            # Verificar si la resolución está soportada
            if not self.windows_service.is_resolution_supported(width, height):
                self.view.log_warning(f"Resolution {width}x{height} may not be supported by your system")
                available_resolutions = self.windows_service.get_available_resolutions()
                if available_resolutions:
                    self.view.log_info(f"Available resolutions: {available_resolutions[:5]}...")  # Mostrar solo las primeras 5
            
            self.view.log_info(f"Attempting to change resolution to {width}x{height}")
            
            if self.windows_service.change_resolution(width, height):
                # Verificar que el cambio fue exitoso
                if self.windows_service.verify_resolution_change(width, height):
                    self.view.log_info(f"Resolution successfully changed to {width}x{height}")
                    self.steam_service.launch_game(steam_path, game.id)
                    self._monitor_game(game)
                else:
                    self.view.log_warning(f"Resolution change may have failed - current resolution doesn't match expected")
                    # Continuar con el juego de todos modos
                    self.steam_service.launch_game(steam_path, game.id)
                    self._monitor_game(game)
            else:
                self.view.show_error("Failed to change resolution")
                self.view.log_error(f"Could not change resolution to {width}x{height}")

    def calculate_4_3_resolution(self) -> None:
        """Calcula y establece una resolución 4:3"""
        # Obtener la resolución actual del sistema
        current_width, current_height = self.windows_service._get_current_resolution()
        self.view.log_info(f"Current resolution: {current_width}x{current_height}")
        
        # Obtener resoluciones disponibles del sistema
        available_resolutions = self.windows_service.get_available_resolutions()
        
        # Calcular la resolución 4:3 considerando las disponibles
        width, height = self.resolution_model.calculate_4_3_resolution(current_width, current_height, available_resolutions)
        resolution_str = f"{width}x{height}"
        
        # Verificar si la resolución calculada está disponible
        if available_resolutions and (width, height) not in available_resolutions:
            self.view.log_warning(f"Calculated 4:3 resolution {resolution_str} not in system's available resolutions")
            # Buscar la mejor 4:3 disponible
            four_three_available = []
            for w, h in available_resolutions:
                ratio = round(w / h, 2)
                if abs(ratio - 4/3) < 0.05:  # Tolerancia para 4:3
                    four_three_available.append((w, h))
            
            if four_three_available:
                # Tomar la más grande que quepa en la pantalla actual
                four_three_available.sort(key=lambda x: x[0] * x[1], reverse=True)
                for w, h in four_three_available:
                    if w <= current_width and h <= current_height:
                        width, height = w, h
                        resolution_str = f"{width}x{height}"
                        break
                else:
                    # Si ninguna cabe, tomar la más pequeña
                    width, height = four_three_available[-1]
                    resolution_str = f"{width}x{height}"
                
                self.view.log_info(f"Using available 4:3 resolution: {resolution_str}")
        else:
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
        
        # Si se habilita auto 4:3, deshabilitar remember last
        if enabled:
            self.config_manager.set("remember_last_resolution", False)
            self.view.set_remember_last(False)
            self.view.log_info("Remember last resolution disabled (auto 4:3 enabled)")
        
        self.view.log_info(f"Auto 4:3 {'enabled' if enabled else 'disabled'}")
        
    def on_remember_last_change(self, enabled: bool) -> None:
        """Maneja cambios en la opción de recordar última resolución"""
        self.config_manager.set("remember_last_resolution", enabled)
        
        # Si se habilita remember last, deshabilitar auto 4:3
        if enabled:
            self.config_manager.set("auto_4_3", False)
            self.view.set_auto_4_3(False)
            self.view.log_info("Auto 4:3 disabled (remember last resolution enabled)")
            
            # Guardar la resolución actual como última
            current_resolution = self.view.get_current_resolution()
            if current_resolution:
                self.config_manager.set("last_resolution", current_resolution)
                self.view.log_info(f"Saved current resolution as last: {current_resolution}")
        
        self.view.log_info(f"Remember last resolution {'enabled' if enabled else 'disabled'}")
        
    def on_custom_resolution_request(self) -> None:
        """Maneja la solicitud de resolución personalizada"""
        # La vista debería mostrar un diálogo y emitir una señal con los valores
        pass
        
    def add_custom_resolution(self, width: int, height: int) -> None:
        """Añade una resolución personalizada"""
        if width <= 0 or height <= 0:
            self.view.show_error("Width and height must be positive numbers")
            return
            
        if width > 7680 or height > 4320:  # 8K límite
            self.view.show_error("Resolution too large (max: 7680x4320)")
            return
            
        if self.resolution_model.add_resolution(width, height):
            resolution_str = f"{width}x{height}"
            self.view.log_info(f"Added custom resolution: {resolution_str}")
            
            # Actualizar la lista de resoluciones en la vista
            resolutions = self.resolution_model.get_all_resolutions()
            self.view.update_resolution_list(list(resolutions.keys()))
            
            # Seleccionar la nueva resolución
            self.view.set_current_resolution(resolution_str)
            self.view.show_info(f"Custom resolution {resolution_str} added successfully!")
        else:
            self.view.show_error("Resolution already exists or failed to add")