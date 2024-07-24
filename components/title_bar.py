from .icon_button import IconButton
from .settings import settings
from . import (
    QWidget,
    QCursor,
    Qt,
    QSize,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
)

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSvgWidgets import QSvgWidget

_is_maximized = False
_old_size = QSize()

class TitleBar(QWidget):
    clicked = pyqtSignal(object)
    released = pyqtSignal(object)

    def __init__(
        self,
        parent,
        logo_image="no_icon.svg",
        height=60,
        bg_color="#343b48",
        btn_bg_color="#343b48",
        btn_bg_color_hover="#3c4454",
        btn_bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        context_color="#6c99f4",
        radius=8,
        font_family="Segoe UI",
        title_size=12,
        title=settings.app_name,
    ):
        super().__init__()

        # PARAMETERS
        self.parent = parent
        self.logo_image = logo_image
        self.btn_bg_color = btn_bg_color
        self.btn_bg_color_hover = btn_bg_color_hover
        self.btn_bg_color_pressed = btn_bg_color_pressed
        self.context_color = context_color
        self.icon_color_hover = icon_color_hover
        self.icon_color_pressed = icon_color_pressed
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
                parent.move(parent.pos() + event.globalPosition().toPoint() - parent.drag_position)
                # parent.move(parent.pos() + event.globalPosition().toPoint() - parent.drag_position)
                parent.drag_position = event.globalPosition().toPoint()
                event.accept()


        # MOVE APP WIDGETS
        self.top_logo.mouseMoveEvent = moveWindow
        self.title_label.mouseMoveEvent = moveWindow

        # MAXIMIZE / RESTORE
        self.top_logo.mouseDoubleClickEvent = self.maximize_restore
        self.title_label.mouseDoubleClickEvent = self.maximize_restore

    def maximize_restore(self, e=None):
        global _is_maximized
        global _old_size

        # CHANGE UI AND RESIZE GRIP
        def change_ui():
            if _is_maximized:
                self.parent.ui.central_widget_layout.setContentsMargins(0, 0, 0, 0)
                self.parent.ui.window.set_stylesheet(border_radius=0, border_size=0)
                self.maximize_restore_button.set_icon(
                    str(settings.assets_directory / "icon_restore.svg")
                )
            else:
                self.parent.ui.central_widget_layout.setContentsMargins(10, 10, 10, 10)
                self.parent.ui.window.set_stylesheet(border_radius=10, border_size=2)
                self.maximize_restore_button.set_icon(
                    str(settings.assets_directory / "icon_maximize.svg")
                )

        # CHECK EVENT
        if self.parent.isMaximized():
            _is_maximized = False
            self.parent.showNormal()
            # change_ui()
        else:
            _is_maximized = True
            _old_size = QSize(self.parent.width(), self.parent.height())
            self.parent.showMaximized()
            # change_ui()

    def attach_title_label(self):
        self.title_label = QLabel()
        self.bg_layout.addWidget(self.title_label)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.title_label.setStyleSheet(f"font-size: {self.title_size}pt;")
        self.title_label.setText(self.title)

    def attach_logo(self):

        # LEFT FRAME WITH MOVE APP
        self.top_logo = QLabel()
        self.bg_layout.addWidget(self.top_logo)
        self.top_logo_layout = QVBoxLayout(self.top_logo)
        self.top_logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_svg = QSvgWidget()
        self.logo_svg.load(str(settings.assets_directory / self.logo_image))
        self.top_logo_layout.addWidget(
            self.logo_svg, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter
        )
        self.top_logo.setMinimumWidth(100)
        self.top_logo.setMaximumWidth(100)

    def attach_buttons(self):
        self.custom_buttons_layout = QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_buttons_layout.setSpacing(3)

        button_style = dict(
            bg_color=self.btn_bg_color,
            bg_color_hover=self.btn_bg_color_hover,
            bg_color_pressed=self.btn_bg_color_pressed,
            icon_color_hover=self.icon_color_hover,
            icon_color_pressed=self.icon_color_pressed,
            icon_color_active=self.icon_color_active,
            context_color=self.context_color,
            radius=6,
        )

        # MINIMIZE BUTTON
        self.minimize_button = IconButton(
            **button_style,
            icon_path=str(settings.assets_directory / "icon_minimize.svg"),
        )
        self.bg_layout.addWidget(self.minimize_button)
        self.minimize_button.released.connect(lambda: self.parent.showMinimized())

        # MAXIMIZE / RESTORE BUTTON
        self.maximize_restore_button = IconButton(
            **button_style,
            icon_path=str(settings.assets_directory / "icon_maximize.svg"),
        )
        self.bg_layout.addWidget(self.maximize_restore_button)
        self.maximize_restore_button.released.connect(lambda: self.maximize_restore())

        # CLOSE BUTTON
        self.close_button = IconButton(
            **button_style,
            icon_path=str(settings.assets_directory / "icon_close.svg"),
        )
        self.bg_layout.addWidget(self.close_button)
        self.close_button.released.connect(lambda: self.parent.close())
