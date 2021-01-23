#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Find out OK headwords after manual correction of an annotation.

    WARNING - Run this code only on the dicts you have proofread after annotation.
    Usage - python3 extract_ok_hw.py
    e.g. python3 extract_ok_hw.py
"""
import sys
import codecs
import os
from utils import code_to_dict
from indic_transliteration import sanscript


def extract_hw(AnnotationCompleted):
    fout = codecs.open('okwords.txt', 'a', 'utf-8')
    for dic in AnnotationCompleted:
        bookname = code_to_dict(dic)
        difffile = os.path.join('..', bookname, 'annotated', dic + '_AN_diff.txt')
        fout.write(';' + bookname + '\n')
        with codecs.open(difffile, 'r', 'utf-8') as fin:
            for lin in fin:
                if lin.startswith('#'):
                    lin = lin.lstrip('#')
                    lin = lin.rstrip()
                    hws = lin.split(',')
                    for hw in hws:
                        hw = sanscript.transliterate(hw, 'devanagari', 'slp1')
                        fout.write(hw + '\n')


if __name__ == "__main__":
    AnnotationCompleted = ['ARMH']
    extract_hw(AnnotationCompleted)
