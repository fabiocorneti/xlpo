#!/usr/bin/env python
"""
Usage: xls2po <input.xlsx> <output.po>

Reads messages and translations from the first two columns of an xls/xlsx file
and creates or updates the specified Gettext translation file.

Options:

  -h --help
  --version

"""
from __future__ import print_function

import os
import sys
import xlpo
from docopt import docopt
from xlpo.readers.xlsx import XLSXTranslationsReader
from xlpo.writers.gettext import POFileTranslationsWriter


def execute(argv=None):
    arguments = docopt(__doc__, argv=argv[1:], version=xlpo.__version__)
    input_file = arguments['<input.xlsx>']
    output_file = arguments['<output.po>']
    encoding = 'utf-8'
    discard = False
    metadata = None

    if not os.path.exists(input_file):
        print("File not found: {0}".format(input_file), file=sys.stderr)
        sys.exit(1)

    # TODO: autodetect xls/xlsx?
    if input_file.endswith('.xlsx'):
        reader = XLSXTranslationsReader(input_file)
    else:
        print("Unsupported input file format", file=sys.stderr)
        sys.exit(1)

    if output_file.endswith('.po'):
        try:
            writer = POFileTranslationsWriter(output_file, encoding=encoding)
        except Exception as e:
            print(e.message, file=sys.stderr)
            sys.exit(1)
    else:
        print("Unsupported output file format", file=sys.stderr)
        sys.exit(1)

    try:
        reader.read()
    except Exception as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)

    try:
        writer.write(reader,
                     discard_existing_translations=discard,
                     metadata=metadata)
    except Exception as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)


if __name__ == 'main':
    execute()
