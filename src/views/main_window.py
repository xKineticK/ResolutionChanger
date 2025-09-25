from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QComboBox,
    QListWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import os

from .widgets.title_bar import TitleBar
from .widgets.console_widget import ConsoleWidget
from ..utils.logger import attach_console_widget, log_info, log_warning, log_error

class MainWindow(QDialog):
    # Señales
    resolution_changed = pyqtSignal(str)
    game_selected = pyqtSignal(str)
    play_clicked = pyqtSignal()
    aspect_ratio_clicked = pyqtSignal()  # Nueva señal para el botón 4:3
    auto_4_3_changed = pyqtSignal(bool)  # Señal para la casilla de 4:3 automático
    custom_resolution_requested = pyqtSignal()  # Señal para resolución personalizada
    remember_last_changed = pyqtSignal(bool)  # Señal para recordar última resolución
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Resolution Changer")
        self.resize(1200, 700)
        self.default_steam_path = "C:/Program Files (x86)/Steam/steam.exe"
        
        # Cargar estilos
        self._load_styles()
        
        # Inicializar UI
        self.init_ui()
        
    def _load_styles(self):
        """Carga los estilos CSS desde el archivo"""
        style_path = os.path.join(os.path.dirname(__file__), "styles/dark_theme.qss")
        with open(style_path, "r") as f:
            self.setStyleSheet(f.read())
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra de título
        self.title_bar = TitleBar(self)
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximize)
        self.title_bar.close_clicked.connect(self.close)
        
        # Contenido principal
        content = QFrame()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Panel izquierdo (lista de juegos)
        left_panel = self._create_left_panel()
        
        # Panel derecho (configuración)
        right_panel = self._create_right_panel()
        
        # Agregar paneles al layout principal
        content_layout.addWidget(left_panel, 1)  # ratio 1
        content_layout.addWidget(right_panel, 2)  # ratio 2
        
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content)
        
    def _create_left_panel(self):
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Label
        games_label = QLabel("STEAM GAMES")
        games_label.setProperty("type", "section")
        
        # Lista de juegos
        self.game_list = QListWidget()
        self.game_list.setMinimumWidth(300)
        self.game_list.currentItemChanged.connect(self._on_game_selected)
        
        layout.addWidget(games_label)
        layout.addWidget(self.game_list, 1)
        
        return panel
        
    def _create_right_panel(self):
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Steam Path
        path_label = QLabel("STEAM PATH")
        path_label.setProperty("type", "section")
        
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        
        self.path_edit = QLineEdit(self.default_steam_path)
        self.path_edit.setPlaceholderText("Select Steam.exe path")
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFixedWidth(100)
        self.browse_button.clicked.connect(self._browse_steam_path)
        
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_button)
        
        # Resolution
        res_label = QLabel("RESOLUTION")
        res_label.setProperty("type", "section")
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.currentTextChanged.connect(self._on_resolution_changed)
        
        resolution_buttons = QHBoxLayout()
        resolution_buttons.setSpacing(10)
        
        self.custom_res_button = QPushButton("Custom")
        self.custom_res_button.setFixedWidth(100)
        self.custom_res_button.clicked.connect(self._add_custom_resolution)
        
        self.aspect_ratio_button = QPushButton("4:3")
        self.aspect_ratio_button.setFixedWidth(80)
        self.aspect_ratio_button.clicked.connect(self._calculate_4_3_resolution)
        
        resolution_buttons.addWidget(self.custom_res_button)
        resolution_buttons.addWidget(self.aspect_ratio_button)
        resolution_buttons.addStretch()
        
        # Checkbox para 4:3 automático
        auto_4_3_layout = QHBoxLayout()
        from PyQt6.QtWidgets import QCheckBox
        self.auto_4_3_check = QCheckBox("Auto 4:3 on startup")
        self.auto_4_3_check.stateChanged.connect(self._on_auto_4_3_changed)
        auto_4_3_layout.addWidget(self.auto_4_3_check)
        auto_4_3_layout.addStretch()
        
        # Checkbox para recordar última resolución
        remember_last_layout = QHBoxLayout()
        self.remember_last_check = QCheckBox("Remember last resolution")
        self.remember_last_check.stateChanged.connect(self._on_remember_last_changed)
        remember_last_layout.addWidget(self.remember_last_check)
        remember_last_layout.addStretch()
        
        # System Info
        info_label = QLabel("SYSTEM INFO")
        info_label.setProperty("type", "section")
        
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        
        # Console
        self.console = ConsoleWidget()
        attach_console_widget(self.console.get_widget())
        
        # Play button
        self.play_button = QPushButton("▶  PLAY")
        self.play_button.setObjectName("playButton")
        self.play_button.clicked.connect(self._on_play_clicked)
        
        # Agregar widgets al layout
        layout.addWidget(path_label)
        layout.addLayout(path_layout)
        layout.addWidget(res_label)
        layout.addWidget(self.resolution_combo)
        layout.addLayout(resolution_buttons)
        layout.addLayout(auto_4_3_layout)
        layout.addLayout(remember_last_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.info_label)
        layout.addWidget(self.console)
        layout.addWidget(self.play_button)
        
        return panel
        
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
            
    def _browse_steam_path(self):
        file_filter = 'Executable File (*.exe)'
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select Steam.exe', 
            'C:/Program Files (x86)/Steam', 
            file_filter
        )
        if file_path:
            self.path_edit.setText(file_path)
            log_info(f"Steam path updated: {file_path}")
            
    def _on_resolution_changed(self, resolution: str):
        self.resolution_changed.emit(resolution)
        
    def _on_game_selected(self, current, previous):
        if current:
            self.game_selected.emit(current.text())
            
    def _on_play_clicked(self):
        self.play_clicked.emit()
        
    def _calculate_4_3_resolution(self):
        """Solicita el cálculo de resolución 4:3"""
        log_info("Calculating 4:3 resolution...")
        self.aspect_ratio_clicked.emit()  # Emitir señal al presenter
        
    def _add_custom_resolution(self):
        """Abre el diálogo para añadir resolución personalizada"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Custom Resolution")
        dialog.setModal(True)
        dialog.resize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        # Campo de ancho
        width_label = QLabel("Width:")
        width_input = QLineEdit()
        width_input.setPlaceholderText("e.g., 1920")
        
        # Campo de altura
        height_label = QLabel("Height:")
        height_input = QLineEdit()
        height_input.setPlaceholderText("e.g., 1080")
        
        # Botones
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        # Agregar widgets al layout
        layout.addWidget(width_label)
        layout.addWidget(width_input)
        layout.addWidget(height_label)
        layout.addWidget(height_input)
        layout.addLayout(button_layout)
        
        # Conectar botones
        cancel_button.clicked.connect(dialog.reject)
        
        def on_ok():
            try:
                width = int(width_input.text().strip())
                height = int(height_input.text().strip())
                
                if width <= 0 or height <= 0:
                    QMessageBox.warning(dialog, "Invalid Input", "Width and height must be positive numbers")
                    return
                    
                # Notificar al presenter
                if hasattr(self, 'presenter'):
                    self.presenter.add_custom_resolution(width, height)
                
                dialog.accept()
                
            except ValueError:
                QMessageBox.warning(dialog, "Invalid Input", "Please enter valid numbers for width and height")
        
        ok_button.clicked.connect(on_ok)
        
        # Mostrar el diálogo
        dialog.exec()
        
    def _on_auto_4_3_changed(self, state: int):
        """Maneja cambios en la casilla de verificación de 4:3 automático"""
        is_checked = state == Qt.CheckState.Checked.value
        
        # Si se activa auto 4:3, desactivar remember last
        if is_checked:
            self.remember_last_check.blockSignals(True)
            self.remember_last_check.setChecked(False)
            self.remember_last_check.blockSignals(False)
            
        self.auto_4_3_changed.emit(is_checked)
        
    def _on_remember_last_changed(self, state: int):
        """Maneja cambios en la casilla de verificación de recordar última resolución"""
        is_checked = state == Qt.CheckState.Checked.value
        
        # Si se activa remember last, desactivar auto 4:3
        if is_checked:
            self.auto_4_3_check.blockSignals(True)
            self.auto_4_3_check.setChecked(False)
            self.auto_4_3_check.blockSignals(False)
            
        self.remember_last_changed.emit(is_checked)
        
    def set_auto_4_3(self, enabled: bool):
        """Establece el estado de la casilla de verificación de 4:3 automático"""
        self.auto_4_3_check.blockSignals(True)
        self.auto_4_3_check.setChecked(enabled)
        self.auto_4_3_check.blockSignals(False)
        
    def set_remember_last(self, enabled: bool):
        """Establece el estado de la casilla de verificación de recordar última"""
        self.remember_last_check.blockSignals(True)
        self.remember_last_check.setChecked(enabled)
        self.remember_last_check.blockSignals(False)
        
    # Métodos públicos para el presenter
    def update_game_list(self, games: list):
        """Actualiza la lista de juegos"""
        self.game_list.clear()
        self.game_list.addItems(games)
        
    def update_resolution_list(self, resolutions: list):
        """Actualiza la lista de resoluciones"""
        current = self.resolution_combo.currentText()
        self.resolution_combo.clear()
        self.resolution_combo.addItems(resolutions)
        if current in resolutions:
            self.resolution_combo.setCurrentText(current)
            
    def update_system_info(self, info: dict):
        """Actualiza la información del sistema"""
        self.info_label.setText("\n".join([f"{k}: {v}" for k, v in info.items()]))
        
    def get_steam_path(self) -> str:
        """Retorna la ruta de Steam"""
        return self.path_edit.text()
        
    def get_current_resolution(self) -> str:
        """Retorna la resolución seleccionada"""
        return self.resolution_combo.currentText()
        
    def set_current_resolution(self, resolution: str):
        """Establece la resolución actual"""
        self.resolution_combo.setCurrentText(resolution)
        
    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        QMessageBox.critical(self, "Error", message)
        log_error(message)
        
    def show_info(self, message: str):
        """Muestra un mensaje informativo"""
        QMessageBox.information(self, "Information", message)
        
    def log_info(self, message: str):
        """Registra un mensaje informativo"""
        log_info(message)
        
    def log_warning(self, message: str):
        """Registra un mensaje de advertencia"""
        log_warning(message)
        
    def log_error(self, message: str):
        """Registra un mensaje de error"""
        log_error(message)