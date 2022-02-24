import spacy
from spacy.tokens import DocBin
from data.trainingData.AdressTrainingData import TRAIN_DATA
from data.trainingData.AdressValidationData import training_data

nlp = spacy.blank("en")

infixes = nlp.Defaults.infixes + [r'\,']
nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer

# infixes = nlp.Defaults.infixes + [r'\,',]
# infix_reg = spacy.util.compile_infix_regex(infixes)
# nlp.tokenizer.infix_finditer = infix_reg.finditer

# suffixes = nlp.Defaults.suffixes + [r'(?<=[0-9]\,)',]
# suffix_regex = spacy.util.compile_suffix_regex(suffixes)
# nlp.tokenizer.suffix_search = suffix_regex.search

# prefixes = nlp.Defaults.prefixes + [r'(?<=[0-9]\,)',]
# prefix_regex = spacy.util.compile_prefix_regex(prefixes)
# nlp.tokenizer.prefix_search = prefix_regex.search


db = DocBin()
for text, annotations in TRAIN_DATA:
    doc = nlp(text)
    for token in doc:
        print(token,end='; ')
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span is None:
            print("Problem:" + doc.text + " (" + doc.text[start:end] + ")" )
        else:
            ents.append(span)
    # print(ents)
    doc.ents = ents
    db.add(doc)
db.to_disk("./data/binaryData/train.spacy")

# training_data = [
#   ("Cake is a common fast food.", [(0, 4, "FOOD")]),
#   ("Water is an italian recipe", [(0, 5, "FOOD")]),
#   ("China's chicken nuggets are very famous", [(8,23, "FOOD")]),
#   ("Ijs are famous in China too", [(0,3, "FOOD")]),
# ]

db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        # print(doc.text[start:end])
        span = doc.char_span(start, end, label=label)
        if span is None:
            print("Problem:" + doc.text + " (" + doc.text[start:end] + ")" )
        else:
            ents.append(span)
    # print(ents)
    doc.ents = ents
    db.add(doc)
db.to_disk("./data/binaryData/dev.spacy")



