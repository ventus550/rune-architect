from . import (
    Component,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QApplication,
    Qt,
    QPoint,
    QFontDatabase,
    QIcon,
    QRect,
    QPropertyAnimation,
)
from ...settings import settings
import sys
import ctypes
from contextlib import suppress


class CentralWidget(QWidget, metaclass=Component):
    def __init__(
        self,
        text_size=settings.theme.text.size.normal,
        font_family=settings.theme.text.family,
        text_foreground=settings.theme.text.color.description,
    ) -> None:
        super().__init__()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.addWidget = self.layout.addWidget

        font_id = QFontDatabase.addApplicationFont(
            str(settings.directories.assets / settings.application.font)
        )
        if font_id == -1:
            print("Failed to load the custom font.")
            return

        font_family = QFontDatabase.applicationFontFamilies(font_id)
        if not font_family:
            print("No font families found.")
            return


class Window(QMainWindow):
    def __init__(
        self,
        minw=settings.application.width,
        minh=settings.application.height,
        name=settings.application.name,
    ) -> None:
        self.sysapp = QApplication(sys.argv)
        self.sysapp.setQuitOnLastWindowClosed(True)
        self.sysapp.setWindowIcon(QIcon(str(settings.directories.assets / "icon.ico")))
        self.sysapp.setApplicationName(name)
        self.sysapp.setEffectEnabled(Qt.UIEffect.UI_AnimateCombo, False);
        self.drag_position: QPoint = None
        self.fullscreen = False
        with suppress(AttributeError):
            # set application group icon for windows
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(name)

        super().__init__()
        self.setWindowTitle(name)
        self.setMouseTracking(True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

        self.addWidget = self.central_widget.addWidget

        self.setMinimumSize(minw, minh)
        self.center()

    def mousePressEvent(self, event):
        self.drag_position = event.globalPosition().toPoint()

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_point = screen_geometry.center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def toogle_fullscreen(self):
        if self.fullscreen:
            self.showNormal()
        else:
            self.showMaximized()
        self.fullscreen = not self.fullscreen

    def exec(self):
        self.show()
        self.sysapp.exec()
        # self.sysapp.shutdown()
