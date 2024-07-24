
from .parameters import stylized
from . import QGroupBox, QVBoxLayout, QWidget, QLayout

@stylized
class QFrame(QGroupBox):
    def __init__(self, *args, layout: QLayout=QVBoxLayout(), **kwargs):
        QGroupBox.__init__(self, *args, **kwargs)
        self.layout: QLayout = layout
        self.setLayout(self.layout)
        self.addWidget = self.layout.addWidget
