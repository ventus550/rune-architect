from . import (
    Component,
    Editor,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QStyledItemDelegate,
    Qt,
    QHeaderView,
    QSize,
)
from .alignment import *
import numpy
import pandas
from itertools import product
from .settings import settings


class Delegate(QStyledItemDelegate):
    def __init__(
        self,
        parent=None,
        numeric=False,
        maxlen=10,
        placeholder="",
        bg_color=settings.theme.background.frames,
    ):
        super().__init__(parent)
        self.maxlen = maxlen
        self.placeholder = placeholder
        self.bg_color = bg_color
        self.numeric = numeric

    def createEditor(self, parent, option, index):
        return Editor(
            parent=parent,
            numeric=self.numeric,
            placeholder=self.placeholder,
            maxlen=self.maxlen,
            bg_color="transparent"
        )

    def setEditorData(self, editor, index):
        text = str(index.model().data(index, Qt.ItemDataRole.EditRole))
        editor.setText(text)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)

    def paint(self, painter, option, index):
        painter.save()
        text = str(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        if text == "" or (self.numeric and not text.isnumeric()):
            text = self.placeholder
        painter.drawText(option.rect, AlignCenter, str(text))
        painter.restore()


class DataFrame(QTableWidget, metaclass=Component):
    def __init__(
        self,
        data=pandas.DataFrame(),
        numeric=False,
        placeholder="",
        flexible_rows=False,
        maxlen=10,
        editable=True,
        row_height=30,
        padding=10,
        radius=settings.theme.items.radius,
        # bg_color="transparent",
        bg_color=settings.theme.items.color.headers,
        color=settings.theme.text.color.description,
        selection_color=settings.theme.items.color.primary,
        header_horizontal_color=settings.theme.items.color.headers,
        header_vertical_color=settings.theme.items.color.headers,
        bottom_line_color=settings.theme.background.container,
        grid_line_color=settings.theme.background.container,
        scroll_bar_bg_color=settings.theme.background.container,
        scrollbar_color=settings.theme.items.color.primary,
    ):
        QTableWidget.__init__(self)
        self.padding = padding
        # Horizontal header (labels) settings
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionsClickable(False)
        self.horizontalHeader().setMaximumHeight(row_height)
        self.horizontalHeader().setStyleSheet(f"background-color: {bg_color};")

        # Vertical header (index) settings
        if not flexible_rows:
            self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setStyleSheet(f"background-color: {bg_color};")
        self.verticalHeader().setSectionsClickable(False)
        self.verticalHeader().setMinimumSectionSize(row_height)

        # Window settings
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setItemDelegate(
            Delegate(self, numeric=numeric, maxlen=maxlen, placeholder=placeholder)
        )
        self.editable = editable
        self.index = []
        self.label = []
        self.data = data

    @property
    def data(self):
        rows, cols = len(self.index), len(self.label)
        matrix = numpy.zeros((rows, cols)).tolist()
        for row, col in product(range(rows), range(cols)):
            text = self.item(row, col).text()

            matrix[row][col] = text if text else None
        return pandas.DataFrame(matrix, columns=self.label, index=self.index)
    
    def sizeHint(self):
        if self.rowCount() == 0:
            return QSize(self.width(), 0)
        return QSize(self.width(), (self.rowCount() + 1) * (self.rowHeight(0) + 1))

    @data.setter
    def data(self, df: pandas.DataFrame):
        self.label = df.columns.astype(str)
        self.index = df.index.astype(str)
        rows, cols = len(self.index), len(self.label)

        self.setColumnCount(cols)
        self.setHorizontalHeaderLabels(self.label)

        self.setRowCount(rows)
        self.setVerticalHeaderLabels(self.index)

        for row, col in product(range(rows), range(cols)):
            value = df.iloc[row, col]
            self.setItem(
                row, col, QTableWidgetItem(str(value) if pandas.notna(value) else "")
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            index = self.indexAt(event.pos())
            if index.isValid() and self.editable:
                self.model().setData(index, "")  # Clear cell data
                self.edit(index)  # Enter edit mode
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.editable:
            super().mouseDoubleClickEvent(event)
