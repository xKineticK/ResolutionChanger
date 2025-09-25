from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional
import json
import os
import shutil

@dataclass
class Resolution:
    width: int
    height: int
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
    
    def to_tuple(self) -> Tuple[int, int]:
        return (self.width, self.height)

class ResolutionModel:
    def __init__(self):
        # Usar AppData para tener permisos de escritura
        app_data = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "ResolutionChanger")
        os.makedirs(app_data, exist_ok=True)
        self.config_file = os.path.join(app_data, "resolutions.json")
        
        # Si no existe el archivo en AppData, copiarlo desde la instalación
        if not os.path.exists(self.config_file):
            try:
                # Intentar cargar desde la carpeta de instalación como plantilla
                install_config = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "resolutions.json")
                if os.path.exists(install_config):
                    import shutil
                    shutil.copy2(install_config, self.config_file)
            except:
                pass  # Si falla, usará los valores por defecto
        
        self.resolutions: Dict[str, Resolution] = {}
        self._cached_dict = {}
        self.load_resolutions()
    
    def load_resolutions(self) -> None:
        """Carga las resoluciones desde el archivo de configuración"""
        default_resolutions = {
            "3840x2160": (3840, 2160),
            "2560x1440": (2560, 1440),
            "1920x1080": (1920, 1080),
            "1600x1200": (1600, 1200),
            "1280x960": (1280, 960)
        }
        
        try:
            with open(self.config_file, 'r') as f:
                saved_resolutions = json.load(f)
        except FileNotFoundError:
            saved_resolutions = default_resolutions
            with open(self.config_file, 'w') as f:
                json.dump(saved_resolutions, f, indent=4)
        
        for res_str, (width, height) in saved_resolutions.items():
            self.resolutions[res_str] = Resolution(width, height)
        self._cached_dict = {k: v.to_tuple() for k, v in self.resolutions.items()}

    def add_resolution(self, width: int, height: int) -> bool:
        """Añade una nueva resolución"""
        res_str = f"{width}x{height}"
        
        if res_str in self._cached_dict:
            return False
            
        for _, (w, h) in self._cached_dict.items():
            if w == width and h == height:
                return False
        
        self.resolutions[res_str] = Resolution(width, height)
        self._cached_dict[res_str] = (width, height)
        
        try:
            self._save_resolutions()
            return True
        except Exception:
            del self.resolutions[res_str]
            del self._cached_dict[res_str]
            return False

    def get_resolution(self, resolution_str: str) -> Optional[Tuple[int, int]]:
        """Obtiene una resolución específica"""
        if resolution_str in self.resolutions:
            return self.resolutions[resolution_str].to_tuple()
        return None

    def get_all_resolutions(self) -> Dict[str, Tuple[int, int]]:
        """Devuelve todas las resoluciones disponibles"""
        return self._cached_dict.copy()

    def calculate_4_3_resolution(self, current_width: int, current_height: int, available_resolutions=None) -> Tuple[int, int]:
        """Calcula la resolución 4:3 más adecuada basada en la resolución actual.
        
        Si se proporcionan available_resolutions, busca la mejor 4:3 disponible en el sistema.
        Sino, usa el método original de cálculo.
        """
        
        # Si tenemos las resoluciones disponibles, usarlas para encontrar la mejor 4:3
        if available_resolutions:
            # Filtrar solo las resoluciones 4:3 disponibles
            four_three_resolutions = []
            for width, height in available_resolutions:
                ratio = round(width / height, 2)
                if abs(ratio - 4/3) < 0.05:  # Tolerancia para 4:3 (1.33)
                    four_three_resolutions.append((width, height))
            
            if four_three_resolutions:
                # Ordenar por área (mayor a menor) y tomar la más grande que quepa
                four_three_resolutions.sort(key=lambda x: x[0] * x[1], reverse=True)
                for width, height in four_three_resolutions:
                    if width <= current_width and height <= current_height:
                        return (width, height)
                
                # Si ninguna cabe, tomar la más pequeña disponible
                return four_three_resolutions[-1]
        
        # Método original como fallback
        # Calcular posibles resoluciones 4:3
        width_based = (current_width, int(current_width * 3/4))  # mantiene el ancho
        height_based = (int(current_height * 4/3), current_height)  # mantiene el alto
        
        # Lista de resoluciones 4:3 comunes para referencia
        common_4_3_resolutions = [
            (1600, 1200),
            (1400, 1050),
            (1280, 960),
            (1024, 768),
            (800, 600),
            (640, 480)
        ]
        
        # Función para encontrar la resolución común más cercana
        def find_closest_common(target_width: int, target_height: int) -> Tuple[int, int]:
            closest = common_4_3_resolutions[0]
            min_diff = float('inf')
            
            for res in common_4_3_resolutions:
                # Calcula la diferencia de área con la resolución objetivo
                diff = abs(res[0] * res[1] - target_width * target_height)
                if diff < min_diff and res[0] <= current_width and res[1] <= current_height:
                    min_diff = diff
                    closest = res
            
            return closest
        
        # Si width_based cabe en la pantalla, usar esa
        if width_based[1] <= current_height:
            return find_closest_common(width_based[0], width_based[1])
        
        # Si height_based cabe en la pantalla, usar esa
        if height_based[0] <= current_width:
            return find_closest_common(height_based[0], height_based[1])
        
        # Si ninguna cabe, usar la resolución común más alta que quepa
        return find_closest_common(current_width, current_height)

    def _save_resolutions(self) -> None:
        """Guarda las resoluciones en el archivo de configuración"""
        with open(self.config_file, 'w') as f:
            resolutions_dict = {
                k: (v.width, v.height) 
                for k, v in self.resolutions.items()
            }
            json.dump(resolutions_dict, f, indent=4)