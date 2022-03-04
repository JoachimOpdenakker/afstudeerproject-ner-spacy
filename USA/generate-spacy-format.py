import csv
from itertools import count
import re
from unidecode import unidecode
def fout(element,adres, fails):
    f = open("./output/fouten_generate.txt", 'a')
    f.write(element + ": " + adres + "\n")
    f.close()
    return fails + 1

with open('./data/samples/500ksample-americanfilter-address.csv', newline="\n") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    counter = 0 
    f = open("./output/fouten_generate.txt", 'w')
    f.close
    f = open("./data/trainingData/training_USA.py", 'w')
    f.write("TRAININGS_DATA = [\n")
    f.close()
    f = open("./data/trainingData/dev_USA.py", 'w')
    f.write("TRAININGS_DATA = [\n")
    f.close()
    f = open("./data/validation/validation_USA.txt", 'w')
    f.close
    fail_nummer = 0
    fail_straat = 0
    fail_city = 0
    fail_zipcode = 0
    fail_state = 0
    counter = 0
    nummmer = ""
    straat = ""
    city = ""
    zipcode = ""
    state = ""
    for row in csvreader:
        correct = False
        adres = ','.join(row)
        adres = unidecode(adres)
        adres1 = row[0]
        adres2 = row[1]
        totale_lengte_straat = len(adres1) + 1
        full_string = "\t(\""+adres+"\","+"["
        #nummer
        if re.match('(/ )?([0-9]+)', adres1):
            nummer = re.search('(/ )?([0-9]+)', adres1).span(2)
            full_string += "("+str(nummer[0])+","+str(nummer[1])+", \"NUMBER\"),"
            correct = True
        else:
            fail_nummer = fout("Nummer", adres1, fail_nummer)
            continue
        #straat
        if re.search('[0-9]+ ([\s\S]*)$', adres1):
            straat = re.search('[0-9]+ ([\s\S]*)$', adres1).span(1)
            full_string += "("+str(straat[0])+","+str(straat[1])+", \"STREET\"),"
            correct = True
        else:
            fail_straat = fout("Straat", adres1, fail_straat)
            continue
        # if not re.match('([0-9]+)', adres1) and not re.match('[0-9]+ ([\s\S]*)$', adres1):
            
        #city
        if re.match('([a-zA-Z ]+?(?=,))', adres2):
            city = re.search('([a-zA-Z ]+?(?=,))', adres2).span(1)
            city = list(city)
            city[0] += totale_lengte_straat
            city[1] += totale_lengte_straat
            full_string += "("+str(city[0])+","+str(city[1])+", \"CITY\"),"
            correct = True
        else:
            fail_city = fout("City", adres2, fail_city)
            continue
        #zipcode
        if re.search('([0-9\-]+$)', adres2):
            zipcode = re.search('([0-9\-]+$)', adres2).span(1)
            zipcode = list(zipcode)
            zipcode[0] += totale_lengte_straat
            zipcode[1] += totale_lengte_straat
            full_string += "("+str(zipcode[0])+","+str(zipcode[1])+", \"ZIPCODE\"),"
            correct = True
        else:
            fail_zipcode = fout("Zipcode", adres2, fail_zipcode)
            continue
        #state
        if re.search('(,? )([ A-Za-z]*)(?<! ),? [0-9]', adres2):
            state = re.search('(,? )([ A-Za-z]*)(?<! ),? [0-9]', adres2).span(2)
            state = list(state)
            state[0] += totale_lengte_straat
            state[1] += totale_lengte_straat
            if not city[1] >= state[0]:
                full_string += "("+ str(state[0])+","+str(state[1])+", \"STATE\")"
                correct = True
        else:
            fail_state = fout("State", adres2, fail_state)
            continue
        # if not re.match('((?=, )[A-Za-z]+)', adres2) or not re.match('([0-9\-]+$)', adres2) or not re.match(', ([A-Za-z]*)', adres2):
        #     f = open("./output/USA/fouten_generate.txt", 'a')
        #     f.write("city/zipcode/state: " + adres + "\n")
        #     f.close()
        #     fail_city += 1
        #     correct = False
        #     continue
        

        if correct:
            counter += 1
            if counter < 5:
                f = open("./data/trainingData/training_USA.py", 'a')
                f.write(full_string + "]),\n")
                f.close()
            else:
                f = open("./data/trainingData/dev_USA.py", 'a')
                f.write(full_string + "]),\n")
                f.close()
                counter = 0
            f = open("./data/validation/validation_USA.txt", 'a')
            f.write(adres+"&"+str(straat[0])+";"+str(straat[1])+";STREET&"+str(nummer[0])+";"+str(nummer[1])+";NUMBER&"+str(city[0])+";"+str(city[1])+";CITY&"+str(zipcode[0])+";"+str(zipcode[1])+";ZIPCODE&"+str(state[0])+";"+str(state[1])+";STATE\n")
            f.close()
            # print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")
    f = open("./data/trainingData/training_USA.py", "a")
    f.write("]")
    f.close()
    f = open("./data/trainingData/dev_USA.py", "a")
    f.write("]")
    f.close()
    print("failed on street: ", fail_straat)
    print("failed on number: ", fail_nummer)
    print("failed on city: ", fail_city)
    print("failed on zipcode: ", fail_zipcode)
    print("failed on state: ", fail_state)