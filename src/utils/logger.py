import logging
from PyQt6.QtWidgets import QTextEdit
from typing import Optional

class QTextEditHandler(logging.Handler):
    """Handler personalizado para enviar logs a un QTextEdit"""
    def __init__(self):
        super().__init__()
        self._widget: Optional[QTextEdit] = None

    def emit(self, record):
        if self._widget:
            msg = self.format(record)
            self._widget.append(msg)
            # Auto-scroll
            self._widget.verticalScrollBar().setValue(
                self._widget.verticalScrollBar().maximum()
            )

    def set_widget(self, widget: QTextEdit):
        """Establece el widget que mostrará los logs"""
        self._widget = widget

class Logger:
    """Clase singleton para manejar el logging en toda la aplicación"""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            # Configurar el logger principal
            self.logger = logging.getLogger("ResolutionChanger")
            self.logger.setLevel(logging.DEBUG)

            # Formatter con timestamp, nivel y mensaje
            self.formatter = logging.Formatter(
                "%(asctime)s.%(msecs)03d | ## %(levelname)-5s | %(message)s",
                "%H:%M:%S"
            )

            # Handler para consola del sistema
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.stream_handler)

            # Handler para QTextEdit
            self.qt_handler = QTextEditHandler()
            self.qt_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.qt_handler)

            Logger._initialized = True

    def attach_widget(self, widget: QTextEdit):
        """Conecta un QTextEdit para mostrar los logs"""
        self.qt_handler.set_widget(widget)

    def info(self, msg: str):
        """Registra un mensaje informativo"""
        self.logger.info(msg)

    def warning(self, msg: str):
        """Registra un mensaje de advertencia"""
        self.logger.warning(msg)

    def error(self, msg: str):
        """Registra un mensaje de error"""
        self.logger.error(msg)

    def debug(self, msg: str):
        """Registra un mensaje de depuración"""
        self.logger.debug(msg)

# Crear instancia global del logger
_logger = Logger()

# Funciones de utilidad para uso directo
def attach_console_widget(widget: QTextEdit):
    """Conecta un QTextEdit para mostrar los logs"""
    _logger.attach_widget(widget)

def log_info(msg: str):
    """Registra un mensaje informativo"""
    _logger.info(msg)

def log_warning(msg: str):
    """Registra un mensaje de advertencia"""
    _logger.warning(msg)

def log_error(msg: str):
    """Registra un mensaje de error"""
    _logger.error(msg)

def log_debug(msg: str):
    """Registra un mensaje de depuración"""
    _logger.debug(msg)