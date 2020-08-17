import sys, json, spacy
from modules import dictionary
jsonArgFile = ''

nlp = None
dict = dictionary.Dict()
goldenWords = []

### functions ------------------------------------------
def wordsAreEmpty(argWordsArray):
    return len(argWordsArray[0]) == 0 or len(argWordsArray[2]) == 0

def findVocabId(word):
    return nlp.vocab[word].orth

def findWordById(id):
    return nlp.vocab[int(id)].text

def saveToDisk():
    print(f'Writing dictionary to: {jsonArgFile}')
    dict.save(jsonArgFile + '.json')

    for dictItem in dict.getItems():
        if dictItem[1] not in goldenWords:
            goldenWords.append(dictItem[1])

    with open(jsonArgFile + '-gw.json', 'w') as file2Write:
        file2Write.write(json.dumps(goldenWords))

    nlp.to_disk('vocabby')

def loadFromDisk():
    global nlp
    nlp = spacy.load('vocabby')

    print(f'Reading dictionary from: {jsonArgFile}')
    dict.load(jsonArgFile + '.json')

    with open(jsonArgFile + '-gw.json') as fileLoaded:
        goldenWords = json.load(fileLoaded)

### code ------------------------------------------

if len(sys.argv) > 1:
    jsonArgFile = sys.argv[1]

if len(jsonArgFile) > 0:

    loadFromDisk()

    print('')
    print('Format of command: word [!]= word')
    print('Print :q/:exit/:quit to quit and save data.')
    inputString = input('> ')
    while inputString != ':q' and inputString != ':exit' and inputString != ':quit':
        argWordsArray = inputString.lower().split()

        if inputString == ':len':
            print(f'Dictionary size: {dict.size()}')

        elif inputString == ':print':
            dict.print()

        elif inputString == ':save':
            saveToDisk()

        elif len(argWordsArray) == 3 and argWordsArray[1] == '=' and not wordsAreEmpty(argWordsArray):
            firstWordId = findVocabId(argWordsArray[0])
            secondWordId = findVocabId(argWordsArray[2])
            if firstWordId and secondWordId and not dict.exists(firstWordId):
                dict.add(firstWordId, secondWordId)
                if secondWordId not in goldenWords:
                    goldenWords.append(secondWordId)
                print('.. added')
            else:
                print('.. pair already exists')

        elif len(argWordsArray) == 3 and argWordsArray[1] == '!=' and not wordsAreEmpty(argWordsArray):
            firstWordId = findVocabId(argWordsArray[0])
            secondWordId = findVocabId(argWordsArray[2])
            if dict.exists(firstWordId) and secondWordId == dict.findValue(firstWordId):
                dict.delete(firstWordId)
                print('.. deleted')

        elif len(argWordsArray) == 1 and argWordsArray[0][0] == '?':
            findValueWord = argWordsArray[0][1:].lower()
            findValueWordId = findVocabId(findValueWord)
            foundWords = []
            for dictItem in dict.getItems():
                if dictItem[1] == findValueWordId:
                    foundWord = findWordById(dictItem[0])
                    foundWords.append(foundWord)

            if len(foundWords) > 0:
                print(foundWords)
            else:
                print('.. no matches')

        else:
            print('.. not recognized')

        inputString = input('> ')

    saveToDisk()
else:
    print('Error: file is not set\r\n'\
        'Format: dicter JSON_FILE')