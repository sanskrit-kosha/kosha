import codecs
import sys
import os
import re
import json
import shutil
from collections import defaultdict
import utils
import lxml.etree as ET
from indic_transliteration import sanscript
"""
Usage - python3 parse_data.py dictCode [babylon|md|json|xml|html|cologne]
e.g. python3 parse_data.py ENSK [babylon|md|json|xml|html|cologne]

For dictCodes, see dictcode.json.
They are 4 letter codes unique to each dictionary.

The code version corresponds to the version of ../docs/annotation_thoughts.md.
This code can convert the files conformant to that version of annotation.
"""

__version__ = '2.0.0'
__author__ = 'Dr. Dhaval Patel, drdhaval2785@gmail.com'
__licence__ = 'GNU GPL version 3'


def createdir(mydir):
    if not os.path.exists(mydir):
        os.makedirs(mydir)


def unique(lst):
    """Keep only unique items in the list, preserving the order."""
    result = []
    for itm in lst:
        if itm not in result:
            result.append(itm)
    return result


class HW():
    def __init__(self, headword, gender=''):
        self.hw = headword
        self.gender = gender


def putVerse(verse, wordsOnHand, result):
    """Empty the wordsOnHand to result.

    result has (headword, meanings, verse, verseNumDetails and pageNumDetails).
    Blank verse and blank wordsOnHand are also returned for onward process.
    """
    # Get Verse number details
    verseNumDetails = verseDetails.give_verse_num_details()
    # Get page number details.
    pageNumDetails = verseDetails.give_page_details()
    # Remove trailing new lines if any.
    verse = verse.rstrip('<BR>')
    # Append to result.
    for (headword, meanings) in wordsOnHand:
        result.append((headword, meanings, verse, verseNumDetails, pageNumDetails))
    # Empty the temporary wordsOnHand list.
    wordsOnHand = []
    # Reset verse to blank string to store next verse.
    verse = ''
    return (verse, wordsOnHand, result)


def homonymic_list_generator(content):
    """Prepare a list with (headword, meanings, verse, verseNumDetails and pageNumDetails) tuple."""
    # Making it global so that it can be used in other functions too.
    global verseDetails
    # Result will store tuples (headword, meaning, verse)
    result = []
    # Initialize blank verse
    verse = ''
    # lineType list holds 'h', 'm', 'v' for headword, meaning and verse lines.
    lineType = []
    # Read the content into list of lines.
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')
    lines = content.split('\n')
    # A temporary placeholder which will be emptied into result list
    # whenever the verse is allocated to it.
    wordsOnHand = []
    for line in lines:
        # If the line is headword line,
        if line.startswith('$'):
            # If the preceding line was a verse, and current a headword,
            # time to add to result list
            if lineType[-1] == 'v':
                verseDetails.update_verseNum(verse)
                (verse, wordsOnHand, result) = putVerse(verse, wordsOnHand, result)
            # Extract the headword and gender from headword line.
            # Typical headword line is `$headword;gender` or `$headword`
            gender = ''
            if ';' in line:
                hw, gender = line.rstrip().lstrip('$').split(';')
                headword = HW(hw, gender)
            else:
                hw = line.rstrip().lstrip('$')
                headword = HW(hw)
            # lineType is appended with 'h' for headword.
            lineType.append('h')
        # If the line is a meaning line,
        elif line.startswith('#'):
            # typical meaning line is `#meaning1,meaning2,meaning3,...`
            meanings = line.rstrip().lstrip('#').split(',')
            meanings = [HW(meaning) for meaning in meanings]
            # Store the (headword, meaning) tuples in temporary wordsOnHand list.
            # They will keep on waiting for the verse.
            # Once verse is added, and a new headword starts, this will be added to result list.
            wordsOnHand.append((headword, meanings))
            # lineType is marked 'm' for meaning.
            lineType.append('m')
        # Pass the lines having some other markers like ;k for kanda, ;v for varga etc.
        elif line.startswith(';end'):
            # Put the last verse, as there will not be any next headword.
            putVerse(verse, wordsOnHand, result)
        elif line.startswith(';'):
            (tag, value) = utils.extract_tag(line)
            if tag == 'p':
                verseDetails.update_pageNum(value)
            if tag == 'k':
                verseDetails.update_kanda(value)
            if tag == 'v':
                verseDetails.update_varga(value)
            if tag == 'vv':
                verseDetails.update_subvarga(value)
        # Lines which are unmarked are verses.
        # The verses may span more than one line too. Therefore adding them up.
        else:
            verse += line + '<BR>'
            # Mark lineType 'v' for verse.
            lineType.append('v')
    return result


