from . import Component, QPushButton, Qt
from .settings import settings
from .hex import adjust_brightness

bg_color = settings.theme.items.color.primary
class Button(QPushButton, metaclass=Component):
    def __init__(
        self,
        text="Button",
        height=None,
        width=None,
        margin=0,
        color=settings.theme.text.color.important,
        bg_color=bg_color,
        bg_hover_color=adjust_brightness(bg_color, 1.2),
        bg_pressed_color=adjust_brightness(bg_color, 0.8),
        font_size=settings.theme.text.size.large,
        border_radius=settings.theme.items.radius,
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
