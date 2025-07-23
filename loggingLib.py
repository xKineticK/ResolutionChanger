# loggingLib.py
import logging
from PyQt6.QtWidgets import QTextEdit

_console_widget = None

class QTextEditHandler(logging.Handler):
    def emit(self, record):
        if _console_widget:
            msg = self.format(record)
            _console_widget.append(msg)
            _console_widget.verticalScrollBar().setValue(_console_widget.verticalScrollBar().maximum())

# Formatter with timestamp, level, and message
formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d | ## %(levelname)-5s | %(message)s",
    "%H:%M:%S"
)

# Main logger setup
logger = logging.getLogger("ResolutionChanger")
logger.setLevel(logging.DEBUG)

# Console output
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# QTextEdit output (optional)
qt_handler = QTextEditHandler()
qt_handler.setFormatter(formatter)
logger.addHandler(qt_handler)

def attach_console_widget(widget: QTextEdit):
    global _console_widget
    _console_widget = widget

def printInfo(msg):
    logger.info(msg)

def printWarning(msg):
    logger.warning(msg)

def printError(msg):
    logger.error(msg)
