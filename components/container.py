from . import (
    QFrame,
    QWidget,
    Qt,
    QGraphicsDropShadowEffect,
    QColor,
    QLayout,
    QGridLayout,
)
from .settings import theme


@theme
class Container(QFrame):
    def __init__(
        self,
        parent,
        margin=0,
        spacing=2,
        shadow=False,
        # STYLESHEET
        bg_color=theme.bg_one,
        text_color="#fff",
        # text_font = "9pt 'Segoe UI'",
        border_radius=10,
        border_size=2,
        border_color=theme.bg_two,
    ):
        super().__init__()

        # PROPERTIES
        # ///////////////////////////////////////////////////////////////
        self.parent = parent
        self.layout: QLayout = QGridLayout(self)
        self.setLayout(self.layout)
        # self.addWidget = self.layout.addWidget

        # ADD LAYOUT
        # ///////////////////////////////////////////////////////////////
        # self.layout.setContentsMargins(margin, margin, margin, margin)
        # self.layout.setSpacing(spacing)

        # ADD DROP SHADOW
        # ///////////////////////////////////////////////////////////////
        if shadow:
            self.shadow = QGraphicsDropShadowEffect()
            self.shadow.setBlurRadius(20)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 160))
            self.setGraphicsEffect(self.shadow)

    def __getattr__(self, name: str):
        return getattr(self.layout, name)
