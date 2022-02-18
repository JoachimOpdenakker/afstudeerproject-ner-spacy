import pandas as pd


#data = pd.read_pickle("PS21B_PERSON_smplR10K.p")

data = pd.read_pickle("PS21B_PERSON_ORIG.xz.p", compression='xz')

print(data.to_string())
