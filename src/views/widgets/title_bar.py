from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QPoint

class TitleBar(QFrame):
    """Barra de título personalizada"""
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(32)
        self.old_pos = None
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(0)

        # Título
        self.title_label = QLabel("Resolution Changer")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setFixedHeight(32)
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Botones
        self.minimize_button = self._create_title_button("─", "Minimize")
        self.maximize_button = self._create_title_button("□", "Maximize")
        self.close_button = self._create_title_button("×", "Close", is_close=True)
        
        # Conectar señales
        self.minimize_button.clicked.connect(self.minimize_clicked)
        self.maximize_button.clicked.connect(self.maximize_clicked)
        self.close_button.clicked.connect(self.close_clicked)
        
        # Agregar widgets al layout
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        
    def _create_title_button(self, text, tooltip, is_close=False):
        btn = QPushButton(text)
        btn.setFixedSize(45, 32)
        btn.setToolTip(tooltip)
        btn.setObjectName("exitButton" if is_close else "titleButton")
        return btn
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            parent = self.parent() or self
            parent.move(parent.x() + delta.x(), parent.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None