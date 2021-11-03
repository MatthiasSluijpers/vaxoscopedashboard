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
def prepareVaccAttitudesAll():
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


# Vaccination coverage per age level for NL
def prepareVaccAgeNL():

    # Load data
    nlAge = pd.read_csv('https://data.rivm.nl/data/covid-19/COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.csv', sep=';')

    # Replace outliers with NaNs
    nlAge['Vaccination_coverage_partly'] = nlAge['Vaccination_coverage_partly'].replace(">=95", np.nan)
    nlAge['Vaccination_coverage_partly'] = nlAge['Vaccination_coverage_partly'].replace("9999", np.nan)
    nlAge['Vaccination_coverage_completed'] = nlAge['Vaccination_coverage_completed'].replace(">=95", np.nan)
    nlAge['Vaccination_coverage_completed'] = nlAge['Vaccination_coverage_completed'].replace("9999", np.nan)

    # Select subset of rows with 'Veiligheidsregio' as region level, because using both 'Veiligheidsregio' and 'Gemeente' would be double
    regionLevel = ['Veiligheidsregio']
    nlAge = nlAge.loc[nlAge['Region_level'].isin(regionLevel)]

    # Make the vaccination coverages floats
    nlAge['Vaccination_coverage_partly'] = nlAge['Vaccination_coverage_partly'].astype('float')
    nlAge['Vaccination_coverage_completed'] = nlAge['Vaccination_coverage_completed'].astype('float')

    # Group the age groups over all regions for the vaccination coverage
    nlAge = nlAge.groupby(['Date_of_statistics', 'Age_group']).mean()

    # Make the indexes normal columns
    nlAge.reset_index(level=0, inplace=True)
    nlAge.reset_index(level=0, inplace=True)

    # Order relevant columns
    nlAge = nlAge[['Date_of_statistics', 'Age_group', 'Vaccination_coverage_partly', 'Vaccination_coverage_completed']]

    # Drop duplicates (check before and after)
    nlAge = nlAge.drop_duplicates()

    # Rename columns
    nlAge = nlAge.rename(columns={'Date_of_statistics': 'date'})
    nlAge = nlAge.rename(columns={'Age_group': 'age_group'})
    nlAge = nlAge.rename(columns={'Vaccination_coverage_partly': 'coverage_one_dose'})
    nlAge = nlAge.rename(columns={'Vaccination_coverage_completed': 'coverage_full_dose'})

    # Change data types
    nlAge['date']= pd.to_datetime(nlAge['date'])

    # Add 'count_one_dose', 'count_full_dose', and 'country' column
    nlAge.insert(2, 'count_one_dose', np.nan)
    nlAge.insert(3, 'count_full_dose', np.nan)
    nlAge['country'] = 'NL'

    # Return data
    return nlAge


# Vaccination coverage per age level for UK
def prepareVaccAgeUK():

    # Load data
    ukAge = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=E92000001&metric=vaccinationsAgeDemographics&format=csv')

    # Select relevant columns
    ukAge = ukAge[['date', 'age', 'cumPeopleVaccinatedFirstDoseByVaccinationDate', 'cumPeopleVaccinatedCompleteByVaccinationDate', 'cumVaccinationFirstDoseUptakeByVaccinationDatePercentage', 'cumVaccinationCompleteCoverageByVaccinationDatePercentage']]

    # Drop duplicates (check before and after)
    ukAge = ukAge.drop_duplicates()

    # Rename columns
    ukAge = ukAge.rename(columns={'age': 'age_group'})
    ukAge = ukAge.rename(columns={'cumPeopleVaccinatedFirstDoseByVaccinationDate': 'count_one_dose'})
    ukAge = ukAge.rename(columns={'cumVaccinationFirstDoseUptakeByVaccinationDatePercentage': 'coverage_one_dose'})
    ukAge = ukAge.rename(columns={'cumPeopleVaccinatedCompleteByVaccinationDate': 'count_full_dose'})
    ukAge = ukAge.rename(columns={'cumVaccinationCompleteCoverageByVaccinationDatePercentage': 'coverage_full_dose'})

    # Change data types
    ukAge['date']= pd.to_datetime(ukAge['date'])

    # Add 'country' column
    ukAge['country'] = 'UK'

    # Recode age labels
    ukAge['age_group'] = ukAge['age_group'].replace({'12_15': '12-15', '16_17': '16-17', '18_24': '18-24', '25_29': '25-29',
                                                      '30_34': '30-34', '35_39': '35-39', '40_44': '40-44', '45_49': '45-49',
                                                       '50_54': '50-54', '55_59': '55-59', '60_64': '60-64', '65_69': '65-69',
                                                      '70_74': '70-74', '75_79': '75-79', '80_84': '80-84', '90+': '90+'})

    # Filter by latest date
    ukAge = ukAge[ukAge["date"]==ukAge["date"].max()]

    # Return data
    return ukAge

