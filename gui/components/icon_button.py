from . import (
    QPushButton,
    Qt,
    QPainter,
    QBrush,
    QRect,
    QPixmap,
    QColor,
)


class IconButton(QPushButton):
    def __init__(
        self,
        btn_id=None,
        width=30,
        height=30,
        radius=8,
        bg_color="#343b48",
        bg_color_hover="#3c4454",
        bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        icon_path="no_icon.svg",
        context_color="#568af2",
        is_active=False,
    ):
        super().__init__()

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName(btn_id)

        self.bg_color = bg_color
        self.bg_color_hover = bg_color_hover
        self.bg_color_pressed = bg_color_pressed
        self.icon_color = icon_color
        self.icon_color_hover = icon_color_hover
        self.icon_color_pressed = icon_color_pressed
        self.icon_color_active = icon_color_active
        self.context_color = context_color
        self.is_active = is_active

        self.set_bg_color = bg_color
        self.set_icon_path = icon_path
        self.set_icon_color = icon_color
        self.set_border_radius = radius

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.is_active:
            brush = QBrush(QColor(self.context_color))
        else:
            brush = QBrush(QColor(self.set_bg_color))

        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.PenStyle.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(rect, self.set_border_radius, self.set_border_radius)
        self.icon_paint(paint, self.set_icon_path, rect)
        paint.end()

    def icon_paint(self, qp, image, rect):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        if self.is_active:
            painter.fillRect(icon.rect(), QColor(self.icon_color_active))
        else:
            painter.fillRect(icon.rect(), QColor(self.set_icon_color))
        qp.drawPixmap(
            (rect.width() - icon.width()) // 2,
            (rect.height() - icon.height()) // 2,
            icon,
        )
        painter.end()

    def enterEvent(self, event):
        self.set_bg_color = self.bg_color_hover
        self.set_icon_color = self.icon_color_hover
        self.repaint()

    def leaveEvent(self, event):
        self.set_bg_color = self.bg_color
        self.set_icon_color = self.icon_color
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_bg_color = self.bg_color_pressed
            self.set_icon_color = self.icon_color_pressed
            self.repaint()
            self.setFocus()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_bg_color = self.bg_color_hover
            self.set_icon_color = self.icon_color_hover
            self.repaint()
            return self.released.emit()

    def set_icon(self, icon_path):
        self.set_icon_path = icon_path
        self.repaint()
