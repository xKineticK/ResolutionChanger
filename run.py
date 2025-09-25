#!/usr/bin/env python
"""
ResolutionChanger - Punto de entrada principal
"""
from PyQt6.QtWidgets import QApplication
import sys

from src.models.game_model import GameModel
from src.models.resolution_model import ResolutionModel
from src.views.main_window import MainWindow
from src.presenters.main_presenter import MainPresenter
from src.utils.logger import log_info

def main():
    """Punto de entrada principal de la aplicación"""
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    
    try:
        # Inicializar modelos
        game_model = GameModel()
        resolution_model = ResolutionModel()
        
        # Crear la vista principal
        main_window = MainWindow()
        
        # Crear y conectar el presenter
        presenter = MainPresenter(main_window, game_model, resolution_model)
        
        # Asignar referencia del presenter a la vista para resoluciones personalizadas
        main_window.presenter = presenter
        
        # Mostrar la ventana
        main_window.show()
        log_info("Application started successfully")
        
        # Ejecutar el loop principal
        return app.exec()
        
    except Exception as e:
        from src.utils.logger import log_error
        log_error(f"Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())