from . import Component, QCheckBox, QCursor, Qt
from ...settings import settings


class CheckBox(QCheckBox, metaclass=Component):
    def __init__(
        self,
        text="",
        border_width=2,
        border_color=settings.theme.text.color.description,
        color=settings.theme.text.color.description,
        bg_unchecked_color="transparent",
        bg_checked_color=settings.theme.items.color.primary,
    ):
        super().__init__(text=text)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
