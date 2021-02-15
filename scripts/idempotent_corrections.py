# -*- coding: utf-8 -*-
"""Apply idempotent corrections to a file.

There are many generic changes which are idempotent in nature.
We can use this script on the same file for infinite time.

Usage - python3 idempotent_corrections.py CODE
e.g. python3 idempotent_corrections.py AMAR
"""
import codecs
import re
import sys
import os
import utils


def idempotent_corrections(line):
    """Apply corrections to line."""
    line = re.sub(r'\r\n', r'\n', line)  # Windows to unix line endings.
    line = re.sub(r'^[ ]+', r'', line)  # Remove initial spaces.
    line = re.sub(r'([।॥])[ ]+\n', r'\g<1>\n', line)  # Remove trailing spaces
    # Change accidental colon to visarga.
    line = re.sub(r'([^a-zA-Z0-9]):', r'\g<1>ः', line)
    # Remove multiple consecutive spaces.
    line = re.sub(r'[ ]{2,}', r' ', line)
    # Keep proper spacing around danda.
    line = re.sub(r'([^ ])([।॥])', r'\g<1> \g<2>', line)
    # Space before verse number
    line = re.sub(r'॥([०१२३४५६७८९]+[ ]*)॥', r'॥ \g<1>॥', line)
    # Change P,V,L,VV,C to p,v,l,vv,c.
    line = line.replace(';P', ';p')
    line = line.replace(';VV', ';v')
    line = line.replace(';V', ';v')
    line = line.replace(';L', ';l')
    line = line.replace(';C', ';c')
    line = line.replace(';c{ ॥', ';c{॥')
    line = line.replace(';cONTENT', ';CONTENT')
    # line = line.replace('“', '"')
    # line = line.replace('”', '"')
    return line


"""
def apply_changes(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    for line in fin:
        line = idempotent_corrections(line)
        fout.write(line)
    fin.close()
    fout.close()
"""


def apply_changes(code):
    """Apply idempotent changes to file corresponding to the given code."""
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'orig', bookName + '.txt')
    fin = codecs.open(filein, 'r', 'utf-8')
    # Create path if does not exist.
    directory = os.path.join('..', fullName, 'orig')
    if not os.path.exists(directory):
        os.mkdir(directory)
    # Output file.
    fileout = os.path.join(directory, bookName + '1.txt')
    fout = codecs.open(fileout, 'w', 'utf-8')
    # Apply idempotent corrections to each line.
    for line in fin:
        line = idempotent_corrections(line)
        fout.write(line)
    fin.close()
    fout.close()


if __name__ == "__main__":
    code = sys.argv[1]
    # Apply idempotent changes to the file of given code.
    apply_changes(code)
