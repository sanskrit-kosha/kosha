# -*- coding: utf-8 -*-

import codecs
import re
import sys
import os
import json

with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
	dictdata = json.load(fin)

def code_to_dict(code):
	return dictdata[code]		


def generic_preprocess(text):
	text = text.replace('|', '।')
	text = text.replace('।।', '॥')
	text = re.sub('॥ ([^१२३४५६७८९०])', '॥\n\g<1>', text)
	text = re.sub('। ([^१२३४५६७८९०])', '।\n\g<1>', text)
	return text


def specific_preprocess(text, code):
	if code in ['ABCH', 'NGSH', 'ACPH', 'ACSJ']:
		text = re.sub('॥([ १२३४५६७८९०]+)([^॥])', '॥\g<1>॥\n\g<2>', text)
	return text


def generic_postprocess(text):
	text = re.sub('\n[ -~]+\n', '\n', text)
	text = re.sub('\n[१२३४५६७८९० 1234567890।*=\-]{0,4}\n', '\n', text)
	text = re.sub('(\n)+', '\n', text)
	text = re.sub('॥([१२३४५६७८९०])', '॥ \g<1>', text)
	text = re.sub('([१२३४५६७८९०])॥', '\g<1> ॥', text)
	text = re.sub('([^ ])([।॥])', '\g<1> \g<2>', text)
	return text


def specific_postprocess(text, code):
	if code not in ['DKDD', 'SRMS']:
		text = re.sub('([^१२३४५६७८९०]) ॥\n', '\g<1> ।\n', text)
	text = re.sub(r'\n[। ]+\n', '\n', text)
	if code == 'KKTV':
		text = re.sub('([।॥]+)[ ]*([१२३४५६७८९०]+)[ ]+([^।॥\n]+)', '\g<1> \g<2> ॥\n\g<3>', text)
		text = re.sub('([१२३४५६७८९०]+)[ ]+\n', '\g<1> ॥\n', text)
	return text


if __name__ == "__main__":
	code = sys.argv[1]
	dictname = code_to_dict(code)
	print(dictname)
	filein = os.path.join('..', dictname, 'orig', dictname+'_googleocr.txt')
	fileout = os.path.join('..', dictname, 'orig', dictname+'_googleocr_adjusted.txt')
	print(filein)
	data = codecs.open(filein, 'r', 'utf-8').read()
	data = generic_preprocess(data)
	data = specific_preprocess(data, code)
	data = generic_postprocess(data)
	data = specific_postprocess(data, code)
	print(fileout)
	fout = codecs.open(fileout, 'w', 'utf-8')
	fout.write(data)
	fout.close()


