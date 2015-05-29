#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from xlpo import Translation

from xlpo.readers import TranslationsReader
from xlpo.writers import TranslationsWriter
import os
import unittest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.FILES_DIR = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'files')


class TestReader(TranslationsReader):

    def __init__(self, translations):
        super(TestReader, self).__init__()
        self._translations = translations

    def read(self):
        pass


class TestBaseClasses(BaseTestCase):

    def test_base_classes(self):
        reader = TranslationsReader()
        self.assertRaises(NotImplementedError, lambda: reader.metadata)

        writer = TranslationsWriter()
        self.assertRaises(NotImplementedError, lambda: writer.write([]))

    def test_equality(self):
        r1 = TestReader([
            Translation('Hello', 'Ciao')
        ])
        r2 = TestReader([
            Translation('Hello', 'Ciao'),
            Translation('Yes', 'Sì')
        ])
        self.assertNotEqual(r1, r2)

    def test_in(self):
        reader = TestReader([
            Translation('Hello', 'Ciao'),
            Translation('Yes', 'Sì', context='frontend'),
            Translation('Yes', 'Certo', context='backend')
        ])
        self.assertTrue(Translation('Hello', 'Ciao') in reader)
        self.assertFalse(Translation('Yes', 'Sì') in reader)
        self.assertTrue(Translation('Yes', 'Sì', context='frontend') in reader)
        self.assertTrue('Yes' in reader)

    def test_find(self):
        reader = TestReader([
            Translation('Hello', 'Ciao'),
            Translation('Yes', 'Sì', context='frontend'),
            Translation('Yes', 'Certo', context='backend')
        ])
        self.assertEqual(len(reader.find('Hello')), 1)
        self.assertEqual(len(reader.find('Yes')), 2)
        self.assertEqual(len(reader.find('Yes', context='frontend')), 1)
        self.assertEqual(len(reader.find('Yes', context='api')), 0)


if __name__ == '__main__':
    unittest.main()
