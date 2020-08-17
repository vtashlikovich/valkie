import sys, json

class Dict:

    def __init__(self):
        self.dictionary = {}

    def getItems(self):
        return self.dictionary.items()

    def delete(self, id):
        del self.dictionary[id]

    def print(self):
        print(self.dictionary)

    def add(self, key, value):
        self.dictionary[str(key)] = value

    def exists(self, id):
        return str(id) in self.dictionary

    def findValue(self, id):
        result = None

        if self.exists(id):
            result = self.dictionary[str(id)]

        return result

    def size(self):
        return len(self.dictionary)

    def load(self, fileName):
        with open(fileName) as fileLoaded:
            self.dictionary = json.load(fileLoaded)

    def save(self, fileName):
        with open(fileName, 'w') as file2Write:
            file2Write.write(json.dumps(self.dictionary))