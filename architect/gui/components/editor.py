from PyQt6.QtGui import QKeyEvent
from . import Component, QKeyEvent, QLineEdit, QTimer, QColor, QPainter, QIntValidator, Qt
from .settings import settings


class Editor(QLineEdit, metaclass=Component):
	def __init__(
		self,
		parent=None,
		numeric=False,
		maxlen=10,
		caret_width=2,
		placeholder="",
		color=settings.theme.text.color.description,
		selection_color=settings.theme.items.color.primary,
		bg_color=settings.theme.background.frames,
	):
		super().__init__(parent=parent)
		if numeric:
			self.setValidator(QIntValidator())

		self.setMaxLength(maxlen)
		self.setPlaceholderText(placeholder)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.setReadOnly(True)

		self.caret_visible = True
		self.cursor_timer = QTimer(self)
		self.cursor_timer.timeout.connect(self.toggle_caret)
		self.cursor_timer.start(500)  # Blink interval for the caret
		self.caret_color = QColor(color)
		self.caret_width = caret_width

	def toggle_caret(self):
		self.caret_visible = not self.caret_visible
		self.update()

	def keyPressEvent(self, a0: QKeyEvent | None) -> None:
		self.setReadOnly(False);
		res = super().keyPressEvent(a0)
		self.setReadOnly(True);
		return res

	def paintEvent(self, event):
		super().paintEvent(event)

		if not self.caret_visible:
			return

		cursor_rect = self.cursorRect()
		cursor_rect.setWidth(self.caret_width)  # Set the custom caret width
		cursor_rect.moveLeft(
			cursor_rect.left() + 3 * self.caret_width
		)  # Adjust position for center alignment
		painter = QPainter(self)
		painter.fillRect(cursor_rect, self.caret_color)
