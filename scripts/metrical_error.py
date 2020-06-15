#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tries to identify verses with imperfect meters from given file.

Prerequisites:
    Put metrical_error.py file in shreevatsa/sanskrit folder.
    Put the input_file to be checked for metrical inconsistencies

Usage from commandline:
    python metrical_error.py input_file

    python metrical_error.py input_file > log.txt

"""
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import sys
import codecs
import identifier_pipeline


if __name__ == '__main__':
    # Set logging level.
    logging.getLogger().setLevel(logging.WARNING)
    # create identifier class.
    identifier = identifier_pipeline.IdentifierPipeline()
    # input file.
    filein = sys.argv[1]
    # Read input file.
    fin = codecs.open(filein, 'r', 'utf-8')
    # Initialize empty verse.
    verse = ''
    # For each line,
    for line in fin:
        # Ignore lines starting with semicolon. Process others.
        if not line.startswith(';'):
            # Add to verse.
            verse += line
            # Double danda denotes end of verse. Start identifying meter.
            if '॥' in line:
                # print(verse)
                # Identify meter.
                identifier.IdentifyFromText(verse)
                # Extract debug information.
                debug_info = identifier.AllDebugOutput()
                # for perfect match, raise no error.
                if 'exact match' in debug_info:
                    pass
                # Else print the verse and associated debug information.
                else:
                    print(verse.encode('utf-8'))
                    print(debug_info.encode('utf-8'))
                # Reset verse to blank
                verse = ''
