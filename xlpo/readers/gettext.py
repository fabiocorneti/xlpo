# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


import polib
from xlpo.readers import TranslationsReader
from xlpo import Translation
import os


class POFileTranslationsReader(TranslationsReader):
    """
    Reads translations from a gettext PO file using polib.
    """

    def __init__(self, filename):
        self._metadata = None
        self.filename = filename

        if not filename:
            raise Exception("No file specified")

        super(POFileTranslationsReader, self).__init__()

    @property
    def metadata(self):
        self.read()
        return self._metadata

    def read(self):
        if self._translations is not None:
            return

        if not os.path.exists(self.filename):
            raise IOError("File not found: {0}".format(self.filename))

        if not os.path.isfile(self.filename):
            raise IOError("Invalid file path: {0}".format(self.filename))

        try:
            pofile = polib.pofile(self.filename)
        except IOError:
            raise IOError("Invalid or corrupted file: {0}"
                          .format(self.filename))

        self._translations = []
        for entry in pofile:
            self._translations.append(Translation(entry.msgid,
                                                  translation=entry.msgstr,
                                                  context=entry.msgctxt))

        self._metadata = pofile.metadata.copy()

        return self._translations
