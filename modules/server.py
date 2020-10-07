from flask import json, request, session
import spacy
from modules import dictionary
import logging
from modules import mind as mindModule

log = logging.getLogger(__name__)

wordsDictionary = dictionary.Dict()
hyperonymList = []
nlp = None


# functions ------------------------------------------------


def sayRequestProcessor(api: object):
    global nlp
    mind = mindModule.Mind(nlp, wordsDictionary, hyperonymList, api)

    mind.loadFromSession(session)

    mind.analyzePhrase(request.form.get("phrase"))

    mind.saveToSession(session)

    return json.dumps({"answer": mind.getProcessedPhrase(), "success": True}), 201


# -------


def init(path):
    global nlp
    global hyperonymList
    nlp = spacy.load(path + "vocabby")
    wordsDictionary.load(path + "dict.json")

    with open(path + "dict-gw.json") as fileLoaded:
        hyperonymList = json.load(fileLoaded)

    if len(hyperonymList) == 0:
        log.info("hyperonymList is empty")
