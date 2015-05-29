#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from xlpo import Translation
import six
import unittest


class TranslationTestCase(unittest.TestCase):

    def test_equality(self):
        t1 = Translation('Hello')
        t2 = Translation('Hello')
        self.assertEqual(t1, t2)
        t1 = Translation('Hello', 'Ciao')
        t2 = Translation('Hello', 'Ciao')
        self.assertEqual(t1, t2)
        t1 = Translation('Hello', 'Ciao', context='frontend')
        t2 = Translation('Hello', 'Ciao', context='frontend')
        self.assertEqual(t1, t2)
        t1 = Translation('Hello', 'Ciao', context='frontend',
                         comment='A comment')
        t2 = Translation('Hello', 'Ciao', context='frontend',
                         comment='Another comment')
        self.assertEqual(t1, t2)
        t1 = Translation('Hello', 'Ciao')
        t2 = Translation('Hello', 'Salve')
        self.assertNotEqual(t1, t2)
        t1 = Translation('Hello', 'Ciao', context='frontend')
        t2 = Translation('Hello', 'Ciao', context='backend')
        self.assertNotEqual(t1, t2)

    def test_str(self):
        t = Translation('Sì')
        self.assertEqual(six.text_type(t), 'Sì')


if __name__ == '__main__':
    unittest.main()
