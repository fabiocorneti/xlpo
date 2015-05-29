class TranslationsWriter(object):
    """
    Writes translations to a stream.
    """

    def write(self, translations, discard_existing_translations=False,
              metadata=None):
        """
        Writes translations to the underlying output stream.

        Expects ``translations`` to be a list of ``Translation`` instances.
        """
        raise NotImplementedError
