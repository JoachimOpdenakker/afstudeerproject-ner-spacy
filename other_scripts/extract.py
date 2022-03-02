import pandas as pd
data = pd.read_pickle("PS21B_PERSON.xz.p", compression='xz')

for i in data.person_address:
    f = open("test.txt", "a")
    f.write(str(i)+"\n")
    f.close()
