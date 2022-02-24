import csv
import re
with open('address.csv', newline="\n") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    counter = 0 
    f = open("result.py", 'w')
    f.write("TRAININGS_DATA = [\n")
    f.close()
    counter = 0
    for row in csvreader:
        counter += 1
        # print(row)
        # exit()
        counter +=1
        # print("counter: " + str(counter))
        adres = ','.join(row)
        if re.match(".*,.*,.*", adres):
            print(adres)
            # print("FUCK YOU")
        else:
            # print("counter: " + str(counter))
            adreslengte = len(adres)
            straat = row[0]
            totale_lengte_straat = len(straat)
            city = row[1]
            straatposbegin = ""
            straatposeind = ""
            nummerposbegin =""
            nummerposeind = ""
            cityposbegin = ""
            cityposeind = ""
            zipcodeposbegin =""
            zipcodeposeind =""
            # nummer + straat
            # oud: ([0-9]+[A-Z]*)( )?([a-zA-Z]+)
            # nieuw: (^[0-9]+.*([\u00C0-\u017Fa-zA-Z]+)),
            # probeersel: ^([0-9]+)( .*)*( )([\u00C0-\u017Fa-zA-Z]+)
            if re.match('^([0-9]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\']+)', straat):
                split = re.search('^([0-9]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\']+)', straat)
                splitstraat = split.group(3)
                splitnummer = split.group(1)
                straatlengte = len(splitstraat)
                nummerlengte = len(splitnummer)
                nummerposbegin = 0
                nummerposeind = nummerlengte
                straatposbegin = nummerposeind + 1
                straatposeind = straatposbegin + straatlengte

            # straat + nummer
            # oude: ([a-zA-Z]+)( )?([0-9]+)
            # nieuw: (([a-zA-Z]+) ([0-9]+.*,))
            elif re.match('^([ \u00C0-\u017Fa-zA-Z\']+) ([0-9]+( ?bis)?)', straat):
                split = re.search('^([ \u00C0-\u017Fa-zA-Z\']+) ([0-9]+( ?bis)?)', straat)
                splitstraat = split.group(1)
                splitnummer = split.group(2)
                nummerlengte = len(splitnummer)
                straatlengte = len(splitstraat)
                straatposbegin = 0
                straatposeind = straatlengte
                nummerposbegin = straatlengte + 1
                nummerposeind = nummerposbegin + nummerlengte
            else:
                continue
            
            # zipcode + city
            # oud: ([A-Z]*-?[0-9]+)( )?([\u00C0-\u017Fa-zA-Z]+)
            # nieuw: ([ A-Z-]*[0-9]+) ?([\u00C0-\u017Fa-zA-Z .\/-]+)$
            if re.match('([ A-Z-]*[0-9]+) ?([\u00C0-\u017Fa-zA-Z .\/-]+)$', city):
                split = re.search('([ A-Z-]*[0-9]+) ?([\u00C0-\u017Fa-zA-Z .\/-]+)$', city)
                splitcity = split.group(2)
                splitzipcode = split.group(1)
                print("city: " + splitcity)
                print("zipcode: " + splitzipcode)
                citylengte = len(splitcity)
                zipcodelengte = len(splitzipcode)
                zipcodeposbegin = totale_lengte_straat + 1
                zipcodeposeind = zipcodeposbegin + zipcodelengte
                cityposbegin = zipcodeposeind + 1
                cityposeind = cityposbegin + citylengte

            # city + zipcode 
            elif re.match('([\u00C0-\u017Fa-zA-Z .\/-]+) ?([ A-Z-]*[0-9]+)$', city):
                split = re.search('([\u00C0-\u017Fa-zA-Z .\/-]+) ?([ A-Z-]*[0-9]+)$', city)
                splitcity = split.group(1)
                splitzipcode = split.group(2)
                print("city: " + splitcity)
                print("zipcode: " + splitzipcode)
                zipcodelengte = len(splitzipcode)
                citylengte = len(splitcity)
                cityposbegin = totale_lengte_straat + 1
                cityposeind = cityposbegin + citylengte
                zipcodeposbegin = cityposeind + 1
                zipcodeposeind = zipcodeposbegin + zipcodelengte
            else:
                continue




        # city = row[1]
        # citylengte = len(city)
        # straatposbegin = 0
        # straatposeind = straatlengte
        # cityposbegin = straatlengte+1
        # cityposeind = adreslengte
        # # print(row[0] + "length: " + str(len(row[0])))
            f = open("result.py", 'a')
            f.write("\t(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")]),\n")
            f.close()
            # print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")
    f = open("result.py", "a")
    f.write("]")
    f.close()
        # ("Reuterstr. 131,53113 Bonn", [(0, 10, "STREET"), (11, 14, "NUMBER"), (15, 20, "ZIPCODE"), (21, 25, "CITY")],