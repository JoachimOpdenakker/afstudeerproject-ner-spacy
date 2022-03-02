import pickle
import pandas as pd

df = pd.read_pickle("./data/samples/500ksample.pkl")

# extract_street = df.filter(items=['street', 'city', 'zip_code', 'person_ctry_code'])
# dropstreet = extract_street.dropna()
# filterstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# nostreet = filterstreet[filterstreet['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]
# dropstreet = dropstreet.sort_values(by=[('person_ctry_code')])
# newstreet = dropstreet[dropstreet['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]]
# pf = pf.groupby(['person_ctry_code'])

pf = df.filter(items=['address_1', 'address_2', 'person_ctry_code'])
pf = pf.dropna()
pf = pf.sort_values(by=[('person_ctry_code')])
pf = pf[pf['person_ctry_code'].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PO','PT','RO','SE','SI','SK'])]
result = pf.filter(items=['address_1', 'address_2'])

result.to_csv('./data/samples/500ksample-europefilter-address.csv', index=False)