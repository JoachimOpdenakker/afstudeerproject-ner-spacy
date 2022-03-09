import csv
import spacy
import pandas as pd
from spacy.tokens import DocBin
from spacy import displacy

# test_text = ["Keilalahdentie 4,02150 Espoo", "Weisshsusstrasse 2,52066 Aachen", "14 rue Royale,75008 Paris", "Hüninger Strasse 25,14195 Berlin", "19 bis rue Hoche,49100 Angers"]
test_text = []

df = pd.read_pickle("./data/samples/500ksample-americanfilter-address.pkl")

labeledData = open('./data/validation/validation_USA.txt', 'r')
adreslist = []
for line in labeledData.readlines():
    line = line.strip('\n')
    line = line.split("&")
    record = []
    recordtuple = (line[0],record)
    for i in line:
        i = i.split(";")
        record.append(i)
    record.pop(0)
    adreslist.append(recordtuple)

nlp = spacy.load("./model/model-best")
# nlp = spacy.load("./model/model-last")
lijst = []
correct_counter = 0
total_counter = 0
total_correct_straat = 0
total_correct_nummer = 0
total_correct_city = 0
total_correct_zipcode = 0
total_correct_state = 0

total_straat = 0
total_nummer = 0
total_city = 0
total_zipcode = 0
total_state = 0

def validate(row):
    global total_counter
    global total_correct_straat
    global total_correct_nummer
    global total_correct_city
    global total_correct_zipcode
    global total_correct_state

    global total_straat
    global total_nummer
    global total_city
    global total_zipcode
    global total_state 
    full_address = row.address_1 + ',' + row.address_2
    doc = nlp(full_address)
    ents = list(doc.ents)
    for at in adreslist:
        if at[0] == str(doc):
            for j in at[1]:
                for token in ents:
                    bool1 = str(j[0]) == str(token.start_char)
                    bool2 = str(j[1]) == str(token.end_char)
                    bool3 = j[2] == token.label_
                    if bool1 and bool2 and bool3 and token.label_ == "STREET":
                        total_correct_straat +=1
                    if bool1 and bool2 and bool3 and token.label_ == "NUMBER":
                        total_correct_nummer +=1
                    if bool1 and bool2 and bool3 and token.label_ == "CITY":
                        total_correct_city +=1
                    if bool1 and bool2 and bool3 and token.label_ == "ZIPCODE":
                        total_correct_zipcode +=1
                    if bool1 and bool2 and bool3 and token.label_ == "STATE":
                        total_correct_state +=1
                if j[2] == "STREET":
                    total_straat += 1
                if j[2] == "NUMBER":
                    total_nummer += 1
                if j[2] == "CITY":
                    total_city += 1
                if j[2] == "ZIPCODE":
                    total_zipcode += 1
                if j[2] == "STATE":
                    total_state += 1
    lijst.append(doc)
    total_counter += 1

df.apply(lambda x: validate(x),axis=1)

print("straat: " + str(total_correct_straat) + " percentage: " + str(total_correct_straat / total_straat * 100)+ "%")
print("nummer: " + str(total_correct_nummer) + " percentage: " + str(total_correct_nummer / total_nummer* 100)+ "%")
print("city: " + str(total_correct_city) + " percentage: " + str(total_correct_city / total_city* 100)+ "%")
print("zipzode: " + str(total_correct_zipcode) + " percentage: " + str(total_correct_zipcode / total_zipcode* 100)+ "%")
print("state: " + str(total_correct_state) + " percentage: " + str(total_correct_state / total_state* 100)+ "%")
print("adress in list: " + str(total_counter))

colors = {"STREET": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "NUMBER": "linear-gradient(90deg, #3f5efb, #fc466b)", "ZIPCODE": "linear-gradient(90deg, #090979, #00d4ff)", "CITY": "linear-gradient(90deg, #eeaeca, #94bbe9)", "STATE": "linear-gradient(90deg, #22c1c3, #fdbb2d)",}
options = {"ents": ["CITY", "STREET", "NUMBER", "ZIPCODE", "STATE"], "colors": colors}
displacy.serve(lijst, style="ent", options=options)

