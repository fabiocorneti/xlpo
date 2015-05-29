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

        reader = XLSXTranslationsReader(invalid_file)
        self.assertRaises(IOError, lambda: reader.read())

        invalid_file = os.path.join(self.FILES_DIR, 'not_an_xlsx.txt')
        reader = XLSXTranslationsReader(invalid_file)
        self.assertRaises(IOError, lambda: reader.read())

    def test_duplicate_messages(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'duplicates.xlsx')
        reader = XLSXTranslationsReader(xlsx_file)
        self.assertRaises(Exception, lambda: reader.read())

    def test_invalid_filenames(self):
        self.assertRaises(Exception, lambda: XLSXTranslationsReader(None))

        reader = XLSXTranslationsReader('not_here')
        self.assertRaises(IOError, lambda: reader.read())

        reader = XLSXTranslationsReader(self.FILES_DIR)
        self.assertRaises(IOError, lambda: reader.read())

    def test_invalid_indexes(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'en_it__noheaders.xlsx')

        self.assertRaises(Exception,
                          lambda: XLSXTranslationsReader(xlsx_file, sheet=-1))

        self.assertRaises(Exception,
                          lambda: XLSXTranslationsReader(xlsx_file, sheet='a'))

        reader = XLSXTranslationsReader(xlsx_file, sheet=1)
        self.assertRaises(IOError, lambda: reader.read())

        self.assertRaises(Exception,
                          lambda: XLSXTranslationsReader(xlsx_file,
                                                         messages_col=-1))

        self.assertRaises(Exception,
                          lambda: XLSXTranslationsReader(xlsx_file,
                                                         messages_col='a'))

        reader = XLSXTranslationsReader(xlsx_file, messages_col=3)
        self.assertRaises(IOError, lambda: reader.read())

        self.assertRaises(Exception,
                               lambda: XLSXTranslationsReader(
                                       xlsx_file,
                                       translations_col=-1))

        self.assertRaises(Exception,
                          lambda: XLSXTranslationsReader(xlsx_file,
                                                         translations_col='a'))

        reader = XLSXTranslationsReader(xlsx_file, translations_col=3)
        self.assertRaises(IOError, lambda: reader.read())

    def test_caching(self):
        xlsx_file = os.path.join(self.FILES_DIR, 'en_it__noheaders.xlsx')
        reader = XLSXTranslationsReader(xlsx_file)
        reader.read()
        self.assertTrue(reader._translations is not None)
        t1 = reader._translations
        self.assertEqual(len(t1), 2)
        reader.read()
        t2 = reader._translations
        self.assertTrue(t1 is t2)


if __name__ == '__main__':
    unittest.main()
