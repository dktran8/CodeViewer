import sys

from PyQt5 import QtWebEngineWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QAction, QMenu, QFileDialog, \
    QToolBar, QTabWidget, QLabel
from editor_window import htmlEditor
from tabview import Tabs


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.navMenuFileTemplate = r"NavMenuTemplate.html"
        self.currentDirectory = r'C:\RC-Studio\3.0-lib\pic\Animation\FlexTile-Nav-Menu-V03\build'

        # Set window main properties
        self.setWindowTitle('JSON Viewer')
        self.setObjectName("MainWindow")
        self.resize(900, 700)

        # Menu/Tool Bar
        self._createActions()
        self._createMenuBar()
        self._createToolBar()
        self._connectActions()

        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.tabWidget = Tabs()
        # self.tabWidget.setTabsClosable(True)
        # self.tabWidget.setMovable(True)
        # self.tabWidget.tabCloseRequested.connect(self.removeTab)
        # self.tabWidget.currentChanged.connect(self.changed)
        self.generalLayout.addWidget(self.tabWidget)
        # self.tabNames = []

        # self.window_view = htmlEditor(self.navMenuFileTemplate)
        # self.tabWidget.addTab(self.window_view, "Tab 1")
        # self.generalLayout.addWidget(self.window_view)

        # self.window_view.editor.modificationChanged.connect(self.textchanged)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # File menu
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exitAction)

    def _createToolBar(self):
        toolbar = self.addToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        toolbar.setMovable(False)
        # Buttons
        toolbar.addAction(self.newAction)
        toolbar.addAction(self.openAction)
        toolbar.addAction(self.saveAction)

    def _createActions(self):
        # File actions
        self.newAction = QAction(QIcon("document--plus.png"), "&New", self)
        self.openAction = QAction(QIcon("folder-open-document-text.png"), "&Open...", self)
        self.saveAction = QAction(QIcon("disk.png"), "&Save", self)
        self.saveAsAction = QAction(QIcon("disk.png"), "Save As...", self)
        self.exitAction = QAction(QIcon("cross.png"), "&Exit", self)

    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newCall)
        self.openAction.triggered.connect(self.openCall)
        # self.saveAction.triggered.connect(self.saveCall)
        # self.saveAsAction.triggered.connect(self.saveAsCall)
        # self.exitAction.triggered.connect(self.closeCall)

    # def changed(self):
    #     print("changed")
    #
    def newCall(self):
        self.tabWidget.newTab()
    #     self.updateTabNames()
    #     count = 0
    #     while True:
    #         count += 1
    #         newName = f"new {count}"
    #         tabIndex = self.findTab(newName)
    #         if tabIndex == -1:
    #             # self.tabNames.append(newName)
    #             window_view = htmlEditor(self.navMenuFileTemplate)
    #             self.tabWidget.addTab(window_view, newName)
    #             # self.updateTabNames()
    #             return
    #
    # def findTab(self, name):
    #     tabNames = []
    #     for index in range(self.tabWidget.count()):
    #         tabNames.append(self.tabWidget.tabText(index))
    #     if name in tabNames:
    #         print(tabNames.index(name), name)
    #         return tabNames.index(name)
    #     else:
    #         return -1
    #
    # def updateTabNames(self):
    #     self.tabNames = []
    #     for number in range(self.tabWidget.count()):
    #         self.tabNames.append(self.tabWidget.tabText(number))
    #     print(self.tabNames)
    #
    # def removeTab(self, index):
    #     widget = self.tabWidget.widget(index)
    #     tabName = self.tabWidget.tabText(index)
    #     self.tabNames.remove(tabName)
    #     if widget is not None:
    #         widget.deleteLater()
    #     self.tabWidget.removeTab(index)
    #     self.updateTabNames()
    #
    def openCall(self):
        self.tabWidget.openJSON()
    #     fileDir, _ = QFileDialog.getOpenFileName(self, 'Open JSON File', self.currentDirectory, "JSON files (*.json)")
    #     if fileDir:
    #         split_path = fileDir.rsplit('/', 1)
    #         self.currentDirectory = split_path[0]
    #         fileName = split_path[1]
    #         self.updateTabNames()
    #         if fileName not in self.tabNames:
    #             window_view = htmlEditor(self.navMenuFileTemplate)
    #             with open(fileDir, 'r', encoding='utf-8') as f:
    #                 data = f.read()
    #             window_view.currentFile = fileName
    #             window_view.editor.setText(data)
    #             window_view.fileName = fileName
    #             window_view.title = window_view.fileName
    #             self.setWindowTitle(window_view.title)
    #             self.tabNames.append(fileName)
    #             self.tabWidget.addTab(window_view, window_view.fileName)
    #             self.updateTabNames()
    #             self.tabWidget.setCurrentIndex(self.tabNames.index(fileName))
    #         else:
    #             self.tabWidget.setCurrentIndex(self.tabNames.index(fileName))
    #
    # def saveCall(self):
    #     if not self.window_view.currentFile:
    #         self.saveAsCall()
    #     else:
    #         with open(self.window_view.currentFile, 'w', encoding='utf-8') as f:
    #             f.write(self.window_view.editor.text())
    #         self.window_view.title = self.window_view.fileName
    #         self.setWindowTitle(self.window_view.title)
    #         self.window_view.editor.setModified(False)
    #
    # def saveAsCall(self):
    #     fileName, _ = QFileDialog.getSaveFileName(self, 'Open JSON File', self.currentDirectory, "JSON files (*.json)")
    #     if fileName:
    #         with open(fileName, 'w', encoding='utf-8') as f:
    #             f.write(self.window_view.editor.text())
    #         self.window_view.currentFile = fileName
    #         split_path = self.window_view.currentFile.rsplit('/', 1)
    #         self.currentDirectory = split_path[0]
    #         self.window_view.fileName = split_path[1]
    #         self.window_view.title = self.window_view.fileName
    #         self.setWindowTitle(self.window_view.title)
    #         self.window_view.editor.setModified(False)
    #
    # def textchanged(self):
    #     if self.window_view.editor.isModified():
    #         self.window_view.title = self.window_view.fileName + '*'
    #         self.setWindowTitle(self.window_view.title)
    #         print("changed")
    #     else:
    #         self.window_view.title = self.window_view.fileName
    #         self.setWindowTitle(self.window_view.title)
    #
    # def closeCall(self):
    #     pass


if __name__ == '__main__':
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)

    demo = App()
    demo.show()

    try:
        sys.exit(app.exec_())
    except:
        print('Closing Window...')
