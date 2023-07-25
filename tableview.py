from PyQt5.QtCore import (Qt, QAbstractTableModel)
from PyQt5.QtGui import     (QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QProxyStyle,QStyleOption,
                            QTableView, QHeaderView,
                            QItemDelegate,
                            QApplication)


class customModel(QStandardItemModel):
    def dropMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        response = super().dropMimeData(data, Qt.CopyAction, row, 0, parent)
        return response


class customTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSelectionBehavior(self.SelectRows)  # Select whole rows
        self.setAcceptDrops(True)
        self.setSelectionMode(self.SingleSelection)  # Only select/drag one row each time
        self.setDragDropMode(self.InternalMove)  # Objects can only be drag/dropped internally and are moved instead of copied
        self.setDragDropOverwriteMode(False)  # Removes the original item after moving instead of clearing it

        # Set our custom style - this draws the drop indicator across the whole row
        self.setStyle(customStyle())

        model = customModel()
        self.setModel(model)
        self.populate()

    def populate(self):
        set_enabled = True  # We'll change this value to show how to drag rows with disabled elements later
        model = self.model()
        for row in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            data = []
            for column in range(5):
                item = QStandardItem(f'{row}-{column}')
                item.setDropEnabled(False)
                if column == 3:
                    item.setEnabled(set_enabled)
                data.append(item)
            model.appendRow(data)


class customStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row rather than just the column
        we're hovering over.  This may not always work depending on global
        style - for instance I think it won't work on OSX.
        """
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)
