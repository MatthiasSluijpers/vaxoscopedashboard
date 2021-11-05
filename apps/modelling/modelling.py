## MODELLING CODE --------------------------------------------------------------

# This file only contains modelling for predictive analytics and target reports.
# The modelling for descriptive analytics is included in visuation code.

## IMPORT LIBRARIES ------------------------------------------------------------
import pandas as pd
import numpy as np
import re
from apps.preparation import preparation

## PREDICTIVE MODELLING --------------------------------------------------------






## TARGET REPORT MODELLING -----------------------------------------------------

# Target recommendation for age group in NL
def ageTargetRecNL():
    a = preparation.vaccAgeNL
    a = a[a["coverage_full_dose"] == a["coverage_full_dose"].min()]["age_group"]
    a = a.to_string(index=False)
    return a

# Target recommendation for age group in UK
def ageTargetRecUK():
    a = preparation.vaccAgeUK
    a = a[a["coverage_full_dose"] == a["coverage_full_dose"].min()]["age_group"]
    a = a.to_string(index=False)
    return a

# Target recommendation for age group in US
def ageTargetRecUS():
    a = preparation.vaccAgeUS
    a = a[a["coverage_full_dose"] == a["coverage_full_dose"].min()]["age_group"]
    a = a.to_string(index=False)
    return a

# Target recommendation for locations in NL
def locTargetRecNL():
    l = preparation.vaccLocNL
    l = l.sort_values(by='coverage_full_dose').iloc[0:10,2].to_string(index=False)
    l = re.sub('\s+',' ',l).strip().replace(" ", ", ")
    return l

# Target recommendation for locations in UK
def locTargetRecUK():
    l = preparation.vaccLocUK
    l = l.sort_values(by='coverage_full_dose').iloc[0:10,2].to_string(index=False)
    l = l.replace('\n', ",")
    l = re.sub('\s+',' ',l).strip()
    return l

# Target recommendation for locations in US
def locTargetRecUS():
    l = preparation.vaccLocUSState
    l = l.sort_values(by='coverage_full_dose').iloc[0:10,2].to_string(index=False)
    l = l.replace("\n", ", ")
    l = re.sub('\s+',' ',l).strip()
    return l

# Target recommendation for income group in UK
def incomeTargetRecUK():
    i = preparation.vaccIncomeUK
    i = i[i["coverage_one_dose"] == i["coverage_one_dose"].min()]["income_group"]
    i = i.to_string(index=False)
    return i

# Target recommendation for income group in US
def incomeTargetRecUS():
    i = preparation.vaccIncomeUS
    # Line below excludes "no income reported" class as this is no clear target group
    i = i[i["income_group"] != "No Income Reported"]
    i = i[i["coverage_full_dose"] == i["coverage_full_dose"].min()]["income_group"]
    i = i.to_string(index=False)
    return i

# County included in dashboard with highest vaccination coverage
def highestCovComp():
    c = preparation.vaccCov
    c = c[c["coverage_full_dose"]==c["coverage_full_dose"].max()]["country"]
    c = c.to_string(index=False)
    c = c.replace("NL","The Netherlands")
    c = c.replace("UK","United Kingdom")
    c = c.replace("US","United States")
    return c

# County included in dashboard with highest vaccination unwillingness
def highestUnwilComp():
    u = preparation.vaccAttitudes
    u = u[u["unwilling_percentage"]==u["unwilling_percentage"].max()]["country"]
    u = u.to_string(index=False)
    u = u.replace("NL","The Netherlands")
    u = u.replace("UK","United Kingdom")
    u = u.replace("US","United States")
    return u
