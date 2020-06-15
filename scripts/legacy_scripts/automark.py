"""
This file was used to do some preprocessing to do semi automatic annotation of dictionaries.
Subsequently a separate script kosha_annotator.py was created.
This file does not have much future use.
Abandoned.
"""
import codecs
import sys
import re
import os.path
import json
from indic_transliteration import sanscript


commonFillers = ['ca', 'tu', 'cEva', 'ha', 'hi', 'aTa', 'aTAnye', 'kecit', 'syuH', 'syu', 'syus', 'api', 'apica', 'avyayAni', 'avyayam', 'vA', 'nA', 'na', 'yadi', 'sa', 'asya', 'tasya', 'yasya', 'cATa']

with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
	dictdata = json.load(fin)

def code_to_dict(code):
	return dictdata[code]

def readHw(pathToSanhw1):
	with codecs.open(pathToSanhw1, 'r', 'utf-8') as fin:
		data = fin.readlines()
		headwords = [member.split(':')[0] for member in data]
	headwords = set(headwords)
	return headwords

def preprocess(text):
	text = sanscript.transliterate(text, 'devanagari', 'slp1')
	text = text.replace('\n', '')
	text = text.replace("'", " a")
	text = text.replace("ss", "s s")
	text = text.replace("ll", "t l")
	text = text.replace("jj", "t j")
	text = re.sub("S([Sc])", "s \g<1>", text)
	text = re.sub("zz", "s z", text)
	text = re.sub('[ ]+', ' ', text)
	text = re.sub('[^A-Za-z |]', '', text)
	return text

def processblob(bloblist, headwords):
	output = []
	for itm in bloblist:
		itm = re.sub('ityapi$', '', itm)
		itm = re.sub('^syA[dtnl]', '', itm)
		itm = re.sub('avyaya[mM]', '', itm)
		itm = re.sub('strI$', '', itm)
		itm = re.sub('striyAm', '', itm)
		itm = re.sub('yoH$', 'a', itm)
		itm = re.sub('o$', 'a', itm)
		itm = re.sub('([aAiIuUf])H$', '\g<1>', itm)
		itm = re.sub('a[HMm]$', 'a', itm)
		itm = re.sub('Sca$', '', itm)
		itm = re.sub('A[Hs]$', 'A', itm)
		itm = re.sub('astu$', 'a', itm)
		itm = re.sub('s$', '', itm)
		if re.search("([iu])r([aAiIuUfFeEoOhyvrlYmNRnJBGQDjbgqd])", itm):
			itm1 = re.sub("([iu])r([aAiIuUfFeEoOhyvrlYmNRnJBGQDjbgqd])", "\g<1>H \g<2>", itm)
			splt = itm1.split('H ')
			addSplt = False
			for spl in splt:
				if spl in headwords and len(spl) > 1:
					addSplt = True
			if addSplt:
				output += splt
			else:
				output.append(itm)
		else:
			output.append(itm)
	trimmedOutput = []
	for member in output:
		if (member not in trimmedOutput) and (member is not '') and (member not in commonFillers):
			trimmedOutput.append(member)
			"""
			if member not in headwords:
				print(member)
			"""
	return trimmedOutput

if __name__ == "__main__":
	code = sys.argv[1]
	dictname = code_to_dict(code)
	bare_dictname = dictname.split('_')[0]
	filein = os.path.join('..', dictname, 'orig', bare_dictname + '.txt')
	headwords = readHw('sanhw1.txt')
	fileout = os.path.join('..', dictname, 'orig', bare_dictname+'_marked.txt')
	fout = codecs.open(fileout, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	for line in fin:
		# Remove blank lines
		if line == '\n':
			pass
		# For the data scraped from SanskNet
		elif re.search('[0-9]+\n', line):
			fout.write(';v{' + line.rstrip() + '}\n')
		elif re.search('^[\;\{]', line) or not re.search('[।॥]', line):
			fout.write(line)
		else:
			print(line)
			text = preprocess(line)
			bloblist = text.split(' ')
			print(bloblist)
			bloblist = processblob(bloblist, headwords)
			print(bloblist)
			bloblist = [sanscript.transliterate(member, 'slp1', 'devanagari') for member in bloblist]
			fout.write('$' + bloblist[0] + '\n')
			fout.write('#' + ','.join(bloblist) + '\n')
			fout.write(line)
	fin.close()
	fout.close()
