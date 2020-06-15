"""
This file had purpose of converting the University of Hyderabad Amarakosha data to the standard style of sanskrit-kosha repository.
I do not foresee any reason to rerun this file.
"""
from __future__ import division
import codecs
import sys
import re
from indic_transliteration import sanscript

def preprocess_amara(filein, fileout):
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	verseNum = '1'
	for line in fin:
		line = line.replace('\r\n', '\n')
		line = re.sub('([^ ])([।॥])', '\g<1> \g<2>', line)
		mtch = re.match('<[/]*Sloka_[0-9]+[.][0-9]+[.]([0-9]+)>\n', line)
		if mtch:
			verseNum = mtch.group(1)
		line = re.sub('<[/]*Sloka[^>]*>\n', '', line)
		line = re.sub('[ ]*अथ (.*)वर्गः([ ।॥]*)', ';v{\g<1>वर्गः}\n;c{अथ \g<1>वर्गः\g<2>}', line)
		line = re.sub('[ ]*इति (.*)वर्गः[ ।॥]*', ';c{इति \g<1>वर्गः}', line)
		line = re.sub('<kANda[^>]*>', ';k{}', line)
		line = re.sub('</kANda[^>]*>', '', line)
		line = re.sub('॥\n', '॥ ' + sanscript.transliterate(verseNum, 'slp1', 'devanagari') + ' ॥\n', line)
		fout.write(line)
	fin.close()
	fout.close()


if __name__ == "__main__":
	#preprocess_amara('../namalinganushasana_amarasinha/orig/amara_uohyd.utf8', '../namalinganushasana_amarasinha/orig/namalinganushasana.txt')
	preprocess_amara('../namalinganushasana_amarasinha/orig/amara_aupasana.utf8', '../namalinganushasana_amarasinha/orig/namalinganushasana1.txt')

