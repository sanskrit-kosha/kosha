#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Find errors in given file.

Usage - python3 error_summary.py file
e.g. python3 error_summary.py abhidhanachintamani_hemachandra/orig/abhidhanachintamani.txt
"""
import codecs
import sys
import re
from indic_transliteration.sanscript import transliterate


def extract_tag(data):
    """Extracts the tag from lines starting with ';'."""
    if data.startswith(';'):
        data = data.rstrip()
        blob = re.sub(r';([a-zA-Z]+)\{([^}]+)\}', r'\g<1>&&\g<2>', data)
        return(blob.split('&&'))
    else:
        return False


def verse_num_extractor(data):
    """Extract verse number from a verse."""
    if re.search('॥ [०१२३४५६७८९]+ ॥\n', data):
        num = re.sub(r'.*॥ ([०१२३४५६७८९]+) ॥\n', r'\g<1>', data)
        num = transliterate(num, 'devanagari', 'slp1')
        num = int(num)
        return num
    else:
        return False


class Error:
    """Class to find out errors in the text."""
    def __init__(self):
        """Default values."""
        self.pages = []
        self.lastpage = 0
        self.linenums = []
        self.lastlinenum = 0
        self.chapters = []
        self.comments = []
        self.numberSeparator = 'v'
        self.kanda = ''
        self.varga = ''
        self.lastverse = 0
        self.singleDanda = False
        self.doubleDanda = True

    def _addpages(self, line):
        """Update page number related details."""
        if line.startswith(';p{'):
            (tag, pagenum) = extract_tag(line)
            pagenum = int(pagenum)
            # print(pagenum)
            # If page number is not one more than the previous number,
            # raise an error
            if (pagenum != self.lastpage + 1) and self.lastpage != 0:
                print('Page numbering error.')
                print(pagenum)
                print('can not follow')
                print(self.lastpage)
            # Update the pagenumber.
            self.pages.append(pagenum)
            self.lastpage = pagenum

    # Reference - https://github.com/sanskrit-kosha/kosha/issues/21
    def _line_num_errors(self, line, increment=5):
        """Find line number errors."""
        if line.startswith(';l{'):
            (tag, linenum) = extract_tag(line)
            linenum = int(linenum)
            # print(pagenum)
            # If the increment is not as per specification, raise an error.
            if (linenum != self.lastlinenum + increment) and self.lastlinenum != 0:
                print('Line numbering error.')
                print(linenum)
                print('can not follow')
                print(self.lastlinenum)
            # Update line number
            self.linenums.append(linenum)
            self.lastlinenum = linenum

    def _addchapters(self, line):
        """Update chapter type and chapter name."""
        if re.match(r';[akv]+\{', line):
            (chapter, chaptername) = extract_tag(line)
            # print(chapter, chaptername)
            self.chapters.append((chapter, chaptername))

    def _addcomments(self, line):
        """Update comments."""
        if re.match(';c{', line):
            (co, comment) = extract_tag(line)
            # print(co, comment)
            self.comments.append(comment)

    def _identify_extra_spaces(self, line):
        """"Raise an error if there are extra spaces."""
        if re.search('[ ]{2,}', line) or ' \n' in line or line.startswith(' '):
            print('Extra spaces error.')
            print(self.lastpage, line)

    def _identify_missing_spaces(self, line):
        """Raise an error if there are missing spaces."""
        if re.search('[^ {][॥।]', line) or ' \n' in line:
            print('Missing spaces error.')
            print(self.lastpage, line)

    def _verse_number_mismatch(self, line):
        """Raise an error if the verse numbers are not consequent."""
        if re.search('॥ [०१२३४५६७८९]+ ॥\n', line):
            verseNum = verse_num_extractor(line)
            if (verseNum != self.lastverse + 1) and verseNum != 1:
                print('Verse number error.')
                print('On page {}, {} can not follow {}'.format(self.lastpage, verseNum, self.lastverse))
            self.lastverse = verseNum

    def _verse_end_check(self, line):
        """Raise an error regarding single and double danda."""
        if line.startswith(';'):
            pass
        elif re.search('।\n', line):
            if not self.doubleDanda:
                print('Single danda does not follow double danda.')
                print(self.lastpage, line)
            self.singleDanda = True
            self.doubleDanda = False
        elif re.search('॥\n', line):
            if not self.singleDanda:
                print('Double danda does not follow single danda.')
                print(self.lastpage, line)
            self.doubleDanda = True
            self.singleDanda = False

    def _check_colon(self, line):
        """Raise an error if colon is used instead of visarga."""
        if ':' in line:
            print('Colon found. Check whether visarga needed.')
            print(self.lastpage, line)

    # Reference - https://github.com/sanskrit-kosha/kosha/issues/26
    def _issue26(self, line):
        """Raise an error in case of known problematic letters."""
        problematicItems = ['श्र्व', 'श्र्च', 'श्र्ल', 'श्रृ', '|']
        for prblm in problematicItems:
            if prblm in line:
                print('Illegal character error. ' + prblm)
                print(line)


if __name__ == "__main__":
    filein = sys.argv[1]
    # Read data from input file.
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.readlines()
    fin.close()
    # Initialize the error class.
    errors = Error()
    print('Errors if any found')
    # For every line, find errors.
    for line in data:
        # print(line)
        errors._addpages(line)
        errors._addchapters(line)
        errors._addcomments(line)
        errors._identify_extra_spaces(line)
        errors._identify_missing_spaces(line)
        errors._verse_number_mismatch(line)
        errors._verse_end_check(line)
        errors._check_colon(line)
        errors._issue26(line)
        errors._line_num_errors(line)

    # Print chapter names at the end, to check for continuity.
    print('Chapter names extracted from txt file')
    for (chapter, chaptername) in errors.chapters:
        if chapter == 'k':
            print(chapter, chaptername)
        elif chapter == 'v':
            print('\t', chapter, chaptername)
        elif chapter == 'vv':
            print('\t', '\t', chapter, chaptername)
