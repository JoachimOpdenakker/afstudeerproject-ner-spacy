import csv
import re
with open('address.csv', newline="\n") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        adres = ','.join(row)
        adreslengte = len(adres)
        straat = row[0]
        city = row[1]
        straatposbegin = ""
        straatposeind = ""
        nummerposbegin =""
        nummerposeind = ""
        cityposbegin = ""
        cityposeind = ""
        zipcodeposbegin =""
        zipcodeposeind =""
        if re.match('[0-9]+( )?[a-zA-Z]+', straat):
            splitstreet = re.search('([0-9]+)( )?([a-zA-Z]+)', straat)
            straat = splitstreet.group(2)
            nummer = splitstreet.group(0)
            straatlengte = len(straat)
            nummerlengte = len(nummer)
            nummerposbegin = 0
            nummerposeind = nummerlengte
            straatposbegin = nummerposeind + 1
            straatposeind = straatposbegin + len(straat)

        elif re.match('([a-zA-Z]+)( )?([0-9]+)', straat):
            splitstreet = re.search('([a-zA-Z]+)( )?([0-9]+)', straat)
            straat = splitstreet.group(0)
            nummer = splitstreet.group(2)
            nummerlengte = len(nummer)
            straatlengte = len(straat)
            straatposbegin = 0
            straatposeind = straatlengte
            nummerposbegin = straatlengte + 1
            nummerposeind = nummerposbegin + len(nummer)
        else:
            continue
        
        if re.match('([A-Z]*-?[0-9]+)( )?([\u00C0-\u017Fa-zA-Z]+)', city):
            splitcity = re.search('([A-Z]*-?[0-9]+)( )?([\u00C0-\u017Fa-zA-Z]+)', city)
            city = splitcity.group(2)
            zipcode = splitcity.group(0)
            citylengte = len(city)
            zipcodelengte = len(zipcode)
            zipcodeposbegin = 0
            zipcodeposeind = zipcodelengte
            cityposbegin = zipcodeposeind + 1
            cityposeind = cityposbegin + len(city)

        elif re.match('([\u00C0-\u017Fa-zA-Z]+)( )?([A-Z]*-?[0-9]+)', city):
            splitcity = re.search('([\u00C0-\u017Fa-zA-Z]+)( )?([A-Z]*-?[0-9]+)', city)
            city = splitcity.group(0)
            zipcode = splitcity.group(2)
            zipcodelengte = len(zipcode)
            citylengte = len(city)
            cityposbegin = 0
            cityposeind = citylengte
            zipcodeposbegin = citylengte + 1
            zipcodeposeind = zipcodeposbegin + len(zipcode)
        else:
            continue




        # city = row[1]
        # citylengte = len(city)
        # straatposbegin = 0
        # straatposeind = straatlengte
        # cityposbegin = straatlengte+1
        # cityposeind = adreslengte
        # # print(row[0] + "length: " + str(len(row[0])))
        print("(\""+adres+"\","+"[("+str(straatposbegin)+","+str(straatposeind)+", \"STREET\"),("+str(nummerposbegin)+","+str(nummerposeind)+", \"NUMBER\"),("+str(cityposbegin)+","+str(cityposeind)+", \"CITY\"),("+str(zipcodeposbegin)+","+str(zipcodeposeind)+", \"ZIPCODE\")])")


        # ("Reuterstr. 131,53113 Bonn", [(0, 10, "STREET"), (11, 14, "NUMBER"), (15, 20, "ZIPCODE"), (21, 25, "CITY")],