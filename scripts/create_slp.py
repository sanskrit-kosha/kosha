# -*- coding: utf-8 -*-
import os
import sys
import utils
import codecs
import json
from indic_transliteration import sanscript

def create_slp(code):	
	# ENSK -> ekaksharanamamala_sadhukalashagani
	fullName = utils.code_to_dict(code)
	# ekaksharanamamala, sadhukalashagani
	bookName, author = fullName.split('_')
	# Read the .txt file
	filein = os.path.join('..', fullName, 'orig', bookName+'.txt')
	fin = codecs.open(filein, 'r', 'utf-8')
	data = fin.read()
	fin.close()
	data = sanscript.transliterate(data, 'devanagari', 'slp1')
	directory = os.path.join('..', fullName, 'slp')
	if not os.path.exists(directory):
		os.mkdir(directory)
	fileout = os.path.join(directory, bookName+'.txt')
	fout = codecs.open(fileout, 'w', 'utf-8')
	fout.write(data)
	fout.close()

if __name__ == "__main__":
	print(utils.timestamp())
	with codecs.open('workingdicts.json', 'r', 'utf-8') as fin:
		dictcodes = json.load(fin)
	for code in dictcodes:
		print(code)
		create_slp(code)
	print(utils.timestamp())