def synonymic_list_generator(content):
    """Prepare a list with (headword, meanings, verse, verseNumDetails and pageNumDetails) tuple."""
    # Making it global so that it can be used in other functions too.
    global verseDetails
    # Result will store tuples (headword, meaning, verse)
    result = []
    # Initialize blank verse
    verse = ''
    # lineType list holds 'h', 'm', 'v' for headword, meaning and verse lines.
    lineType = []
    # Read the content into list of lines.
    lines = content.split('\n')
    # A temporary placeholder which will be emptied into result list
    # whenever the verse is allocated to it.
    wordsOnHand = []
    for line in lines:
        # If the line is headword line,
        if line.startswith('#'):
            # If the preceding line was a verse, and current a headword,
            # time to add to result list
            if lineType[-1] == 'v':
                verseDetails.update_verseNum(verse)
                (verse, wordsOnHand, result) = putVerse(verse, wordsOnHand, result)
            # Extract the headword and gender from headword line.
            # Typical headword line is `#headwordList1;gender1:headwordList2:gender2` or `#headwordList;gender` or `#headwordList`
            blocks = line.rstrip().lstrip('#').split(':')
            updateHeadword = True
            for itm in blocks:
                splt = itm.split(';')
                headwords = splt[0]
                if len(splt) == 2:
                    gender = splt[1]
                else:
                    gender = ''
                hwlist = headwords.split(',')
                # This creation of hwlist and meanings is arbitrary.
                # In synonymic dictionaries, there is no headword / meaning.
                # This artificial partition is just to keep the program similar
                # for synonymic and homonymic as much as possible.
                headword = hwlist[0]
                headword = HW(headword, gender)
                meanings = hwlist[1:]
                meanings = [HW(meaning, gender) for meaning in meanings]
                # lineType is appended with 'h' for headword.
                lineType.append('h')
                # Store the (headword, meaning) tuples in temporary wordsOnHand list.
                # They will keep on waiting for the verse.
                # Once verse is added, and a new headword starts, this will be added to result list.
                wordsOnHand.append((headword, meanings))
        # Pass the lines having some other markers like ;k for kanda, ;v for varga etc.
        elif line.startswith(';end'):
            # Put the last verse, as there will not be any next headword.
            putVerse(verse, wordsOnHand, result)
        elif line.startswith(';'):
            (tag, value) = utils.extract_tag(line)
            if tag == 'p':
                verseDetails.update_pageNum(value)
            if tag == 'k':
                verseDetails.update_verseNum(verse)
                (verse, wordsOnHand, result) = putVerse(verse, wordsOnHand, result)
                lineType.append('tag')
                verseDetails.update_kanda(value)
            if tag == 'v':
                verseDetails.update_verseNum(verse)
                (verse, wordsOnHand, result) = putVerse(verse, wordsOnHand, result)
                lineType.append('tag')
                verseDetails.update_varga(value)
            if tag == 'vv':
                verseDetails.update_verseNum(verse)
                (verse, wordsOnHand, result) = putVerse(verse, wordsOnHand, result)
                lineType.append('tag')
                verseDetails.update_subvarga(value)
        # Lines which are unmarked are verses.
        # The verses may span more than one line too. Therefore adding them up.
        else:
            verse += line + '<BR>'
            # Mark lineType 'v' for verse.
            lineType.append('v')
    return result


