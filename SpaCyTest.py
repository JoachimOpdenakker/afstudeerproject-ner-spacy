import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a test. $1 billion")

for pipe in nlp.pipe_names:
    print (pipe)

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)