import csv
from curses.ascii import ctrl
import spacy
import pandas as pd
from spacy.tokens import DocBin
from spacy import displacy

test_text = []
df = pd.read_pickle("./data/samples/500ksample-europefilter-address.pkl")

labeledData = open('./data/validation/validation_EU.txt', 'r')
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
total_counter_straat = 0
total_counter_nummer = 0
total_counter_city = 0
total_counter_zipcode = 0
ctry_code = ""

def validate(row):
    global lijst
    global correct_counter
    global total_counter
    global total_counter_straat
    global total_counter_nummer
    global total_counter_city
    global total_counter_zipcode
    global ctry_code
    adres_ctry_code = row.person_ctry_code
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
                        total_counter_straat +=1
                    if bool1 and bool2 and bool3 and token.label_ == "NUMBER":
                        total_counter_nummer +=1
                    if bool1 and bool2 and bool3 and token.label_ == "CITY":
                        total_counter_city +=1
                    if bool1 and bool2 and bool3 and token.label_ == "ZIPCODE":
                        total_counter_zipcode +=1
    lijst.append(doc)
    total_counter += 1
    if ctry_code != adres_ctry_code:
        print("----------------------" + ctry_code + "--------------------------------")
        print("straat: " + str(total_counter_straat) + " percentage: " + str(total_counter_straat / total_counter * 100)+ "%")
        print("nummer: " + str(total_counter_nummer) + " percentage: " + str(total_counter_nummer / total_counter * 100)+ "%")
        print("city: " + str(total_counter_city) + " percentage: " + str(total_counter_city / total_counter * 100)+ "%")
        print("zipcode: " + str(total_counter_zipcode) + " percentage: " + str(total_counter_zipcode / total_counter * 100)+ "%")
        print("counter: " + str(total_counter))
        ctry_code = adres_ctry_code
        total_counter = 0
        total_counter_straat = 0
        total_counter_nummer = 0
        total_counter_city = 0
        total_counter_zipcode = 0

df.apply(lambda x: validate(x),axis=1)

colors = {"STREET": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "NUMBER": "linear-gradient(90deg, #3f5efb, #fc466b)", "ZIPCODE": "linear-gradient(90deg, #090979, #00d4ff)", "CITY": "linear-gradient(90deg, #eeaeca, #94bbe9)", "OTHER": "linear-gradient(90deg, #22c1c3, #fdbb2d)",}
options = {"ents": ["CITY", "STREET", "NUMBER", "ZIPCODE", "OTHER"], "colors": colors}
displacy.serve(lijst, style="ent", options=options)

