from ply import lex


class FeatureLexer(object):

    reserved = {
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        "in": 'IN',
        "if": 'IF',
        "then": 'THEN',
        "else": 'ELSE',
    }

    tokens = (
        'HEX',
        'FLOAT',
        'NUMBER',
        'LPAREN',
        'RPAREN',
        'EQUALS',
        'NOT_EQUALS',
        'GT',
        'LT',
        'GTE',
        'LTE',
        'COMMENT',
        'STRING',
        'ID',
        'TRUE',
        'FALSE',
        'DOT',
        'COMMA',
    ) + tuple(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_EQUALS = r'=='
    t_NOT_EQUALS = r'!='
    t_GT = r'>'
    t_LT = r'<'
    t_GTE = r'>='
    t_LTE = r'<='

    t_ignore = ' \t'

    literals = '+-*/'

    def __init__(self, context=None):
        if context is None:
            context = {}
        self.context = context

    def symbol_lookup(self, id_):
        return self.context.get(id_, id_)

    def t_HEX(self, t):
        r'0x[0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        pass
        # No return value. Token discarded

    def t_DOT(self, t):
        r'\.'
        return t

    def t_COMMA(self, t):
        r'\,'
        return t

    def t_TRUE(self, t):
        r'True'
        t.value = True
        return t

    def t_FALSE(self, t):
        r'False'
        t.value = False
        return t

    def t_STRING(self, t):
        r"(?P<quote>['\"]).*?(?P=quote)"
        t.value = t.value[1:-1]
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')    # Check for reserved words
        t.value = self.symbol_lookup(t.value)
        return t

    def t_IF(self, t):
        r'if'
        return t

    def t_THEN(self, t):
        r'then'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        # tok.type, tok.value, tok.lineno, tok.lexpos
        return [tok for tok in self.lexer]
