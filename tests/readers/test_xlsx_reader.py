#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from xlpo.readers import XLSXTranslationsReader
from tests.base import BaseTestCase
import os
import unittest


class TestXLSXTranslationsReader(BaseTestCase):

    def test_valid_files(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'en_it__noheaders.xlsx')
        reader = XLSXTranslationsReader(xlsx_file)
        self.assertEqual(len(reader), 2)
        self.assertEqual(reader[0].message, 'Hello')
        self.assertEqual(reader[0].translation, 'Ciao')
        self.assertEqual(reader[1].message, 'Yes')
        self.assertEqual(reader[1].translation, 'Sì')

    def test_invalid_files(self):
        invalid_file = os.path.join(self.FILES_DIR, 'not_an_xlsx.xlsx')
        with self.assertRaises(IOError):
            reader = XLSXTranslationsReader(invalid_file)
            reader.read()
        invalid_file = os.path.join(self.FILES_DIR, 'not_an_xlsx.txt')
        with self.assertRaises(IOError):
            reader = XLSXTranslationsReader(invalid_file)
            reader.read()

    def test_duplicate_messages(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'duplicates.xlsx')
        reader = XLSXTranslationsReader(xlsx_file)
        with self.assertRaises(Exception):
            reader.read()

    def test_invalid_filenames(self):
        with self.assertRaises(Exception):
            XLSXTranslationsReader(None)
        with self.assertRaises(IOError):
            reader = XLSXTranslationsReader('not_here')
            reader.read()
        with self.assertRaises(IOError):
            reader = XLSXTranslationsReader(self.FILES_DIR)
            reader.read()

    def test_invalid_indexes(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'en_it__noheaders.xlsx')

        with self.assertRaises(Exception):
            XLSXTranslationsReader(xlsx_file, sheet=-1)

        with self.assertRaises(Exception):
            XLSXTranslationsReader(xlsx_file, sheet='a')

        reader = XLSXTranslationsReader(xlsx_file, sheet=1)
        with self.assertRaises(IOError):
            reader.read()

        with self.assertRaises(Exception):
            XLSXTranslationsReader(xlsx_file, messages_col=-1)

        with self.assertRaises(Exception):
            XLSXTranslationsReader(xlsx_file, messages_col='a')

        reader = XLSXTranslationsReader(xlsx_file, messages_col=3)
        with self.assertRaises(IOError):
            reader.read()

        with self.assertRaises(Exception):
            XLSXTranslationsReader(xlsx_file, translations_col=-1)

        with self.assertRaises(Exception):
            XLSXTranslationsReader(xlsx_file, translations_col='a')

        reader = XLSXTranslationsReader(xlsx_file, translations_col=3)
        with self.assertRaises(IOError):
            reader.read()

    def test_caching(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'en_it__noheaders.xlsx')
        reader = XLSXTranslationsReader(xlsx_file)
        reader.read()
        self.assertIsNotNone(reader._translations)
        t1 = reader._translations
        self.assertEqual(len(t1), 2)
        reader.read()
        t2 = reader._translations
        self.assertIs(t1, t2)


if __name__ == '__main__':
    unittest.main()