def write_to_babylon(dictData, fileout):
    """Write to babylon file from dictData.

    Input - List of (headword, meanings, verseNum, pageNum) tuples.
    Output - Properly formatted xyz.babylon file.
    """
    # print(dictData)
    # Prepare the output file
    fout = codecs.open(fileout, 'w', 'utf-8')

    # For each (headword, meanings, verseNumber, PageNum) tuples,
    for (headword, meanings, verse, verseNumDetails, pageNumDetails) in dictData:
        allHeadWords = [headword] + meanings
        allHeadWords = [itm.hw for itm in allHeadWords]
        allHeadWords = unique(allHeadWords)
        piped = '|'.join(allHeadWords)
        commaed = ', '.join(allHeadWords)
        # Write in babylon format. <BR><BR> is to separate verses.
        fout.write(piped + '\n' + headword.hw + ';' + headword.gender + '<BR>' + commaed + '<BR>' + verse + '<BR>verse ' + verseNumDetails + '<BR>page ' + pageNumDetails + '\n\n')
    fout.close()

    # Give some summary to the user
    print('Babylon generated. Success!')
    print('{} headwords written to babylon file.'.format(len(dictData)))


def prepare_hw_dict(dictData):
    """Return the dict with headword as key and 6 details as value."""
    result = defaultdict(list)
    for (headword, meanings, verse, verseNumDetails, pageNumDetails) in dictData:
        allHeadWords = [headword] + meanings
        for itm in allHeadWords:
            result[itm.hw].append((headword.hw, headword.gender, [x.hw for x in meanings], verse, verseNumDetails, pageNumDetails))
    return result


def write_to_json(dictData, fileout):
    """Write to json file from hwData.

    """
    # Prepare the output file
    fout = codecs.open(fileout, 'w', 'utf-8')
    hwDict = prepare_hw_dict(dictData)
    json.dump(hwDict, fout, indent=4, ensure_ascii=False)
    # Give some summary to the user
    print('JSON generated. Success!')
    print('{} headwords written to JSON file.'.format(len(hwDict)))


def write_to_md(dictData, outputDirectory):
    """Write to separate .md files from dictData.

    Input - List of (headword, meanings, verse, verseNum, pageNum) tuples.
    Output - Properly formatted xyz.md file for each headword.
    """
    # Empty the MD folder i.e. outputDirectory
    # See https://github.com/drdhaval2785/sanskrit-lexica-ocr/issues/36
    shutil.rmtree(outputDirectory)
    os.makedirs(outputDirectory)
    # Prepare headword data
    dic = prepare_hw_dict(dictData)
    for hw in dic:
        fileout = os.path.join(outputDirectory, hw + '.md')
        # Prepare the output file
        fout = codecs.open(fileout, 'w', 'utf-8')
        # Write frontmatter
        fout.write('---\ntitle: "' + hw + '"\n---\n\n')
        # For each (headword, meanings, verseNumber, PageNum) tuples,
        for (headword, gender, meanings, verse, verseNumDetails, pageNumDetails) in dic[hw]:
            commaed = ', '.join(meanings)
            verse = verse.replace('<BR>', '<br />')
            # Write in babylon format. <BR><BR> is to separate verses.
            fout.write('# ' + headword + '; ' + gender + '\n## ' + commaed + '\n' + verse + '<br />verse ' + verseNumDetails + '<br />page ' + pageNumDetails +'\n\n')
        fout.close()

    # Give some summary to the user
    print('MD files generated. Success!')
    print('{} separate .md files written, one per headword.'.format(len(dic)))


