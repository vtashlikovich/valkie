from spacy.tokens import Token
from modules import dictionary

WORD_SEPARATOR = ' '
devSAOList = [
    ['ROUTINE', 'READ', 'DATA'],
    ['ROUTINE', 'PRINT', 'DATA'],
]


class Mind:

    def __init__(self, nlp, wordsDictionary: dictionary, hyperonymList: list):
        self.nlp = nlp
        self.wordsDictionary = wordsDictionary
        self.hyperonymList = hyperonymList
        self.state = self.getDefaultState()
        self.processedPhrase = self.getDefaultPhraseStorage()
        self.topics = []
        self.algorithm = []

    def processPhrase(self, phrase: str) -> dict or None:
        self.processedPhrase = self.getDefaultPhraseStorage()

        if phrase == ':clear':
            self.clear()
            return None

        # ---------------
        # ACTION

        # replace "it", etc with current context topics
        phrase = self.processItPronoun(phrase)

        # TODO: [the (det) topic] can be replaced with object/noun/topic already described
        # TODO: [a/an topic] must create new topic

        self.processedPhrase['phrase'] = phrase

        # travel through the phrase, token by token
        phraseDoc = self.nlp(phrase)
        phraseSAO = []
        for token in phraseDoc:

            # process each token
            t_lemma, t_hyperonim, t_pos, t_tag, t_dep = self.prepareTokenOutput(token, self.findMatchingWord(token))

            self.processedPhrase['tagged_phrase'].append((t_lemma, t_hyperonim, t_pos, t_tag, t_dep))

            if self.isTokenFromSAO(t_pos, t_dep):
                phraseSAO.append(t_hyperonim)

            # maintain a list of topics - nouns = files, methods, programs, data, etc.
            # remember the last noun
            if t_pos == 'NOUN':
                self.rememberTopic(t_hyperonim)
                self.setLast('noun', t_lemma)

        self.processedPhrase['sao'] = phraseSAO

        # let's find matching SAO's
        # put determined SAO into the algorithm flow
        if phraseSAO and phraseSAO in devSAOList:
            self.processedPhrase['devsao_detected'] = True
            self.state['algorithm'].append(phraseSAO)

        self.processedPhrase['topics'] = self.state['topics']
        self.processedPhrase['algorithm'] = self.state['algorithm']

        # TODO: if no matching SAO's let's find the closest ones: SA*, S*O, *AO, etc.

        # TODO: ask about previous duplicated SAO's

        # TODO: let's check what SAO may require as additional attrs

        # TODO: let's create a list of missing attrs for matching SAO

        # TODO: ask questions for missing attrs

    def processItPronoun(self, phrase: str) -> str:
        newPhrase = ''
        phraseDoc = self.nlp(phrase)
        for token in phraseDoc:

            word4NewPhrase = token.text

            if token.tag_ == 'PRP' and token.text.lower() == 'it' and self.getLast('noun') is not None:
                word4NewPhrase = self.getLast('noun')

            if len(newPhrase) > 0 and token.pos_ != 'PUNCT':
                newPhrase += ' '
            newPhrase += word4NewPhrase

        return newPhrase

    def prepareTokenOutput(self, token: Token, word: dict) -> tuple:
        wordIsHyperonym = word["id"] is not None and word["id"] in self.hyperonymList
        determinedHyperonim = token.lemma_.upper()

        # tokenLemma = token.lemma_
        # tokenPos = ':' + token.pos_ + ':' + token.tag_ + ':' + token.dep_

        if token.lemma in self.hyperonymList or wordIsHyperonym:
            if word["text"] is not None:
                determinedHyperonim = word["text"].upper()
            # output = tokenLemma + '<span style="color:#b6b9c2">[' + determinedHyperonim + tokenAddon + ']</span>'
        # else:
        #     output = tokenLemma + '<span style="color:#b6b9c2">' + tokenAddon + '</span>'

        return token.lemma_, determinedHyperonim, token.pos_, token.tag_, token.dep_

    def findMatchingWord(self, token: Token) -> dict:
        word = dict({
            "id": None,
            "text": None
        })

        word["id"] = self.wordsDictionary.findValue(token.lemma)

        if word["id"] is not None:
            word["text"] = self.findWordById(word["id"])

        return word

    @staticmethod
    def getDefaultPhraseStorage():
        return {
            'phrase': '',
            'tagged_phrase': [],
            'sao': [],
            'devsao_detected': False,
            'topics': None,
            'algorithm': None
        }

    def findVocabId(self, word: str) -> int:
        return self.nlp.vocab[word.lower()].orth

    def findWordById(self, searchId: int) -> str:
        return self.nlp.vocab[int(searchId)].text

    def getProcessedPhrase(self) -> dict:
        return self.processedPhrase

    def saveToSession(self, session):
        session['state'] = self.state

    def loadFromSession(self, session):
        if 'state' in session:
            self.state = session['state']

    def getLast(self, key: str) -> str or None:
        result = None
        if key in self.state['last']:
            result = self.state['last'][key]

        return result

    def setLast(self, key: str, value: str):
        self.state['last'][key] = value

    @staticmethod
    def getDefaultState():
        return {
            "talker": {},
            "author": {},
            "last_sent": {},
            "cur_topic": {},
            "topics": [],
            "algorithm": [],

            "last": {
                "noun": None,
                "subject": None,
                "verb": None,
                "object": None,
            }
        }

    def clear(self):
        self.state = self.getDefaultState()

    def rememberTopic(self, topicHyperonim: str):
        if topicHyperonim is not None and topicHyperonim not in self.state['topics']:
            self.state['topics'].append(topicHyperonim)

    def isTokenFromSAO(self, t_pos: str, t_dep: str) -> bool:
        return t_dep in ('nsubj', 'dobj', 'compound') or t_dep == 'ROOT' and t_pos in ('VERB', 'AUX');
