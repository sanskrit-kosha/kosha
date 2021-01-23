# -*- coding: utf-8 -*-
"""Annotate koshas automatically.

Usage 1 - python3 kosha_annotator.py
It annotates all dictionaries afresh.

Usage 2 - python3 kosha_annotator.py CODE
e.g python3 kosha_annotator.py AMAR
"""
import re
import os
import sys
import codecs
import datetime
import json
from math import log
from indic_transliteration import sanscript
import utils


# Function to return timestamp
def timestamp():
    return datetime.datetime.now()


# Known stopwords.
stopwords = set(['mata', 'ca', 'vidu', 'sa', 'jYeya', 'tatra', 'smfta', 'tu', 'aTa', 'api', 'strI', 'striyA', 'na', 'taTA', 'syAt', 'puMsi', 'nA', 'trizu', 'astrI', 'nari', 'sA', 'ukta', 'ya', 'puna', 'Bavet', 'klIba', 'sama', 'cATa', 'ityapi','?', 'para', 'astriyA', 'antya', 'prokta', 'asO', 'syu', 'hi', 'zaRQa', 'eva', 'tadvat', 'vA', 'tat', 'yoziti', 'prakIrtita', 'prakIrttita', 'Bavati', 'samO', 'dvaMdva', 'iti', 'sta', 'syAcca', 'Irita', 'yat', 'atra', 'striyO', 'iha', 'yasya', 'tasya', 'yA', 'nigadyata', 'dvO', 'yadi', 'asya', 'tritaya', 'dva', 'yaTA', 'taTA', 'cApyaTa', 'cA', 'ete', 'amI', 'amUni', 'pumAn', 'zaR', 'kramAt', 'sEva', 'napuMsaka', 'samA', 'cEva', 'paryAya', 'kIrtita', 'cAnyatra', 'ity', 'avyaya', 'kaTyata', 'vartata', 'ucyata', 'procyata', 'tri', 'aya', 'napuMs', 'pumAnBavet', 'pu', 'napu', 'pumAnaya', 'puMnapuMsi', 'cezyata', 'pracakzyata', 'striyAmapi', 'tattri', 'trizUcyata', 'tatstriyA', 'tatklIba', 'tatparikIrtita', 'parikIrtita', 'kIrtyata', 'paricakzyata', 'pracakzata', 'cAvyaya', 'puMnapuMsakayorapi', 'klI', 'zaR', 'Irita', 'tadIrita', 'Bedyavat', 'napi', 'striyAmiya', 'nap', '\u200c', 'nap\u200c', 'pumA', 'punastri', 'nfliNgaka', 'dvayoraya', 'stryarTa', 'apaWIt', 'nfSaRqa', 'punardva', 'pulli~Nga', 'aBiDeyavat', 'manvata', 'dfSyata', 'BedyaliNgaka', 'Baved', 'raBasastvAha', 'nfstri', 'napyada', 'brUta', 'ityaya', 'Sabdavittama', 'kezucit', 'punnapuMsaka', 'ityAha', 'abravIt', 'Sabdavit', 'ajayastvAha', 'punnapa', 'nfstrI', 'ityeza', 'smaret', 'vidyAt', 'cApara', 'strIRA', 'pumAYjYeya', 'nfliNga', 'napstri', 'trirnA', 'iya', 'cAnya', 'pumAMstri', 'prAhu', 'Ahu', 'manIziBi', 'strISaRqa', 'cAha', 'eza', 'raBasa', 'dvaya', 'anya', 'tadvat', 'BedyaliNga', 'vijYeya', 'prAha', 'samAsAdi', 'Aha', 'eza', 'ada', 'taTEva', 'samAsAdyatra', 'smfta', 'kecana', 'kecit', 'yadA', 'kaScit', 'jYeya', 'BUmni', 'ceti', 'Sruta', 'KyAta', 'kvacit', 'strIliNga', 'bahuvrIhi', 'samAsAdIni', 'klIbaliNga', 'anA', 'BAzita', 'kaTita', 'apara', 'ityeva', 'kIrtita', 'etat', 'kutracit', 'vE', 'ida', 'viKyAta', 'kramataH'])


def readwords(dictionary):
    return codecs.open(dictionary, 'r', 'utf-8').read().split()


# Read all headwords in list.
basewords = readwords('allheadwords.txt')
# Create a set. Searching for membership in set is very speedy.
base = set(basewords)
# wordcost and maxword are used for infer_spaces function.
# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
wordcost = dict((k, log((i+1)*log(len(basewords)))) for i,k in enumerate(basewords))
maxword = max(len(x) for x in basewords)


