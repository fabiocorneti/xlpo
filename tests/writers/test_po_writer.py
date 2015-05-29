#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from tests.base import BaseTestCase
from xlpo import Translation
from xlpo.readers import POFileTranslationsReader
from xlpo.writers import POFileTranslationsWriter
import os
import shutil
import tempfile
import unittest


class TestPOTranslationsWriter(BaseTestCase):
    def test_create(self):
        source_reader = POFileTranslationsReader(os.path.join(self.FILES_DIR,
                                                              'messages.po'))
        tmp_file = tempfile.NamedTemporaryFile('r')
        writer = POFileTranslationsWriter(tmp_file.name)
        writer.write(source_reader)
        dest_reader = POFileTranslationsReader(tmp_file.name)
        self.assertEqual(source_reader, dest_reader)
        tmp_file.close()

    def test_invalid_filenames(self):
        translations = [
            Translation('Hello', 'Salve')
        ]
        with self.assertRaises(Exception):
            writer = POFileTranslationsWriter(None)
            writer.write(translations)
        with self.assertRaises(Exception):
            writer = POFileTranslationsWriter('')
            writer.write(translations)
        with self.assertRaises(IOError):
            temp_dir = tempfile.mkdtemp()
            writer = POFileTranslationsWriter(os.path.join(temp_dir,
                                                           'a',
                                                           'invalid.po'))
            os.rmdir(temp_dir)
            writer.write(translations)

    def test_create(self):
        temp_dir = tempfile.mkdtemp()
        new_filename = os.path.join(temp_dir, 'new.po')
        translations = [
            Translation('Hello', 'Salve'),
            Translation('Good morning', 'Buongiorno')
        ]
        metadata = {
            'Project-Id-Version': '1.0',
            'POT-Creation-Date': '2015-05-28 01:00+0100',
            'Last-Translator': 'Fabio Corneti <info@corneti.com>',
            'Language-Team': 'Italian <info@corneti.com>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }
        writer = POFileTranslationsWriter(new_filename)
        writer.write(translations, metadata=metadata)
        reader = POFileTranslationsReader(new_filename)
        self.assertEqual(reader, translations)
        self.assertEqual(reader.metadata, metadata)
        os.unlink(new_filename)
        os.rmdir(temp_dir)
        self.assertFalse(os.path.exists(temp_dir))

    def test_create_empty(self):
        temp_dir = tempfile.mkdtemp()
        new_filename = os.path.join(temp_dir, 'empty.po')
        translations = []
        writer = POFileTranslationsWriter(new_filename)
        writer.write(translations)
        self.assertEqual(os.path.getsize(new_filename), 22)
        os.unlink(new_filename)
        os.rmdir(temp_dir)
        self.assertFalse(os.path.exists(temp_dir))

    def test_update(self):
        tmp_file = tempfile.NamedTemporaryFile('r')
        translations = [
            Translation('Hello', 'Salve'),
            Translation('Good morning', 'Buongiorno')
        ]
        shutil.copyfile(os.path.join(self.FILES_DIR, 'messages.po'),
                        tmp_file.name)
        writer = POFileTranslationsWriter(tmp_file.name)
        writer.write(translations)
        dest_reader = POFileTranslationsReader(tmp_file.name)
        self.assertEqual(len(dest_reader), 3)
        self.assertEqual(dest_reader[0], translations[0])
        self.assertEqual(dest_reader[1].message, 'Yes')
        self.assertEqual(dest_reader[1].translation, 'Sì')
        self.assertEqual(dest_reader[2], translations[1])
        self.assertEqual(dest_reader[2], translations[1])
        tmp_file.close()

    def test_update_invalid_file(self):
        tmp_file = tempfile.NamedTemporaryFile('r')
        translations = [
            Translation('Hello', 'Salve'),
        ]
        shutil.copyfile(os.path.join(self.FILES_DIR, 'not_a_po.po'),
                        tmp_file.name)
        writer = POFileTranslationsWriter(tmp_file.name)
        with self.assertRaises(IOError):
            writer.write(translations)
        tmp_file.close()


if __name__ == '__main__':
    unittest.main()
