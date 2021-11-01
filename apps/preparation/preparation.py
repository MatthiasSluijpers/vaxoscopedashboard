## DATA PREPARATION CODE -------------------------------------------------------

# This file contains data retrieval and perparation.
# These files are written to the data/prepared folder.
# The prepared files are used by modelling and visualisation code.

## IMPORT LIBRARIES ------------------------------------------------------------
import pandas as pd
import numpy as np

## RETRIEVE AND PREPARE DATA ---------------------------------------------------

# Vaccination coverage for all three countries
def prepareVaccCovAll():
    # Load data
    global vaccCov
    vaccCov = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

    # Select relevant columns
    vaccCov = vaccCov[['date', 'iso_code', 'people_vaccinated', 'people_vaccinated_per_hundred', 'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred']]

    # Select relevant countries
    countries = ['USA', 'GBR', 'NLD']
    vaccCov = vaccCov.loc[vaccCov['iso_code'].isin(countries)]

    # Drop duplicates (check before and after)
    vaccCov = vaccCov.drop_duplicates()

    # Rename columns
    vaccCov = vaccCov.rename(columns={'iso_code': 'country'})
    vaccCov = vaccCov.rename(columns={'people_vaccinated': 'count_one_dose'})
    vaccCov = vaccCov.rename(columns={'people_vaccinated_per_hundred': 'coverage_one_dose'})
    vaccCov = vaccCov.rename(columns={'people_fully_vaccinated': 'count_full_dose'})
    vaccCov = vaccCov.rename(columns={'people_fully_vaccinated_per_hundred': 'coverage_full_dose'})

    # Change data types
    vaccCov['date']= pd.to_datetime(vaccCov['date'])

    # Change 'country' values to correct abbreviations
    vaccCov['country'] = vaccCov['country'].replace("USA", "US")
    vaccCov['country'] = vaccCov['country'].replace("GBR", "UK")
    vaccCov['country'] = vaccCov['country'].replace("NLD", "NL")

prepareVaccCovAll()
