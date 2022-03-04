import csv
import spacy
from spacy.tokens import DocBin
from spacy import displacy

# test_text = ["Keilalahdentie 4,02150 Espoo", "Weisshsusstrasse 2,52066 Aachen", "14 rue Royale,75008 Paris", "Hüninger Strasse 25,14195 Berlin", "19 bis rue Hoche,49100 Angers"]
test_text = []
with open('./data/samples/500ksample-americanfilter-address.csv', newline="\n") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        row = ','.join(row)
        test_text.append(row)

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
        # print(record)
    record.pop(0)
    adreslist.append(recordtuple)
# print(adreslist[0])

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

for i in test_text:    
    doc = nlp(i)
    ents = list(doc.ents)
    for at in adreslist:
        if at[0] == str(doc):
            for j in at[1]:
                for token in ents:
                    # print(token)
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
print("straat: " + str(total_correct_straat) + " percentage: " + str(total_correct_straat / total_straat)+ "%")
print("nummer: " + str(total_correct_nummer) + " percentage: " + str(total_correct_nummer / total_nummer)+ "%")
print("city: " + str(total_correct_city) + " percentage: " + str(total_correct_city / total_city)+ "%")
print("zipzode: " + str(total_correct_zipcode) + " percentage: " + str(total_correct_zipcode / total_zipcode)+ "%")
print("state: " + str(total_correct_state) + " percentage: " + str(total_correct_state / total_state)+ "%")
print("counter: " + str(total_counter))

colors = {"STREET": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "NUMBER": "linear-gradient(90deg, #3f5efb, #fc466b)", "ZIPCODE": "linear-gradient(90deg, #090979, #00d4ff)", "CITY": "linear-gradient(90deg, #eeaeca, #94bbe9)", "STATE": "linear-gradient(90deg, #22c1c3, #fdbb2d)",}
options = {"ents": ["CITY", "STREET", "NUMBER", "ZIPCODE", "STATE"], "colors": colors}
displacy.serve(lijst, style="ent", options=options)

