WORD_SEPARATOR = ' '
devSAOList = [
    ['ROUTINE', 'READ', 'DATA'],
    ['ROUTINE', 'PRINT', 'DATA'],
]


class Mind:

    def __init__(self, nlp, wordsDictionary, hyperonymList):
        self.nlp = nlp
        self.wordsDictionary = wordsDictionary
        self.hyperonymList = hyperonymList
        self.state = self.getDefaultState()
        self.processedPhrase = self.getDefaultPhraseStorage()

    def processPhrase(self, phrase):
        self.processedPhrase = self.getDefaultPhraseStorage()

        if phrase == ':clear':
            self.clear()
            return None

        # ACTION
        # replace "it", etc with current context topics
        phrase = self.processItPronoun(phrase)

        self.processedPhrase['phrase'] = phrase

        # travel through the phrase, token by token
        phraseDoc = self.nlp(phrase)
        phraseSAO = []
        for token in phraseDoc:

            # process each token
            t_lemma, t_hyperonim, t_pos, t_tag, t_dep = self.prepareTokenOutput(token, self.findMatchingWord(token))

            # prepare a processed result
            # if token2Output != '' and self.processedPhrase != '':
            #     self.processedPhrase = self.processedPhrase + WORD_SEPARATOR
            # self.processedPhrase = self.processedPhrase + token2Output
            self.processedPhrase['tagged_phrase'].append((t_lemma, t_hyperonim, t_pos, t_tag, t_dep));

            if t_dep in ('nsubj', 'dobj', 'compound') or t_dep == 'ROOT' and t_pos in ('VERB', 'AUX'):
                phraseSAO.append(t_hyperonim)

            if t_pos == 'NOUN':
                self.setLast('noun', t_lemma)

        self.processedPhrase['sao'] = phraseSAO

        if phraseSAO and phraseSAO in devSAOList:
            self.processedPhrase['devsao_detected'] = True

        #   [the (det) topic] can be replaced with object/noun/topic already described
        #   [a/an topic] must create new topic

        #   let's find matching SAO's

        #   if no matching SAO's let's find the closest ones: SA*, S*O, *AO, etc.

        #   let's check what SAO may require as additional parameters

        #   let's create a list of missing parameters for matching SAO

        #   list of topics - nouns = files, methods, programs, data, etc.

        #   let's ask user for parameters - that come from inbuilt SAO's

    def processItPronoun(self, phrase):
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

    def prepareTokenOutput(self, token, word):
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

    def findMatchingWord(self, token):
        word = dict({
            "id": None,
            "text": None
        })

        word["id"] = self.wordsDictionary.findValue(token.lemma)

        if word["id"] is not None:
            word["text"] = self.findWordById(word["id"])

        return word

    def getDefaultPhraseStorage(self):
        return {
            'phrase': '',
            'tagged_phrase': [],
            'sao': [],
            'devsao_detected': False
        }

    def findVocabId(self, word):
        return self.nlp.vocab[word.lower()].orth

    def findWordById(self, searchId):
        return self.nlp.vocab[int(searchId)].text

    def getProcessedPhrase(self):
        return self.processedPhrase

    def saveToSession(self, session):
        session['state'] = self.state

    def loadFromSession(self, session):
        if 'state' in session:
            self.state = session['state']

    def getLast(self, key):
        result = None
        if key in self.state['last']:
            result = self.state['last'][key]

        return result

    def setLast(self, key, value):
        self.state['last'][key] = value

    def getDefaultState(self):
        return {
            "talker": {},
            "author": {},
            "last_sent": {},
            "cur_topic": {},

            "last": {
                "noun": None,
                "subject": None,
                "verb": None,
                "object": None,
            }
        }

    def clear(self):
        self.state = self.getDefaultState()
