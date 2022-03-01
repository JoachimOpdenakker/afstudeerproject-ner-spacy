import spacy
import sys
from spacy.tokens import DocBin
sys.path.insert(0, '../data/trainingData')
from training import TRAININGS_DATA as TD

f = open("./output/problems.txt", 'w')
f.close()


nlp = spacy.blank("en")

infixes = nlp.Defaults.infixes + [r'\,']
nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
counter = 0
db = DocBin()
for text, annotations in TD:
    doc = nlp(text)
    # for token in doc:
        # print(token,end='; ')
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span is None:
            f = open("./output/problems.txt", 'a')
            f.write("Problem:" + doc.text + " (" + doc.text[start:end] + ")\n")
            f.close()
        else:
            ents.append(span)
    if len(ents) == 4:
        counter += 1
        doc.ents = ents
        db.add(doc)
print(counter)
db.to_disk("../data/binaryData/train.spacy")

db = DocBin()
for text, annotations in TD:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        # print(doc.text[start:end])
        span = doc.char_span(start, end, label=label)
        if span is not None:
            ents.append(span)
    if len(doc.ents) == 4:
        doc.ents = ents
        db.add(doc)
db.to_disk("../data/binaryData/dev.spacy")



