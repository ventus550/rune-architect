from . import (
    Component,
    Editor,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QStyledItemDelegate,
    Qt,
    QHeaderView,
)
from .alignment import *
import numpy
import pandas
from itertools import product
from .settings import theme


class Delegate(QStyledItemDelegate):
    def __init__(
        self,
        parent=None,
        numeric=False,
        maxlen=10,
        placeholder="",
        bg_color=theme.bg_two,
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
        radius=8,
        color=theme.text_foreground,
        selection_color=theme.context_color,
        bg_color="transparent",
        header_horizontal_color=theme.dark_two,
        header_vertical_color=theme.dark_two,
        bottom_line_color=theme.bg_three,
        grid_line_color=theme.bg_one,
        scroll_bar_bg_color=theme.bg_one,
        scroll_bar_btn_color=theme.dark_four,
        context_color=theme.context_color,
    ):
        QTableWidget.__init__(self)
        # Horizontal header (labels) settings
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionsClickable(False)
        self.horizontalHeader().setMinimumHeight(30)

        # Vertical header (index) settings
        if not flexible_rows:
            self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionsClickable(False)
        self.verticalHeader().setMinimumSectionSize(30)

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

            matrix[row][col] = text if text else None  # pandas.NA
        return pandas.DataFrame(matrix, columns=self.label, index=self.index)

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
