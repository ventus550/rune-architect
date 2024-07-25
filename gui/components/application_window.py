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
)
from .settings import theme, settings
import sys


class CentralWidget(QWidget, metaclass=Component):
    def __init__(
        self,
        text_size=theme.text_size,
        font_family=theme.font_family,
        text_foreground=theme.text_foreground,
    ) -> None:
        super().__init__()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.addWidget = self.layout.addWidget

        # move somewhere else?
        font_id = QFontDatabase.addApplicationFont(str(settings.font_path))
        if font_id == -1:
            print("Failed to load the custom font.")
            return

        font_family = QFontDatabase.applicationFontFamilies(font_id)
        if not font_family:
            print("No font families found.")
            return


class ApplicationWindow(QMainWindow):
    def __init__(self, minw=800, minh=600, name="ApplicationName") -> None:
        self.sysapp = QApplication(sys.argv)
        self.sysapp.setQuitOnLastWindowClosed(True)
        self.sysapp.setWindowIcon(QIcon(str(settings.assets_directory / "icon.ico")))
        self.sysapp.setApplicationName(name)
        self.drag_position: QPoint = None

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

    def exec(self):
        self.show()
        self.sysapp.exec()
        # self.sysapp.shutdown()
