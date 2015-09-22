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

        parser = FeatureParser(context)
        parser.build()

        parser.evaluate("12 + 12")
        # 24

        parser.evaluate("12 == 12")
        # True

        parser.evaluate("12 != 12")
        # False

        parser.evaluate("12 and False")
        # False

        parser.evaluate("12 or False")
        # 12

        parser.evaluate("12 > 10")
        # True

        parser.evaluate("12 < 10")
        # False

        parser.evaluate("12 <= 12")
        # True

        parser.evaluate("12 >= 12")
        # True

        parser.evaluate("country")
        # 'US'

        parser.evaluate("country == 'US'")
        # True

        parser.evaluate("user.username")
        # 'regular_user'

        parser.evaluate("user.data_bag.payload")
        # 'abc'

License
-------

This software is released under the MIT License.
