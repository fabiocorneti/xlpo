from __future__ import absolute_import, unicode_literals

from xlpo.writers import TranslationsWriter
import os
import polib


class POFileTranslationsWriter(TranslationsWriter):
    """
    Writes translations to a gettext PO file.
    """

    def __init__(self, filename, encoding='utf-8'):
        """
        Creates a new POTranslationsWriter.

        Arguments:

        ``filename``
            the path to the PO file that will be created or updated.

        ``encoding``
            the encoding of the output file.
        """
        self.filename = filename
        self.encoding = encoding

        if not filename:
            raise Exception("No file specified")

        super(POFileTranslationsWriter, self).__init__()

    def write(self, translations, discard_existing_translations=False,
              metadata=None):
        """
        Writes translations to the underlying output file; the file will be
        automatically created if it doesn't exist.

        If the file exists, existing translations will be preserved, unless
        the ``discard_existing`` parameter is set to ``True``.

        Arguments:

        ``translations``
            a list of ``Translation`` instances.

        ``metadata``
            a dictionary containing gettext metadata entries.

        ``discard_existing_translations``
            if set to ``True`` and the destination file exists, existing
            translations will be removed.
        """

        if os.path.exists(self.filename):
            try:
                # TODO: handle encoding mismatchs
                pofile = polib.pofile(self.filename, check_for_duplicates=True)
            except IOError:
                raise IOError(
                    "Invalid or corrupted file: {0}".format(self.filename))
        else:
            pofile = polib.POFile(check_for_duplicates=True,
                                  encoding=self.encoding)

        if metadata:
            pofile.metadata = metadata

        for translation in translations:
            existing = pofile.find(translation.message,
                                   msgctxt=translation.context)
            if existing:
                existing.msgstr = translation.translation
            else:
                pofile.append(polib.POEntry(msgid=translation.message,
                                            msgstr=translation.translation,
                                            msgctxt=translation.context))

        try:
            pofile.save(self.filename)
        except:
            raise IOError(
                "Cannot write translations to file {0}".format(self.filename))
