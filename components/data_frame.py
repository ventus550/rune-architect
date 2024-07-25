from . import (
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QStyledItemDelegate,
    QLineEdit,
    QIntValidator,
    Qt,
    QHeaderView,
    QPalette,
    QColor,
)
import numpy
import pandas
from itertools import product
from .settings import theme
from .editor import Editor
from .component import Component


class NumericDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, maxlen=10, placeholder="", bg_color=theme.bg_two):
        super().__init__(parent)
        self.maxlen = maxlen
        self.placeholder = placeholder
        self.bg_color = bg_color

    def createEditor(self, parent, option, index):
        return Editor(
            parent=parent,
            numeric=True,
            placeholder=self.placeholder,
            maxlen=self.maxlen,
        )

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)

    def paint(self, painter, option, index):
        painter.save()
        text = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if text == "":
            text = self.placeholder
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, str(text))
        painter.restore()


class DataFrame(QTableWidget, metaclass=Component):
    def __init__(
        self,
        data,
        placeholder="",
        flexible_rows=False,
        radius=8,
        color=theme.text_foreground,
        selection_color=theme.context_color,
        bg_color="transparent", #theme.bg_two,
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
        self.setItemDelegate(NumericDelegate(self, maxlen=10, placeholder=placeholder))
        self.index = []
        self.label = []
        self.data = data


    @property
    def data(self):
        rows, cols = len(self.index), len(self.label)
        matrix = numpy.zeros((rows, cols))
        for row, col in product(range(rows), range(cols)):
            item = self.item(row, col)
            matrix[row, col] = item.text() if item is not None else ""
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
            self.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                self.model().setData(index, "")  # Clear cell data
                self.edit(index)  # Enter edit mode
        super().mousePressEvent(event)
