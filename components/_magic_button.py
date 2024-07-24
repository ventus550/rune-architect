from PyQt5.QtWidgets import QPushButton
from .parameters import stylized

@stylized
class QMagicButton(QPushButton):
    def __init__(self, text="QMagicButton", **kwargs):
        super().__init__(text=text, **kwargs)
        self._text = ""
        self.text = text

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, string):
        self._text = string
        self.setText(self._text)