def prep_line(inputline):
    """Prepare the line before it is split into words by spaces."""
    inputline = inputline.rstrip()  # Remove trailing whitespaces.
    # Convert to SLP1.
    inputline = sanscript.transliterate(inputline, 'devanagari', 'slp1')
    inputline = inputline.replace('izyate', '')
    inputline = re.sub(r"([oe])'", r"\g<1> a", inputline)  # kumAro'zwa
    inputline = inputline.replace(r"A'", r"A a")  # kumAro'zwa
    inputline = re.sub(r'YS', r'n S', inputline)  # SreyAYSreyAMsaH->SreyAn SreyAMSaH
    inputline = inputline.replace('ScA', 'H a')  # samudravijayaSCASvasenaH->samudravijayaH aSvasenaH
    inputline = inputline.replace('SC', 'H C')  # mfgaSCAgaH->mfgaH CAgaH
    inputline = inputline.replace(r"ATa ", r"A aTa ")  # naradattATa->naradattA aTa
    inputline = inputline.replace('stva', ' a')  # atihAsastvanusyUtaH->atihAsa anusyUtaH
    inputline = inputline.replace(' ca ', ' ')
    # '+' and '.' is usually used for denoting undecipherable texts.
    inputline = re.sub('[+.]*', '', inputline)
    return inputline


