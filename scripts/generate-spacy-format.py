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
            with open('../data/samples/500ksample-europefilter-address.csv', newline="\n") as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                counter = 0 
                f = open("./output/fouten.txt", 'w')
                f.close
                f = open("../data/trainingData/training.py", 'w')
                f.write("TRAININGS_DATA = [\n")
                f.close()
                counter = 0
                fail_numberstreet = 0
                fail_cityzip = 0 
                for row in csvreader:
                    correct = True
                    counter += 1
                    # print(row)
                    # exit()
                    counter +=1
                    # print("counter: " + str(counter))
                    adres = ','.join(row)
                    adres = unidecode(adres)
                    # print(adres)
                    # adres = adres.replace(",", ";")
                    # if re.match(".*,.*,.*", adres):
                        # print(adres)
                        # print("FUCK YOU")
                    # else:
                    if not re.match(".*,.*,.*", adres):
                        # print("counter: " + str(counter))
                        adreslengte = len(adres)
                        adres1 = row[0]
                        totale_lengte_straat = len(adres1) + 1
                        adres2 = row[1]
                        # nummer + straat
                        # oud: ([0-9]+[A-Z]*)( )?([a-zA-Z]+)
                        # nieuw: (^[0-9]+.*([\u00C0-\u017Fa-zA-Z]+)),
                        # probeersel: ^([0-9]+)( .*)*( )([\u00C0-\u017Fa-zA-Z]+)
                        if re.match('^([0-9\-]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\'\-]+)', adres1):
                            split = re.search('^([0-9\-]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\'\-]+)', adres1)
                            print(split.span(3))
                            straat = split.span(3)
                            nummer = split.span(1)
                            # splitstraat = split.group(3)
                            # splitnummer = split.group(1)
                            # straatlengte = len(splitstraat)
                            # nummerlengte = len(splitnummer)
                            # nummerposbegin = 0
                            # nummerposeind = nummerlengte
                            # straatposbegin = nummerposeind + 1
                            # straatposeind = straatposbegin + straatlengte

                        # straat + nummer
                        # oude: ([a-zA-Z]+)( )?([0-9]+)
                        # nieuw: (([a-zA-Z]+) ([0-9]+.*,))
                        # oude nieuwe: ^([ \u00C0-\u017Fa-zA-Z\']+) ([0-9]+( ?bis)?)
                        elif re.match('^([ \u00C0-\u017Fa-zA-Z\'\-]+) ([0-9\/\-]+( ?[a-zA-Z]*)?)', adres1):
                            split = re.search('^([ \u00C0-\u017Fa-zA-Z\'\-]+) ([0-9\/\-]+( ?[a-zA-Z]*)?)', adres1)
                            straat = split.span(1)
                            nummer = split.span(2)
                            # splitstraat = split.group(1)
                            # splitnummer = split.group(2)
                            # nummerlengte = len(splitnummer)
                            # straatlengte = len(splitstraat)
                            # straatposbegin = 0
                            # straatposeind = straatlengte
                            # nummerposbegin = straatlengte + 1
                            # nummerposeind = nummerposbegin + nummerlengte
                        else:
                            f = open("fouten.txt", 'a')
                            f.write("street: " + adres + "\n")
                            f.close()
                            fail_numberstreet +=1
                            correct = False
                        
                        # zipcode + city
                        # oud: ([A-Z]*-?[0-9]+)( )?([\u00C0-\u017Fa-zA-Z]+)
                        # nieuw: ([ A-Z-]*[0-9]+) ?([\u00C0-\u017Fa-zA-Z .\/-]+)$
                        if re.match('([ A-Z-]*[0-9]+( ?[A-Z]{2})?) ?([\u00C0-\u0338a-zA-Z ./-]+)$', adres2):
                            split = re.search('([ A-Z-]*[0-9]+( ?[A-Z]{2})?) ?([\u00C0-\u0338a-zA-Z ./-]+)$', adres2)
                            zipcode = list(split.span(1))
                            city = list(split.span(3))
                            zipcode[0] += totale_lengte_straat
                            zipcode[1] += totale_lengte_straat
                            city[0] += totale_lengte_straat
                            city[1] += totale_lengte_straat
                            # splitcity = split.group(3)
                            # splitzipcode = split.group(1)
                            # print("city: " + splitcity)
                            # print("zipcode: " + splitzipcode)
                            # citylengte = len(splitcity)
                            # zipcodelengte = len(splitzipcode)
                            # zipcodeposbegin = totale_lengte_straat + 1
                            # zipcodeposeind = zipcodeposbegin + zipcodelengte
                            # cityposbegin = zipcodeposeind + 1
                            # cityposeind = cityposbegin + citylengte

                        # city + zipcode 
                        elif re.match('([\u00C0-\u017Fa-zA-Z ./-]+) ?([ A-Z-]*[0-9]+)$', adres2):
                            split = re.search('([\u00C0-\u017Fa-zA-Z ./-]+) ?([ A-Z-]*[0-9]+)$', adres2)
                            zipcode = list(split.span(2))
                            city = list(split.span(1))
                            zipcode[0] += totale_lengte_straat
                            zipcode[1] += totale_lengte_straat
                            city[0] += totale_lengte_straat
                            city[1] += totale_lengte_straat
                            # splitcity = split.group(1)
                            # splitzipcode = split.group(2)
                            # # print("city: " + splitcity)
                            # # print("zipcode: " + splitzipcode)
                            # zipcodelengte = len(splitzipcode)
                            # citylengte = len(splitcity)
                            # cityposbegin = totale_lengte_straat + 1
                            # cityposeind = cityposbegin + citylengte
                            # zipcodeposbegin = cityposeind + 1
                            # zipcodeposeind = zipcodeposbegin + zipcodelengte
                        else:
                            f = open("fouten.txt", 'a')
                            f.write("city: " + adres + "\n")
                            f.close()
                            fail_cityzip += 1
                            correct = False

                        if correct:
                            f = open("../data/trainingData/training.py", 'a')
                            f.write("\t(\""+adres+"\","+"[("+str(straat[0])+","+str(straat[1])+", \"STREET\"),("+str(nummer[0])+","+str(nummer[1])+", \"NUMBER\"),("+str(city[0])+","+str(city[1])+", \"CITY\"),("+str(zipcode[0])+","+str(zipcode[1])+", \"ZIPCODE\")]),\n")
                            f.close()
                        # print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")
                f = open("../data/trainingData/training.py", "a")
                f.write("]")
                f.close()
                print("failed on street: ", fail_numberstreet)
                print("failed on city: ", fail_cityzip)
        elif currentArgument in ("-u", "--USA"):
            print("USA")

except getopt.error as err:
    print("Use : -e, -u, --Europe, --USA")