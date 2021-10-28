import pandas as pd
import re

ageNL = pd.read_csv("data/agesNL.csv")
a = ageNL
a = a[a["vaccinated"] == a["vaccinated"].min()]["age_group"]
a = a.to_string(index=False)
print(a)
