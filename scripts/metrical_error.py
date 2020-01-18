#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tries to identify verses with imperfect meters from given file.

Prerequisites:
	Put dict_error.py file in shreevatsa/sanskrit folder.
	Put the input_file to be checked for metrical inconsistencies

Usage from commandline:
	python dict_error.py input_file
	
	python dict_error.py input_file > log.txt

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys
import codecs
import print_utils
import identifier_pipeline


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.WARNING)
  identifier = identifier_pipeline.IdentifierPipeline()
  filein = sys.argv[1]
  fin = codecs.open(filein, 'r', 'utf-8')
  verse = ''
  for line in fin:
    if not line.startswith(';'):
        verse += line
        if '॥' in line:
            #print(verse)
            identifier.IdentifyFromText(verse)
            debug_info = identifier.AllDebugOutput()
            if 'exact match' in debug_info:
                pass
            else:
                print(verse.encode('utf-8'))
                print(debug_info.encode('utf-8'))
            verse = ''
