from . import (
    Component,
    QColor,
    Qt,
    QComboBox,
    QGraphicsDropShadowEffect,
)
from .settings import settings


class Dropdown(QComboBox, metaclass=Component):
    def __init__(
        self,
        parent=None,
        width=None,
        button_border_color="transparent",
        button_border_radius=settings.theme.items.radius,
        button_background_color=settings.theme.background.container,
        button_color=settings.theme.text.color.description,
        menu_background_color=settings.theme.items.color.headers,
        menu_color=settings.theme.text.color.description,
        selection_background_color= settings.theme.background.frames,
        selection_color=settings.theme.items.color.primary,
        arrow_icon_url=f"url({settings.directories.assets / "icon_menu.svg"})"
    ):
        super().__init__(parent)
        self.view().window().setStyleSheet("border-radius: 10px;")

        self.view().setStyleSheet(
            """
            QListView {
                border: none;
                border-radius: 8px;
                margin: 4px;
                margin-top: 10px;
            }"""
        )

        if width:
            self.setFixedWidth(width)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
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

    @property
    def value(self) -> str:
        return self.currentText()

    @value.setter
    def value(self, text: str):
        self.setCurrentText(text)

    def addItems(self, items):
        super().addItems(items)
        return self
