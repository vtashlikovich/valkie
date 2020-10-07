import sys, json, spacy
from modules import dictionary
from modules.dictionary import Dict

from spacy.tokens import Token, Doc

jsonArgFile = ""

nlp = None
hyperonymDictionary: Dict = dictionary.Dict()
hyperonyms = []

# functions ------------------------------------------


def wordsAreEmpty(argWordsArray):
    return len(argWordsArray[0]) == 0 or len(argWordsArray[2]) == 0


def findVocabId(word):
    return nlp.vocab[word].orth


def findWordById(wordId):
    return nlp.vocab[int(wordId)].text


def saveToDisk():
    """
    Saves dictionary to file as JSON
    Saves the current Spacy vocabulary
    """
    print(f"Writing dictionary to: {jsonArgFile}")
    hyperonymDictionary.save(jsonArgFile + ".json")

    for dict_item in hyperonymDictionary.getItems():
        if dict_item[1] not in hyperonyms:
            hyperonyms.append(dict_item[1])

    with open(jsonArgFile + "-gw.json", "w") as file2Write:
        file2Write.write(json.dumps(hyperonyms))

    nlp.to_disk("vocabby")


def loadFromDisk():
    """
    Loads the current Spacy vocabulary
    Loads dictionary from file in JSON format
    """
    global nlp
    global hyperonyms
    nlp = spacy.load("vocabby")

    print(f"Reading dictionary from: {jsonArgFile}")
    hyperonymDictionary.load(jsonArgFile + ".json")

    with open(jsonArgFile + "-gw.json") as fileLoaded:
        hyperonyms = json.load(fileLoaded)


# code ------------------------------------------

if len(sys.argv) > 1:
    jsonArgFile = sys.argv[1]

if len(jsonArgFile) > 0:

    loadFromDisk()

    print(
        """
:q/:exit/:quit - exit
:len - size of the dictionary
:print - print the whole dictionary
:save - save dictionary and vocabulary
:all - print all hyperonims
hyponim = hyperonim - connects hyponim and hyperonim
hyponim != hyperonim - disconnects hyponim and hyperonim
?hyperonim - lists of hyponims
        """
    )
    inputString = input("> ")

    while inputString != ":q" and inputString != ":exit" and inputString != ":quit":
        # processes all commands
        argWordsArray = inputString.lower().split()

        if inputString == ":len":
            print(f"Dictionary size: {hyperonymDictionary.size()}")

        elif inputString == ":print":
            hyperonymDictionary.print()

        elif inputString == ":save":
            saveToDisk()

        elif inputString == ":all":
            allHyperonims = [
                findWordById(wordId) for wordId in hyperonymDictionary.getHyperonims()
            ]
            print(allHyperonims)

        elif (
            len(argWordsArray) == 3
            and argWordsArray[1] == "="
            and not wordsAreEmpty(argWordsArray)
        ):
            firstWordId = findVocabId(argWordsArray[0])
            secondWordId = findVocabId(argWordsArray[2])
            if (
                firstWordId
                and secondWordId
                and not hyperonymDictionary.exists(firstWordId)
            ):
                hyperonymDictionary.add(firstWordId, secondWordId)
                if secondWordId not in hyperonyms:
                    hyperonyms.append(secondWordId)
                print(".. added")
            else:
                print(".. pair already exists")

        elif (
            len(argWordsArray) == 3
            and argWordsArray[1] == "!="
            and not wordsAreEmpty(argWordsArray)
        ):
            firstWordId = findVocabId(argWordsArray[0])
            secondWordId = findVocabId(argWordsArray[2])
            if hyperonymDictionary.exists(
                firstWordId
            ) and secondWordId == hyperonymDictionary.findValue(firstWordId):
                hyperonymDictionary.delete(firstWordId)
                print(".. deleted")

        elif len(argWordsArray) == 1 and argWordsArray[0][0] == "?":
            findValueWord = argWordsArray[0][1:].lower()
            findValueWordId = findVocabId(findValueWord)
            foundWords = []
            for dictItem in hyperonymDictionary.getItems():
                if dictItem[1] == findValueWordId:
                    foundWord = findWordById(dictItem[0])
                    foundWords.append(foundWord)

            if len(foundWords) > 0:
                print(foundWords)
            else:
                print(".. no matches")

        else:
            print(".. not recognized")

        inputString = input("> ")

    saveToDisk()
else:
    print("Error: file is not set\r\nFormat: dicter JSON_FILE")

