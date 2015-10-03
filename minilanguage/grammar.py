from ply import yacc


from .lexer import FeatureLexer


class FeatureParser(object):

    precedence = (
        ('left', 'COMMA', 'DOT',),
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def __init__(self, context=None):
        if context is None:
            context = {}
        self.context = context
        self.lexer = FeatureLexer(context)

    def p_expression_comment(self, p):
        'expression : expression COMMENT'
        p[0] = p[1]

    def p_expression_plus(self, p):
        '''expression : expression '+' term'''
        p[0] = p[1] + p[3]

    def p_expression_minus(self, p):
        '''expression : expression '-' term'''
        p[0] = p[1] - p[3]

    def p_expression_and(self, p):
        '''expression : expression AND term'''
        p[0] = p[1] and p[3]

    def p_expression_or(self, p):
        '''expression : expression OR term'''
        p[0] = p[1] or p[3]

    def p_expression_equals(self, p):
        '''expression : expression EQUALS term'''
        p[0] = p[1] == p[3]

    def p_expression_not_equals(self, p):
        '''expression : expression NOT_EQUALS term'''
        p[0] = p[1] != p[3]

    def p_expression_gt(self, p):
        '''expression : expression GT term'''
        p[0] = p[1] > p[3]

    def p_expression_lt(self, p):
        '''expression : expression LT term'''
        p[0] = p[1] < p[3]

    def p_expression_gte(self, p):
        '''expression : expression GTE term'''
        p[0] = p[1] >= p[3]

    def p_expression_lte(self, p):
        '''expression : expression LTE term'''
        p[0] = p[1] <= p[3]

    def p_expression_in(self, p):
        '''expression : expression IN term'''
        p[0] = p[1] in p[3]

    def p_expression_if_else(self, p):
        '''expression : expression IF term ELSE term'''
        p[0] = p[1] if p[3] else p[5]

    def p_expression_if_then_else(self, p):
        '''expression : IF expression THEN term ELSE term'''
        p[0] = p[4] if p[2] else p[6]

    def p_expression_times(self, p):
        '''expression : expression '*' term'''
        p[0] = p[1] * p[3]

    def p_expression_div(self, p):
        '''expression : expression '/' term'''
        p[0] = p[1] / p[3]

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_tuple(self, p):
        'tuple : term COMMA term'
        p[0] = (p[1], p[3])

    def p_term_tuple(self, p):
        'term : tuple'
        p[0] = p[1]

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_term_not(self, p):
        'term : NOT factor'
        p[0] = not p[2]

    def p_factor_method_args(self, p):
        'factor : factor DOT ID LPAREN tuple RPAREN'
        src = p[1]
        attr = p[3]
        arg = p[5]

        p[0] = getattr(src, attr)(*arg)

    def p_factor_method(self, p):
        'factor : factor DOT ID LPAREN factor RPAREN'
        src = p[1]
        attr = p[3]
        arg = p[5]

        p[0] = getattr(src, attr)(arg)

    def p_factor_dot(self, p):
        'factor : factor DOT factor'
        src = p[1]
        attr = p[3]

        try:
            p[0] = src[attr]
        except KeyError:
            p[0] = getattr(src, attr)

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_factor_hex(self, p):
        'factor : HEX'
        p[0] = p[1]

    def p_factor_float(self, p):
        'factor : FLOAT'
        p[0] = p[1]

    def p_factor_num(self, p):
        'factor : NUMBER'
        p[0] = p[1]

    def p_factor_id(self, p):
        'factor : ID'
        p[0] = p[1]

    def p_factor_string(self, p):
        'factor : STRING'
        p[0] = p[1]

    def p_factor_true(self, p):
        'factor : TRUE'
        p[0] = p[1]

    def p_factor_false(self, p):
        'factor : FALSE'
        p[0] = p[1]

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")

    def build(self, **kwargs):
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def evaluate(self, data, context=None):
        if context is None:
            context = self.context
        self.lexer.context = context
        return self.parser.parse(data)
