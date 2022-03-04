import csv
from itertools import count
import re
from unidecode import unidecode

with open('./data/samples/500ksample-europefilter-address.csv', newline="\n") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    counter = 0
    f = open("./output/fouten_generate.txt", 'w')
    f.close
    f = open("./data/validation/validation_EU.txt", 'w')
    f.close
    f = open("./data/trainingData/training_EU.py", 'w')
    f.write("TRAININGS_DATA = [\n")
    f.close()
    f = open("./data/trainingData/dev_EU.py", 'w')
    f.write("TRAININGS_DATA = [\n")
    f.close()
    fail_numberstreet = 0
    fail_cityzip = 0 
    for row in csvreader:
        correct = True
        adres = row[0] + ',' + row[1]
        adres = unidecode(adres)
        if not re.match(".*,.*,.*", adres):
            adreslengte = len(adres)
            adres1 = row[0]
            totale_lengte_straat = len(adres1) + 1
            adres2 = row[1]
            # nummer + straat
            if re.match('^([0-9\-]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\'\-]+)', adres1):
                split = re.search('^([0-9\-]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\'\-]+)', adres1)
                straat = split.span(3)
                nummer = split.span(1)

            # straat + nummer
            elif re.match('^([ \u00C0-\u017Fa-zA-Z\'\-]+) ([0-9\/\-]+( ?[a-zA-Z]*)?)', adres1):
                split = re.search('^([ \u00C0-\u017Fa-zA-Z\'\-]+) ([0-9\/\-]+( ?[a-zA-Z]*)?)', adres1)
                straat = split.span(1)
                nummer = split.span(2)
            else:
                f = open("./output/fouten_generate.txt", 'a')
                f.write("street: " + adres + "\n")
                f.close()
                fail_numberstreet +=1
                correct = False
            
            # zipcode + city
            if re.match('([ A-Z-]*[0-9]+( ?[A-Z]{2})?) ?([\u00C0-\u0338a-zA-Z ./-]+)$', adres2):
                split = re.search('([ A-Z-]*[0-9]+( ?[A-Z]{2})?) ?([\u00C0-\u0338a-zA-Z ./-]+)$', adres2)
                zipcode = list(split.span(1))
                city = list(split.span(3))
                zipcode[0] += totale_lengte_straat
                zipcode[1] += totale_lengte_straat
                city[0] += totale_lengte_straat
                city[1] += totale_lengte_straat

            # city + zipcode 
            elif re.match('([\u00C0-\u017Fa-zA-Z ./-]+) ?([ A-Z-]*[0-9]+)$', adres2):
                split = re.search('([\u00C0-\u017Fa-zA-Z ./-]+) ?([ A-Z-]*[0-9]+)$', adres2)
                zipcode = list(split.span(2))
                city = list(split.span(1))
                zipcode[0] += totale_lengte_straat
                zipcode[1] += totale_lengte_straat
                city[0] += totale_lengte_straat
                city[1] += totale_lengte_straat
            else:
                f = open("./output/fouten_generate.txt", 'a')
                f.write("city: " + adres + "\n")
                f.close()
                fail_cityzip += 1
                correct = False

            if correct:
                counter += 1
                if counter < 5:
                    f = open("./data/trainingData/training_EU.py", 'a')
                    f.write("\t(\""+adres+"\","+"[("+str(straat[0])+","+str(straat[1])+", \"STREET\"),("+str(nummer[0])+","+str(nummer[1])+", \"NUMBER\"),("+str(city[0])+","+str(city[1])+", \"CITY\"),("+str(zipcode[0])+","+str(zipcode[1])+", \"ZIPCODE\")]),\n")
                    f.close()
                else:
                    f = open("./data/trainingData/dev_EU.py", 'a')
                    f.write("\t(\""+adres+"\","+"[("+str(straat[0])+","+str(straat[1])+", \"STREET\"),("+str(nummer[0])+","+str(nummer[1])+", \"NUMBER\"),("+str(city[0])+","+str(city[1])+", \"CITY\"),("+str(zipcode[0])+","+str(zipcode[1])+", \"ZIPCODE\")]),\n")
                    f.close()
                    counter = 0
                f = open("./data/validation/validation_EU.txt", 'a')
                f.write(adres+"&"+str(straat[0])+";"+str(straat[1])+";STREET&"+str(nummer[0])+";"+str(nummer[1])+";NUMBER&"+str(city[0])+";"+str(city[1])+";CITY&"+str(zipcode[0])+";"+str(zipcode[1])+";ZIPCODE\n")
                f.close()
            # print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")
    f = open("./data/trainingData/training_EU.py", "a")
    f.write("]")
    f.close()
    f = open("./data/trainingData/dev_EU.py", "a")
    f.write("]")
    f.close()
    print("failed on street: ", fail_numberstreet)
    print("failed on city: ", fail_cityzip)