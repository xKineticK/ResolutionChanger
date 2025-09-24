import json
import os
from typing import Any, Dict

class ConfigManager:
    """Gestor de configuración de la aplicación"""
    def __init__(self):
        self.config_file = "config/settings.json"
        self.default_config = {
            "auto_4_3": False,  # Activar 4:3 automáticamente
            "steam_path": "C:/Program Files (x86)/Steam/steam.exe"
        }
        self.current_config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo"""
        os.makedirs("config", exist_ok=True)
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Asegurarse de que todas las opciones por defecto existan
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está corrupto, usar configuración por defecto
            self.save_config(self.default_config)
            return self.default_config.copy()

    def save_config(self, config: Dict[str, Any]) -> None:
        """Guarda la configuración en el archivo"""
        self.current_config = config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def get(self, key: str) -> Any:
        """Obtiene un valor de configuración"""
        return self.current_config.get(key, self.default_config.get(key))

    def set(self, key: str, value: Any) -> None:
        """Establece un valor de configuración"""
        self.current_config[key] = value
        self.save_config(self.current_config)