import pickle
import pandas as pd
import numpy as np
import re
from unidecode import unidecode

df = pd.read_pickle("./data/samples/500ksample.pkl")

#STREET CITY ZIPCODE
# extract_street = df.filter(items=['street', 'city', 'zip_code', 'person_ctry_code'])
# dropstreet = extract_street.dropna()
# filterstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# nostreet = filterstreet[filterstreet['person_ctry_code'].isin(['US'])]
# dropstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# newstreet = dropstreet[dropstreet['person_ctry_code'].isin(['US'])]]
# pf = pf.groupby(['person_ctry_code'])

#ADDRESS1 ADDRESS2
df = df.filter(items=['address_1', 'address_2', 'person_ctry_code'])
df = df.dropna()
df = df.sort_values(by=[('person_ctry_code')])
df = df[df['person_ctry_code'].isin(['US'])]
result = df.filter(items=['address_1', 'address_2'])

result.to_pickle('./data/samples/500ksample-americanfilter-address.pkl')

stringf = pd.DataFrame(columns=['full_address', 'straat', 'nummer', 'city', 'zipcode', 'state'])
spanf = pd.DataFrame(columns=['full_address', 'straat', 'nummer', 'city', 'zipcode', 'state'])

fail_nummer = 0
fail_straat = 0
fail_city = 0
fail_zipcode = 0
fail_state = 0

def fout(element,adres, fails):
    f = open("./output/fouten_generate.txt", 'a')
    f.write(element + ": " + adres + "\n")
    f.close()
    return fails + 1

def get_address(row):
    global fail_nummer
    global fail_straat
    global fail_city
    global fail_zipcode
    global fail_state
    nummer = ""
    nummerspan = ""
    straat = ""
    straatspan = ""
    city = ""
    cityspan = ""
    zipcode = ""
    zipcodespan = ""
    state = ""
    statespan = ""
    row[0] = unidecode(row[0])
    row[1] = unidecode(row[1])
    full_address = row.address_1 + ',' + row.address_2
    totale_lengte_straat = len(row[0]) + 1
    if re.match('(/ )?([0-9]+)', row[0]):
        nummer = re.search('(/ )?([0-9]+)', row[0]).group(2)
        nummerspan = re.search('(/ )?([0-9]+)', row[0]).span(2)
    else:
        fail_nummer = fout("Nummer", row[0], fail_nummer)
    #straat
    if re.search('[0-9]+ ([\s\S]*)$', row[0]):
        straat = re.search('[0-9]+ ([\s\S]*)$', row[0]).group(1)
        straatspan = re.search('[0-9]+ ([\s\S]*)$', row[0]).span(1)
    else:
        fail_straat = fout("Straat", row[0], fail_straat)
        
    #city
    if re.match('([a-zA-Z ]+?(?=,))', row[1]):
        city = re.search('([a-zA-Z ]+?(?=,))', row[1]).group(1)
        cityspan = re.search('([a-zA-Z ]+?(?=,))', row[1]).span(1)
        cityspan = list(cityspan)
        cityspan[0] += totale_lengte_straat
        cityspan[1] += totale_lengte_straat
    else:
        fail_city = fout("City", row[1], fail_city)
    #zipcode
    if re.search('([0-9\-]+$)', row[1]):
        zipcode = re.search('([0-9\-]+$)', row[1]).group(1)
        zipcodespan = re.search('([0-9\-]+$)', row[1]).span(1)
        zipcodespan = list(zipcodespan)
        zipcodespan[0] += totale_lengte_straat
        zipcodespan[1] += totale_lengte_straat
    else:
        fail_zipcode = fout("Zipcode", row[1], fail_zipcode)
    #state
    if re.search('(,? )([ A-Za-z]*)(?<! ),? [0-9]', row[1]):
        state = re.search('(,? )([ A-Za-z]*)(?<! ),? [0-9]', row[1]).group(2)
        statespan = re.search('(,? )([ A-Za-z]*)(?<! ),? [0-9]', row[1]).span(2)
        statespan = list(statespan)
        statespan[0] += totale_lengte_straat
        statespan[1] += totale_lengte_straat
                
    else:
        fail_state = fout("State", row[1], fail_state)

    valuesstring = np.array([full_address, straat, nummer, city, zipcode, state], dtype=object)
    valuesspan = np.array([full_address, straatspan, nummerspan, cityspan, zipcodespan, statespan], dtype=object)
    stringf.loc[row.name,:]=valuesstring
    spanf.loc[row.name,:]=valuesspan

df.apply(lambda x: get_address(x),axis=1)

stringf.to_pickle("./data/lableddata/stringformat.pkl")
spanf.to_pickle("./data/lableddata/spanformat.pkl")

print("failed on number: ", fail_nummer)
print("failed on street: ", fail_straat)
print("failed on city: ", fail_city)
print("failed on zipcode: ", fail_zipcode)
print("failed on state: ", fail_state)
