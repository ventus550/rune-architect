from . import Component, QPushButton, Qt
from .settings import settings


class Button(QPushButton, metaclass=Component):
    def __init__(
        self,
        text="Button",
        height=None,
        width=None,
        color=settings.theme.text.color.important,
        bg_color=settings.theme.items.color.context,
        bg_hover_color=settings.theme.items.color.hover,
        bg_pressed_color=settings.theme.items.color.press,
        **kwargs
    ):
        super().__init__(text=text, **kwargs)
        self.text = text
        if height:
            self.setMinimumHeight(height)
        if width:
            self.setMinimumWidth(width)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, string):
        self._text = string
        self.setText(self._text)
