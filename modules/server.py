from flask import json, request
import spacy
from modules import dictionary
import logging
from typing import Dict, Any

log = logging.getLogger(__name__)

goldenDictionary = dictionary.Dict()
goldenWordsList = []
nlp = None

mindState = {
    "status": "ok",
    "me": {
        "state": "ok"
    },
    "talker": {},
    "author": {},
    "last_sentence": {},
    "current_topic": {},
    "last_noun": {},
    "last_subject": {},
    "last_object": {}
}


# functions ------------------------------------------------

def init(path):
    global nlp
    global goldenWordsList
    nlp = spacy.load(path + 'vocabby')
    goldenDictionary.load(path + 'dict.json')

    with open(path + 'dict-gw.json') as fileLoaded:
        goldenWordsList = json.load(fileLoaded)

    if len(goldenWordsList) == 0:
        log.info('goldenWordsList is empty')


def findVocabId(word):
    return nlp.vocab[word.lower()].orth


def findWordById(id):
    return nlp.vocab[int(id)].text


def prepareOutput(token, word):
    wordIsGolden = word["id"] is not None and word["id"] in goldenWordsList

    if token.lemma in goldenWordsList or wordIsGolden:
        if word["text"] is not None:
            output = '[' + word["text"].upper() + ']'
        else:
            output = '[' + token.lemma_.upper() + ']'
    else:
        output = token.lemma_

    return output


def findMatchingWord(token):
    word = {
        "id": None,
        "text": None
    }

    word["id"] = goldenDictionary.findValue(token.lemma)

    if word["id"] is not None:
        word["text"] = findWordById(word["id"])

    return word


def sayRequestProcessor():
    global mindState
    global nlp
    phrase = request.form.get('phrase')
    output = ''
    phraseDoc = nlp(phrase)

    # travel through the phrase, token by token
    for token in phraseDoc:

        token2Output = prepareOutput(token, findMatchingWord(token))

        if token2Output != '' and output != '':
            output = output + ', '

        output = output + token2Output

    return json.dumps(
        {'answer': output, 'success': True, 'mind': mindState}), 201
