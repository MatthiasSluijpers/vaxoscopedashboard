## DATA PREPARATION CODE -------------------------------------------------------

# This file contains data retrieval and perparation.
# These files are written to the data/prepared folder.
# The prepared files are used by modelling and visualisation code.

## IMPORT LIBRARIES ------------------------------------------------------------
print("preparation start")
import pandas as pd
import geopandas as gpd
import numpy as np
import pyproj
import datetime

## RETRIEVE AND PREPARE DATA ---------------------------------------------------

# Vaccination coverage for all three countries
def prepareVaccCovAll():

    # Set data variable
    global vaccCov

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccCov = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
        vaccCov[['date', 'iso_code', 'people_vaccinated', 'people_vaccinated_per_hundred', 'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccCov = pd.read_csv("data/backup/vaccCov.csv")
        print("Note: could not load vaccination coverage data from online source, used local backup file instead.")

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

    # Drop missing values
    vaccCov = vaccCov.dropna(subset=["date", "coverage_full_dose"])

    # Also provide smaller seperate versions for each of the three countries
    global vaccCovNL
    vaccCovNL = vaccCov
    vaccCovNL = vaccCovNL[vaccCovNL["country"] == "NL"][["country", "date","coverage_full_dose"]]

    global vaccCovUK
    vaccCovUK = vaccCov
    vaccCovUK = vaccCovUK[vaccCovUK["country"] == "UK"][["country", "date","coverage_full_dose"]]

    global vaccCovUS
    vaccCovUS = vaccCov
    vaccCovUS = vaccCovUS[vaccCovUS["country"] == "US"][["country", "date","coverage_full_dose"]]


# Vaccination attitudes for all three countries:
def prepareVaccAttitudesAll():


    # Note: this data cannot be dynamically retrieved as there is no stable url/api.
    # Therefore: the dashboard uses local backup version of the dataset from 05-11-2021.
    # Optional: manually download the most recent datafile by following the three steps below:
    # Link: file can be downloaded via 'https://ourworldindata.org/covid-vaccinations#attitudes-to-covid-19-vaccinations'
    # Download: on this page, select 'Download' under the second 'Willingness to get vaccinated against COVID-19'-graph.
    # Replace: rename the file to "vaccAttitudes.csv" and place it in the "data/backup/"" folder.

    # Set data variable
    global vaccAttitudes

    # Load data
    vaccAttitudes = pd.read_csv('data/backup/vaccAttitudes.csv')

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

    # Also provide seperate versions for each of the three countries
    global vaccAttitudesNL
    vaccAttitudesNL = vaccAttitudes
    vaccAttitudesNL = vaccAttitudesNL[vaccAttitudesNL["country"] == "NL"]

    global vaccAttitudesUK
    vaccAttitudesUK = vaccAttitudes
    vaccAttitudesUK = vaccAttitudesUK[vaccAttitudesUK["country"] == "UK"]

    global vaccAttitudesUS
    vaccAttitudesUS = vaccAttitudes
    vaccAttitudesUS = vaccAttitudesUS[vaccAttitudesUS["country"] == "US"]


# Vaccination coverage per age level for NL
def prepareVaccAgeNL():

    # Set data variable
    global vaccAgeNL

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccAgeNL = pd.read_csv('https://data.rivm.nl/data/covid-19/COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.csv', sep=';')
        vaccAgeNL[['Vaccination_coverage_partly','Vaccination_coverage_completed','Date_of_statistics', 'Age_group']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccAgeNL = pd.read_csv("data/backup/vaccAgeNL.csv", sep=';')
        print("Note: could not load vaccination age data for NL from online source, used local backup file instead.")

    # Replace outliers with NaNs
    vaccAgeNL['Vaccination_coverage_partly'] = vaccAgeNL['Vaccination_coverage_partly'].replace(">=95", np.nan)
    vaccAgeNL['Vaccination_coverage_partly'] = vaccAgeNL['Vaccination_coverage_partly'].replace("9999", np.nan)
    vaccAgeNL['Vaccination_coverage_completed'] = vaccAgeNL['Vaccination_coverage_completed'].replace(">=95", np.nan)
    vaccAgeNL['Vaccination_coverage_completed'] = vaccAgeNL['Vaccination_coverage_completed'].replace("9999", np.nan)

    # Select subset of rows with 'Veiligheidsregio' as region level, because using both 'Veiligheidsregio' and 'Gemeente' would be double
    regionLevel = ['Veiligheidsregio']
    vaccAgeNL = vaccAgeNL.loc[vaccAgeNL['Region_level'].isin(regionLevel)]

    # Make the vaccination coverages floats
    vaccAgeNL['Vaccination_coverage_partly'] = vaccAgeNL['Vaccination_coverage_partly'].astype('float')
    vaccAgeNL['Vaccination_coverage_completed'] = vaccAgeNL['Vaccination_coverage_completed'].astype('float')

    # Group the age groups over all regions for the vaccination coverage
    vaccAgeNL = vaccAgeNL.groupby(['Date_of_statistics', 'Age_group']).mean()

    # Make the indexes normal columns
    vaccAgeNL.reset_index(level=0, inplace=True)
    vaccAgeNL.reset_index(level=0, inplace=True)

    # Order relevant columns
    vaccAgeNL = vaccAgeNL[['Date_of_statistics', 'Age_group', 'Vaccination_coverage_partly', 'Vaccination_coverage_completed']]

    # Drop duplicates (check before and after)
    vaccAgeNL = vaccAgeNL.drop_duplicates()

    # Rename columns
    vaccAgeNL = vaccAgeNL.rename(columns={'Date_of_statistics': 'date'})
    vaccAgeNL = vaccAgeNL.rename(columns={'Age_group': 'age_group'})
    vaccAgeNL = vaccAgeNL.rename(columns={'Vaccination_coverage_partly': 'coverage_one_dose'})
    vaccAgeNL = vaccAgeNL.rename(columns={'Vaccination_coverage_completed': 'coverage_full_dose'})

    # Change data types
    vaccAgeNL['date']= pd.to_datetime(vaccAgeNL['date'])

    # Add 'count_one_dose', 'count_full_dose', and 'country' column
    vaccAgeNL.insert(2, 'count_one_dose', np.nan)
    vaccAgeNL.insert(3, 'count_full_dose', np.nan)
    vaccAgeNL['country'] = 'NL'

    # Set column order
    vaccAgeNL = vaccAgeNL[['date', 'country', 'age_group', 'count_one_dose', 'coverage_one_dose', 'count_full_dose', 'coverage_full_dose']]


# Vaccination coverage per age level for UK
def prepareVaccAgeUK():

    # Set data variable
    global vaccAgeUK

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccAgeUK = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=E92000001&metric=vaccinationsAgeDemographics&format=csv')
        vaccAgeUK[['date', 'age', 'cumPeopleVaccinatedFirstDoseByVaccinationDate', 'cumPeopleVaccinatedCompleteByVaccinationDate', 'cumVaccinationFirstDoseUptakeByVaccinationDatePercentage', 'cumVaccinationCompleteCoverageByVaccinationDatePercentage']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccAgeUK = pd.read_csv("data/backup/vaccAgeUK.csv")
        print("Note: could not load vaccination age data for UK from online source, used local backup file instead.")

    # Select relevant columns
    vaccAgeUK = vaccAgeUK[['date', 'age', 'cumPeopleVaccinatedFirstDoseByVaccinationDate', 'cumPeopleVaccinatedCompleteByVaccinationDate', 'cumVaccinationFirstDoseUptakeByVaccinationDatePercentage', 'cumVaccinationCompleteCoverageByVaccinationDatePercentage']]

    # Drop duplicates (check before and after)
    vaccAgeUK = vaccAgeUK.drop_duplicates()

    # Rename columns
    vaccAgeUK = vaccAgeUK.rename(columns={'age': 'age_group'})
    vaccAgeUK = vaccAgeUK.rename(columns={'cumPeopleVaccinatedFirstDoseByVaccinationDate': 'count_one_dose'})
    vaccAgeUK = vaccAgeUK.rename(columns={'cumVaccinationFirstDoseUptakeByVaccinationDatePercentage': 'coverage_one_dose'})
    vaccAgeUK = vaccAgeUK.rename(columns={'cumPeopleVaccinatedCompleteByVaccinationDate': 'count_full_dose'})
    vaccAgeUK = vaccAgeUK.rename(columns={'cumVaccinationCompleteCoverageByVaccinationDatePercentage': 'coverage_full_dose'})

    # Change data types
    vaccAgeUK['date']= pd.to_datetime(vaccAgeUK['date'])

    # Add 'country' column
    vaccAgeUK['country'] = 'UK'

    # Recode age group category labels
    vaccAgeUK['age_group'] = vaccAgeUK['age_group'].replace({'12_15': '12-15', '16_17': '16-17', '18_24': '18-24', '25_29': '25-29',
                                                      '30_34': '30-34', '35_39': '35-39', '40_44': '40-44', '45_49': '45-49',
                                                       '50_54': '50-54', '55_59': '55-59', '60_64': '60-64', '65_69': '65-69',
                                                      '70_74': '70-74', '75_79': '75-79', '80_84': '80-84', '90+': '90+'})

    # Filter by latest date
    vaccAgeUK = vaccAgeUK[vaccAgeUK["date"]==vaccAgeUK["date"].max()]

    # Set column order
    vaccAgeUK = vaccAgeUK[['date', 'country', 'age_group', 'count_one_dose', 'coverage_one_dose', 'count_full_dose', 'coverage_full_dose']]


# Vaccination coverage per age level for US
def prepareVaccAgeUS():

    # Set data variable
    global vaccAgeUS

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccAgeUS = pd.read_csv("https://data.cdc.gov/resource/km4m-vcsb.csv")
        vaccAgeUS[['date','demographic_category','administered_dose1','administered_dose1_pct','series_complete_yes','series_complete_pop_pct']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccAgeUS = pd.read_csv("data/backup/vaccAgeUS.csv")
        print("Note: could not load vaccination age data for US from online source, used local backup file instead.")


    age_groups = ['Ages_<12yrs','Ages_12-15_yrs','Ages_16-17_yrs','Ages_18-24_yrs','Ages_18-29_yrs',
    'Ages_25-39_yrs','Ages_30-39_yrs','Ages_40-49_yrs','Ages_50-64_yrs','Ages_65-74_yrs','Ages_75+_yrs',
    'Ages_<18yrs','Age_unknown','Age_known']

    vaccAgeUS = vaccAgeUS.loc[vaccAgeUS['demographic_category'].isin(age_groups)]

    # Select relevant columns
    vaccAgeUS = vaccAgeUS[['date',
     'demographic_category',
     'administered_dose1',
     'administered_dose1_pct',
     'series_complete_yes',
     'series_complete_pop_pct']]

    # Rename columns
    vaccAgeUS = vaccAgeUS.rename(columns={'demographic_category': 'age_group'})
    vaccAgeUS = vaccAgeUS.rename(columns={'recip_state': 'state'})
    vaccAgeUS = vaccAgeUS.rename(columns={'administered_dose1': 'count_one_dose'})
    vaccAgeUS = vaccAgeUS.rename(columns={'administered_dose1_pct': 'coverage_one_dose'})
    vaccAgeUS = vaccAgeUS.rename(columns={'series_complete_yes': 'count_full_dose'})
    vaccAgeUS = vaccAgeUS.rename(columns={'series_complete_pop_pct': 'coverage_full_dose'})

    # Change data types
    vaccAgeUS = vaccAgeUS.astype({'date': 'datetime64[ns]'})

    # Drop duplicates (check before and after)
    vaccAgeUS = vaccAgeUS.drop_duplicates()

    # Add 'country' column
    vaccAgeUS['country'] = 'US'

    # Recode age group category labels
    vaccAgeUS['age_group'] = vaccAgeUS['age_group'].replace({'Ages_18-24_yrs': '18-24', 'Ages_50-64_yrs': '50-64', 'Ages_75+_yrs': '75+', 'Ages_65-74_yrs': '65-74',
                                                      'Ages_25-39_yrs': '25-39', 'Ages_50-65_yrs': '50-65', 'Ages_16-17_yrs': '16-17', 'Ages_<12yrs': '12-',
                                                       'Ages_40-49_yrs': '40-49', 'Ages_<18yrs': '18-', 'Ages_12-15_yrs': '12-15', 'Ages_30-39_yrs': '30-39',
                                                      'Ages_18-29_yrs': '18-29', 'Age_unknown': 'Age unknown', 'Age_known': 'Age known'})

    # Filter by latest date
    vaccAgeUS = vaccAgeUS[vaccAgeUS["date"]==vaccAgeUS["date"].max()]

    # Drop age known, age unkown and 18 minus columns
    vaccAgeUS = vaccAgeUS[~vaccAgeUS["age_group"].isin(["Age known", "Age unknown", "18-"])]

    # Sort by age group
    vaccAgeUS = vaccAgeUS.sort_values(by="age_group")

    # Set column order
    vaccAgeUS = vaccAgeUS[['date', 'country', 'age_group', 'count_one_dose', 'coverage_one_dose', 'count_full_dose', 'coverage_full_dose']]


# Vaccination coverage per age level for all countries
def prepareVaccAgeAll():

    # First retrieve and prepare vaccination coverage per age for each seperate country
    prepareVaccAgeNL()
    prepareVaccAgeUK()
    prepareVaccAgeUS()

    # Then merge tables into one table
    global vaccAge
    vaccAge = pd.concat([vaccAgeNL, vaccAgeUK, vaccAgeUS], ignore_index=True, sort=False)
    vaccAge = vaccAge[['date', 'country', 'age_group', 'count_one_dose', 'coverage_one_dose', 'count_full_dose', 'coverage_full_dose']]

# Vaccination coverage per municipality location in NL
def prepareVaccLocNL():

    # Set data variable
    global vaccLocNL

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccLocNL = pd.read_csv('https://data.rivm.nl/data/covid-19/COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.csv', sep=';')
        vaccLocNL[['Region_level', 'Region_code', 'Region_name', 'Birth_year','Date_of_statistics',  'Vaccination_coverage_completed', 'Vaccination_coverage_partly']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccLocNL = pd.read_csv("data/backup/vaccLocNL.csv", sep=";")
        print("Note: could not load vaccination location data for NL from online source, used local backup file instead.")

    # Replace outliers with NaNs
    vaccLocNL['Vaccination_coverage_partly'] = vaccLocNL['Vaccination_coverage_partly'].replace(">=95", np.nan)
    vaccLocNL['Vaccination_coverage_partly'] = vaccLocNL['Vaccination_coverage_partly'].replace("9999", np.nan)
    vaccLocNL['Vaccination_coverage_completed'] = vaccLocNL['Vaccination_coverage_completed'].replace(">=95", np.nan)
    vaccLocNL['Vaccination_coverage_completed'] = vaccLocNL['Vaccination_coverage_completed'].replace("9999", np.nan)

    # Replace Dutch Region_level names with English translations
    vaccLocNL['Region_level'] = vaccLocNL['Region_level'].replace("Gemeente", "Municipality")
    vaccLocNL['Region_level'] = vaccLocNL['Region_level'].replace("Veiligheidsregio", "Safety region")

    # Make the vaccination coverages floats
    vaccLocNL['Vaccination_coverage_partly'] = vaccLocNL['Vaccination_coverage_partly'].astype('float')
    vaccLocNL['Vaccination_coverage_completed'] = vaccLocNL['Vaccination_coverage_completed'].astype('float')

    # Select relevant columns
    vaccLocNL = vaccLocNL[['Region_level', 'Region_code', 'Region_name', 'Birth_year','Date_of_statistics',  'Vaccination_coverage_completed', 'Vaccination_coverage_partly']]

    # Drop duplicates (check before and after)
    vaccLocNL = vaccLocNL.drop_duplicates()

    # Rename columns
    vaccLocNL = vaccLocNL.rename(columns={'Date_of_statistics': 'date'})
    vaccLocNL = vaccLocNL.rename(columns={'Region_level': 'location_level'})
    vaccLocNL = vaccLocNL.rename(columns={'Region_name': 'location_name'})
    vaccLocNL = vaccLocNL.rename(columns={'Region_code': 'location_code'})
    vaccLocNL = vaccLocNL.rename(columns={'Birth_year': 'age_group'})
    vaccLocNL = vaccLocNL.rename(columns={'Vaccination_coverage_partly': 'coverage_one_dose'})
    vaccLocNL = vaccLocNL.rename(columns={'Vaccination_coverage_completed': 'coverage_full_dose'})

    # Change data types
    vaccLocNL = vaccLocNL.astype({'date': 'datetime64[ns]'})

    # Add 'count_one_dose', 'count_full_dose', and 'country' column
    vaccLocNL.insert(4, 'count_full_dose', np.nan)
    vaccLocNL.insert(5, 'count_one_dose', np.nan)
    vaccLocNL['country'] = 'NL'

    # Filter by municipality level
    vaccLocNL = vaccLocNL[vaccLocNL["location_level"]=="Municipality"]

    # Filter by latest date
    vaccLocNL = vaccLocNL[vaccLocNL["date"] == vaccLocNL["date"].max()]

    # Filter by aged 12+
    vaccLocNL = vaccLocNL[vaccLocNL["age_group"] == "<2004"]

    # Drop age group column
    vaccLocNL = vaccLocNL.drop(labels = "age_group", axis=1)

    # Match and merge data with country geography to draw map
    global vaccLocMapNL
    geoNL = gpd.read_file("data/geometry/municipalitiesNL.json")
    geoNL.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    vaccLocMapNL = geoNL.set_index('statnaam').join(vaccLocNL.set_index('location_name'))

# Vaccination coverage per lower tier local authority location in UK
def prepareVaccLocUK():

    # Set data variable
    global vaccLocUK

    # Load dynamic data by retrieving from online source
    try:
        vaccLocUK = pd.read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=cumVaccinationCompleteCoverageByVaccinationDatePercentage&format=csv")
        vaccLocUK[['areaType','areaName', 'areaCode', 'cumVaccinationCompleteCoverageByVaccinationDatePercentage', 'date']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccLocUK = pd.read_csv("data/backup/vaccLocUK.csv")
        print("Note: could not load vaccination location data for UK from online source, used local backup file instead.")

    # Drop unnecessary column
    del vaccLocUK['areaType']

    # Drop duplicates (check before and after)
    vaccLocUK = vaccLocUK.drop_duplicates()

    # Rename columns NOTE: difference between location_name and location_code
    vaccLocUK = vaccLocUK.rename(columns={'areaName': 'location_name'})
    vaccLocUK = vaccLocUK.rename(columns={'areaCode': 'location_code'})
    vaccLocUK = vaccLocUK.rename(columns={'cumVaccinationCompleteCoverageByVaccinationDatePercentage': 'coverage_full_dose'})

    # Change data types
    vaccLocUK['date']= pd.to_datetime(vaccLocUK['date'])

    # Add 'location_level' and 'country' column
    vaccLocUK.insert(0, 'location_level', 'Lower tier local authority')
    vaccLocUK['country'] = 'UK'

    # Filter by latest date
    vaccLocUK = vaccLocUK[vaccLocUK["date"]==vaccLocUK["date"].max()]

    # Match and merge data with country geography to draw map
    global vaccLocMapUK
    geoUK = gpd.read_file("data/geometry/ltlaUK.json")
    vaccLocMapUK = geoUK.set_index('AREANM').join(vaccLocUK.set_index('location_name'))

# Vaccination coverage per county and state location in US
def prepareVaccLocUS():

    # (1/2) Location on county level:

    # Set data variable
    global vaccLocUSCounty

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccLocUSCounty = pd.read_csv("https://data.cdc.gov/resource/8xkx-amqh.csv?$limit=10000")
        vaccLocUSCounty[['date','fips','recip_county','series_complete_pop_pct','series_complete_yes','administered_dose1_recip','administered_dose1_pop_pct']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccLocUSCounty = pd.read_csv("data/backup/vaccLocUSCounty.csv")
        print("Note: could not load vaccination location data for US counties from online source, used local backup file instead.")


    # Select relevant columns
    vaccLocUSCounty = vaccLocUSCounty[['date','fips','recip_county','series_complete_pop_pct','series_complete_yes','administered_dose1_recip','administered_dose1_pop_pct']]

    # Rename columns
    vaccLocUSCounty = vaccLocUSCounty.rename(columns={'recip_county': 'location_name'})
    vaccLocUSCounty = vaccLocUSCounty.rename(columns={'fips': 'location_code'})
    vaccLocUSCounty = vaccLocUSCounty.rename(columns={'administered_dose1_recip': 'count_one_dose'})
    vaccLocUSCounty = vaccLocUSCounty.rename(columns={'administered_dose1_pop_pct': 'coverage_one_dose'})
    vaccLocUSCounty = vaccLocUSCounty.rename(columns={'series_complete_yes': 'count_full_dose'})
    vaccLocUSCounty = vaccLocUSCounty.rename(columns={'series_complete_pop_pct': 'coverage_full_dose'})

    # Change data types
    vaccLocUSCounty = vaccLocUSCounty.astype({'date': 'datetime64[ns]'})

    # Drop duplicates
    vaccLocUSCounty = vaccLocUSCounty.drop_duplicates()

    # Add 'location_level' and 'country' column
    vaccLocUSCounty.insert(0, 'location_level', 'County')
    vaccLocUSCounty['country'] = 'US'

    # Filter by latest date
    vaccLocUSCounty = vaccLocUSCounty[vaccLocUSCounty["date"]==vaccLocUSCounty["date"].max()]

    # Match and merge data with country geography to draw map
    global vaccLocMapCountyUS
    geoUSCounties = gpd.read_file("data/geometry/countiesUS.json")
    geoUSCounties.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    vaccLocUSCounty["location_code"] = vaccLocUSCounty["location_code"].astype("string")
    vaccLocMapCountyUS = geoUSCounties.set_index('id').join(vaccLocUSCounty.set_index('location_code'))

    # (2/2) Location on state level:

    # Set data variable
    global vaccLocUSState

    # Load dynamic data by retrieving from online source and check structure
    try:
        vaccLocUSState = pd.read_csv("https://data.cdc.gov/resource/unsk-b7fc.csv?$limit=200")
        vaccLocUSState[['date','location','series_complete_pop_pct','series_complete_yes','administered_dose1_recip','administered_dose1_pop_pct']]
    # If data cannot be retrieved: load local backup file from 05-11-2021
    except:
        vaccLocUSState = pd.read_csv("data/backup/vaccLocUSState.csv")
        print("Note: could not load vaccination location data for US states from online source, used local backup file instead.")


    # Select relevant columns
    vaccLocUSState = vaccLocUSState[['date','location','series_complete_pop_pct','series_complete_yes','administered_dose1_recip','administered_dose1_pop_pct']]

    # Rename columns
    vaccLocUSState = vaccLocUSState.rename(columns={'location': 'location_name'})
    vaccLocUSState = vaccLocUSState.rename(columns={'fips': 'location_code'})
    vaccLocUSState = vaccLocUSState.rename(columns={'administered_dose1_recip': 'count_one_dose'})
    vaccLocUSState = vaccLocUSState.rename(columns={'administered_dose1_pop_pct': 'coverage_one_dose'})
    vaccLocUSState = vaccLocUSState.rename(columns={'series_complete_yes': 'count_full_dose'})
    vaccLocUSState = vaccLocUSState.rename(columns={'series_complete_pop_pct': 'coverage_full_dose'})

    # Change data types
    vaccLocUSState = vaccLocUSState.astype({'date': 'datetime64[ns]'})

    # Drop duplicates
    vaccLocUSState = vaccLocUSState.drop_duplicates()

    # Add 'location_level' and 'country' column
    vaccLocUSState.insert(0, 'location_level', 'County')
    vaccLocUSState['country'] = 'US'

    # Recode state names
    stateNames = {"AL" : "Alabama",
                  "AK" : "Alaska",
                  "AZ" : "Arizona",
                  "AR" : "Arkansas",
                  "CA" : "California",
                  "CO" : "Colorado",
                  "CT" : "Connecticut",
                  "DE" : "Delaware",
                  "DC" : "District of Columbia",
                  "FL" : "Florida",
                  "GA" : "Georgia",
                  "HI" : "Hawaii",
                  "ID" : "Idaho",
                  "IL" : "Illinois",
                  "IN" : "Indiana",
                  "IA" : "Iowa",
                  "KS" : "Kansas",
                  "KY" : "Kentucky",
                  "LA" : "Louisiana",
                  "ME" : "Maine",
                  "MD" : "Maryland",
                  "MA" : "Massachusetts",
                  "MI" : "Michigan",
                  "MN" : "Minnesota",
                  "MS" : "Mississippi",
                  "MO" : "Missouri",
                  "MT" : "Montana",
                  "NE" : "Nebraska",
                  "NV" : "Nevada",
                  "NH" : "New Hampshire",
                  "NJ" : "New Jersey",
                  "NM" : "New Mexico",
                  "NY" : "New York",
                  "NC" : "North Carolina",
                  "ND" : "North Dakota",
                  "OH" : "Ohio",
                  "OK" : "Oklahoma",
                  "OR" : "Oregon",
                  "PA" : "Pennsylvania",
                  "RI" : "Rhode Island",
                  "SC" : "South Carolina",
                  "SD" : "South Dakota",
                  "TN" : "Tennessee",
                  "TX" : "Texas",
                  "UT" : "Utah",
                  "VT" : "Vermont",
                  "VA" : "Virginia",
                  "WA" : "Washington",
                  "WV" : "West Virginia",
                  "WI" : "Wisconsin",
                  "WY" : "Wyoming"
                 }

    vaccLocUSState['location_name'] = vaccLocUSState['location_name'].map(stateNames)
    vaccLocUSState.dropna(subset=['location_name'], inplace = True)

    # Filter by latest date
    vaccLocUSState = vaccLocUSState[vaccLocUSState["date"]==vaccLocUSState["date"].max()]

    # Match and merge data with country geography to draw map
    global vaccLocMapStateUS
    geoUSStates = gpd.read_file("data/geometry/statesUS.json")
    geoUSStates.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    vaccLocMapStateUS = geoUSStates.set_index('name').join(vaccLocUSState.set_index('location_name'))


# Vaccination coverage per location for all three countries
def prepareVaccLocAll():

    # Retrieve and prepare vaccination coverage per location for each country
    prepareVaccLocUS()
    prepareVaccLocNL()
    prepareVaccLocUK()


# Vaccination coverage per income for NL
def prepareVaccIncomeNL():

    # Note: currently no open data is available for vaccination coverage per income group in NL.
    # Therefore: this function is a placeholder that creates an empty dataframe with expected structure.
    # Extendable: function can be updated if data becomes available in future.

    global vaccIncomeNL
    vaccIncomeNL = pd.DataFrame()
    vaccIncomeNL['date'] = np.NaN
    vaccIncomeNL['income_group'] = np.NaN
    vaccIncomeNL['coverage_one_dose'] = np.NaN
    vaccIncomeNL['coverage_full_dose'] = np.NaN
    vaccIncomeNL['count_one_dose'] = np.NaN
    vaccIncomeNL['count_full_dose'] = np.NaN
    vaccIncomeNL['country'] = "NL"

# Vaccination coverage per income for UK
def prepareVaccIncomeUK():

    # Note: this data cannot be dynamically retrieved as there is no stable url/api.
    # Furthermore: data source did not update data for last few months, next release date unkown.
    # Reference: see 'https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandwellbeing/datasets/coronavirusandvaccinehesitancygreatbritain'
    # Instead: dashboard uses pre-included and pre-processed version of dataset from July 2021 (most recent version during development).

    # Load data
    global vaccIncomeUK
    vaccIncomeUK = pd.read_csv("data/backup/incomeUK.csv")

# Vaccination coverage per income for US
def prepareVaccIncomeUS():

    # Note: this data cannot be dynamically retrieved as there is no stable url/api.
    # Furthermore: structure of data prone to change, thereby disallowing automation.
    # Reference: see table 5a from 'https://www.census.gov/data/tables/2021/demo/hhp/hhp39.html'
    # Instead: dashboard uses pre-included and pre-processed version of dataset from October 2021 (most recent version during development).
    # Update: data can be updated by manually extracting relevant statistics and calculating coverage per income group.

    # Load data
    global vaccIncomeUS
    vaccIncomeUS = pd.read_csv("data/backup/incomeUSA.csv")


# Vaccination coverage per income group for all three countries
def prepareVaccIncomeAll():

    # Retrieve and prepare vaccination coverage per income group for each country
    prepareVaccIncomeUK()
    prepareVaccIncomeNL()
    prepareVaccIncomeUS()


## DATA REFRESH MECHANISM ------------------------------------------------------

# Function to retrieve updated data from data sources
def refreshData():

    print("Refreshing data, note that this might take 0,5 to 3 minutes...")

    prepareVaccIncomeAll()
    prepareVaccLocAll()
    prepareVaccAgeAll()
    prepareVaccAttitudesAll()
    prepareVaccCovAll()

    print("Succefully refreshed data.")

def checkForRefresh():

    # Calculate minutes since last refresh
    global lastRefreshTime
    currentTime = datetime.datetime.now()
    timeElapsed = currentTime - lastRefreshTime
    minutesElapsed = timeElapsed.total_seconds() / 60

    # Refresh data if more than an hour has passed
    if(minutesElapsed > 60):
        lastRefreshTime = datetime.datetime.now()
        return True
    else:
        return False

def recordLaunchTime():

    # Record timestamp when launching dashboard
    global lastRefreshTime
    lastRefreshTime = datetime.datetime.now()


## RUN FUNCTIONS DURING LAUNCH -------------------------------------------------

recordLaunchTime()
prepareVaccIncomeAll()
prepareVaccLocAll()
prepareVaccAgeAll()
prepareVaccAttitudesAll()
prepareVaccCovAll()

print("preparation end")
