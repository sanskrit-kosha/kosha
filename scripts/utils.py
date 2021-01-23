# -*- coding: utf-8 -*-
"""Store different reusable utilities for other programs."""
import codecs
import re
import json
from datetime import datetime
from indic_transliteration.sanscript import transliterate


def extract_tag(metaline):
    """Extract tag from metaline i.e. lines having semicolon."""
    # Typical line in metadata is of the structure `;tag{value}`
    m = re.search(r';([^{]*)\{([^}]*)\}', metaline)
    # If matches typical line,
    if m:
        # Extract tag and value.
        tag = m.group(1)
        value = m.group(2)
    else:
        tag = False
        value = False
    return (tag, value)


def prepare_metadata(metatext):
    """Extract metadata from the text file and return a dict."""

    # Read line wise
    lines = metatext.split('\n')
    # Initialize the blank metadata dict.
    metadata = {}
    for line in lines:
        # Ignore if the line is blank or a marker for starting of metadata.
        if line.startswith(';METADATA') or line == '':
            pass
        # If the line does not start with ';' - there is some error.
        elif not line.startswith(';'):
            print('Check line. Does not follow metadata structure.')
            print(line)
        else:
            (tag, value) = extract_tag(line)
            if tag:
                # Add to the metadata dict.
                metadata[tag] = value
            else:
                # There may be some error. Check up.
                print('Check line. Does not follow metadata structure.')
    return metadata


def remove_page_line(content):
    """Remove page markers and line markers."""

    result = []
    # read lines into a list
    lines = content.split('\n')
    for line in lines:
        # Ignore the page and line markers
        if line.startswith(';p{') or line.startswith(';l{'):
            pass
        else:
            # Add to the output list
            result.append(line)
    # Join with new line marker.
    return '\n'.join(result)


def code_to_dict(code):
    """Return book_author string for code."""
    with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
        dictdata = json.load(fin)
    return dictdata[code]


def timestamp():
    """Return timestamp."""
    return datetime.now()


class VerseInfo():
    """Hold the information regarding current verse being handled."""

    def __init__(self):
        """Initialize with default values."""
        self.kanda = ''
        self.varga = ''
        self.subvarga = ''
        self.kandaNum = 0
        self.vargaNum = 1
        self.subvargaNum = 1
        self.pageNum = 1
        self.verseNum = 1
        self.lastVerseNum = 0

    def update_pageNum(self, pageNum):
        """Upadate pageNum."""
        self.pageNum = pageNum

    def update_subvarga(self, subvarga):
        """Update subvarga. Also identify its name."""
        self.subvarga = subvarga
        self.subvargaNum += 1

    def update_varga(self, varga):
        """Update varga. Reset subvargaNum to 1."""
        self.subvarga = ''
        self.subvargaNum = 1
        self.varga = varga
        self.vargaNum += 1

    def update_kanda(self, kanda):
        """Update kanda. Reset vargaNum and subvargaNum to 1."""
        self.subvarga = ''
        self.subvargaNum = 1
        self.varga = ''
        self.vargaNum = 1
        self.kanda = kanda
        self.kandaNum += 1

    def update_verseNum(self, verse):
        """Identify the verse number from verse and update verseNum."""
        m = re.search('[॥|..] ([0123456789०१२३४५६७८९]+) [॥|..]', verse)
        if m:
            self.lastVerseNum = int(transliterate(m.group(1), 'devanagari', 'slp1'))
            self.verseNum = self.lastVerseNum
        # Unless you encounter the next verse number, you need to use prev + 1.
        else:
            self.verseNum = self.lastVerseNum + 1

    def give_verse_details(self):
        """Return names of kanda, varga, subvarga and number of verse."""
        return self.kanda + '.' + self.varga + '.' + self.subvarga + '.' + str(self.verseNum)

    def give_page_details(self):
        """Return pageNum."""
        return self.pageNum

    def give_verse_num_details(self):
        """Return numbers of kanda, varga, subvarga and verse."""
        return str(self.kandaNum) + '.' + str(self.vargaNum) + '.' + str(self.subvargaNum) + '.' + str(self.verseNum)
