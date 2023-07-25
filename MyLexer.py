from PyQt5.QtGui import *
from PyQt5.Qsci import *
import re
import lark
from lark import Lark


class MyLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(MyLexer, self).__init__(parent)
        # self.setAutoIndentStyle(QsciScintilla.AiOpening | QsciScintilla.AiClosing)
        self.create_parser()
        self.create_styles()

    def create_styles(self):
        cream = QColor("#d8dee9")
        red = QColor("#a74242")
        blue = QColor("#60b4b4")
        green = QColor("#99b673")
        grey = QColor("#303841")
        orange = QColor("#f9ae57")
        purple = QColor("#b595b6")

        styles = {
            0: cream,
            1: red,
            2: blue,
            3: green,
            4: orange,
            5: purple,
        }

        for style, color in styles.items():
            self.setColor(color, style)
            self.setPaper(grey, style)
            self.setFont(self.parent().font(), style)

        # self.token_styles = {
        #     "OPEN_TAG": 2,
        #     "WORD": 1,
        # }
        self.token_styles = {
            "BEGIN_OPEN_TAG": 2,
            "OPEN_TAG": 2,
            "CLOSE_TAG": 2,
            "END_OPEN_TAG": 2,
            "TAG_STRING": 1,
            "WORD": 0,
        }

    def create_parser(self):
        grammar = '''
            start: OPEN_TAG
            anons: ":" "{" "}" "," "[" "]"
            OPEN_TAG: /<(?!(\s)+)/
            TAG_STRING: /(?<=<)\w+/
            TRUE: "true"
            FALSE: "false"
            NULL: "NULL"
            %import common.ESCAPED_STRING -> STRING
            %import common.SIGNED_NUMBER  -> NUMBER
            %import common.WS
            %ignore WS
        '''

        self.lark = Lark(grammar, parser=None, lexer='basic')
        # All tokens: print([t.name for t in self.lark.parser.lexer.tokens])

    def defaultPaper(self, style):
        return QColor("#303841")

    def language(self):
        return "Json"

    def description(self, style):
        return {v: k for k, v in self.token_styles.items()}.get(style, "")

    def styleText(self, start, end):
        self.startStyling(start)
        text = self.parent().text()[start:end]
        last_pos = 0

        try:
            for token in self.lark.lex(text):
                print(token, token.type)
                ws_len = token.start_pos - last_pos
                if ws_len:
                    self.setStyling(ws_len, 0)    # whitespace

                token_len = len(bytearray(token, "utf-8"))
                self.setStyling(
                    token_len, self.token_styles.get(token.type, 0))

                last_pos = token.start_pos + token_len
        except Exception as e:
            print(e)
