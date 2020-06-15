"""Prepare Sansknet data for sanskrit-kosha repository.

Would not be required for rerun. Sending to legacy folder.
"""
import codecs
import re
import sys


def preprocess_sansknet(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    verseNum = '0'
    for line in fin:
        line = line.replace('।।', '॥')
        m = re.search(r'^([0-9\- ]+)$', line)
        if m:
            v1 = m.group(1)
            verseNum = v1.split('-')[-1].lstrip().rstrip()
        elif '॥' in line:
            line = line.rstrip()
            line += ' ' + verseNum + ' ' + '॥\n'
            fout.write(line)
        else:
            fout.write(line)
    fin.close()
    fout.close()


if __name__ == "__main__":
    filein = sys.argv[1]
    fileout = sys.argv[2]
    preprocess_sansknet(filein, fileout)