# Vaccination coverage per age level for US
def prepareVaccAgeUS():

    # Load data
    usa = pd.read_csv("https://data.cdc.gov/resource/km4m-vcsb.csv")

    age_groups = ['Ages_<12yrs','Ages_12-15_yrs','Ages_16-17_yrs','Ages_18-24_yrs','Ages_18-29_yrs',
    'Ages_25-39_yrs','Ages_30-39_yrs','Ages_40-49_yrs','Ages_50-64_yrs','Ages_65-74_yrs','Ages_75+_yrs',
    'Ages_<18yrs','Age_unknown','Age_known']

    usaAge = usa.loc[usa['demographic_category'].isin(age_groups)]

    # Select relevant columns
    usaAge = usaAge[['date',
     'demographic_category',
     'administered_dose1',
     'administered_dose1_pct',
     'series_complete_yes',
     'series_complete_pop_pct']]

    # Rename columns
    usaAge = usaAge.rename(columns={'demographic_category': 'age_group'})
    usaAge = usaAge.rename(columns={'recip_state': 'state'})
    usaAge = usaAge.rename(columns={'administered_dose1': 'count_one_dose'})
    usaAge = usaAge.rename(columns={'administered_dose1_pct': 'coverage_one_dose'})
    usaAge = usaAge.rename(columns={'series_complete_yes': 'count_full_dose'})
    usaAge = usaAge.rename(columns={'series_complete_pop_pct': 'coverage_full_dose'})

    # Change data types
    usaAge = usaAge.astype({'date': 'datetime64[ns]'})

    # Drop duplicates (check before and after)
    usaAge = usaAge.drop_duplicates()

    # Add 'country' column
    usaAge['country'] = 'US'

    usaAge['age_group'] = usaAge['age_group'].replace({'Ages_18-24_yrs': '18-24', 'Ages_50-64_yrs': '50-64', 'Ages_75+_yrs': '75+', 'Ages_65-74_yrs': '65-74',
                                                      'Ages_25-39_yrs': '25-39', 'Ages_50-65_yrs': '50-65', 'Ages_16-17_yrs': '16-17', 'Ages_<12yrs': '12-',
                                                       'Ages_40-49_yrs': '40-49', 'Ages_<18yrs': '18-', 'Ages_12-15_yrs': '12-15', 'Ages_30-39_yrs': '30-39',
                                                      'Ages_18-29_yrs': '18-29', 'Age_unknown': 'Age unknown', 'Age_known': 'Age known'})

    # Filter by latest date
    usaAge = usaAge[usaAge["date"]==usaAge["date"].max()]

    # Drop age known, age unkown and 18 minus columns
    usaAge = usaAge[~usaAge["age_group"].isin(["Age known", "Age unknown", "18-"])]

    # Sort by age group
    usaAge = usaAge.sort_values(by="age_group")

    # Return data
    return usaAge

# Vaccination coverage per age level for all countries
def prepareVaccAgeAll():

    # First retrieve and prepare vaccination coverage per age for each seperate country
    nlAge = prepareVaccAgeNL()
    ukAge = prepareVaccAgeUK()
    usaAge = prepareVaccAgeUS()

    # Then merge tables into one table
    global vaccAge
    vaccAge = pd.concat([nlAge, ukAge, usaAge], ignore_index=True, sort=False)
    vaccAge = vaccAge[['date', 'country', 'age_group', 'count_one_dose', 'coverage_one_dose', 'count_full_dose', 'coverage_full_dose']]

    vaccAge

    vaccAge.age_group.unique()


prepareVaccAgeAll()
prepareVaccAttitudesAll()
prepareVaccCovAll()
