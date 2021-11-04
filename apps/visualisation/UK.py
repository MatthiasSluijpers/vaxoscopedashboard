from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np
import pyproj
import pathlib
from app import app
import dash_bootstrap_components as dbc
from apps.preparation import preparation



## DATA OPHALEN ------------------------------------------------------------------------------------------------

# # Data vaccinatiegraad UK OUD
# vaccinations = pd.read_csv("data/backup/vaccinations.csv")
# vacUK = vaccinations.copy()
# vacUK = vacUK[vacUK["location"] == "United Kingdom"][["location", "date","people_fully_vaccinated_per_hundred"]]
# vacUK.dropna(inplace = True)

# Data vaccination coverage UK
vacUK = preparation.vaccCov
vacUK = vacUK[vacUK["country"] == "UK"][["country", "date","coverage_full_dose"]]
vacUK.dropna(inplace = True)

# Data attitudes UK OUD
# attitudes = pd.read_csv("data/backup/attitudes.csv")
# attUK = attitudes.copy()
# attUK = attUK[attUK["Entity"] == "United Kingdom"]
# attUK.columns = ["country", "code", "date", "unwilling", "uncertain", "willing", "vaccinated"]

# Data vaccination attitudes UK
attUK = preparation.vaccAttitudes
attUK = attUK[attUK["country"] == "UK"]

# Data inkomensgroepen UK
incomeUK = pd.read_csv("data/backup/incomeUK.csv")

# Data age groups UK
ageUK = preparation.vaccAge
ageUK = ageUK[ageUK["country"] == "UK"]

# Data lower tier local authorities UK
ltlaUKGeo = gpd.read_file("data/geometry/ltlaUK.json")
ltlaUKData = pd.read_csv("data/backup/ltlaUK.csv", sep=";")
ltlaUKGeoData = ltlaUKGeo.set_index('AREANM').join(ltlaUKData.set_index('ltla_name'))



## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad UK
figVacUK = px.line(  vacUK,
                x="date",
                y="coverage_full_dose",
                title='<b>Vaccination level in the United Kingdom:</b>',
                labels = {"coverage_full_dose" : "Vaccination Level (%)",
                          "date" : "Date"},
                range_y = [0,100],
                template = "seaborn")

figVacUK.update_traces(connectgaps=True)
figVacUK.update_traces(line_color="crimson")
figVacUK.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")

# Figuur attitudes UK
def custom_legend_name(figure, new_names):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


figAttUK = px.line(  attUK,
                x="date",
                y=["unwilling_percentage", "uncertain_percentage", "willing_percentage"],
                title='<b>Attitudes towards vaccination in the United Kingdom:</b>',
                labels = {"date" : "Date",
                          "value" : "Share of Population (%)",
                          "variable" : "Attitude category:"},
                range_y = [0,100],
                template = "seaborn",
                color_discrete_map = {"unwilling_percentage":"black", "uncertain_percentage":"purple", "willing_percentage":"seagreen"})

figAttUK.update_traces(connectgaps=True)
custom_legend_name(figAttUK, ['unwilling to get vaccinated','uncertain about vaccination', "willing but not yet vaccinated"])

# Figuur inkomensgroepen UK
figIncomeUK = px.bar(  incomeUK,
                    x='deprivation',
                    y='vaccinated',
                    title='<b>Vaccination level per deprivation class the United Kingdom:</b>',
                    labels= {"deprivation" : "Index of Multiple Deprivation (IMD) Groups",
                             "vaccinated" : "Vaccination Level (%) one-or-two doses"},
                    range_y = [75,100],
                    template = "seaborn")

figIncomeUK.update_traces(marker_color='crimson')

# Figure age groups NL
figAgeUK = px.bar(  ageUK,
                    x='age_group',
                    y='coverage_full_dose',
                    title='<b>Vaccination level per age group The Netherlands:</b>',
                    labels= {"age_group" : "Age Group",
                             "coverage_full_dose" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeUK.update_traces(marker_color='crimson')

# Figuur lower tier local authorities UK
figLtlaUK = px.choropleth( preparation.vaccLocUK,
                            geojson=preparation.vaccLocUK.geometry,
                            locations=preparation.vaccLocUK.index,
                            color="coverage_full_dose",
                            title="<b>Vaccination level per UK Lower Tier Local Authority:</b>",
                            labels = {"coverage_full_dose":"Vaccination Level (%)", "AREANM":"Lower Tier Local Authority"},
                            color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                            template = "seaborn")
figLtlaUK.update_geos(fitbounds="locations", visible=False)
figLtlaUK.update_geos(projection_type="orthographic")



## LAYOUT VAN PAGINA ------------------------------------------------------------------------------------------------

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vaccinations_UK', figure=figVacUK)
        ], width = {"size":5, "offset":1}),
        dbc.Col([
            dcc.Graph(id='attitudes_UK', figure=figAttUK)
        ], width = {"size":5})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='age_UK', figure=figAgeUK)
        ], width = {"size":5, "offset":1}),
        dbc.Col([
            dcc.Graph(id='region_UK', figure=figLtlaUK)
        ], width = {"size":5})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='income_UK', figure=figIncomeUK)
        ], width = {"size":5, "offset":1}),
    ]),

], fluid = True)
