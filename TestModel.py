import spacy
from spacy import displacy

test_text = "Keilalahdentie 4,02150 Espoo\n20 Park Crescent,London W1N 4AL\nWeisshsusstrasse 2 52066, Aachen\n14,rue Royale 75008 Paris\n32 Wakelin Avenue,Sawston, Cambridgeshire CB2 4DA\nHüninger Strasse 25,14195 Berlin"
nlp = spacy.load("./output/model-best")
# nlp = spacy.load("./output/model-last")
doc = nlp(test_text)
colors = {"STREET": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "NUMBER": "linear-gradient(90deg, #3f5efb, #fc466b)", "ZIPCODE": "linear-gradient(90deg, #090979, #00d4ff)", "CITY": "linear-gradient(90deg, #eeaeca, #94bbe9)", "OTHER": "linear-gradient(90deg, #22c1c3, #fdbb2d)",}
options = {"ents": ["CITY", "STREET", "NUMBER", "ZIPCODE", "OTHER"], "colors": colors}
displacy.serve(doc, style="ent", options=options)
# print("Entities in '%s'" % test_text)
# for ent in doc.ents:
#   print(ent)