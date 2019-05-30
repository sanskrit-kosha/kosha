import codecs
import sys
import re
from indic_transliteration.sanscript import transliterate

def extract_tag(data):
	if data.startswith(';'):
		data = data.rstrip()
		blob = re.sub(';([a-zA-Z]+)\{([^}]+)\}', '\g<1>&&\g<2>', data)
		return(blob.split('&&'))
	else:
		return False

def verse_num_extractor(data):
	if re.search('॥ [०१२३४५६७८९]+ ॥\n', data):
		num = re.sub('.*॥ ([०१२३४५६७८९]+) ॥\n', '\g<1>', data)
		num = transliterate(num, 'devanagari', 'slp1')
		num = int(num)
		return num
	else:
		return False

class Error:
	def __init__(self):
		self.pages = []
		self.lastpage = 0
		self.chapters = []
		self.comments = []
		self.numberSeparator = 'v'
		self.kanda = ''
		self.varga = ''
		self.lastverse = 0

	def _addpages(self, line):
		if line.startswith(';p{'):
			(tag, pagenum) = extract_tag(line)
			pagenum = int(pagenum)
			if (pagenum != self.lastpage + 1) and self.lastpage != 0:
				print('Page numbering error.')
				print('{} can not follow {}').format(pagenum, self.lastpage)
			self.pages.append(pagenum)
			self.lastpage = pagenum

	def _addchapters(self, line):
		if re.match(';[akv]+\{', line):
			(chapter, chaptername) = extract_tag(line)
			#print(chapter, chaptername)
			self.chapters.append((chapter, chaptername))

	def _addcomments(self, line):
		if re.match(';c{', line):
			(co, comment) = extract_tag(line)
			#print(co, comment)
			self.comments.append(comment)

	def _identify_extra_spaces(self, line):
		if re.search('[ ]{2,}', line) or ' \n' in line or line.startswith(' '):
			print('Extra spaces error.')
			print(self.lastpage, line)

	def _identify_missing_spaces(self, line):
		if re.search('[^ {][॥।]', line) or ' \n' in line:
			print('Missing spaces error.')
			print(self.lastpage, line)

	def _verse_number_mismatch(self, line):
		if re.search('॥ [०१२३४५६७८९]+ ॥\n', line):
			verseNum =  verse_num_extractor(line)
			if (verseNum != self.lastverse + 1) and verseNum != 1:
				print('Verse number error.')
				print('On page {}, {} can not follow {}'.format(self.lastpage, verseNum, self.lastverse))
			self.lastverse = verseNum
			

if __name__ == "__main__":
	filein = sys.argv[1]
	fin = codecs.open(filein, 'r', 'utf-8')
	data = fin.readlines()
	fin.close()
	errors = Error()
	print('Errors if any found')
	for line in data:
		#print(line)
		errors._addpages(line)
		errors._addchapters(line)
		errors._addcomments(line)
		errors._identify_extra_spaces(line)
		errors._identify_missing_spaces(line)
		errors._verse_number_mismatch(line)
	print('Chapter names extracted from txt file')
	for (chapter, chaptername) in errors.chapters:
		print(chapter, chaptername)

