from dataclasses import dataclass
from typing import Dict, Tuple
import json
import os

@dataclass
class Resolution:
    width: int
    height: int
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
    
    def to_tuple(self) -> Tuple[int, int]:
        return (self.width, self.height)

class ResolutionManager:
    def __init__(self):
        self.config_file = "config/resolutions.json"
        self.resolutions: Dict[str, Resolution] = {}
        self._cached_dict = {}  # Para mantener una versión en caché del diccionario
        self.load_resolutions()
        
    def calculate_4_3_resolution(self, original_width: int, original_height: int) -> Tuple[int, int]:
        """Calcula la resolución 4:3 más adecuada"""
        # Lista de resoluciones 4:3 comunes (ordenadas de mayor a menor)
        common_4_3_resolutions = [
            (1600, 1200),  # UXGA
            (1400, 1050),  # SXGA+
            (1280, 960),   # SXGA-
            (1024, 768),   # XGA
            (800, 600),    # SVGA
            (640, 480)     # VGA
        ]
        
        # Encontrar la resolución 4:3 más alta que sea menor o igual al ancho actual
        for width, height in common_4_3_resolutions:
            if width <= original_width:
                return (width, height)
        
        # Si ninguna es adecuada, usar la más pequeña
        return common_4_3_resolutions[-1]
    
    def load_resolutions(self):
        default_resolutions = {
            "3840x2160": (3840, 2160),
            "2560x1440": (2560, 1440),
            "1920x1080": (1920, 1080),
            "1920x1060": (1920, 1060),
            "1600x1200": (1600, 1200),
            "1280x1024": (1280, 1024),
            "1280x960": (1280, 960)
        }
        
        os.makedirs("config", exist_ok=True)
        
        try:
            with open(self.config_file, 'r') as f:
                saved_resolutions = json.load(f)
        except FileNotFoundError:
            saved_resolutions = default_resolutions
            with open(self.config_file, 'w') as f:
                json.dump(saved_resolutions, f, indent=4)
        
        for res_str, (width, height) in saved_resolutions.items():
            self.resolutions[res_str] = Resolution(width, height)
            
        # Actualizar el caché
        self._cached_dict = {k: v.to_tuple() for k, v in self.resolutions.items()}
    
    def add_custom_resolution(self, width: int, height: int) -> bool:
        """Añade una resolución personalizada"""
        res_str = f"{width}x{height}"
        
        # Verificar si la resolución ya existe (por string o por dimensiones)
        if res_str in self._cached_dict:
            return False
            
        # Verificar si existe una resolución con las mismas dimensiones
        for _, (w, h) in self._cached_dict.items():
            if w == width and h == height:
                return False
        
        # Si no existe, añadirla
        self.resolutions[res_str] = Resolution(width, height)
        self._cached_dict[res_str] = (width, height)
        
        # Guardar en archivo
        try:
            with open(self.config_file, 'w') as f:
                resolutions_dict = {
                    k: (v.width, v.height) 
                    for k, v in self.resolutions.items()
                }
                json.dump(resolutions_dict, f, indent=4)
            return True
        except Exception as e:
            # Si hay error al guardar, revertir los cambios
            del self.resolutions[res_str]
            del self._cached_dict[res_str]
            return False
    
    def get_resolution(self, resolution_str: str) -> Tuple[int, int]:
        if resolution_str in self.resolutions:
            return self.resolutions[resolution_str].to_tuple()
        return None
    
    def get_all_resolutions(self) -> Dict[str, Tuple[int, int]]:
        """Devuelve todas las resoluciones disponibles"""
        return self._cached_dict.copy()  # Devolver una copia para evitar modificaciones externas