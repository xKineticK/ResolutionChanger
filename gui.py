# gui.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QComboBox,
    QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QFileDialog, QTextEdit, QInputDialog,
    QMessageBox
)
from PyQt6.QtGui import QFont, QMouseEvent, QIcon
from PyQt6.QtCore import Qt, QPoint, QSize
from logic import resolutions, info, open_game_in_steam, resolution_manager
from games.steam import load_games
from loggingLib import attach_console_widget, printInfo, printWarning, printError

class ModernResolutionChanger(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Resolution Changer")
        self.resize(1200, 700)
        self.old_pos = None

        self.steam_path = "C:/Program Files (x86)/Steam/steam.exe"
        self.game_var = None
        self.resolution_var = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Barra superior
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(32)
        self.title_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a475e, stop:1 #1b2838);
            }
        """)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 5, 0)
        title_layout.setSpacing(0)

        self.title_label = QLabel("Resolution Changer")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #c7d5e0;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        self.title_label.setFixedHeight(32)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        def build_icon_button(text, tooltip):
            btn = QPushButton(text)
            btn.setFixedSize(45, 32)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 10px;
                    color: #c7d5e0;
                }
                QPushButton:hover {
                    background-color: #3d6c8d;
                }
                QPushButton:pressed {
                    background-color: #2a475e;
                }
            """)
            return btn

        self.minimize_button = build_icon_button("─", "Minimize")
        self.maximize_button = build_icon_button("□", "Maximize")
        self.exit_button = build_icon_button("×", "Close")
        
        # Estilo especial para el botón de cerrar
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #c7d5e0;
            }
            QPushButton:hover {
                background-color: #c75050;
            }
            QPushButton:pressed {
                background-color: #b33030;
            }
        """)

        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.exit_button.clicked.connect(self.close)

        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.maximize_button)
        title_layout.addWidget(self.exit_button)

        main_layout.addWidget(self.title_bar)

        # Cuerpo principal con layout horizontal
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background-color: #1b2838;
            }
        """)
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Panel izquierdo (lista de juegos)
        left_panel = QFrame()
        left_panel.setStyleSheet("background: transparent;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Panel derecho (configuración)
        right_panel = QFrame()
        right_panel.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # Ruta Steam
        path_label = QLabel("STEAM PATH")
        path_label.setStyleSheet("""
            QLabel {
                color: #66c0f4;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        
        self.path_edit = QLineEdit(self.steam_path)
        self.path_edit.setPlaceholderText("Select Steam.exe path")
        self.path_edit.setStyleSheet("""
            QLineEdit {
                background-color: #151f2d;
                border: 1px solid #244861;
                border-radius: 3px;
                color: #c7d5e0;
                padding: 5px;
                selection-background-color: #244861;
            }
            QLineEdit:focus {
                border: 1px solid #66c0f4;
            }
        """)
        
        self.path_button = QPushButton("Browse")
        self.path_button.setFixedWidth(100)
        self.path_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c237c, stop:1 #2b5788);
                border: none;
                border-radius: 2px;
                color: #c7d5e0;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5c2b96, stop:1 #356baa);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3d1b66, stop:1 #1f3f64);
            }
        """)
        self.path_button.clicked.connect(self.open_file_dialog)
        
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.path_button)

        # Panel izquierdo: Lista de juegos
        game_label = QLabel("STEAM GAMES")
        game_label.setStyleSheet("""
            QLabel {
                color: #66c0f4;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        games = load_games()
        self.games = games
        self.game_list = QListWidget()
        self.game_list.addItems([game.name for game in games])
        self.game_list.setMinimumWidth(300)
        self.game_list.currentItemChanged.connect(self.selected_game)
        self.game_list.setStyleSheet("""
            QListWidget {
                background-color: #151f2d;
                border: 1px solid #244861;
                border-radius: 3px;
                color: #c7d5e0;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background-color: #244861;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #193c5a;
            }
            QScrollBar:vertical {
                border: none;
                background: #151f2d;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #244861;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
                background: none;
            }
        """)
        
        left_layout.addWidget(game_label)
        left_layout.addWidget(self.game_list, 1)  # 1 para que se expanda verticalmente
        
        # Panel derecho: Configuración
        # Resolución
        res_label = QLabel("RESOLUTION")
        res_label.setStyleSheet("""
            QLabel {
                color: #66c0f4;
                font-size: 12px;
                font-weight: bold;
                margin-top: 10px;
            }
        """)
        self.res_combo = QComboBox()
        self.res_combo.addItems(list(resolutions.keys()))
        self.res_combo.currentTextChanged.connect(self.get_resolution)
        
        # Botones de resolución con estilo moderno
        resolution_buttons = QHBoxLayout()
        resolution_buttons.setSpacing(10)
        
        button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c237c, stop:1 #2b5788);
                border: none;
                border-radius: 2px;
                color: #c7d5e0;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5c2b96, stop:1 #356baa);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3d1b66, stop:1 #1f3f64);
            }
        """
        
        self.custom_res_button = QPushButton("Custom")
        self.custom_res_button.clicked.connect(self.add_custom_resolution)
        self.custom_res_button.setFixedWidth(100)
        self.custom_res_button.setStyleSheet(button_style)
        
        self.aspect_4_3_button = QPushButton("4:3")
        self.aspect_4_3_button.setToolTip("Calculate and use 4:3 resolution")
        self.aspect_4_3_button.clicked.connect(self.use_4_3_resolution)
        self.aspect_4_3_button.setFixedWidth(80)
        self.aspect_4_3_button.setStyleSheet(button_style)
        
        resolution_buttons.addWidget(self.custom_res_button)
        resolution_buttons.addWidget(self.aspect_4_3_button)
        resolution_buttons.addStretch()
        
        # Actualizar el estilo del ComboBox
        self.res_combo.setStyleSheet("""
            QComboBox {
                background-color: #151f2d;
                border: 1px solid #244861;
                border-radius: 2px;
                color: #c7d5e0;
                padding: 5px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #c7d5e0;
                margin-right: 5px;
            }
            QComboBox:on {
                border: 1px solid #66c0f4;
            }
            QComboBox QAbstractItemView {
                background-color: #151f2d;
                border: 1px solid #244861;
                color: #c7d5e0;
                selection-background-color: #244861;
            }
        """)
        
        # Agregar widgets al panel derecho con espaciado adecuado
        right_layout.addWidget(path_label)
        right_layout.addLayout(path_layout)
        right_layout.addSpacing(15)
        right_layout.addWidget(res_label)
        right_layout.addWidget(self.res_combo)
        right_layout.addLayout(resolution_buttons)
        
        # Info
        info_label = QLabel("SYSTEM INFO")
        info_label.setStyleSheet("""
            QLabel {
                color: #66c0f4;
                font-size: 12px;
                font-weight: bold;
                margin-top: 15px;
            }
        """)
        self.info_label = QLabel("\n".join([f"{k}: {v}" for k, v in info.items()]))
        self.info_label.setStyleSheet("color: #8f98a0; font-size: 12px;")
        self.info_label.setWordWrap(True)
        
        right_layout.addWidget(info_label)
        right_layout.addWidget(self.info_label)
        
        # Sección de Logs
        log_label = QLabel("APPLICATION LOGS")
        log_label.setStyleSheet("""
            QLabel {
                color: #66c0f4;
                font-size: 12px;
                font-weight: bold;
                margin-top: 15px;
            }
        """)
        
        # Frame para los logs con estilo moderno
        log_frame = QFrame()
        log_frame.setStyleSheet("""
            QFrame {
                background-color: #151f2d;
                border: 1px solid #244861;
                border-radius: 3px;
            }
        """)
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(1, 1, 1, 1)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(150)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #8f98a0;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 8px;
            }
            QScrollBar:vertical {
                background: #151f2d;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #244861;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
                background: none;
            }
        """)
        attach_console_widget(self.console)
        # Initial log messages
        printInfo("Application started successfully")
        printInfo("Logging system activated")
        
        log_layout.addWidget(self.console)
        
        right_layout.addWidget(log_label)
        right_layout.addWidget(log_frame)
        right_layout.addSpacing(15)
        
        # Botón Play
        self.play_button = QPushButton("▶  PLAY")
        self.play_button.setFixedHeight(50)
        self.play_button.clicked.connect(self.play_game)
        self.play_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c237c, stop:1 #2b5788);
                border: none;
                border-radius: 3px;
                color: #ffffff;
                padding: 5px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5c2b96, stop:1 #356baa);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3d1b66, stop:1 #1f3f64);
            }
        """)
        right_layout.addWidget(self.play_button)
        
        # Agregar los paneles al layout principal
        # Agregar paneles al layout principal
        content_layout.addWidget(left_panel, 1)  # ratio 1
        content_layout.addWidget(right_panel, 2)  # ratio 2

        main_layout.addWidget(content)

        # Estilos globales
        self.setStyleSheet("""
            * {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QWidget {
                background-color: #1b2838;
                color: #c7d5e0;
            }
            QLineEdit, QComboBox, QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1f3b53, stop:1 #1b2838);
                border: 1px solid #244861;
                border-radius: 3px;
                padding: 6px;
                color: #c7d5e0;
            }
            QLineEdit:hover, QComboBox:hover, QListWidget:hover {
                border: 1px solid #66c0f4;
            }
            QLineEdit:focus, QComboBox:focus, QListWidget:focus {
                border: 1px solid #66c0f4;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #244861, stop:1 #1f3b53);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QListWidget {
                background: #1b2838;
                border: 1px solid #244861;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background: #244861;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4d5bc9, stop:1 #7c5ac0);
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4d5bc9, stop:1 #7c5ac0);
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5668e2, stop:1 #8d68d8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4353b5, stop:1 #6b4ea8);
            }
            QTextEdit {
                background-color: #0e141b;
                border: 1px solid #244861;
                border-radius: 3px;
                padding: 6px;
                color: #8f98a0;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                color: #c7d5e0;
            }
        """)

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setIcon(QIcon("images/maximize.png"))
        else:
            self.showMaximized()
            self.maximize_button.setIcon(QIcon("images/restore.png"))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.rect().contains(event.pos()):
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.old_pos = None

    def open_file_dialog(self):
        file_filter = 'Executable File (*.exe)'
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Steam.exe', 'C:/Program Files (x86)/Steam', file_filter)
        if file_path:
            self.path_edit.setText(file_path)
            self.steam_path = file_path
            printInfo(f"Steam path updated: {file_path}")

    def get_resolution(self):
        old_resolution = self.resolution_var
        self.resolution_var = self.res_combo.currentText()
        if self.resolution_var != old_resolution:
            printInfo(f"Selected resolution: {self.resolution_var}")

    def selected_game(self, current, previous):
        if current:
            self.game_var = current.text()
            printInfo(f"Selected game: {self.game_var}")

    def use_4_3_resolution(self):
        """Use recommended 4:3 resolution"""
        printInfo("Calculating 4:3 resolution...")
        import win32api
        current_width = win32api.GetSystemMetrics(0)
        current_height = win32api.GetSystemMetrics(1)
        
        # Calculate recommended 4:3 resolution
        width, height = resolution_manager.calculate_4_3_resolution(current_width, current_height)
        resolution_str = f"{width}x{height}"
        
        # Si la resolución ya existe en el combo box, simplemente seleccionarla
        if self.res_combo.findText(resolution_str) != -1:
            self.res_combo.setCurrentText(resolution_str)
            self.resolution_var = resolution_str
            printInfo(f"Selected 4:3 resolution: {resolution_str}")
            return
            
        # Si no existe, añadirla
        if resolution_manager.add_custom_resolution(width, height):
            self.res_combo.blockSignals(True)
            self.res_combo.addItem(resolution_str)
            self.res_combo.setCurrentText(resolution_str)
            self.res_combo.blockSignals(False)
            
            global resolutions
            resolutions = resolution_manager.get_all_resolutions()
            self.resolution_var = resolution_str
            
            printInfo(f"Added and selected 4:3 resolution: {resolution_str}")
        else:
            printWarning("Could not add 4:3 resolution")

    def play_game(self):
        self.steam_path = self.path_edit.text()
        self.get_resolution()
        
        if not self.steam_path:
            printError("Steam path not selected")
            QMessageBox.warning(self, "Error", "Please select Steam path first.")
            return
            
        if not self.game_var:
            printError("No game selected")
            QMessageBox.warning(self, "Error", "Please select a game first.")
            return
            
        if not self.resolution_var:
            printInfo("No resolution selected, using 4:3")
            self.use_4_3_resolution()
            
        try:
            printInfo(f"Launching {self.game_var} with resolution {self.resolution_var}")
            open_game_in_steam(self.steam_path, self.game_var, self.resolution_var, self.games)
            printInfo("Game launched successfully")
        except Exception as e:
            printError(f"Error launching game: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error launching game: {str(e)}")

    def add_custom_resolution(self):
        printInfo("Starting custom resolution dialog...")
        width, ok = QInputDialog.getInt(
            self, "Custom Resolution", 
            "Width:", 1920, 640, 7680
        )
        if ok:
            height, ok = QInputDialog.getInt(
                self, "Custom Resolution", 
                "Height:", 1080, 480, 4320
            )
            if ok:
                resolution_str = f"{width}x{height}"
                
                # Check if resolution already exists
                if self.res_combo.findText(resolution_str) != -1:
                    printWarning(f"Resolution {resolution_str} already exists")
                    return
                
                printInfo(f"Attempting to add custom resolution: {resolution_str}")
                # Try to add resolution
                result = resolution_manager.add_custom_resolution(width, height)
                
                if result:
                    try:
                        # Bloquear señales temporalmente
                        self.res_combo.blockSignals(True)
                        
                        # Actualizar el combo box
                        self.res_combo.addItem(resolution_str)
                        self.res_combo.setCurrentText(resolution_str)
                        
                        # Actualizar las resoluciones y la variable
                        global resolutions
                        resolutions = resolution_manager.get_all_resolutions()
                        self.resolution_var = resolution_str
                        
                        printInfo(f"Resolución personalizada añadida con éxito: {resolution_str}")
                    finally:
                        # Asegurarse de que las señales se desbloquean
                        self.res_combo.blockSignals(False)
                else:
                    printWarning(f"No se pudo añadir la resolución {resolution_str}")
            else:
                printInfo("Height input cancelled")
        else:
            printInfo("Width input cancelled")
