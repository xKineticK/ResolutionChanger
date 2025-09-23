# gui.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QComboBox,
    QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QFileDialog, QTextEdit, QInputDialog
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
        self.resize(900, 600)
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
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("background-color: #2a2f3b;")

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(10)

        self.title_label = QLabel("  Resolution Changer")
        self.title_label.setStyleSheet("color: #a0a0a0; font-size: 13px;")
        self.title_label.setFixedHeight(36)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        def build_icon_button(icon_path, tooltip):
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(16, 16))
            btn.setFixedSize(32, 24)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #3e4455;
                    border-radius: 6px;
                }
                QPushButton:pressed {
                    background-color: #4a5060;
                }
            """)
            return btn

        self.minimize_button = build_icon_button("images/minimize.png", "Minimize")
        self.maximize_button = build_icon_button("images/maximize.png", "Maximize")
        self.exit_button = build_icon_button("images/close.png", "Close")

        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.exit_button.clicked.connect(self.close)

        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.maximize_button)
        title_layout.addWidget(self.exit_button)

        main_layout.addWidget(self.title_bar)

        # Cuerpo principal
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #222630; border-radius: 10px; }")
        frame_layout = QGridLayout(frame)

        # Ruta Steam
        path_label = QLabel("Steam Path:")
        path_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.path_edit = QLineEdit(self.steam_path)
        self.path_edit.setPlaceholderText("Select Steam.exe path")
        self.path_button = QPushButton("Browse")
        self.path_button.clicked.connect(self.open_file_dialog)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.path_button)

        frame_layout.addWidget(path_label, 0, 0)
        frame_layout.addLayout(path_layout, 0, 1)

        # Resolución
        res_label = QLabel("Select Resolution:")
        res_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.res_combo = QComboBox()
        self.res_combo.addItems(list(resolutions.keys()))
        self.res_combo.activated.connect(self.get_resolution)

        frame_layout.addWidget(res_label, 1, 0)
        frame_layout.addWidget(self.res_combo, 1, 1)

        # Juegos
        game_label = QLabel("Select Game:")
        game_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        games = load_games()
        self.games = games  # Guardamos los objetos para acceder luego
        self.game_list = QListWidget()
        self.game_list.addItems([game.name for game in games])  # Lista de nombres
        self.game_list.setMaximumHeight(130)
        self.game_list.itemClicked.connect(self.selected_game)

        frame_layout.addWidget(game_label, 2, 0)
        frame_layout.addWidget(self.game_list, 2, 1)

        # Info
        self.info_label = QLabel("\n".join([f"{k}: {v}" for k, v in info.items()]))
        self.info_label.setFont(QFont("Consolas", 10))
        self.info_label.setWordWrap(True)
        self.info_label.setMaximumHeight(80)
        frame_layout.addWidget(self.info_label, 3, 0, 1, 2)

        # Log Console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(120)
        attach_console_widget(self.console)
        frame_layout.addWidget(self.console, 4, 0, 1, 2)

        # Botón Play
        self.play_button = QPushButton("▶  Play")
        self.play_button.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.play_button.clicked.connect(self.play_game)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.play_button)
        button_layout.addStretch()
        frame_layout.addLayout(button_layout, 5, 0, 1, 2)

        # Añadir botón para resolución personalizada
        self.custom_res_button = QPushButton("Add Custom Resolution")
        self.custom_res_button.clicked.connect(self.add_custom_resolution)
        
        # Añadirlo al layout cerca del combo de resoluciones
        res_layout = QHBoxLayout()
        res_layout.addWidget(self.res_combo)
        res_layout.addWidget(self.custom_res_button)
        frame_layout.addLayout(res_layout, 1, 1)

        main_layout.addWidget(frame)

        # Estilos globales
        self.setStyleSheet("""
            * {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QWidget {
                background-color: #1b1f2a;
                color: #f0f0f0;
            }
            QLineEdit, QComboBox, QListWidget, QTextEdit {
                background-color: #2b2f3b;
                border: 1px solid #3c3f4e;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #3a3f5c;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4b5273;
            }
            QPushButton:pressed {
                background-color: #5c6384;
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

    def get_resolution(self):
        self.resolution_var = self.res_combo.currentText()

    def selected_game(self, item):
        self.game_var = item.text()

    def play_game(self):
        self.steam_path = self.path_edit.text()
        self.get_resolution()
        if self.steam_path and self.game_var and self.resolution_var:
            open_game_in_steam(self.steam_path, self.game_var, self.resolution_var, self.games)

    def add_custom_resolution(self):
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
                
                # Verificar si ya existe en el combo box
                if self.res_combo.findText(resolution_str) != -1:
                    printWarning("Resolution already exists")
                    return
                
                # Intentar añadir la resolución
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
                        
                        printInfo(f"Added custom resolution: {resolution_str}")
                    finally:
                        # Asegurarse de que las señales se desbloquean
                        self.res_combo.blockSignals(False)
                else:
                    printWarning("Resolution already exists")
