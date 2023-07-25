from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDropEvent
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QTableView


from PyQt5 import QtWidgets, QtCore

class ReorderTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None, *args):
        super().__init__(parent, *args)
        self._data = data

    def columnCount(self, parent=None) -> int:
        return len(self._data[0])

    def dropMimeData(self, data, action, row, col, parent):
        print("dropped mime data")
        """
        Always move the entire row, and don't allow column "shifting"
        """
        response = super().dropMimeData(data, Qt.CopyAction, row, 0, parent)
        return response

    def rowCount(self, parent=None) -> int:
        return len(self._data)

    def headerData(self, column: int, orientation, role: QtCore.Qt.ItemDataRole):
        return (('Object', 'Descriptor', 'Device ID')[column]
                if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal
                else None)

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt.ItemDataRole):
        if not index.isValid() or role not in {QtCore.Qt.DisplayRole, QtCore.Qt.EditRole}:
            return None
        return (self._data[index.row()][index.column()] if index.row() < len(self._data) else
                "edit me" if role == QtCore.Qt.DisplayRole else "")

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        # https://doc.qt.io/qt-5/qt.html#ItemFlag-enum
        if not index.isValid():
            return QtCore.Qt.ItemIsDropEnabled
        if index.row() < len(self._data):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

    def supportedDropActions(self) -> bool:
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction

    def relocateRow(self, row_source, row_target) -> None:
        print("relocate")
        row_a, row_b = max(row_source, row_target), min(row_source, row_target)
        print(row_a, row_b)
        try:
            self.beginMoveRows(QtCore.QModelIndex(), row_a, row_a, QtCore.QModelIndex(), row_b)
            self._data.insert(row_target, self._data.pop(row_source))
            self.endMoveRows()
        except Exception as e:
            print(e)


class ReorderTableView(QtWidgets.QTableView):
    """QTableView with the ability to make the model move a row with drag & drop"""

    class DropmarkerStyle(QtWidgets.QProxyStyle):
        def drawPrimitive(self, element, option, painter, widget=None):
            """Draw a line across the entire row rather than just the column we're hovering over.
            This may not always work depending on global style - for instance I think it won't
            work on OSX."""
            if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
                option_new = QtWidgets.QStyleOption(option)
                option_new.rect.setLeft(0)
                if widget:
                    option_new.rect.setRight(widget.width())
                option = option_new
            super().drawPrimitive(element, option, painter, widget)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.verticalHeader().hide()
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setAcceptDrops(True)

        self.setStyle(self.DropmarkerStyle())

        model = ReorderTableModel([[1,2,3],[4,5,6],[7,8,9]])
        self.setModel(model)

    def dropEvent(self, event):
        print("dropevent")
        if (event.source() is not self or
            (event.dropAction() != Qt.MoveAction and
             self.dragDropMode() != QtWidgets.QAbstractItemView.InternalMove)):
            super().dropEvent(event)

        selection = self.selectedIndexes()
        from_index = selection[0].row() if selection else -1
        to_index = self.drop_on(event)
        print(from_index, to_index)
        if (0 <= from_index < self.model().rowCount() and
            0 <= to_index < self.model().rowCount() and
            from_index != to_index):
            self.model().relocateRow(from_index, to_index)
            event.accept()
        super().dropEvent(event)

    # def dropEvent(self, event: QDropEvent):
    #     if not event.isAccepted() and event.source() == self:
    #         drop_row = self.drop_on(event)
    #
    #         rows = sorted(set(item.row() for item in self.selectedItems()))
    #         rows_to_move = [
    #             [QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
    #             for row_index in rows]
    #         for row_index in reversed(rows):
    #             self.removeRow(row_index)
    #             if row_index < drop_row:
    #                 drop_row -= 1
    #
    #         for row_index, data in enumerate(rows_to_move):
    #             row_index += drop_row
    #             self.insertRow(row_index)
    #             for column_index, column_data in enumerate(data):
    #                 self.setItem(row_index, column_index, column_data)
    #         event.accept()
    #
    #         for row_index in range(len(rows_to_move)):  # maybe can be done smarter
    #             for col in range(self.columnCount()):
    #                 self.item(drop_row + row_index, col).setSelected(True)
    #
    #     super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.model().rowCount()
        return index.row() if self.is_below(event.pos(), index) else max(index.row()-1,0)

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            print("Is above")
            return False
        elif rect.bottom() - pos.y() < margin:
            print("Is below")
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (
                    int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()
