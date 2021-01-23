import re
import os
import codecs


base = '../../kalpadrukosha_keshava/orig/'


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
    return line


def a1(file0, file1):
    fin0 = codecs.open(file0, 'r', 'utf-8')
    fin1 = codecs.open(file1, 'w', 'utf-8')
    for line in fin0:
        line = idempotent_corrections(line)
        line = line.replace('ऽ', '')
        fin1.write(line)
    fin0.close()
    fin1.close()


def kd1(file0, file1):
    fin0 = codecs.open(file0, 'r', 'utf-8')
    fin1 = codecs.open(file1, 'w', 'utf-8')
    for line in fin0:
        line = line.replace(',', '')
        line = line.replace('ऽ', '')
        line = line.replace('र्त्त', 'र्त')
        fin1.write(line)
    fin0.close()
    fin1.close()


if __name__ == "__main__":
    file0 = base + 'KDKS_comparision/KDKS_AB_0.txt'
    file1 = base + 'KDKS_comparision/KDKS_AB_1.txt'
    k0 = base + 'kalpadrukosha.txt'
    k1 = base + 'KDKS_comparision/kd1.txt'
    a1(file0, file1)
    kd1(k0, k1)
