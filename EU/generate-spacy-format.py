import pandas as pd
import re

df = pd.read_pickle("./data/lableddata/spanformat.pkl")

counter = 0
train = ""
dev = ""
validation = ""

def formatline(row):
    global counter
    global train
    global dev
    global validation
    if not (row.straat == "" and row.nummer == "" and row.city == "" and row.zipcode == ""):
        line = "\t(\""+row.full_address+"\","+"["
        valit = row.full_address + "&"
        if row.straat != "":
            line += "("+str(row.straat[0])+","+str(row.straat[1])+", \"STREET\"),"
            valit += str(row.straat[0]) + ";" + str(row.straat[1]) + ";STREET&"
        if row.nummer != "":
            line += "("+str(row.nummer[0])+","+str(row.nummer[1])+", \"NUMBER\"),"
            valit += str(row.nummer[0]) + ";" + str(row.nummer[1]) + ";NUMBER&"
        if row.city != "":
            line += "("+str(row.city[0])+","+str(row.city[1])+", \"CITY\"),"
            valit += str(row.city[0])+";"+str(row.city[1])+";CITY&"
        if row.zipcode != "":
            line += "("+str(row.zipcode[0])+","+str(row.zipcode[1])+", \"ZIPCODE\"),"
            valit += str(row.zipcode[0])+";"+str(row.zipcode[1])+";ZIPCODE"
        line += "]),\n"
        valit += "\n"

        validation += valit
        counter += 1
        if counter < 5:
            train += line
            # print(train)
        else:
            dev += line
            counter = 0

df.apply(lambda x: formatline(x),axis=1)

f = open("./output/fouten_generate.txt", 'w')
f.close
f = open("./data/validation/validation_EU.txt", 'w')
f.close
f = open("./data/trainingData/training_EU.py", 'w')
f.write("TRAININGS_DATA = [\n" + train + "]")
f.close()
f = open("./data/trainingData/dev_EU.py", 'w')
f.write("TRAININGS_DATA = [\n" + dev + "]")
f.close()

f = open("./data/validation/validation_EU.txt", 'w')
f.write(validation)
f.close()
