import spacy
from spacy.tokens import DocBin
from data.trainingData.TrainingData import TRAIN_DATA

nlp = spacy.blank("en")

db = DocBin()
for text, annotations in TRAIN_DATA:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span is None:
            print(doc.text[start:end])
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

# db = DocBin()
# for text, annotations in training_data:
#     doc = nlp(text)
#     ents = []
#     for start, end, label in annotations:
#         # print(doc.text[start:end])
#         span = doc.char_span(start, end, label=label)
#         # print(span)
#         ents.append(span)
#     # print(ents)
#     doc.ents = ents
#     db.add(doc)
# db.to_disk("./data/binaryData/dev.spacy")



