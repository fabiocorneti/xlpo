#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from tests.base import BaseTestCase
from xlpo.commands import xls2po
from xlpo.readers import POFileTranslationsReader
import os
import tempfile
import unittest


class TestXsl2poCommand(BaseTestCase):

    def test_xlsx2po(self):
        temp_dir = tempfile.mkdtemp()
        input_filename = os.path.join(self.FILES_DIR, 'en_it__noheaders.xlsx')
        output_filename = os.path.join(temp_dir, 'output.po')
        argv = [input_filename, output_filename]
        xls2po.execute(argv)
        reader = POFileTranslationsReader(output_filename)
        self.assertEqual(len(reader), 2)
        os.unlink(output_filename)
        os.rmdir(temp_dir)
        self.assertFalse(os.path.exists(temp_dir))

if __name__ == '__main__':
    unittest.main()