def write_to_xml(dictData, metadata, xmlfile):
    """Write to xml file from dictData.

    Input - List of (headword, meanings, verse, verseNum, pageNum) tuples.
    Output - Properly formatted .xml file.
    """
    fout = codecs.open(xmlfile, 'w', 'utf-8')
    fout.write('<?xml version = "1.0" encoding = "UTF-8" standalone = "no" ?>\n')
    fout.write('<?xml-stylesheet type="text/xsl" href="maketable.xsl"?>\n')
    fout.write('<root>\n')
    fout.write('<meta>\n')
    for key, value in metadata.items():
        fout.write('<' + key + '>' + value + '</' + key + '>\n')
    fout.write('</meta>\n')
    fout.write('<content>\n')
    for (headword, meanings, verse, verseNumDetails, pageNumDetails) in dictData:
        xmlline = ''
        xmlline += '<word><headword><hw>' + headword.hw + '</hw><gender>' + headword.gender + '</gender></headword><meanings>'
        for meaning in meanings:
            xmlline += '<m><hw>' + meaning.hw + '</hw><gender>' + meaning.gender+ '</gender></m>'
        xmlline += '</meanings>'
        xmlline += '<verse>'
        lines = verse.split('<BR>')
        for line in lines:
            xmlline += '<line>' + line + '</line>'
        xmlline += '</verse>'
        xmlline += '<verseNumber>' + verseNumDetails + '</verseNumber>'
        xmlline += '<pageNumber>' + pageNumDetails + '</pageNumber></word>'
        # Write in babylon format. <BR><BR> is to separate verses.
        fout.write(xmlline + '\n')
        xmlline = ''
    fout.write('</content>\n</root>')
    fout.close()

    # Give some summary to the user
    print('XML file generated. Success!')
    print('{} metadata lines and {} content lines written to XML file.'.format(len(metadata), len(dictData)))


# https://stackoverflow.com/questions/16698935/how-to-transform-an-xml-file-using-xslt-in-python
# Alternative to xsltproc in python.
def write_to_html(xmlfile, xsltfile, htmlfile):
    dom = ET.parse(xmlfile)
    xslt = ET.parse(xsltfile)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    result = ET.tostring(newdom, pretty_print=True)
    fout = codecs.open(htmlfile, 'wb')
    fout.write(result)
    fout.close()
    print('HTML generated. Success!')


def prepare_key1(key2):
    """Generate key1 after stripping unnecessary items from key2 for Cologne."""

    key1 = re.sub(r'[^a-zA-Z]', '', key2)
    return key1


def write_to_cologne(dictData, colognefile):
    """Create Cologne compliant file for a given dictionary code.

    """
    # Prepare the output file
    fout = codecs.open(colognefile, 'w', 'utf-8')
    counter = 1
    # For each (headword, meanings, verseNumber, PageNum) tuples,
    for (headword, meanings, verse, verseNumDetails, pageNumDetails) in dictData:
        # Write for Headword, as it also has some gender information.
        hw = headword.hw
        hw = sanscript.transliterate(hw, 'devanagari', 'slp1')
        key2 = hw
        key1 = prepare_key1(key2)
        gender = headword.gender
        gender = sanscript.transliterate(gender, 'devanagari', 'slp1')
        # Write meta line
        # <L>1<pc>1-001<k1>a<k2>a
        metaline = '<L>' + str(counter) + '<pc>' + pageNumDetails + '<k1>' + key1 + '<k2>' + key2 + '<vn>' + verseNumDetails
        fout.write(metaline + '\n')
        # Write text of entry
        fout.write(hw + ';' + gender + '\n')
        entry = sanscript.transliterate(verse, 'devanagari', 'slp1')
        entry = entry.replace('<BR>', '\n')
        fout.write(entry + '\n')
        fout.write(verseNumDetails + '\n')
        fout.write('<LEND>\n')
        counter += 1
        for meaning in meanings:
            hw = meaning.hw
            gender = meaning.gender
            hw = sanscript.transliterate(hw, 'devanagari', 'slp1')
            key2 = hw
            key1 = prepare_key1(key2)
            # Write meta line
            # <L>1<pc>1-001<k1>a<k2>a
            metaline = '<L>' + str(counter) + '<pc>' + pageNumDetails + '<k1>' + key1 + '<k2>' + key2 + '<vn>' + verseNumDetails
            fout.write(metaline + '\n')
            # Write text of entry
            entry = sanscript.transliterate(verse, 'devanagari', 'slp1')
            entry = entry.replace('<BR>', '\n')
            fout.write(hw + ';' + gender + '\n')
            fout.write(entry + '\n')
            fout.write(verseNumDetails + '\n')
            fout.write('<LEND>\n')
            counter += 1
    fout.close()

    # Give some summary to the user
    print('Cologne file generated. Success!')
    print('{} headwords written to cologne file.'.format(counter))