def prep_word(word):
    """Make changes to words after the split."""
    word = re.sub(r'stataH$', r'', word)  # sumatistataH->sumati
    word = re.sub(r'ABiD[aA][H]$', r'a', word)  # padmapraBABiDaH->padmapraBa
    word = re.sub(r'AKy[aA][H]$', r'a', word)  # yaSoDarAKyaH->yaSoDara
    word = re.sub(r'ityapi$', r'', word)  # kurujANgalamityapi->kurujANgalam
    word = re.sub(r'^pumAn', r'', word)  # pumAnvizaye->vizaye
    word = re.sub(r'zu$', r'', word)  # kIrtizu->kIrti
    word = re.sub(r'nA[mM]$', r'', word)  # bAlAnAm->bAlA
    word = re.sub(r'([^aAiIuUfFxXeEoO])yA[mM]$', r'\g<1>I', word)  # lakzmyAm->lakzmI
    word = re.sub(r'Avapi$', r'i', word)  # maRAvapi->maRi
    word = re.sub(r'etyapi$', r'A', word)  # Kadiretyapi->KadirA
    word = re.sub(r'^tv', r'', word)  # tvindriya->indriya
    word = re.sub(r'AyA[mM]$', r'A', word)  # viSalyAyAm->viSalyA
    word = re.sub(r'Ani$', r'a', word)  # praDAnAni->praDAna
    word = re.sub(r'yoH$', r'', word)
    word = re.sub(r'ezu$', r'a', word)
    word = re.sub(r'Iti$', r'I', word)  # nandinIti->nandinI
    word = re.sub(r'a[Rn]i$', r'an', word)  # janmani->janman
    word = re.sub(r'([Ao])pyaTa$', r'\g<1>', word)  # vESezikopyaTa->vESeziko
    word = re.sub(r'([^aAiIuUfFxeEoO])yapi$', r'\g<1>I', word)  # kzatriyARyapi->kzatriyARI
    word = re.sub(r'[S]cATa$', r'', word)  # piRqItakaScATa->piRqItaka
    word = re.sub(r'apyaTa$', r'', word)  # tamAlapatramaTa->tamAlapatram
    word = re.sub(r'aTa$', r'', word)  # tamAlapatramaTa->tamAlapatram
    word = re.sub(r'antu$', r'a', word)  # sOraByantu->sOraBya
    word = re.sub(r'^puMsy', r'', word)  # puMsyutkoca->utkoca
    word = re.sub(r'^syA[tdnl]', r'', word)  # syAdavarohaH->avarohaH
    word = re.sub(r'^tad([aA])', r'\g<1>', word)  # tadAsTAnaM->AsTAnaM
    word = re.sub(r'([iu])rapi$', r'\g<1>', word)  # parizwirapi->parizwi
    word = re.sub(r'astriyA[mM]$', r'', word)  # udDAramastriyAm->udDAram
    word = re.sub(r'stu$', r'', word)  # sarvArTasidDastu->sarvArTasidDa
    word = re.sub(r'[Ao]pi$', r'a', word)  # bfhatikApi->bfhatikA
    word = re.sub(r'ASca$', r'a', word)  # pUjitASca->pUjita
    word = re.sub(r'ScEva$', r'', word)  # plavagaScEva->plavaga
    word = re.sub(r'^trizv', r'', word)  # trizvADAne->ADAne
    word = re.sub(r'^Baved', r'', word)  # BavedAmalakI->AmalakI
    word = re.sub(r'eva$', r'', word)  # vanameva->vanam
    word = re.sub(r'^apy', r'', word)  # apyaDokzajaH->aDokzajaH
    word = re.sub(r'Sca$', r'', word)  # prARaSca->prARa
    word = re.sub(r'taTA$', r'', word)  # yAtuDAnastaTA->yAtuDAnas
    word = re.sub(r'yaT[ao]$', r'I', word)  # svAmyaTo->svAmI
    word = re.sub(r'yaT[ao]$', r'I', word)  # svAmyaTo->svAmI
    word = re.sub(r'^[0123456789.}\]]+$', r'', word)
    word = re.sub(r'EH', r'a', word)  # nAgarEH->nAgara
    word = re.sub(r'AH$', r'a', word)  # KarAH->Kara
    word = re.sub(r'[HMmsr]$', r'', word)  # Remove trailing visarga, anusvara.
    word = re.sub(r'[e]$', r'a', word)  # deSe->deSa
    word = re.sub(r'o$', r'a', word)  # padmo->padma
    word = re.sub(r'^puMsy', r'', word)  # puMsyABizavaH->ABizavaH
    word = re.sub(r'AdO$', r'Adi', word)  # lakzAdO->lakzAdi
    # Ignore the stopwords
    if word in stopwords:
        word = ''
    # If the word is not in known headwords, but their changes are in HW.
    if word.endswith('O'):
        word1 = re.sub(r'O$', r'u', word)  # SiSO->SiSu
        word2 = re.sub(r'O$', r'i', word)  # vahnO->vahni
        word3 = re.sub(r'O$', r'a', word)  # gaRqakO->gaRqaka
        if word1 in base:
            word = word1
        elif word2 in base:
            word = word2
        elif word3 in base:
            word = word3
    if word.endswith('A'):
        word3 = re.sub(r'A$', r'a', word)  # SukraSizyA->SukraSizya
        if word not in base and word3 in base:
            word = word3
    if word.endswith('I'):
        word4 = re.sub(r'I$', r'in', word)  # DarmaDvajI->DarmaDvajin
        if word not in base and word4 in base:
            word = word4
    if word.endswith('ava'):
        word5 = re.sub(r'ava$', r'u', word)  # fBavav->fBu
        if word not in base and word5 in base:
            word = word5
    if word.endswith('a'):
        word6 = re.sub(r'a$', r'', word)  # kratuBuja->kratuBuj
        if word not in base and word6 in base:
            word = word6
        word6 = re.sub(r'a$', r'A', word)  # gaRadevata->gaRadevatA
        if word not in base and word6 in base:
            word = word6
    if word.endswith('aya'):
        word7 = re.sub(r'aya$', r'i', word)  # dAnavAraya->dAnavAri
        if word not in base and word7 in base:
            word = word7
    if word.endswith('i'):
        word8 = re.sub(r'i$', r'', word)  # vihAyasi->vihAyas
        if word not in base and word8 in base:
            word = word8
    return word


def words_from_line(inputline, base):
    """Return prepared words from given line."""
    # Prepare input line.
    inputline = prep_line(inputline)
    # Split line at known delimiters.
    words = re.split(r'[ \'\-]', inputline)
    # Apply changes to words.
    words = [prep_word(a) for a in words]
    # Ignore empty words
    words = [a for a in words if a != '']
    return words


# http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words/11642687#11642687
def infer_spaces(s, maxword, wordcost):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""
    # Build a cost dictionary,
    # assuming Zipf's law and cost = -math.log(probability).
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        return min((c + wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k:i])
        i -= k
    # return "+".join(reversed(out))
    return list(reversed(out))


def space_inferre_correctly(lst):
    for itm in lst:
        if itm not in base:
            return False
    return True


