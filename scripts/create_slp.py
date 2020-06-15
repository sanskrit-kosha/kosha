# -*- coding: utf-8 -*-
"""Create SLP1 version of all files.

Usage - python3 create_slp.py
"""
import os
import utils
import codecs
import json
from indic_transliteration import sanscript


def create_slp(code):
    """Create SLP file for a given dictionary code.

    code is to be selected from dictcode.json.
    """
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'orig', bookName + '.txt')
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.read()
    fin.close()
    # Convert the data to SLP1.
    data = sanscript.transliterate(data, 'devanagari', 'slp1')
    # Output directory
    directory = os.path.join('..', fullName, 'slp')
    # Create if the directory does not exist.
    if not os.path.exists(directory):
        os.mkdir(directory)
    fileout = os.path.join(directory, bookName + '.txt')
    # Create output file and save the SLP data in it.
    fout = codecs.open(fileout, 'w', 'utf-8')
    fout.write(data)
    fout.close()


if __name__ == "__main__":
    print(utils.timestamp())
    # Load the codes from workingdicts.json.
    # workingdicts.json holds already proofread files.
    # You can also use codes from dictcodes.json file for non proofread files.
    with codecs.open('workingdicts.json', 'r', 'utf-8') as fin:
        dictcodes = json.load(fin)
    # For each dictionary code, create SLP file.
    for code in dictcodes:
        print(code)
        create_slp(code)
    print(utils.timestamp())
