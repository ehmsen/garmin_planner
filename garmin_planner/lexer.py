import ply.lex as lex
from .tokens import reserved, tokens

class WorkoutLexer:
    def __init__(self):
        self.lexer = None

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
        r'\"(?P<string>[^\"\r\n]*)\"'
        # r'\"([^\\\n]|(\\.))*?\"'
        t.value = self.lexer.lexmatch.group("string")
        # print(f"TOKEN: {t}")
        # print(f"STRING: {t.value}")
        # print(f"STRING: {t.lexer.lexmatch.group(0)}")
        # print(f"STRING: {t.lexer.lexmatch.group(1)}")
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line '{t.lexer.lineno}' pos '{t.lexer.lexpos}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()