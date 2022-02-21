import spacy
from spacy import displacy

test_text = "I ate Sushi yesterday. Maggi is a common fast food."
# nlp = spacy.load("./output/model-best")
nlp = spacy.load("./output/model-last")
doc = nlp(test_text)
colors = {"FOOD": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
options = {"ents": ["FOOD"], "colors": colors}
displacy.serve(doc, style="ent", options=options)
print("Entities in '%s'" % test_text)
for ent in doc.ents:
  print(ent)