Minilanguage
============
*A minimal DSL for Python*

.. image:: https://travis-ci.org/fcurella/minilanguage.svg

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

        parser = FeatureParser()
        parser.build()

        parser.evaluate("2 + 0.5", context)
        # 2.5

        parser.evaluate("12 + 12", context)
        # 24

        parser.evaluate("12 == 12", context)
        # True

        parser.evaluate("12 != 12", context)
        # False

        parser.evaluate("12 and False", context)
        # False

        parser.evaluate("12 or False", context)
        # 12

        parser.evaluate("12 > 10", context)
        # True

        parser.evaluate("12 < 10", context)
        # False

        parser.evaluate("12 <= 12", context)
        # True

        parser.evaluate("12 >= 12", context)
        # True

        parser.evaluate("country", context)
        # 'US'

        parser.evaluate("country == 'US'", context)
        # True

        parser.evaluate("user.username", context)
        # 'regular_user'

        parser.evaluate("'a', 'b'", context)
        # tuple('a', 'b')

        parser.evaluate("user.data_bag.payload", context)
        # 'abc'

        parser.evaluate("12 if False else 14", context)
        # 14

License
-------

This software is released under the MIT License.
