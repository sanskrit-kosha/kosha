# -*- coding: utf-8 -*-
"""Search in all dictionaries.

Current version is being developed in kosha-trial repository.
This version is being put in legacy folder.
"""
import os
import codecs
import re
import json
import utils
from flask import Flask, jsonify
from flask_restplus import Api, Resource, reqparse
from flask_cors import CORS
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

# Start Flask app.
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# Show request duration.
app.config.SWAGGER_UI_REQUEST_DURATION = True
CORS(app)
apiversion = 'v0.0.1'
api = Api(app, version=apiversion, title=u'Sanskrit-kosha API', description='Provides APIs to Sanskrit-kosha.')


def preprocess(text):
    """Gives query friendly string."""
    text = text.rstrip('HM')  # SamBuH -> SamBu
    text = re.sub(r'[aAiIuUfFxXeEoO]$', r'', text)  # pAragata -> pAragat
    text = re.sub(r'^[aAiIuUfFxXeEoO]', r'', text)  # azwaka -> zwaka
    text = re.sub(r'a[tsn]$', r'', text)  # Bagavat -> Bagav, Sreyas -> Srey, suDarman -> suDarm
    text = re.sub(r'in$', r'', text)  # kevalin -> keval
    text = re.sub(r'[td]$', r'', text)  # tIrTakft -> tIrTakf (to handle t/d conversion issues)
    print(text)
    return text


def search_in_dict(query, code):
    # ENSK -> ekaksharanamamala_sadhukalashagani
    fullName = utils.code_to_dict(code)
    # ekaksharanamamala, sadhukalashagani
    bookName, author = fullName.split('_')
    # Read the .txt file
    filein = os.path.join('..', fullName, 'slp', bookName + '.txt')
    result = []
    verseDetails = utils.VerseInfo()
    verse = ''
    writeVerse = False
    for lin in codecs.open(filein, 'r', 'utf-8'):
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
        elif re.search(r'^[$#]', lin):
            pass
        else:
            verse += lin
            if query in lin:
                writeVerse = True
            if '..' in lin:
                verseDetails.update_verseNum(verse)
                if writeVerse:
                    page = verseDetails.give_page_details()
                    kanda = verseDetails.kanda
                    varga = verseDetails.varga
                    adhyaya = verseDetails.subvarga
                    versenum = verseDetails.verseNum
                    result.append({'verse': verse, 'page': page, 'versenum': versenum, 'kanda': kanda, 'varga': varga, 'adhyaya': adhyaya})
                writeVerse = False
                verse = ''
    return result


def search_in_all(query):
    output = {}
    with codecs.open('workingdicts.json', 'r', 'utf-8') as fin:
        dictcodes = json.load(fin)
    for code, fullname in dictcodes.items():
        result = search_in_dict(query, code)
        if len(result) > 0:
            output[code] = result
    return output


def dictcode_to_dict():
    with codecs.open('workingdicts.json', 'r', 'utf-8') as fin:
        dictcodes = json.load(fin)
    return dictcodes


@api.route('/' + apiversion + '/dictcode')
class DC(Resource):
    """Return the dictcode and full form of all dictionaries."""

    get_parser = reqparse.RequestParser()

    @api.expect(get_parser, validate=True)
    def get(self):
        result = dictcode_to_dict()
        return jsonify(result)


@api.route('/' + apiversion + '/dictslp')
class DS(Resource):
    """Return the dictcode and full form of all dictionaries in slp1."""

    get_parser = reqparse.RequestParser()

    @api.expect(get_parser, validate=True)
    def get(self):
        with codecs.open('dictcode_slp.json', 'r', 'utf-8') as fin:
            result = json.load(fin)
        return jsonify(result)


@api.route('/' + apiversion + '/query/<string:query>')
@api.doc(params={'query': 'Word to search.'})
class QD(Resource):
    """Return result for given query in all koshas."""

    get_parser = reqparse.RequestParser()

    @api.expect(get_parser, validate=True)
    def get(self, query):
        result = search_in_all(query)
        return jsonify(result)


@api.route('/' + apiversion + '/query/<string:query>/koshas/<string:kosha>')
@api.doc(params={'query': 'Word to search.', 'kosha': 'Dictionary code.'})
class QD1(Resource):
    """Return result for given query in given dictionary."""

    get_parser = reqparse.RequestParser()

    @api.expect(get_parser, validate=True)
    def get(self, query, kosha):
        result = search_in_dict(query, kosha)
        return jsonify({kosha: result})


if __name__ == "__main__":
    app.run(debug=True)
