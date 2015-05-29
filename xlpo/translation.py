from __future__ import absolute_import

import six


@six.python_2_unicode_compatible
class Translation(object):
    """
    A translation.
    """

    def __init__(self, message, translation=None, context=None, comment=None):
        """
        Creates a new Translation.

        Arguments:

        ``message``
            the message to be translated (singular form)

        ``translation``
            the message translation

        ``context``
            the translation context/namespace

        ``comment``
            a comment about the translation
        """
        self.message = message
        self.translation = translation
        self.context = context
        self.comment = comment

    def __str__(self):
        return self.message

    def __eq__(self, other):
        """
        Two translations are considered equal if their message, translation
        and context are equal.
        """
        for attr in ('message', 'translation', 'context'):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        return not self == other
