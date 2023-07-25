from PyQt5.QtGui import *
from PyQt5.Qsci import *


class CombinedLex(QsciLexerCustom):
    def __init__(self, parent):
        super(CombinedLex, self).__init__(parent)
        jsonLex = QsciLexerJSON()
        htmlLex = QsciLexerHTML()