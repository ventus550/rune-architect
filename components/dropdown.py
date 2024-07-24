import sys
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from .settings import theme


@theme
class Dropdown(QComboBox):
    def __init__(
        self,
        parent=None,
        button_background_color=theme.bg_one,
        button_color=theme.text_foreground,
        button_border_color="transparent",
        menu_background_color=theme.bg_two,
        menu_color=theme.text_foreground,
        selection_background_color=theme.bg_one,
        selection_color=theme.context_hover,
    ):
        super().__init__(parent)
        self.view().window().setStyleSheet("border-radius: 10px;")

        self.view().setStyleSheet(
            "QListView{"
            "border: none;"
            "border-radius: 8px;"
            "margin: 4px;"
            "margin-top: 0px;"
            "}"
        )

        self.view().window().setWindowFlags(
            Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.view().setGraphicsEffect(self.shadow)

        # self.setEditable(True)
        # self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.lineEdit().setReadOnly(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.setMaxVisibleItems(30)

    def addItems(self, items):
        super().addItems(items)
        return self
