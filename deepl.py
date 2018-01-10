# coding: utf-8
"""
Translate a text using deepl API.
"""
from __future__ import print_function
import sys
import pydeepl
import nltk.data
import begin

reload(sys)
sys.setdefaultencoding('utf-8')


def read_file(filename, limit=None):
    r = []
    for i, line in enumerate(open(filename).readlines()):
        if limit and i >= limit:
            return r
        r.append(line.decode("utf-8"))
    return r


def translate(line, to_language, from_language=None):
    prefix = ""

    if line.startswith("> ") or line.startswith("- "):
        prefix = line[:2]
        line = line[2:]

    translation = pydeepl.translate(line, to_language, from_lang=from_language)
    return prefix + translation

@begin.start(auto_convert=True)
def translate_file(filename, to_language="EN", from_language=None, limit=None):

    if from_language == "DE":
        sent_detector = nltk.data.load('tokenizers/punkt/german.pickle')
    elif from_language == "EN":
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    elif from_language is None:  # yolo
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    for line in read_file(filename, limit=limit):
        if line:
            for sentence in sent_detector.tokenize(line.strip()):
                translation = translate(sentence, to_language, from_language)
                if translation:
                    print(translation, end=' ')
                else:
                    print(sentence, end=' ')
        else:
            print(line)
        print("")


