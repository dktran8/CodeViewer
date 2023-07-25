import json
import pandas as pd
import re
from dbfread import DBF
from pandas import DataFrame
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QUrl
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QStackedLayout, \
    QTextBrowser, QFileDialog, QRadioButton, QSplitter, QFrame, QAbstractItemView, QTableWidget, QTableWidgetItem, \
    QTableView
from scin_editor import Editor
from PandasModel import pandasModel
from tablewidgetdragrows import ReorderTableView, ReorderTableModel


class htmlEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.htmlType = "NavMenuTemplate.html"
        self.desFilePath = ""
        self.desFileName = ""
        self.desList = []
        # self.currentFile = None
        # self.fileName = 'New File'
        # self.title = self.fileName
        self.initUI()
        # self.editor.textChanged.connect(self.textchanged)

    def initUI(self):
        # Buttons
        self.viewDesBtn = QPushButton("Descriptors")
        self.viewDesBtn.setCheckable(True)
        self.viewDesBtn.clicked.connect(self.see_des)
        self.viewLinkBtn = QPushButton("Links")
        self.viewLinkBtn.setCheckable(True)
        self.viewLinkBtn.clicked.connect(self.see_link)
        self.desFileBtn = QPushButton("Choose Descriptor File...")
        self.desFileBtn.clicked.connect(self.openDesFile)
        self.desLoadBtn = QPushButton("Load Descriptors")
        self.desLoadBtn.clicked.connect(self.loadDes)
        # self.sourceBtn = QPushButton("Source")
        # self.sourceBtn.setCheckable(True)
        # self.sourceBtn.setChecked(True)
        # self.sourceBtn.clicked.connect(self.see_source)
        # self.viewBtn = QPushButton("View")
        # self.viewBtn.setCheckable(True)
        # self.viewBtn.setChecked(True)
        # self.viewBtn.clicked.connect(self.see_view)
        self.renumberButton = QPushButton("Renumber")
        self.renumberButton.clicked.connect(self.renumber)
        self.navBtn = QRadioButton("Nav Menu")
        self.navBtn.setChecked(True)
        self.navBtn.toggled.connect(self.setHtmlType)
        self.accordionBtn = QRadioButton("Accordion")
        self.accordionBtn.toggled.connect(self.setHtmlType)

        # Spacers
        self.spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # Text Boxes
        self.desFileBox = QLineEdit()
        self.desFileBox.setReadOnly(True)
        self.desFileBox.setPlaceholderText("Descriptor File (*.dbf)")
        self.devIdEdit = QLineEdit()
        self.devIdEdit.setPlaceholderText("Device ID...")

        # Text Browser
        self.textBrowser = QTextBrowser()
        self.textBrowser.setMaximumHeight(100)

        # List Widgets
        self.desListWidget = QListWidget()
        self.desListWidget.setFixedWidth(300)
        self.desListWidget.setSortingEnabled(True)
        self.desListWidget.setDragDropMode(QAbstractItemView.DragDrop)

        # Descriptor Table
        self.desTableView = ReorderTableView(self)
        # self.desTableView = QTableView()
        # self.desTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.desTableView.setSortingEnabled(True)
        self.desTableView.setMinimumWidth(400)

        # Editor
        self.editor = Editor()
        self.editor.setMinimumWidth(500)

        # HTML View
        self.html_view = QtWebEngineWidgets.QWebEngineView()
        self.html_view.setMinimumWidth(360)
        self.html_view.setMaximumWidth(1550)
        self.setHtmlType()

        # Outer Layout
        outerLayout = QVBoxLayout()

        # Top Layout
        topLayout = QHBoxLayout()

        # Descriptor Layout
        self.descriptorFrame = QFrame()
        descriptorLayout = QVBoxLayout()
        descriptorLayout.addWidget(self.desFileBox)
        descriptorLayout.addWidget(self.desFileBtn)
        descriptorLayout.addWidget(self.devIdEdit)
        descriptorLayout.addWidget(self.desLoadBtn)
        # descriptorLayout.addWidget(self.desTableView)
        tableLayout = QHBoxLayout()
        tableLayout.addWidget(self.desTableView)
        descriptorLayout.addLayout(tableLayout)
        self.descriptorFrame.setLayout(descriptorLayout)
        self.descriptorFrame.hide()

        # Stacked Layout
        self.splitter = QSplitter(Qt.Horizontal)
        # self.stackedLayout = QStackedLayout()
        # self.stackedLayout.addWidget(self.editor)
        # self.stackedLayout.addWidget(self.html_view)
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.html_view)

        # View Layout
        viewLayout = QVBoxLayout()
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(self.viewDesBtn)
        tabLayout.addWidget(self.viewLinkBtn)
        # tabLayout.addWidget(self.sourceBtn)
        # tabLayout.addWidget(self.viewBtn)
        tabLayout.addWidget(self.renumberButton)
        tabLayout.addSpacerItem(self.spacerItem)
        tabLayout.addWidget(self.navBtn)
        tabLayout.addWidget(self.accordionBtn)
        viewLayout.addLayout(tabLayout)
        # viewLayout.addLayout(self.stackedLayout)
        viewLayout.addWidget(self.splitter)
        viewLayout.addWidget(self.textBrowser)

        # Arrange Layouts
        topLayout.addWidget(self.descriptorFrame, 0)
        topLayout.addLayout(viewLayout, 10)
        outerLayout.addLayout(topLayout)
        self.setLayout(outerLayout)

    class repl:
        def __init__(self):
            self.called = 0

        def __call__(self, match):
            self.called += 1
            return match.group(1)+str(self.called)+match.group(3)

    def renumber(self):
        json_text = self.editor.text()
        if json_text:
            new_text = re.sub("({R?)(\d+)(})", self.repl(), json_text)
            self.editor.SendScintilla(self.editor.SCI_SETTEXT, new_text.encode())

    def openDesFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open Descriptor File', self.desFilePath, "DBF files (*.dbf)")
        if filePath:
            split_path = filePath.rsplit('/', 1)
            self.desFileName = split_path[1]
            self.desFilePath = filePath
            self.desFileBox.setText(self.desFileName)

    def loadDes(self):
        # self.desTableWidget.clear()
        if self.desFilePath:
            if self.devIdEdit.text():
                device_id = int(self.devIdEdit.text())
            else:
                device_id = 0
            dbf = DBF(self.desFilePath)
            frame = DataFrame(iter(dbf))
            dflist = frame.values.tolist()
            if device_id:
                newFrame = frame[frame['DEVICEID'] == device_id]
            else:
                newFrame = frame
            print(dflist)
            model = ReorderTableModel(dflist)
            # proxymodel = QSortFilterProxyModel()
            # proxymodel.setSourceModel(model)
            try:
                self.desTableView.setModel(model)
            except Exception as e:
                print(e)
        # if self.desFilePath:
        #     dbf = DBF(self.desFilePath)
        #     frame = DataFrame(iter(dbf))
        #     print(frame)
        # else:
        #     self.textBrowser.setText("Choose a Descriptor File")

    def setHtmlType(self):
        if self.navBtn.isChecked() == True:
            self.htmlType = "NavMenuTemplate.html"
            self.html_view.setMinimumWidth(380)
            self.html_view.setMaximumWidth(380)
        if self.accordionBtn.isChecked() == True:
            self.htmlType = "AccordionTemplate.html"
            self.html_view.setMinimumWidth(360)
            self.html_view.setMaximumWidth(1700)
        self.renderHtml()

    def accordion_section(self, json_dict):
        section_text = ""
        try:
            dfSections = pd.DataFrame.from_dict(json_dict['Sections'])
            dfSections['HTMLString'] = dfSections['Content'].apply(''.join)
            for row in dfSections.itertuples():
                section_text += f"""
                    <div class="acc-item"><div class="label">{row.Title}</div><div class="acc-content-wrapper">{row.HTMLString}</div></div>"""
            return section_text
        except:
            return section_text

    def accordion_link(self, json_dict):
        link_text = ""
        try:
            dfLinks = pd.DataFrame.from_dict(json_dict['Links'])
            if dfLinks['Links'][0]:
                link_text = f"""<div id="extraLinks">
                        <span class="textlink-holder">{dfLinks['Links'][0]}</span>
                    </div>"""
            return link_text
        except:
            return link_text

    def see_des(self):
        if self.viewDesBtn.isChecked():
            self.descriptorFrame.show()
        else:
            self.descriptorFrame.hide()

    def see_link(self):
        pass

    def see_source(self):
        if self.sourceBtn.isChecked():
            self.editor.show()
        else:
            self.editor.hide()
        # self.stackedLayout.setCurrentIndex(0)

    def see_view(self):
        # self.html_view.setHtml("")
        self.renderHtml()
        if self.viewBtn.isChecked():
            self.html_view.show()
        else:
            self.html_view.hide()
        # self.stackedLayout.setCurrentIndex(1)

    def renderHtml(self):
        self.textBrowser.setText("")
        htmlText = self.htmlFromText()
        self.html_view.setHtml(htmlText)
        # demoURL = QUrl.fromLocalFile("C:/Users/TimothyBaker/PycharmProjects/SourceViewer/animLoaderDemo.html")
        # f = open("animLoaderDemo.html", 'r', encoding='utf-8')
        # data = f.read()
        # print(data)
        # self.html_view.setHtml(data)
        # self.html_view.load(demoURL)

    def htmlFromText(self):
        try:
            json_text = self.editor.text()
            if json_text:
                json_dict = json.loads(json_text)

                var_read_match = re.compile("{R(.*?)(:.*?)?}")
                var_edit_match = re.compile("{([^R].*?)(:.*?)?}")

                links_html = self.accordion_link(json_dict)
                sections_html = self.accordion_section(json_dict)

                sections_html = var_edit_match.sub(r'<span title="\1\2" class="value editable ">0.0</span>', sections_html)
                sections_html = var_read_match.sub(r'<span title="\1\2" class="value ">0.0</span>', sections_html)
            else:
                links_html = ""
                sections_html = ""
            f = open(self.htmlType, 'r', encoding='utf-8')
            data = f.read()
            f.close()
            html_text = data.replace('$links', links_html).replace('$sections', sections_html)
        except ValueError as e:
            self.textBrowser.setText(str(e))
            html_text = ""
        return html_text
