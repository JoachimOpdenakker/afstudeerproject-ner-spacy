import pickle
import numpy as np
import pandas as pd
import re
from unidecode import unidecode

f = open("./output/fouten_generate.txt", 'w')
f.close
df = pd.read_pickle("./data/samples/500ksample.pkl")

# extract_street = df.filter(items=['street', 'city', 'zip_code', 'person_ctry_code'])
# dropstreet = extract_street.dropna()
# filterstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# nostreet = filterstreet[filterstreet['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]
# dropstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# newstreet = dropstreet[dropstreet['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]]
# pf = pf.groupby(['person_ctry_code'])

df = df.filter(items=['address_1', 'address_2', 'person_ctry_code'])
df = df.dropna()
df = df.sort_values(by=[('person_ctry_code')])
df = df[df['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]
df = df.filter(items=['address_1', 'address_2', 'person_ctry_code'])

df.to_pickle('./data/samples/500ksample-europefilter-address.pkl')

stringf = pd.DataFrame(columns=['full_address', 'straat', 'nummer', 'city', 'zipcode'])
spanf = pd.DataFrame(columns=['full_address', 'straat', 'nummer', 'city', 'zipcode'])

fail_numberstreet = 0
fail_cityzip = 0

def get_address(row):
    global fail_numberstreet
    global fail_cityzip
    row[0] = unidecode(row[0])
    row[1] = unidecode(row[1])
    row[2] = unidecode(row[2])
    full_address = unidecode(row['address_1'] + ',' + row['address_2'])
    totale_lengte_straat = len(row['address_1']) + 1
    straat = ""
    nummer = ""
    city = ""
    zipcode = ""
    straatspan = ""
    nummerspan = ""
    cityspan = ""
    zipcodespan = ""
    if re.match('^([0-9\-]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\'\-]+)', row[0]):
        split = re.search('^([0-9\-]+( ?bis)?) ([ \u00C0-\u017Fa-zA-Z\'\-]+)', row[0])
        straat = split.group(3)
        nummer = split.group(1)
        straatspan = split.span(3)
        nummerspan = split.span(1)
    # straat + nummer
    elif re.match('^([ \u00C0-\u017Fa-zA-Z\'\-]+) ([0-9\/\-]+( ?[a-zA-Z]*)?)', row[0]):
        split = re.search('^([ \u00C0-\u017Fa-zA-Z\'\-]+) ([0-9\/\-]+( ?[a-zA-Z]*)?)', row[0])
        straat = split.group(1)
        nummer = split.group(2)
        straatspan = split.span(1)
        nummerspan = split.span(2)
    else:
        f = open("./output/fouten_generate.txt", 'a')
        f.write("street/nummer: " + full_address + "\n")
        f.close()
        fail_numberstreet += 1
    
    # zipcode + city
    if re.match('([ A-Z-]*[0-9]+( ?[A-Z]{2})?) ?([\u00C0-\u0338a-zA-Z ./-]+)$', row[1]):
        split = re.search('([ A-Z-]*[0-9]+( ?[A-Z]{2})?) ?([\u00C0-\u0338a-zA-Z ./-]+)$', row[1])
        zipcode = split.group(1)
        city = split.group(3)
        zipcodespan = list(split.span(1))
        cityspan = list(split.span(3))
        zipcodespan[0] += totale_lengte_straat
        zipcodespan[1] += totale_lengte_straat
        cityspan[0] += totale_lengte_straat
        cityspan[1] += totale_lengte_straat

    # city + zipcode 
    elif re.match('([\u00C0-\u017Fa-zA-Z ./-]+) ?([ A-Z-]*[0-9]+)$', row[1]):
        split = re.search('([\u00C0-\u017Fa-zA-Z ./-]+) ?([ A-Z-]*[0-9]+)$', row[1])
        zipcode = split.group(2)
        city = split.group(1)
        zipcodespan = list(split.span(2))
        cityspan = list(split.span(1))
        zipcodespan[0] += totale_lengte_straat
        zipcodespan[1] += totale_lengte_straat
        cityspan[0] += totale_lengte_straat
        cityspan[1] += totale_lengte_straat
    else:
        f = open("./output/fouten_generate.txt", 'a')
        f.write("city: " + full_address + "\n")
        f.close()
        fail_cityzip += 1
    valuesstring = np.array([full_address, straat, nummer, city, zipcode], dtype=object)
    valuesspan = np.array([full_address, straatspan, nummerspan, cityspan, zipcodespan], dtype=object)
    stringf.loc[row.name,:]=valuesstring
    spanf.loc[row.name,:]=valuesspan
    

df.apply(lambda x: get_address(x),axis=1)

stringf.to_pickle("./data/lableddata/stringformat.pkl")
spanf.to_pickle("./data/lableddata/spanformat.pkl")

print("failed on street: ", fail_numberstreet)
print("failed on city: ", fail_cityzip)


# full_address = ""

# def get_address(address_1, address_2):-
#     full_address = address_1 + ',' + address_2




# result.to_csv('./data/samples/500ksample-europefilter-address.csv', index=False)