from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTextEdit

class ConsoleWidget(QFrame):
    """Widget para mostrar logs de la aplicación"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        label = QLabel("APPLICATION LOGS")
        label.setProperty("type", "section")
        
        # Frame para los logs
        log_frame = QFrame()
        log_frame.setObjectName("consoleFrame")
        log_frame.setStyleSheet("""
            #consoleFrame {
                background-color: #151f2d;
                border: 1px solid #244861;
                border-radius: 3px;
            }
        """)
        
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(1, 1, 1, 1)
        
        # Área de texto para logs
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(150)
        log_layout.addWidget(self.console)
        
        # Agregar widgets al layout principal
        layout.addWidget(label)
        layout.addWidget(log_frame)
        
    def append_log(self, message: str):
        """Añade un mensaje al área de logs"""
        self.console.append(message)
        # Auto-scroll
        self.console.verticalScrollBar().setValue(
            self.console.verticalScrollBar().maximum()
        )
        
    def get_widget(self) -> QTextEdit:
        """Retorna el widget de texto para configurar el logger"""
        return self.console