from __future__ import absolute_import

from xlpo.translation import Translation


class TranslationsReader(object):
    """
    Reads translations from the underlying stream.
    """

    def __init__(self):
        self._translations = None

    @property
    def metadata(self):
        """
        Returns metadata from the underlying stream.
        """
        raise NotImplementedError

    def read(self):
        """
        Reads the translations; implicitly triggered by other operations.
        """
        raise NotImplementedError

    def find(self, message, context=False):
        """
        Returns the translations for the specified message.
        """
        self.read()
        results = []
        for translation in self:
            if translation.message == message:
                if context is not False:
                    if translation.context == context:
                        results.append(translation)
                else:
                    results.append(translation)
        return results

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in xrange(0, len(self)):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __contains__(self, translation):
        """
        If ``translation`` is a ``Translation`` instance, returns ``True``
        if the reader contains a translation for the same message with the
        same context.

        If ``translation`` is a string, returns ``True`` if the reader
        contains one or more translations for the specified string.
        """
        self.read()
        if isinstance(translation, Translation):
            return len(self.find(translation.message,
                                 context=translation.context)) > 0
        return self.find(translation) is not None

    def __len__(self):
        self.read()
        return len(self._translations)

    def __getitem__(self, item):
        self.read()
        return self._translations.__getitem__(item)

    def __iter__(self):
        self.read()
        return self._translations.__iter__()
