from . import (
    QFrame,
    QWidget,
    Qt,
    QGraphicsDropShadowEffect,
    QColor,
    QLayout,
    QGridLayout,
    QSizePolicy,
)
from .settings import theme
from .component import Component


# @theme
class Container(QFrame, metaclass=Component):
    def __init__(
        self,
        margin=0,
        spacing=0,
        shadow=False,
        rstretch = [],
        cstretch = [],
        # STYLESHEET
        border_radius=10,
        border_size=2,
        bg_color="transparent",
        border_color="transparent",
    ):
        super().__init__()

        # PROPERTIES
        # ///////////////////////////////////////////////////////////////
        self.layout: QLayout = QGridLayout(self)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # self.addWidget = self.layout.addWidget

        # ADD LAYOUT
        # ///////////////////////////////////////////////////////////////
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(spacing)
        self.setRowsStretch(rstretch)
        self.setColumnsStretch(cstretch)

        # ADD DROP SHADOW
        # ///////////////////////////////////////////////////////////////
        if shadow:
            self.shadow = QGraphicsDropShadowEffect()
            self.shadow.setBlurRadius(20)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 160))
            self.setGraphicsEffect(self.shadow)

    def setRowsStretch(self, rows, stretch=1):
        if isinstance(rows, int):
            rows = (rows,)
        for row in rows:
            self.setColumnStretch(row, stretch)
        return self

    def setColumnsStretch(self, columns, stretch=1):
        if isinstance(columns, int):
            columns = (columns,)
        for column in columns:
            self.setColumnStretch(column, stretch)
        return self

    def __setitem__(self, key, val):
        if key is None or getattr(val, "_component_alignment", None) is None:
            self.layout.addWidget(val, *(key or []))
        else:
            self.layout.addWidget(val, *(key or []), alignment=val._component_alignment)

    def __getattr__(self, name: str):
        return getattr(self.layout, name)
