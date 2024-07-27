from . import Component, QPushButton, Qt
from .settings import theme


class Button(QPushButton, metaclass=Component):
    def __init__(
        self,
        text="Button",
        height=None,
        width=None,
        color="#fff",
        bg_color=theme.context_color,
        bg_hover_color=theme.context_hover,
        bg_pressed_color=theme.context_pressed,
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
