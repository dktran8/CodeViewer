from PyQt5.Qsci import *
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from MyLexer import MyLexer
from JSONSubclass import JSsubLexer


class Editor(QsciScintilla):
    def __init__(self):
        super().__init__()
        font = self.font()
        font.setFamily('Consolas')
        font.setPointSize(12)
        self.setFont(font)
        self.setPaper(QColor("#303841"))
        self.setMarginsBackgroundColor(QColor("#303841"))
        self.setMarginsForegroundColor(QColor("#848b95"))
        self.setSelectionBackgroundColor(QColor("#4c5863"))

        # create a "Lexer", which is what allows syntax highlighting
        # within the editor; the following is the class for python
        # syntax, but there are other classes for different languages
        lexer = JSsubLexer(self)
        # lexer = MyLexer(self)
        # lexer.setAutoIndentStyle(QsciScintilla.AiOpening | QsciScintilla.AiClosing)
        # lexer.setDefaultFont(font)
        self.setLexer(lexer)
        # self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        # self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setUtf8(True)
        self.setTabWidth(4)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setIndentationGuidesBackgroundColor(QColor("#49515a"))
        self.setIndentationGuidesForegroundColor(QColor("#303841"))
        # Enable and set the caret line background color to slightly transparent blue
        # self.setCaretLineVisible(True)
        # caret_bg_color = QtGui.QColor("#1f0000ff")
        # self.setCaretLineBackgroundColor(caret_bg_color)
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "00000")
