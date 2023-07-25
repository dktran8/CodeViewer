from PyQt5.QtWidgets import QTabWidget, QFileDialog
from editor_window import htmlEditor


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.currentChanged.connect(self.tabChanged)
        self.filePath = ""
        self.fileName = ""

    def newTab(self):
        print("newTab")
        count = 0
        while True:
            count += 1
            newName = f"new {count}"
            tabIndex = self.findTab(newName)
            if tabIndex is None:
                htmlWidget = htmlEditor()
                new_tab = self.addTab(htmlWidget, newName)
                print(new_tab)
                self.setCurrentIndex(new_tab)
                return

    def findTab(self, name):
        tabNames = []
        for index in range(self.count()):
            tabNames.append(self.tabText(index))
        if name in tabNames:
            return tabNames.index(name)
        else:
            return None

    def closeTab(self, index):
        print("closeTab")
        widget = self.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.removeTab(index)

    def tabChanged(self):
        print("tabChanged")

    def openJSON(self):
        print("openJSON")
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open JSON File', self.filePath, "JSON files (*.json)")
        if filePath:
            split_path = filePath.rsplit('/', 1)
            fileName = split_path[1]
            if self.findTab(fileName) is None:
                window_view = htmlEditor()
                with open(filePath, 'r', encoding='utf-8') as f:
                    data = f.read()
                window_view.editor.setText(data)
                window_view.renderHtml()
                self.addTab(window_view, fileName)
                self.setCurrentIndex(self.findTab(fileName))
            else:
                self.setCurrentIndex(self.findTab(fileName))
