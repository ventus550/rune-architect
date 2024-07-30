from . import (
    IconButton,
    QWidget,
    Qt,
    QSize,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    pyqtSignal,
    QSvgWidget,
)
from .alignment import *
from ...settings import settings
class TitleBar(QWidget):
    clicked = pyqtSignal(object)
    released = pyqtSignal(object)

    def __init__(
        self,
        parent,
        logo_image="no_icon.svg",
        height=60,
        bg_color=settings.theme.background.frames,
        btn_bg_color=settings.theme.background.frames,
        btn_bg_color_pressed=settings.theme.background.container,
        icon_color_active=settings.theme.text.color.important,
        radius=settings.theme.items.radius,
        title_size=settings.theme.text.size.medium,
        title=settings.application.name,
    ):
        super().__init__()

        # PARAMETERS
        self.parent = parent
        self.logo_image = logo_image
        self.btn_bg_color = btn_bg_color
        self.btn_bg_color_pressed = btn_bg_color_pressed
        self.icon_color_active = icon_color_active
        self.title_size = title_size
        self.title = title

        # ADD BG
        self.bg = QFrame()
        self.bg_layout = QHBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(10, 0, 5, 0)
        self.bg_layout.setSpacing(0)
        self.bg.setStyleSheet(
            f"background-color: {bg_color}; border-radius: {radius}px;"
        )

        # ADD MENU LAYOUT
        self.title_bar_layout = QVBoxLayout(self)
        self.title_bar_layout.addWidget(self.bg)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # ADD BG LAYOUT
        self.attach_logo()

        # TITLE LABEL
        self.attach_title_label()

        # CUSTOM BUTTONS LAYOUT
        self.attach_buttons()

        # SET LOGO AND WIDTH
        self.setFixedHeight(height)
        # self.top_logo.setPixmap(Functions.set_svg_image(logo_image))

        def moveWindow(event):
            if parent.isMaximized():
                # return
                self.maximize_restore()
                # return
                # # # self.resize(_old_size)
                # parent.drag_position = event.globalPosition().toPoint() - self.rect().topLeft()
                # self.move(event.globalPosition().toPoint() - parent.drag_position)
                # curso_x = parent.pos().x()
                # curso_y = event.globalPosition().toPoint().y() - QCursor.pos().y()
                # parent.move(curso_x, curso_y)
                # parent.move(event.globalPosition().toPoint())
                # event.accept()
                return
            if event.buttons() == Qt.MouseButton.LeftButton:
                parent.move(
                    parent.pos()
                    + event.globalPosition().toPoint()
                    - parent.drag_position
                )
                # parent.move(parent.pos() + event.globalPosition().toPoint() - parent.drag_position)
                parent.drag_position = event.globalPosition().toPoint()
                event.accept()

        # MOVE APP WIDGETS
        self.top_logo.mouseMoveEvent = moveWindow
        self.title_label.mouseMoveEvent = moveWindow

        # MAXIMIZE / RESTORE
        self.top_logo.mouseDoubleClickEvent = self.parent.toogle_fullscreen
        self.title_label.mouseDoubleClickEvent = self.parent.toogle_fullscreen

    def attach_title_label(self):
        self.title_label = QLabel()
        self.bg_layout.addWidget(self.title_label)
        self.title_label.setAlignment(AlignVCenter)
        self.title_label.setStyleSheet(f"font-size: {self.title_size}pt;")
        self.title_label.setText(self.title)

    def attach_logo(self):

        # LEFT FRAME WITH MOVE APP
        self.top_logo = QLabel()
        self.bg_layout.addWidget(self.top_logo)
        self.top_logo_layout = QVBoxLayout(self.top_logo)
        self.top_logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_svg = QSvgWidget()
        self.logo_svg.load(str(settings.directories.assets / self.logo_image))
        self.top_logo_layout.addWidget(self.logo_svg, AlignCenter, AlignCenter)
        self.top_logo.setFixedHeight(30)
        self.top_logo.setFixedWidth(40)

    def attach_buttons(self):
        self.custom_buttons_layout = QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_buttons_layout.setSpacing(3)

        # MINIMIZE BUTTON
        self.minimize_button = IconButton(
            bg_color=self.btn_bg_color,
            radius=6,
            icon_path=str(settings.directories.assets / "icon_minimize.svg"),
        )
        self.bg_layout.addWidget(self.minimize_button)
        self.minimize_button.released.connect(self.parent.toogle_fullscreen)

        # MAXIMIZE / RESTORE BUTTON
        self.maximize_restore_button = IconButton(
            bg_color=self.btn_bg_color,
            radius=6,
            icon_path=str(settings.directories.assets / "icon_maximize.svg"),
        )
        self.bg_layout.addWidget(self.maximize_restore_button)
        self.maximize_restore_button.released.connect(self.parent.toogle_fullscreen)

        # CLOSE BUTTON
        self.close_button = IconButton(
            bg_color=self.btn_bg_color,
            radius=6,
            icon_path=str(settings.directories.assets / "icon_close.svg"),
        )
        self.bg_layout.addWidget(self.close_button)
        self.close_button.released.connect(self.parent.close)
