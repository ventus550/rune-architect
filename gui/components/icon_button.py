from . import QPushButton, Qt, QPainter, QBrush, QRect, QPixmap, QColor, settings

from .hex import adjust_brightness


class IconButton(QPushButton):
    def __init__(
        self,
        btn_id=None,
        width=30,
        height=30,
        radius=8,
        bg_color=settings.theme.background.frames,
        icon_color=settings.theme.background.container,
        icon_active=settings.theme.items.color.primary,
        icon_path="no_icon.svg",
    ):
        super().__init__()

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName(btn_id)

        self.bg_color = bg_color
        self.bg_color_hover = adjust_brightness(bg_color, 1.1)
        self.bg_color_pressed = adjust_brightness(bg_color, 0.9)
        self.icon_color = icon_color
        self.icon_color_hover = adjust_brightness(icon_active, 1.2)
        self.icon_color_pressed = adjust_brightness(icon_active, 1.1)

        self.set_bg_color = bg_color
        self.set_icon_path = icon_path
        self.set_icon_color = icon_color
        self.set_border_radius = radius

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

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
