import spacy

test_text = "I ate Sushi yesterday. Maggi is a common fast food."
# nlp = spacy.load("./output/model-best")
nlp = spacy.load("./output/model-last")
doc = nlp(test_text)
print("Entities in '%s'" % test_text)
for ent in doc.ents:
  print(ent)