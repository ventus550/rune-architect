from . import Component, QCheckBox, QCursor, Qt
from .settings import theme


class CheckBox(QCheckBox, metaclass=Component):
    def __init__(
        self,
        text="",
        border_width=2,
        border_color=theme.text_foreground,
        color=theme.text_foreground,
        bg_unchecked_color="transparent",
        bg_checked_color=theme.context_color,
    ):
        super().__init__(text=text)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

