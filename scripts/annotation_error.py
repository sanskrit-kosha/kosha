#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Find out possible errors in annotation work.

  Usage - python3 annotation_error.py annotatedfile unannotatedfile logfile
  e.g. python3 annotation_error.py ../abhidhanaratnamala_halayudha/annotated/ARMH_manual_annotation.txt ../abhidhanaratnamala_halayudha/orig/abhidhanaratnamala.txt ../abhidhanaratnamala_halayudha/annotated/ARMH_AN_diff.txt
"""
import sys
import codecs
import difflib
import re
import os
from indic_transliteration import sanscript


def finddiff(annotatedfile, unannotatedfile, flog):
    """Find differences between two files, and note in the flog file."""
    # Read texts into lines.
    text1 = codecs.open(annotatedfile, 'r', 'utf-8').readlines()
    text2 = codecs.open(unannotatedfile, 'r', 'utf-8').readlines()
    print('CHANGES OTHER THAN TAGGING\n')
    flog.write('CHANGES OTHER THAN TAGGING\n')
    # For different lines
    for line in difflib.unified_diff(text1, text2):
        # If there is a change in the annotated file,
        if re.search(r'^\+[^+]', line):
            # Write to the flog
            print(line)
            flog.write(line)
    flog.write('----------\n')
    print('----------\n')


def sanhw1set(sanhw1file):
    """Generate a set of headwords from sanhw1.txt file from Cologne."""
    # Initialize
    result = set()
    with codecs.open(sanhw1file, 'r', 'utf-8') as fin:
        for lin in fin:
            # extract headwords and add to the set.
            lin = lin.rstrip()
            hw = lin.split(':')[0]
            result.add(hw)
    return result


def find_abnormal_hw(annotatedfile, flog, hwset):
    """Show headwords not present in hwset and relevant verse lines."""
    print('ABNORMAL HEADWORDS\n')
    flog.write('ABNORMAL HEADWORDS\n')
    with codecs.open(annotatedfile, 'r', 'utf-8') as fin:
        # By default, the verse will not be written.
        writeVerse = False
        for lin in fin:
            # Headword line
            if lin.startswith('#'):
                # No need to write the verse.
                writeVerse = False
                # Trimming
                lin1 = lin.lstrip('#')
                lin1 = lin1.rstrip()
                # Headwords
                hws = lin1.split(',')
                for hw in hws:
                    # headword in slp1
                    hwslp1 = sanscript.transliterate(hw, 'devanagari', 'slp1')
                    # headword absent in sanhw1.txt
                    if hwslp1 not in hwset:
                        # Write to the flog
                        print('#' + hw)
                        flog.write('#' + hw + '\n')
                        # Set writeVerse as True.
                        # Next lines till next occurrence of # will be written.
                        writeVerse = True
            # If there is a headword mismatch, write to flog.
            elif writeVerse:
                print(lin)
                flog.write(lin)
    flog.write('----------\n')


if __name__ == "__main__":
    annotatedfile = sys.argv[1]
    unannotatedfile = sys.argv[2]
    logfile = sys.argv[3]
    # As the logfile is going to be used across functions,
    # using the file object.
    flog = codecs.open(logfile, 'w', 'utf-8')
    # Find difference in lines, other than headword lines.
    finddiff(annotatedfile, unannotatedfile, flog)
    # Initialize the set of known headwords.
    sanhw1file = os.path.join('..', '..', 'cologne', 'hwnorm1', 'sanhw1', 'sanhw1.txt')
    print('CREATING HEADWORD SET FROM SANHW1.')
    sanhwset = sanhw1set(sanhw1file)
    # Also take the OK words from earlier dictionaries as valid words.
    okfile = 'okwords.txt'
    okset = sanhw1set(okfile)
    # Add sanhw1set and okset into one set.
    hwset = sanhwset | okset
    # Find the headwords absent in sanhw1.txt
    find_abnormal_hw(annotatedfile, flog, hwset)
    # Close the log file.
    flog.close()
