import csv
import re
import getopt, sys
from unidecode import unidecode

argumentList = sys.argv[1:]

options = "eu"

long_options = ["Europe", "USA"]

try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    if arguments == []:
        print("Use : -e, -u, --Europe, --USA")
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-e", "--Europe"):
            with open('./data/samples/500ksample-europefilter-address.csv', newline="\n") as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                counter = 0 
                f = open("./output/EU/fouten.txt", 'w')
                f.close
                f = open("./data/trainingData/training_EU.py", 'w')
                f.write("TRAININGS_DATA = [\n")
                f.close()
                counter = 0
                fail_numberstreet = 0
                fail_cityzip = 0 
                for row in csvreader:
                    correct = True
                    counter += 1
                    # print("counter: " + str(counter))
                    adres = ','.join(row)
                    adres = unidecode(adres)
                    if not re.match(".*,.*,.*", adres):
                        # print("counter: " + str(counter))
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
                            f = open("./output/EU/fouten.txt", 'a')
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
                            f = open("./output/EU/fouten.txt", 'a')
                            f.write("city: " + adres + "\n")
                            f.close()
                            fail_cityzip += 1
                            correct = False

                        if correct:
                            f = open("./data/trainingData/training_EU.py", 'a')
                            f.write("\t(\""+adres+"\","+"[("+str(straat[0])+","+str(straat[1])+", \"STREET\"),("+str(nummer[0])+","+str(nummer[1])+", \"NUMBER\"),("+str(city[0])+","+str(city[1])+", \"CITY\"),("+str(zipcode[0])+","+str(zipcode[1])+", \"ZIPCODE\")]),\n")
                            f.close()
                        # print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")
                f = open("./data/trainingData/training_EU.py", "a")
                f.write("]")
                f.close()
                print("failed on street: ", fail_numberstreet)
                print("failed on city: ", fail_cityzip)
        elif currentArgument in ("-u", "--USA"):
            
            def fout(element,adres, fails):
                f = open("./output/USA/fouten.txt", 'a')
                f.write(element + ": " + adres + "\n")
                f.close()
                return fails + 1
                

            with open('./data/samples/500ksample-americanfilter-address.csv', newline="\n") as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                counter = 0 
                f = open("./output/USA/fouten.txt", 'w')
                f.close
                f = open("./data/trainingData/training_USA.py", 'w')
                f.write("TRAININGS_DATA = [\n")
                f.close()
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
                    correct = True
                    counter += 1
                    adres = ','.join(row)
                    adres = unidecode(adres)
                    adres1 = row[0]
                    adres2 = row[1]
                    totale_lengte_straat = len(adres1) + 1
                    #nummer
                    if re.match('([0-9]+)', adres1):
                        nummer = re.search('([0-9]+)', adres1).span(1)
                    else:
                        fout("Nummer", adres1, fail_nummer)
                        correct = False
                        continue
                    #straat
                    if re.search('[0-9]+ ([\s\S]*)$', adres1):
                        straat = re.search('[0-9]+ ([\s\S]*)$', adres1).span(1)    
                    else:
                        fout("Straat", adres1, fail_straat)
                        correct = False
                        continue
                    # if not re.match('([0-9]+)', adres1) and not re.match('[0-9]+ ([\s\S]*)$', adres1):
                        
                    #city
                    if re.match('([a-zA-Z ]+?(?=,))', adres2):
                        city = re.search('([a-zA-Z ]+?(?=,))', adres2).span(1)
                        city = list(city)
                        city[0] += totale_lengte_straat
                        city[1] += totale_lengte_straat
                    else:
                        fout("City", adres2, fail_city)
                        correct = False
                        continue
                    #zipcode
                    if re.search('([0-9\-]+$)', adres2):
                        zipcode = re.search('([0-9\-]+$)', adres2).span(1)
                        zipcode = list(zipcode)
                        zipcode[0] += totale_lengte_straat
                        zipcode[1] += totale_lengte_straat
                    else:
                        fout("Zipcode", adres2, fail_zipcode)
                        correct = False
                        continue
                    #state
                    if re.search(', ([A-Za-z]*)', adres2):
                        state = re.search(', ([A-Za-z]*)', adres2).span(1)
                        state = list(state)
                        state[0] += totale_lengte_straat
                        state[1] += totale_lengte_straat
                    else:
                        fout("State", adres2, fail_state)
                        correct = False
                        continue
                    if not re.match('((?=, )[A-Za-z]+)', adres2) or not re.match('([0-9\-]+$)', adres2) or not re.match(', ([A-Za-z]*)', adres2):
                        f = open("./output/USA/fouten.txt", 'a')
                        f.write("city/zipcode/state: " + adres + "\n")
                        f.close()
                        fail_city += 1
                        correct = False
                        continue
                    

                    if correct:
                        f = open("./data/trainingData/training_USA.py", 'a')
                        f.write("\t(\""+adres+"\","+"[("+str(straat[0])+","+str(straat[1])+", \"STREET\"),("+str(nummer[0])+","+str(nummer[1])+", \"NUMBER\"),("+str(city[0])+","+str(city[1])+", \"CITY\"),("+str(zipcode[0])+","+str(zipcode[1])+", \"ZIPCODE\"),("+ str(state[0])+","+str(state[1])+", \"STATE\")]),\n")
                        f.close()
                        # print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")
                f = open("./data/trainingData/training_USA.py", "a")
                f.write("]")
                f.close()
                # print("failed on street: ", fail_numberstreet)
                # print("failed on city: ", fail_cityzip)

except getopt.error as err:
    print("Use : -e, -u, --Europe, --USA")