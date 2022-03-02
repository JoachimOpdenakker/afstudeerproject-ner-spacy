import pandas as pd

data = pd.read_pickle("PS21B_PERSON.xz.p", compression='xz')
data.to_pickle("uncompressed.pkl")
