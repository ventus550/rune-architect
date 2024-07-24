from .parameters import stylized
from . import QTableWidget, QTableWidgetItem, QAbstractItemView, QStyledItemDelegate, QLineEdit, QIntValidator, Qt
import numpy
import pandas
from itertools import product




class NumericDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, max_length=10, placeholder=""):
        super().__init__(parent)
        self.max_length = max_length
        self.placeholder = placeholder

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setMaxLength(self.max_length)
        editor.setValidator(QIntValidator())  # Restrict to numerical input only
        editor.setPlaceholderText(self.placeholder)  # Set placeholder text
        editor.setAlignment(Qt.AlignCenter)  # Center the text in the editor
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.EditRole)
        editor.setText(str(text))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    def paint(self, painter, option, index):
        painter.save()
        text = index.model().data(index, Qt.DisplayRole)
        if text == "":
            text = self.placeholder
        painter.drawText(option.rect, Qt.AlignCenter, str(text))
        painter.restore()

@stylized
class QDataFrame(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.horizontalHeader().setSectionsClickable(False)
        self.verticalHeader().setSectionsClickable(False)
        self.setItemDelegate(NumericDelegate(self, max_length=10, placeholder=""))
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
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                self.model().setData(index, "")  # Clear cell data
                self.edit(index)  # Enter edit mode
        super().mousePressEvent(event)