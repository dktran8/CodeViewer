from PyQt5.QtGui import *
from PyQt5.Qsci import *


class JSsubLexer(QsciLexerJSON):
    def __init__(self, parent):
        super(JSsubLexer, self).__init__(parent)
