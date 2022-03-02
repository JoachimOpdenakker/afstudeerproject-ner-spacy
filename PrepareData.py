import spacy
import sys
from spacy.tokens import DocBin
sys.path.insert(0, './data/trainingData')
from training_EU import TRAININGS_DATA as TD

f = open("./output/problems.txt", 'w')
f.close()


nlp = spacy.blank("en")

infixes = nlp.Defaults.infixes + [r'\,']
nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
counter = 0
db = DocBin()
for text, annotations in TD:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span is None:
            f = open("./output/problems.txt", 'a')
            f.write("Problem:" + doc.text + " (" + doc.text[start:end] + ")\n")
            f.close()
        else:
            # print(label)
            ents.append(span)
        counter += 1
        doc.ents = ents
        db.add(doc)
print(counter)
db.to_disk("./data/binaryData/train.spacy")

db = DocBin()
for text, annotations in TD:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            ents.append(span)
        doc.ents = ents
        db.add(doc)
db.to_disk("./data/binaryData/dev.spacy")



