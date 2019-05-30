import codecs
import sys
import re
from indic_transliteration.sanscript import transliterate

def convert_shashvatakosha(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    for line in fin:
        output = ''
        line = line.rstrip()
        if line.startswith('#'):
            line = line.lstrip('#')
            parts = line.split(';')
            for part in parts:
                print(part)
                headword, count = part.split(',')
                count = int(transliterate(count, 'devanagari', 'slp1'))
                output += '$' + headword + ';\n'
                output += '#' + ','.join(['' for i in range(count)]) + '\n'
            fout.write(output)
        elif ';{p0' in line:
            fout.write(line.replace(';{p0', ';p{0') + '\n')
        else:
            fout.write(line + '\n')

convert_shashvatakosha('../anekarthasamuchchaya_shashvata/orig/anekarthasamuchchaya_old.txt', '../anekarthasamuchchaya_shashvata/orig/anekarthasamuchchaya.txt')
