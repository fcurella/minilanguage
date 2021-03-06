from collections import namedtuple

from unittest import TestCase

from minilanguage.lexer import Lexer
from minilanguage.grammar import Parser


class TestDSL(TestCase):
    def setUp(self):
        self.data = '''
        12 and 13 and (14 or 15) and country == "US" and not False
        '''
        MyClass = namedtuple('MyClass', ['x', 'y'])
        self.context = {
            'country': 'US',
            'user': {
                'username': 'regular_user',
                'data_bag': {
                    "payload": 'abc',
                }
            },
            'myobj': MyClass(14, 15)
        }

    def test_lexer(self):
        m = Lexer(self.context)
        m.build()
        tokens = m.test(self.data)

        t = tokens[0]
        self.assertEqual(t.type, 'NUMBER')
        self.assertEqual(t.value, 12)

        t = tokens[1]
        self.assertEqual(t.type, 'AND')

        t = tokens[2]
        self.assertEqual(t.type, 'NUMBER')
        self.assertEqual(t.value, 13)

        t = tokens[3]
        self.assertEqual(t.type, 'AND')

        t = tokens[4]
        self.assertEqual(t.type, 'LPAREN')

        t = tokens[5]
        self.assertEqual(t.type, 'NUMBER')
        self.assertEqual(t.value, 14)

        t = tokens[6]
        self.assertEqual(t.type, 'OR')

        t = tokens[7]
        self.assertEqual(t.type, 'NUMBER')
        self.assertEqual(t.value, 15)

        t = tokens[8]
        self.assertEqual(t.type, 'RPAREN')

        t = tokens[9]
        self.assertEqual(t.type, 'AND')

        t = tokens[10]
        self.assertEqual(t.type, 'ID')
        self.assertEqual(t.value, 'US')

        t = tokens[11]
        self.assertEqual(t.type, 'EQUALS')

        t = tokens[12]
        self.assertEqual(t.type, 'STRING')
        self.assertEqual(t.value, 'US')

        t = tokens[13]
        self.assertEqual(t.type, 'AND')

        t = tokens[14]
        self.assertEqual(t.type, 'NOT')

        t = tokens[15]
        self.assertEqual(t.type, 'FALSE')
        self.assertEqual(t.value, False)

        tokens = m.test('0x0F')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].value, 15)

        tokens = m.test('"a string with spaces"')
        self.assertEqual(len(tokens), 1)

        t = tokens[0]
        self.assertEqual(t.type, 'STRING')
        self.assertEqual(t.value, 'a string with spaces')

        tokens = m.test("'a string with single quotes'")
        self.assertEqual(len(tokens), 1)

        t = tokens[0]
        self.assertEqual(t.type, 'STRING')
        self.assertEqual(t.value, 'a string with single quotes')

        tokens = m.test('"a string with \'quotes\' in it"')
        self.assertEqual(len(tokens), 1)

        t = tokens[0]
        self.assertEqual(t.type, 'STRING')
        self.assertEqual(t.value, 'a string with \'quotes\' in it')

        tokens = m.test('user.username')
        self.assertEqual(len(tokens), 3)

        t = tokens[0]
        self.assertEqual(t.type, 'ID')
        self.assertEqual(t.value, self.context['user'])

        t = tokens[1]
        self.assertEqual(t.type, 'DOT')

        t = tokens[2]
        self.assertEqual(t.type, 'ID')

        tokens = m.test("user['data_bag']['payload']")
        self.assertEqual(len(tokens), 7)

        t = tokens[0]
        self.assertEqual(t.type, 'ID')
        self.assertEqual(t.value, self.context['user'])

        t = tokens[1]
        self.assertEqual(t.type, 'LBRACKET')

        t = tokens[2]
        self.assertEqual(t.type, 'STRING')

        t = tokens[3]
        self.assertEqual(t.type, 'RBRACKET')

        t = tokens[4]
        self.assertEqual(t.type, 'LBRACKET')

        t = tokens[5]
        self.assertEqual(t.type, 'STRING')

        t = tokens[6]
        self.assertEqual(t.type, 'RBRACKET')

    def test_parser(self):
        parser = Parser(self.context)
        parser.build()

        result = parser.evaluate("12 + 12")
        self.assertEqual(result, 24)

        result = parser.evaluate("12 == 12")
        self.assertEqual(result, True)

        result = parser.evaluate("12 != 12")
        self.assertEqual(result, False)

        result = parser.evaluate("12 and False")
        self.assertEqual(result, False)

        result = parser.evaluate("12 or False")
        self.assertEqual(result, 12)

        result = parser.evaluate("12 > 10")
        self.assertEqual(result, True)

        result = parser.evaluate("12 < 10")
        self.assertEqual(result, False)

        result = parser.evaluate("12 <= 12")
        self.assertEqual(result, True)

        result = parser.evaluate("12 >= 12")
        self.assertEqual(result, True)

        result = parser.evaluate("country")
        self.assertEqual(result, 'US')

        result = parser.evaluate("country == 'US'")
        self.assertEqual(result, True)

        result = parser.evaluate("myobj.x == 14")
        self.assertEqual(result, True)

        result = parser.evaluate("'cat' if myobj.x == 14 else 'dog'")
        self.assertEqual(result, 'cat')

        result = parser.evaluate("user['username']")
        self.assertEqual(result, 'regular_user')

        result = parser.evaluate("user['data_bag']['payload']")
        self.assertEqual(result, 'abc')

        result = parser.evaluate("0x0F")
        self.assertEqual(result, 15)

        result = parser.evaluate("0.5")
        self.assertEqual(result, 0.5)

        result = parser.evaluate("2 + 0.5")
        self.assertEqual(result, 2.5)

        result = parser.evaluate("'a', 'b'")
        self.assertEqual(result, ('a', 'b',))

        result = parser.evaluate("user.get('missing_key')")
        self.assertEqual(result, None)

        result = parser.evaluate("user.get('missing_key', 'default')")
        self.assertEqual(result, 'default')

        result = parser.evaluate("t if a else b", {"a": False, "b": 'x', "t": "y"})
        self.assertEqual(result, 'x')

        result = parser.evaluate("t if a else b", {"a": True, "b": 'x', "t": "y"})
        self.assertEqual(result, 'y')

        result = parser.evaluate("if a then t else b", {"a": False, "b": 'x', "t": "y"})
        self.assertEqual(result, 'x')

        result = parser.evaluate("if a then t else b", {"a": True, "b": 'x', "t": "y"})
        self.assertEqual(result, 'y')
