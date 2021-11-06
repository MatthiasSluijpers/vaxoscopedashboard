## MODELLING CODE --------------------------------------------------------------

# This file only contains modelling for predictive analytics and target reports.
# The modelling for descriptive analytics is included in visuation code.
print("modelling start")
## IMPORT LIBRARIES ------------------------------------------------------------
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
from datetime import datetime as dt
from datetime import timedelta
import re
from apps.preparation import preparation

## PREDICTIVE MODELLING --------------------------------------------------------

# Predict future vaccination coverage
def predictFutureCoverage(countryVaccCov):

    # Try to predict future vaccination coverage
    try:
        # Extract historical coverage percentages and dates
        trainingSeries = countryVaccCov[['date', 'coverage_full_dose']]
        trainingSeries = trainingSeries.dropna()
        trainingSeries = trainingSeries.reset_index()

        # Create ARIMA time-series forecasting model
        forecastModel = pm.auto_arima(  trainingSeries.coverage_full_dose, start_p=1, start_q=1,
                                          test='adf',       # use adftest to find optimal 'd'
                                          max_p=3, max_q=3, # maximum p and q
                                          m=1,              # frequency of series
                                          d=None,           # let model determine 'd'
                                          seasonal=False,   # No Seasonality
                                          start_P=0,
                                          D=0,
                                          trace=True,
                                          error_action='ignore',
                                          suppress_warnings=True,
                                          stepwise=True)


        # Forecast vaccination coverage for next month
        n_periods = 30
        fc, confint = forecastModel.predict(n_periods=n_periods, return_conf_int=True)
        index_of_fc = np.arange(len(trainingSeries.coverage_full_dose), len(trainingSeries.coverage_full_dose)+n_periods)

        fc_series = pd.Series(fc, index=index_of_fc)
        lower_series = pd.Series(confint[:, 0], index=index_of_fc)
        upper_series = pd.Series(confint[:, 1], index=index_of_fc)


        # Store forecasted values and confidence interval in table
        forecast = pd.DataFrame({ 'predicted': fc_series,
                                    'lower_confint': lower_series,
                                    "upper_confint": upper_series})


        # Add correct dates corresponding to forecasts to table
        last_date = trainingSeries['date'].iloc[-1]
        dates = pd.date_range(last_date + timedelta(days=1), periods = 30, name='date')
        forecast['date'] = dates

    #If forecast fails due to incompatible data, then create empty table
    except:
        forecast = pd.DataFrame()
        forecast['predicted'] = np.NaN
        forecast['lower_confint'] = np.NaN
        forecast['upper_confint'] = np.NaN
        forecast['date'] = np.NaN
        print("Could not forecast vaccination coverage.")

    # Return forcasted coverage
    return forecast

# Refresh pediction of future vaccination coverage for two of three countries:
def refreshFutureCoveragePrediction():

    # No prediction for NL as forecasts have insufficent confidence.
    # global vaccCovPredNL
    # vaccCovPredNL = predictFutureCoverage(preparation.vaccCovNL)

    # Predict future vaccination coverage for NL
    global vaccCovPredUK
    vaccCovPredUK = predictFutureCoverage(preparation.vaccCovUK)

    # Predict future vaccination coverage for US
    global vaccCovPredUS
    vaccCovPredUS = predictFutureCoverage(preparation.vaccCovUS)

# Predict at dashboard launch
refreshFutureCoveragePrediction()

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

print("modelling end")
