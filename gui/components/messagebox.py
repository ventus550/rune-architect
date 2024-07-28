from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from gui.components import Component, Button
from .settings import settings


class MessageBox(QMessageBox, metaclass=Component):
    def __init__(
        self,
        parent,
        text="MessageBox",
        font=settings.theme.text.family,
        color=settings.theme.text.color.important,
    ):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.setText(text)
        self.setWindowTitle("Message")

        self.button = Button("Close", height=40, width=200)
        self.button.clicked.connect(self.accept)
        self.layout().addWidget(
            self.button, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )