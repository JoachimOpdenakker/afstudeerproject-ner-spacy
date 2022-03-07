import pickle
import pandas as pd

df = pd.read_pickle("./data/samples/20msample.pkl")

#STREET CITY ZIPCODE
# extract_street = df.filter(items=['street', 'city', 'zip_code', 'person_ctry_code'])
# dropstreet = extract_street.dropna()
# filterstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# nostreet = filterstreet[filterstreet['person_ctry_code'].isin(['US'])]
# dropstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# newstreet = dropstreet[dropstreet['person_ctry_code'].isin(['US'])]]
# pf = pf.groupby(['person_ctry_code'])

#ADDRESS1 ADDRESS2
pf = df.filter(items=['address_1', 'address_2', 'person_ctry_code'])
pf = pf.dropna()
pf = pf.sort_values(by=[('person_ctry_code')])
pf = pf[pf['person_ctry_code'].isin(['US'])]
result = pf.filter(items=['address_1', 'address_2'])




result.to_csv('./data/samples/500ksample-americanfilter-address.csv', index=False)

#%%
