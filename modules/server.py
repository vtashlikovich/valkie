from flask import json, request
import spacy
from modules import dictionary
import sys, logging

log = logging.getLogger(__name__)

dict = dictionary.Dict()
goldenWordsList = []
nlp = None

WORD_HI = 'hi'

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

def init(path):
    log.info('OOOOOOK')
    global nlp
    global goldenWordsList
    global api
    nlp = spacy.load(path + 'vocabby')
    dict.load(path + 'dict.json')

    with open(path + 'dict-gw.json') as fileLoaded:
        goldenWordsList = json.load(fileLoaded)

    if len(goldenWordsList) == 0:
        log.info('goldenWordsList is empty')

    log.info('OOOOOOK')

def findVocabId(word):
    return nlp.vocab[word.lower()].orth

def findWordById(id):
    return nlp.vocab[int(id)].text

def sayRequestProcessor():
    global mindState
    global nlp
    phrase = request.form.get('phrase')
    output = ''
    phraseDoc = nlp(phrase)

    log.info('BOOM')

    for token in phraseDoc:
        print('token: ' + str(token.lemma))
        goldenWordId = dict.findValue(token.lemma)
        print('found: ' + str(goldenWordId))

        goldenWord = ''
        if goldenWordId != None:
            goldenWord = findWordById(goldenWordId)

        if output != '':
            output = output + ', '

        print(goldenWordsList)
        if token.lemma in goldenWordsList or goldenWordId in goldenWordsList:
            if goldenWord != None:
                output = output + '[' + goldenWord.upper() + ']'
            else:
                output = output + '[' + lemma_.upper() + ']'
        else:
            output = output + token.lemma_

    return json.dumps(
    {
        "answer": output,
        "success": True,
        "mind": mindState
    }), 201