from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from gui.components import Button
from .settings import theme

class MessageBox(QMessageBox):
	def __init__(self, parent, text="MessageBox"):
		super().__init__(parent=parent)
		self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.setStandardButtons(QMessageBox.StandardButton.NoButton)
		self.setText(text)
		self.setWindowTitle("Message")
		
		self.button = Button("Close", height=50, width=200)
		self.button.clicked.connect(self.accept)
		
		self.layout().addWidget(self.button, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
		self.setStyleSheet(f"QMessageBox QLabel {{ font: 16pt {theme.font_family}; color: white; text-align: center; }}")
	