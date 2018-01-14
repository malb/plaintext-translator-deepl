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

    try:
        translation = pydeepl.translate(line, to_language, from_lang=from_language)
    except (IndexError, pydeepl.TranslationError) as e:
        raise pydeepl.TranslationError(e.message)
    if not translation:
        raise pydeepl.TranslationError

    return prefix + translation

def count_words(text):
    return len(text.split(" "))

def split(line, sentence_detector=None, max_words=60):
    if sentence_detector is None:
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    line = sentence_detector.tokenize(line.strip())

    line_ = []
    for sentence in line:
        if count_words(sentence) <= max_words:
            line_.append(sentence)
        else:
            for part in sentence.split(";"):
                if count_words(part) <= max_words:
                    line_.append(part + ";")
                else:
                    for subpart in sentence.split(","):
                        line_.append(subpart + ",")

    return tuple(line_)

@begin.start(auto_convert=True)
def translate_file(filename, to_language="EN", from_language=None, limit=None):

    if from_language == "DE":
        sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')
    elif from_language == "EN":
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    elif from_language is None:  # yolo
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    for line in read_file(filename, limit=limit):
        if line:
            for sentence in split(line.strip(), sentence_detector=sentence_detector):
                try:
                    print(translate(sentence, to_language, from_language), end=' ')
                except pydeepl.TranslationError:
                    print(sentence, end=' ')
        else:
            print(line)
        print("")


