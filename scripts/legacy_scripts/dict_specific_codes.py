# -*- coding: utf-8 -*-
"""Preprocess the dictionaries received from typists.

It seems unnecessary for future use.
"""
from __future__ import division
import codecs
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


def remove_footnotes_from_anekarthatilaka(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    writeToFile = True
    for line in fin:
        if '{{' in line:
            writeToFile = False
        if writeToFile:
            fout.write(line)
        if '}}' in line:
            writeToFile = True
    fin.close()
    fout.close()


def verse_num_anekarthasangraha(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    verseNum = '0'
    for line in fin:
        m = re.search('([0-9]+)\n', line)
        if m:
            verseNum = m.group(1)
        elif '॥' in line:
            line = line.rstrip()
            line = line + ' ' + verseNum + ' ' + '॥\n'
            fout.write(line)
        else:
            fout.write(line)
    fin.close()
    fout.close()


def verse_num_ekarthanamamala(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    verseNum = '0'
    for line in fin:
        m = re.search('([0-9]+)\n', line)
        if m:
            verseNum = m.group(1)
        elif '॥' in line:
            line = line.rstrip()
            line = line + ' ' + transliterate(verseNum, 'slp1', 'devanagari') + ' ' + '॥\n'
            fout.write(line)
        else:
            fout.write(line)
    fin.close()
    fout.close()


def verse_num_kriyanighantu(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    output = ''
    for line in fin:
        m = re.search('^([०१२३४५६७८९]+)[. ]+([^\n]+)\n', line)
        m1 = re.search('^([^\n]+)\(([०१२३४५६७८९]+)\)\n', line)
        if m:
            output += m.group(2) + ' ' + m.group(1) + ' ॥\n'
        elif m1:
            output += m1.group(1) + m1.group(2) + ' ॥\n'
        else:
            output += line
    output = re.sub('([^ ])([।॥])', '\g<1> \g<2>', output)
    output = re.sub('।[ ]*', '।\n', output)
    fout.write(output)
    fin.close()
    fout.close()


def adjust_nanarthamanjari(filein, fileout):
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')
    output = ''
    for line in fin:
        m = re.search('^P', line)
        m1 = re.search('^([^l]+)(l\{[0-9]+\})', line)
        m2 = re.search('^[\t]+(.*)\n', line)
        if m:
            output += line.replace('P', ';p')
        elif m1:
            output += ';' + m1.group(2) + '\n' + m1.group(1).rstrip() + '\n'
        elif m2:
            output += ';c{' + m2.group(1) + '}\n'
        else:
            output += line
    fout.write(output)
    fin.close()
    fout.close()


def add_linenum(filein, fileout, starting=0):
    counter = starting
    fout = codecs.open(fileout, 'w', 'utf-8')
    fin = codecs.open(filein, 'r', 'utf-8')
    for line in fin:
        if not line.startswith(';'):
            counter += 1
            if counter % 5 == 0:
                fout.write(';l{' + '{0:04d}'.format(counter) + '}\n')
        fout.write(line)
    fin.close()
    fout.close()


def convert_numbers_to_devanagari(filein, fileout):
	fout = codecs.open(fileout, 'w', 'utf-8')
	with codecs.open(filein, 'r', 'utf-8') as fin:
		data = fin.read()
		data = transliterate(data, 'slp1', 'devanagari')
		fout.write(data)
	fout.close()


def prep_koshakalpataru(filein, fileout):
	fout = codecs.open(fileout, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	for lin in fin:
		lin = lin.lstrip().rstrip()
		lin = re.sub('^कोषकल्पतरुः ', '', lin)
		if not re.search('^[a-zA-Z0-9\-]', lin):
			fout.write(lin + '\n')
	fin.close()
	fout.close()


def convert_verse_num_to_devanagari(filein, fileout):
	fout = codecs.open(fileout, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	for lin in fin:
		lin = lin.lstrip().rstrip()
		m = re.search('॥ ([0-9]+) ॥', lin)
		if m:
			lin = transliterate(lin, 'slp1', 'devanagari')
		fout.write(lin + '\n')
	fin.close()
	fout.close()


def pad_page_num(filein, fileout):
	fout = codecs.open(fileout, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	for lin in fin:
		lin = lin.lstrip().rstrip()
		lin = re.sub(';p\{([0-9]{3})\}', ';p{0\g<1>}', lin)
		fout.write(lin + '\n')
	fin.close()
	fout.close()


def add_shloka_number(filein, fileout):
	fout = codecs.open(fileout, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	counter = 0
	for lin in fin:
		lin = lin.rstrip('\n')
		if lin.endswith('।'):
			counter += 1
		if counter % 2 == 0 and counter > 0:
			verseNum = counter // 2
			lin = re.sub('।$', '॥ ', lin)
			lin = lin.replace('॥ ', '॥ ' + transliterate(str(verseNum), 'slp1', 'devanagari') + ' ॥')
			print(verseNum)
		fout.write(lin + '\n')
	fin.close()
	fout.close()


def shabdaratnakara_add_shloka_number(filein, fileout):
	fout = codecs.open(fileout, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	counter = 0
	for lin in fin:
		lin = lin.rstrip('\n')
		if lin.endswith('॥'):
			counter += 1
			lin = lin.replace('॥', '॥ ' + transliterate(str(counter), 'slp1', 'devanagari') + ' ॥')
			print(counter)
		fout.write(lin + '\n')
	fin.close()
	fout.close()


#convert_shashvatakosha('../anekarthasamuchchaya_shashvata/orig/anekarthasamuchchaya_old.txt', '../anekarthasamuchchaya_shashvata/orig/anekarthasamuchchaya.txt')
#remove_footnotes_from_anekarthatilaka('../anekarthatilaka_mahipa/orig/anekarthatilaka_with_uncorrected_footnotes.txt', '../anekarthatilaka_mahipa/orig/anekarthatilaka.txt')
#verse_num_anekarthasangraha('../anekarthasangraha_hemachandra/orig/anekarthasangraha.txt', '../anekarthasangraha_hemachandra/orig/anekarthasangraha_bad.txt')
#verse_num_kriyanighantu('../kriyanighantu_virapandya/orig/kriyanighantu.txt', '../kriyanighantu_virapandya/orig/kriyanighantu1.txt')
#verse_num_kriyanighantu('../dvirupadikosha_shriharsha/orig/dvirupadikosha.txt', '../dvirupadikosha_shriharsha/orig/dvirupadikosha1.txt')
#adjust_nanarthamanjari('../nanarthamanjari_raghava/orig/nanarthamanjari_proofread.txt', '../nanarthamanjari_raghava/orig/nanarthamanjari2.txt')
#verse_num_ekarthanamamala('../ekarthanamamala_saubhari/orig/ekarthanamamala.txt', '../ekarthanamamala_saubhari/orig/ekarthanamamala_numbered.txt')
#verse_num_ekarthanamamala('../dvyaksharinamamala_saubhari/orig/dvyaksharinamamala.txt', '../dvyaksharinamamala_saubhari/orig/dvyaksharinamamala_numbered.txt')
#add_linenum('../ekarthanamamala_saubhari/orig/ekarthanamamala.txt', '../ekarthanamamala_saubhari/orig/ekarthanamamala_line.txt')
#add_linenum('../dvyaksharinamamala_saubhari/orig/dvyaksharinamamala.txt', '../dvyaksharinamamala_saubhari/orig/dvyaksharinamamala_line.txt', 200)
#convert_numbers_to_devanagari('../paramanandiyanamamala_makarandadasa/orig/paramanandiyanamamala.txt', '../paramanandiyanamamala_makarandadasa/orig/paramanandiyanamamala_line.txt')
#prep_koshakalpataru('../koshakalpataru_vishvanatha/orig/koshakalpataru_vishvanatha_googleocr_adjusted.txt', '../koshakalpataru_vishvanatha/orig/koshakalpataru_prep.txt')
#convert_verse_num_to_devanagari('../shivakosha_shivadatta/orig/shivakosha.txt', '../shivakosha_shivadatta/orig/shivakosha1.txt')
#pad_page_num('../shivakosha_shivadatta/orig/shivakosha.txt', '../shivakosha_shivadatta/orig/shivakosha1.txt')
#convert_verse_num_to_devanagari('../anekarthanighantu_dhananjaya/orig/anekarthanighantu.txt', '../anekarthanighantu_dhananjaya/orig/anekarthanighantu1.txt')
#verse_num_ekarthanamamala('../ekaksharikosha_amarakavi/orig/ekaksharikosha.txt', '../ekaksharikosha_amarakavi/orig/ekaksharikosha1.txt')
#add_shloka_number('../panchatattvaprakasha_venidatta/orig/panchatattvaprakasha.txt', '../panchatattvaprakasha_venidatta/orig/panchatattvaprakasha1.txt')
shabdaratnakara_add_shloka_number('../../shabdaratnakara_vamanabhatta/orig/shabdaratnakara.txt', '../../shabdaratnakara_vamanabhatta/orig/shabdaratnakara1.txt')
