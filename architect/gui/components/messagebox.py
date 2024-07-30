from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6.QtCore import Qt
from . import Component, Button
from ...settings import settings


class MessageBox(QMessageBox, metaclass=Component):
    def __init__(
        self,
        parent,
        text="MessageBox",
        font=settings.theme.text.family,
        color=settings.theme.text.color.important,
        font_size=settings.theme.text.size.normal,
    ):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.setText(text)
        self.setWindowTitle("Message")

        self.overlay = QWidget(parent)
        self.overlay.setStyleSheet(
            f"background-color: rgba(0, 0, 0, 128); border-radius: {settings.theme.items.radius}"
        )
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay.setGeometry(parent.rect())
        self.overlay.show()

        self.button = Button("Close", height=40, width=200, margin=7)
        self.button.clicked.connect(self.accept)
        self.layout().addWidget(
            self.button, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def exec(self):
        super().exec()
        self.overlay.hide()
        self.overlay.deleteLater()