if __name__ == "__main__":
    # Read the unique code of dictionary from arguments. ENSK
    code = sys.argv[1]
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'orig', bookName + '.txt')
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.read()
    fin.close()
    # Get filename of babylon to store the output
    babylonfile = os.path.join('..', fullName, 'babylon', bookName + '.babylon')
    # Get directory to store MD.
    mdDirectory = os.path.join('..', fullName, 'md')
    # Get directory to store JSON.
    jsonfile = os.path.join('..', fullName, 'json', bookName + '.json')
    # Get filename of xml to store the output
    xmlfile = os.path.join('..', fullName, 'xml', bookName + '.xml')
    # xslt file
    xsltfile = 'maketable.xsl'
    # Get filename of html to store the output
    htmlfile = os.path.join('..', fullName, 'html', bookName + '.html')
    # Get slp file.
    # slpfile = os.path.join('..', fullName, 'slp', bookName + '.txt')
    # Get filename of cologne to store the output
    colognefile = os.path.join('..', fullName, 'cologne', bookName + '.txt')
    # ';CONTENT' is the marker of end of metadata and start of content.
    (metatext, content) = data.split(';CONTENT')
    content = content.lstrip()
    # Read the metadata in a dict
    metadata = utils.prepare_metadata(metatext)
    # decide whether the dictionary is homonymic or synonymic
    nym = metadata['nymic']
    # Initialize a VerseInfo class instance.
    verseDetails = utils.VerseInfo()
    if nym == 'homo':
        # Read the data into a list of (headword, meanings, verse) tuples.
        dictData = homonymic_list_generator(content)
    elif nym == 'syno':
        # Read the data into a list of (headword, meanings, verse) tuples.
        dictData = synonymic_list_generator(content)
    elif nym == 'mixed':
        # It presumes that synonymic content precedes homonymic content
        synomymicContent, homonymicContent = content.split(';nymtype{homo}')
        dictData = synonymic_list_generator(synomymicContent)
        dictData += homonymic_list_generator(homonymicContent)

    # If the user has specified some specific conversion only, do that only.
    if len(sys.argv) > 2:
        conversion = sys.argv[2]
    # If no restriction specified or babylon specified,
    if len(sys.argv) == 2 or conversion == 'babylon':
        # Write to babylon file.
        write_to_babylon(dictData, babylonfile)
    # If no restriction specified or md specified,
    if len(sys.argv) == 2 or conversion == 'md':
        # Write individual .md files into mdDirectory.
        write_to_md(dictData, mdDirectory)
    # If no restriction specified or xml specified,
    if len(sys.argv) == 2 or conversion == 'xml':
        # Write to xml file.
        write_to_xml(dictData, metadata, xmlfile)
    # If no restriction specified or html specified,
    if len(sys.argv) == 2 or conversion == 'html':
        # Create HTMl file from xml and xslt files.
        write_to_html(xmlfile, xsltfile, htmlfile)
    # If no restriction specified or html specified,
    if len(sys.argv) == 2 or conversion == 'json':
        # Create JSON file.
        write_to_json(dictData, jsonfile)
    # If no restriction specified or html specified,
    if len(sys.argv) == 2 or conversion == 'cologne':
        # Create cologne file.
        write_to_cologne(dictData, colognefile)

    print('1. Use `stardict-editor` to convert babylon to stardict files.')
    print('2. After conversion, put dict.dz, idx, ifo and syn files in stardict folder.')
    print('3. Put the md files inside ../../kosha-hugo2/content/{dictcode} folder.')
    print('4. Run ./deploy.sh "your commit message" in kosha-hugo2 repository to generate and upload statically generated hugo website to sanskrit-kosha.github.io/ .')