def annotate_0(filein, fileout):
    """Annotate filein and return fileout."""
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')

    c1 = 0  # Counter for headwords in basewords. Some confidence.
    c2 = 0  # Counter for headwords not in basewords. Mostly need intervention.
    # For each line in input file,
    for inputline in fin:
        # If it starts with '[;#$]', no further intervention is needed.
        if re.search('^[;#$]', inputline):
            fout.write(inputline)
        else:
            # Read words from line.
            words = words_from_line(inputline, base)
            # Initialize two lists of OK and suspect words.
            oklist = []
            suspectlist = []
            # For each word,
            for word in words:
                # Transliterate to SLP1.
                deva = sanscript.transliterate(word, 'slp1', 'devanagari')
                # If word is in the known dictionary headwords, it is OK.
                if word in base:
                    # Write to the output file with tag 1 i.e. OK.
                    fout.write(deva + ':1\n')
                    # Append to OK list.
                    oklist.append(deva)
                    # Increment counter.
                    c1 += 1
                else:
                    # Write to the output file with tag 2 i.e. suspect words.
                    fout.write(deva + ':2\n')
                    # Append to suspect list.
                    suspectlist.append(deva)
                    # Increment counter.
                    c2 += 1
            # Write the verse as it is in the output file.
            words = [sanscript.transliterate(a, 'slp1', 'devanagari') for a in words]
            # fout.write(','.join(words) + '\n')
            fout.write('#' + inputline + '\n')
    # Close files.
    fin.close()
    fout.close()
    # Calculate statistics and display.
    print(c1, '\t', c2, '\t', (c1 / (c1 + c2)) * 100)


def annotate_1(filein, fileout):
    """Annotate filein and return fileout."""
    fin = codecs.open(filein, 'r', 'utf-8')
    fout = codecs.open(fileout, 'w', 'utf-8')

    c1 = 0  # Counter for headwords in basewords. Some confidence.
    c2 = 0  # Counter for headwords not in basewords. Mostly need intervention.
    # For each line in input file,
    for inputline in fin:
        if re.search(':1', inputline):
            fout.write(inputline)
            c1 += 1
        elif re.search(':2', inputline):
            # Initialize two lists of OK and suspect words.
            deva = re.split(':', inputline)[0]
            # Transliterate to SLP1.
            word = sanscript.transliterate(deva, 'devanagari', 'slp1')
            calculated = infer_spaces(word, maxword, wordcost)
            goodInference = True
            for calc in calculated:
                if calc not in base:
                    goodInference = False
                if len(calc) < 4:
                    goodInference = False
            if goodInference:
                for calc in calculated:
                # Write to the output file with tag 3 i.e. inferred words.
                    deva = sanscript.transliterate(calc, 'slp1', 'devanagari')
                    fout.write(deva + ':3\n')
                    # Increment counter.
                    c1 += 1
            else:
                # Write to the output file with tag 2 i.e. suspect words.
                fout.write(deva + ':2\n')
                # Increment counter.
                c2 += 1
                # Write the verse as it is in the output file.
        else:
            fout.write(inputline)
    # Close files.
    fin.close()
    fout.close()
    # Calculate statistics and display.
    print(c1, '\t', c2, '\t', (c1 / (c1 + c2)) * 100)


def apply_annotation0(code):
    """Apply autoannotation to the dictionary corresponding to given code."""
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'orig', bookName + '.txt')
    # Create output file.
    directory = os.path.join('..', fullName, 'annotated')
    if not os.path.exists(directory):
        os.mkdir(directory)
    fileout = os.path.join(directory, code + '0.txt')
    # Annotate the filein and store in fileout.
    annotate_0(filein, fileout)


def apply_annotation1(code):
    """Apply autoannotation to the dictionary corresponding to given code."""
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'annotated', code + '0.txt')
    # Create output file.
    fileout = os.path.join('..', fullName, 'annotated', code + '1.txt')
    # Annotate the filein and store in fileout.
    annotate_1(filein, fileout)


if __name__ == "__main__":
    # If the user has specified some code to annotate,
    if len(sys.argv) > 1:
        code = sys.argv[1]
        print(code)
        # Annotate level 0.
        # apply_annotation0(code)
        # Annotate level 1.
        apply_annotation1(code)
    # If no code is specified, run on all dictioanries.
    else:
        with codecs.open('workingdicts.json', 'r', 'utf-8') as fin:
            codes = json.load(fin)
            # For each proofread dictionary,
            for code in codes:
                print(code)
                # Annotate level 0.
                # apply_annotation0(code)
                # Annotate level 1.
                apply_annotation1(code)
