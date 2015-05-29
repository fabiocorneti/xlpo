#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import unittest
from xlpo.readers import POFileTranslationsReader
from tests.base import BaseTestCase


class TestPOTranslationsReader(BaseTestCase):

    def test_valid_files(self):
        po_file = os.path.join(self.FILES_DIR, 'messages.po')
        reader = POFileTranslationsReader(po_file)
        self.assertEqual(len(reader), 2)
        self.assertEqual(reader[0].message, 'Hello')
        self.assertEqual(reader[0].translation, 'Ciao')
        self.assertEqual(reader[1].message, 'Yes')
        self.assertEqual(reader[1].translation, 'Sì')

    def test_invalid_files(self):
        invalid_file = os.path.join(self.FILES_DIR, 'not_a_po.po')
        with self.assertRaises(IOError):
            reader = POFileTranslationsReader(invalid_file)
            reader.read()

    def test_invalid_filenames(self):
        with self.assertRaises(Exception):
            POFileTranslationsReader(None)
        with self.assertRaises(IOError):
            reader = POFileTranslationsReader('not_here')
            reader.read()
        with self.assertRaises(IOError):
            reader = POFileTranslationsReader(self.FILES_DIR)
            reader.read()

    def test_caching(self):
        po_file = os.path.join(self.FILES_DIR, 'messages.po')
        reader = POFileTranslationsReader(po_file)
        reader.read()
        t1 = reader._translations
        self.assertIsNotNone(t1)
        self.assertEqual(len(reader), 2)
        reader.read()
        t2 = reader._translations
        self.assertIs(t1, t2)


if __name__ == '__main__':
    unittest.main()
