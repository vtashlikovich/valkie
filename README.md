# Valkie

Sample code for detection of predefined SAO's in text using spacy NLP library.

The main code is placed here: modules/mind.py.

## Requirements
Projects needs:
- Spacy vocabulary to work with previouls formed hyperonims. Vocabulary folder "vocabby" must be placed in the root directory;
- list of hyperonims supported. Thye must be placed in the roo directory under dict.json. dict-gw.json contains of all supported hyponims.

UI/API is served by Flask framework.

## Running
To run the project type:
```
python index.py
```

Server is accessible via: *http://127.0.0.1:5000*

## Screenshot
