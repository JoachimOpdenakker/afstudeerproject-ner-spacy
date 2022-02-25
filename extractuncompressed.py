import pickle
import pandas as pd
# pickle_file =  pickle.load(open("100ksample.pkl", 'rb'))
# bla = open("blacombo.txt", "a")

# print(pickle_file)

df = pd.read_pickle("500ksample.pkl")

# print(df.count())

# df.filter(items=['street', 'city'])

# print(df.filter(items=['street', 'city']))

# pf = df.filter(items=['street', 'city', 'zip_code', 'person_ctry_code'])
# pf = pf.dropna()
# # print(pf.groupby(['person_ctry_code']).mean())
# pf.to_csv('./street.csv', index=False)

extract_street = df.filter(items=['street', 'city', 'zip_code', 'person_ctry_code'])
dropstreet = extract_street.dropna()
filterstreet = dropstreet.sort_values(by=[('person_ctry_code')])
nostreet = filterstreet[filterstreet['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]
# dropstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# newstreet = dropstreet[dropstreet['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]]
# pf = pf.groupby(['person_ctry_code'])
bla = df.filter(items=['address_1', 'address_2', 'person_ctry_code'])
pf = bla.dropna()
test = pf.sort_values(by=[('person_ctry_code')])
probeersel = test[test['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]
# pf = pf[pf['address_1'].str.match('[0-9]+( )?[a-zA-Z]+|[a-zA-Z]+( )?[0-9]+')]
result = probeersel.filter(items=['address_1', 'address_2'])



result.to_csv('./500ksample-europefilter-address.csv', index=False)

# bla.close()

#%%
