import ply.lex as lex
import logging
from .tokens import reserved, tokens

logger = logging.getLogger(__name__)

class WDLLexer:
    # List of token names
    tokens = tokens

    # Regular expression rules for simple tokens
    # https://pythex.org/
    t_LBRACKET  = r'\{'
    t_RBRACKET  = r'\}'
    t_HYPHEN    = r'-'
    t_AT        = r'@'
    # t_TIMES     = r'\*'

    # Ignored characters
    t_ignore = ' \t'

    def __init__(self):
        self.lexer = None
        self.input = None

    def t_TIME(self, t):
        r'(?:(\d+):)?([0-5]?\d):([0-5]?\d)'
        t.value = self.lexer.lexmatch.group(2, 3, 4)
        t.value = tuple([int(v) if v is not None else 0 for v in t.value])
        return t

    def t_FLOAT(self, t):
        r'\d+(?:\.\d{0,2})|\.\d{1,2}'
        t.value = self.lexer.lexmatch.group(0)
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_DATE_ISO8601(self, t):
        r'\d{4}-\d{2}-\d{2}'
        t.value = self.lexer.lexmatch.group(0)
        return t

    def t_WEEKDAY(self, t):
        r'(?i:monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)'
        t.value = self.lexer.lexmatch.group(0)
        return t

    def t_ID(self, t):
        r'((\"|\')(?P<long_name>[a-zA-Z0-9_ ]+)(\"|\')|(?P<short_name>[a-zA-Z0-9_]+))(?P<times>\s*\*)?'
        # print(f"BEFORE TOKEN: {t}")
        if t.value in reserved:
            t.type = reserved.get(t.value, 'ID')
        else:
            try:
                t.value = int(self.lexer.lexmatch.group('short_name'))
            except (ValueError, TypeError):
                t.value = self.lexer.lexmatch.group('long_name') or self.lexer.lexmatch.group('short_name')
            else:
                if self.lexer.lexmatch.group('times'):
                    t.type = 'INT_REP'
                else:
                    t.type = 'INT'
        # print(f"AFTER TOKEN: {t}")
        return t

    def t_STRING(self, t):
        r'\"(?P<string>[^\"\r\n\\]*(?:\\.[^\"\r\n\\]*)*)\"'
        # r'\"(?P<string>[^\"\r\n]*)\"'
        t.value = self.lexer.lexmatch.group("string")
        logger.debug(f"String token: {t.value}")
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        # FIXME - this is not working since the lexer is not aware of the input
        column = t.lexpos - self.input.rfind('\n', 0, t.lexpos)
        logger.error(f"Illegal character at {t.linepos}:{t.column}: {t.value[0]}")
        t.lexer.skip(1)

    # def t_error(self, t):
    #     logger.error(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, pos {t.lexer.lexpos}")
    #     t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # def input(self, input):
    #     print(f"INPUT: {input}")
    #     self.input = input
    #     self.lexer.input(input)

    # def token(self):
    #     t = self.lexer.token()
    #     t.column = t.lexpos - self.input.rfind('\n', 0, t.lexpos)
    #     return t