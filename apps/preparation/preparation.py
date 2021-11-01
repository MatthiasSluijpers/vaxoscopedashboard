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

# Vaccination attitudes for all three countries:
def prepareVaccAttitudes():
    # Load data
    # Note: make sure the most recent datafile is stored in the "raw" data-folder.
    # This file can be downloaded via 'https://ourworldindata.org/covid-vaccinations#attitudes-to-covid-19-vaccinations'
    # Select 'Download' under the 'Willingness to get vaccinated against COVID-19'-graph
    global vaccAttitudes
    vaccAttitudes = pd.read_csv('data/raw/covid-vaccine-willingness-and-people-vaccinated-by-country.csv')

    # Select relevant columns
    vaccAttitudes = vaccAttitudes[['Day', 'Code', 'people_vaccinated_per_hundred', 'willingness_covid_vaccinate_this_week_pct_pop', 'uncertain_covid_vaccinate_this_week_pct_pop', 'unwillingness_covid_vaccinate_this_week_pct_pop']]

    # Select relevant countries
    countries = ['USA', 'GBR', 'NLD']
    vaccAttitudes = vaccAttitudes.loc[vaccAttitudes['Code'].isin(countries)]

    # Drop duplicates (check before and after)
    vaccAttitudes = vaccAttitudes.drop_duplicates()

    # Rename columns
    vaccAttitudes = vaccAttitudes.rename(columns={'Day': 'date'})
    vaccAttitudes = vaccAttitudes.rename(columns={'Code': 'country'})
    vaccAttitudes = vaccAttitudes.rename(columns={'people_vaccinated_per_hundred': 'vaccinated_one_dose_percentage'})
    vaccAttitudes = vaccAttitudes.rename(columns={'willingness_covid_vaccinate_this_week_pct_pop': 'willing_percentage'})
    vaccAttitudes = vaccAttitudes.rename(columns={'uncertain_covid_vaccinate_this_week_pct_pop': 'uncertain_percentage'})
    vaccAttitudes = vaccAttitudes.rename(columns={'unwillingness_covid_vaccinate_this_week_pct_pop': 'unwilling_percentage'})
    # Note: the total of Vaccinated, willing, uncertain, and unwilling is always 100%.

    # Change data types
    vaccAttitudes['date']= pd.to_datetime(vaccAttitudes['date'])

    # Change 'country' values to correct abbreviations
    vaccAttitudes['country'] = vaccAttitudes['country'].replace("USA", "US")
    vaccAttitudes['country'] = vaccAttitudes['country'].replace("GBR", "UK")
    vaccAttitudes['country'] = vaccAttitudes['country'].replace("NLD", "NL")

prepareVaccAttitudes()
prepareVaccCovAll()
