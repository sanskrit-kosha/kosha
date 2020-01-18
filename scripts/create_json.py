# -*- coding: utf-8 -*-

import codecs
import re
import sys
import os
import json
import sqlite3
import utils
from indic_transliteration import sanscript
from parse_data import VerseInfo

with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
	dictdata = json.load(fin)

def code_to_dict(code):
	return dictdata[code]		

def read_data(code):
	dictname = code_to_dict(code)
	[book, author] = dictname.split('_')
	filein = os.path.join('..', dictname, 'orig', book+'.txt')
	with codecs.open(filein, 'r', 'utf-8') as fin:
		data = fin.read()
	[metadata, content] = data.split(';CONTENT')
	return(metadata, content)

def create_json(content):
	verseDetails = VerseInfo()
	lines = content.split('\n')
	print(len(lines))
	verse = ''
	for lin in lines:
		if lin.startswith(';'):
			(tag, value) = utils.extract_tag(lin)
			if tag == 'p':
				verseDetails.update_pageNum(value)
			if tag == 'k':
				verseDetails.update_kanda(value)
			if tag == 'v':
				verseDetails.update_varga(value)
			if tag == 'vv':
				verseDetails.update_subvarga(value)
		else:
			verse += lin + '<BR>'
			ser = re.search('॥ ([०१२३४५६७८९\-\/]+) ॥', lin)
			if ser:
				versenum = ser.group(1)
				verse = re.sub('।([^ ])','। \g<1>', verse)
				verseDetails.update_verseNum(verse)
				#verse = sanscript.transliterate(verse, 'devanagari', 'slp1')
				verseNumDetails = verseDetails.give_verse_details()
				pageNumDetails = verseDetails.give_page_details()
				verse = verse.rstrip('<BR>')
				print(verseNumDetails)
				print(pageNumDetails)
				print(verse)
				verse = ''

def create_sql(verseDetails, code):
	dictname = code_to_dict(code)
	[book, author] = dictname.split('_')
	conn = sqlite3.connect('dicts.db')
	conn.execute('''CREATE TABLE IF NOT EXISTS ''' + book + '''(kanda text, varga text, subvarga text, versenum text, verse text);''')
	with conn:
		conn.executemany("INSERT INTO " + book + " (kanda, varga, subvarga, versenum, verse) values (?,?,?,?,?)", verseDetails)



if __name__ == "__main__":
	code = sys.argv[1]
	(metadata, content) = read_data(code)
	create_json(content)
	#create_sql(verseDetails, code)
	#search_table('Daval', 'abhidhanachintamani')
	

