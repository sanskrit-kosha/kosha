# -*- coding: utf-8 -*-
import os
import utils
import codecs
import json
import re


def replace_colon(code):
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'orig', bookName + '.txt')
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.read()
    fin.close()
    data = re.sub(r'([^ps]):', r'\g<1>ः', data)
    directory = os.path.join('..', fullName, 'orig')
    if not os.path.exists(directory):
        os.mkdir(directory)
    fileout = os.path.join(directory, bookName + '.txt')
    fout = codecs.open(fileout, 'w', 'utf-8')
    fout.write(data)
    fout.close()


if __name__ == "__main__":
    print(utils.timestamp())
    with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
        dictcodes = json.load(fin)
    for code in dictcodes:
        print(code)
        replace_colon(code)
    print(utils.timestamp())
