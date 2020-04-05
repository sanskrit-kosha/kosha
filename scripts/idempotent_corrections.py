# -*- coding: utf-8 -*-
import codecs
import re
import sys
import os
import json
import utils


def idempotent_corrections(line):
	line = re.sub('\r\n', '\n', line) # Windows to unix line endings.
	line = re.sub('^[ ]+', '', line) # Remove initial spaces.
	line = re.sub('([।॥])[ ]+\n', '\g<1>\n', line) # Remove trailing spaces
	line = re.sub('([^a-zA-Z0-9]):', '\g<1>ः', line) # Change accidental colon to visarga.
	line = re.sub('[ ]{2,}', ' ', line) # Remove multiple consecutive spaces.
	line = re.sub('([^ ])([।॥])', '\g<1> \g<2>', line) # Keep proper spacing around danda.
	line = re.sub('॥([०१२३४५६७८९]+[ ]*)॥', '॥ \g<1>॥', line) # Space before verse number
	# Change P,V,L,VV,C to p,v,l,vv,c.
	line = line.replace(';P', ';p')
	line = line.replace(';VV', ';v')
	line = line.replace(';V', ';v')
	line = line.replace(';L', ';l')
	line = line.replace(';C', ';c')
	return line


def apply_changes(filein, fileout):
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	for line in fin:
		line = idempotent_corrections(line)
		fout.write(line)
	fin.close()
	fout.close()


def apply_changes(code):	
	# ENSK -> ekaksharanamamala_sadhukalashagani
	fullName = utils.code_to_dict(code)
	# ekaksharanamamala, sadhukalashagani
	bookName, author = fullName.split('_')
	# Read the .txt file
	filein = os.path.join('..', fullName, 'orig', bookName+'.txt')
	fin = codecs.open(filein, 'r', 'utf-8')
	directory = os.path.join('..', fullName, 'orig')
	if not os.path.exists(directory):
		os.mkdir(directory)
	fileout = os.path.join(directory, bookName+'1.txt')
	fout = codecs.open(fileout, 'w', 'utf-8')
	for line in fin:
		line = idempotent_corrections(line)
		fout.write(line)
	fin.close()
	fout.close()

if __name__ == "__main__":
	code = sys.argv[1]
	apply_changes(code)

