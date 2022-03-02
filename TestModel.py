import csv
import spacy
from spacy.tokens import DocBin
from spacy import displacy

# test_text = ["Keilalahdentie 4,02150 Espoo", "Weisshsusstrasse 2,52066 Aachen", "14 rue Royale,75008 Paris", "Hüninger Strasse 25,14195 Berlin", "19 bis rue Hoche,49100 Angers"]
test_text = []
with open('./data/samples/500ksample-europefilter-address.csv', newline="\n") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        row = ','.join(row)
        test_text.append(row)

# print(test_text)

nlp = spacy.load("./model/model-best")
# nlp = spacy.load("./model/model-last")
list = []
correct_counter = 0
total_counter = 0
for i in test_text:    
    doc = nlp(i)
    if len(doc.ents) == 4:
        total_counter += 1
        if len(i) == len(str(doc.ents[0]) + str(doc.ents[1]) + str(doc.ents[2]) + str(doc.ents[3])) + 3:
            list.append(doc)
            correct_counter += 1
    # for token in doc:
    #     print(str(token) + ";")
colors = {"STREET": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "NUMBER": "linear-gradient(90deg, #3f5efb, #fc466b)", "ZIPCODE": "linear-gradient(90deg, #090979, #00d4ff)", "CITY": "linear-gradient(90deg, #eeaeca, #94bbe9)", "OTHER": "linear-gradient(90deg, #22c1c3, #fdbb2d)",}
options = {"ents": ["CITY", "STREET", "NUMBER", "ZIPCODE", "OTHER"], "colors": colors}
print("correctness", correct_counter/total_counter)
print("total", total_counter)
displacy.serve(list, style="ent", options=options)
# print("Entities in '%s'" % test_text)
# for ent in doc.ents:
#   print(ent)