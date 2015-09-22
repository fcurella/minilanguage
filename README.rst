Minilanguage
============
*A minimal DSL for Python*

``Minilanguage`` is a minimal DSL for Python written with `Ply <http://www.dabeaz.com/ply/>`_.

Is it intended to be a starting point for writing more specific DSLs.

Currently, it only implements simple boolean logic and objects/strings evaluation.

Example
-------
::

        from minilanguage.grammar import FeatureParser

        context = {
            'country': 'US',
            'user': {
                'username': 'regular_user',
                'data_bag': {
                    "payload": 'abc',
                }
            }
        }

        parser = FeatureParser(context)
        parser.build()

        parser.test("12 + 12")
        # 24

        parser.test("12 == 12")
        # True

        parser.test("12 != 12")
        # False

        parser.test("12 and False")
        # False

        parser.test("12 or False")
        # 12

        parser.test("12 > 10")
        # True

        parser.test("12 < 10")
        # False

        parser.test("12 <= 12")
        # True

        parser.test("12 >= 12")
        # True

        parser.test("country")
        # 'US'

        parser.test("country == 'US'")
        # True

        parser.test("user.username")
        # 'regular_user'

        parser.test("user.data_bag.payload")
        # 'abc'

License
-------

This software is released under the MIT License.
