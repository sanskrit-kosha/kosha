# -*- coding: utf-8 -*-
"""Legacy code."""
import codecs
import re
import sys
import os
import json

from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
from sanskrit_parser.morphological_analyzer.sanskrit_morphological_analyzer import SanskritMorphologicalAnalyzer
analyzer = SanskritMorphologicalAnalyzer()

def getannotation(v):
	""" Get morphological tags for v """
	vobj = SanskritObject(v, strict_io=False, replace_ending_visarga=None)
	g = analyzer.getSandhiSplits(vobj, tag=True)
	if g:
		splits = g.findAllPaths(10)
	else:
		splits = []
	mres = {}
	for sp in splits:
		p = analyzer.constrainPath(sp)
		if p:
			sl = "_".join([spp.devanagari(strict_io=False) for spp in sp])
			mres[sl] = []
			for pp in p:
				mres[sl].append([(spp.devanagari(strict_io=False), jtag(pp[spp.canonical()])) for spp in sp])
	r = {"input": v, "devanagari": vobj.devanagari(), "analysis": mres}
	return r

print(getannotation('astyuttarasyAm'))

exit(0)

with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
	dictdata = json.load(fin)

def code_to_dict(code):
	return dictdata[code]

def preannotate(text, dicttype='homonymic'):
	return text

if __name__ == 'main':
	code = sys.argv[1]
	dictname = code_to_dict(code)
	filein = os.path.join('..', dictname, 'orig', dictname+'_v1.txt')
	fileout = os.path.join('..', dictname, 'orig', dictname+'_v2.txt')
	print(filein)
	data = codecs.open(filein, 'r', 'utf-8').read()
	if data.startswith(';homonymic'):
		dicttype = 'homonymic'
	elif data.startswith(';synonymic'):
		dicttype = 'synonymic'
	else:
		print('Specify whether the file is homonymic or synonymic in the v1 file first line like ;homonymic or ;synonimic')
		exit(0)
	data = preannotate(data, dicttype)
	print(fileout)
	fout = codecs.open(fileout, 'w', 'utf-8')
	fout.write(data)
	fout.close()
