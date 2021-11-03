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

# Data vaccinatiegraad USA OUD
# vaccinations = pd.read_csv("data/backup/vaccinations.csv")
# vacUSA = vaccinations.copy()
# vacUSA = vacUSA[vacUSA["location"] == "United States"][["location", "date","people_fully_vaccinated_per_hundred"]]
# vacUSA.dropna(inplace = True)

# Data vaccination coverage USA
vacUSA = preparation.vaccCov
vacUSA = vacUSA[vacUSA["country"] == "US"][["country", "date","coverage_full_dose"]]
vacUSA.dropna(inplace = True)

# Data attitudes USA OUD
# attitudes = pd.read_csv("data/backup/attitudes.csv")
# attUSA = attitudes.copy()
# attUSA = attUSA[attUSA["Entity"] == "United States"]
# attUSA.columns = ["country", "code", "date", "unwilling", "uncertain", "willing", "vaccinated"]

# Data vaccination attitudes USA
attUSA = preparation.vaccAttitudes
attUSA = attUSA[attUSA["country"] == "US"]


# Data leeftijdsgroepen USA
ageUSA = preparation.vaccAge
ageUSA = ageUSA[ageUSA["country"] == "US"]

# Data inkomensgroepen USA
incomeUSA = pd.read_csv("data/backup/incomeUSA.csv")

# Data counties USA
countiesUSAGeo = gpd.read_file("data/geometry/countiesUS.json")
countiesUSAGeo.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
countiesUSAData = pd.read_csv("data/backup/countiesUS.csv")
countiesUSAData["fips"] = countiesUSAData["fips"].astype("string")
countiesUSAGeoData = countiesUSAGeo.set_index('id').join(countiesUSAData.set_index('fips'))

# Data states USA
statesUSAGeo = gpd.read_file("data/geometry/statesUS.json")
statesUSAGeo.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
statesUSAData = pd.read_csv("data/backup/statesUS.csv")
statesUSAGeoData = statesUSAGeo.set_index('name').join(statesUSAData.set_index('state'))



## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad USA
figVacUSA = px.line(  vacUSA,
                x="date",
                y="coverage_full_dose",
                title='<b>Vaccination level in the United States:</b>',
                labels = {"coverage_full_dose" : "Vaccination Level (%)",
                          "date" : "Date"},
                range_y = [0,100],
                template = "seaborn")

figVacUSA.update_traces(connectgaps=True)
figVacUSA.update_traces(line_color="steelblue")
figVacUSA.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")

# Figuur attitudes USA
def custom_legend_name(figure, new_names):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


figAttUSA = px.line(  attUSA,
                x="date",
                y=["unwilling_percentage", "uncertain_percentage", "willing_percentage"],
                title='<b>Attitudes towards vaccination in the United States:</b>',
                labels = {"date" : "Date",
                          "value" : "Share of Population (%)",
                          "variable" : "Attitude category:"},
                range_y = [0,100],
                template = "seaborn",
                color_discrete_map = {"unwilling_percentage":"black", "uncertain_percentage":"purple", "willing_percentage":"seagreen"})

figAttUSA.update_traces(connectgaps=True)
custom_legend_name(figAttUSA, ['unwilling to get vaccinated','uncertain about vaccination', "willing but not yet vaccinated"])

# Figuur leeftijdsgroepen USA
figAgeUSA = px.bar(  ageUSA,
                    x='age_group',
                    y='coverage_full_dose',
                    title='<b>Vaccination level per age group the United States:</b>',
                    labels= {"age_group" : "Age Group",
                             "coverage_full_dose" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeUSA.update_traces(marker_color='steelblue')

# Figuur inkomensgroepen USA
figIncomeUSA = px.bar(  incomeUSA,
                    x='income',
                    y='vaccinated',
                    title='<b>Vaccination level per income group the United States:</b>',
                    labels= {"income" : "Income Group",
                             "vaccinated" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figIncomeUSA.update_traces(marker_color='steelblue')


## LAYOUT VAN PAGINA ------------------------------------------------------------------------------------------------

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vaccinations_USA', figure=figVacUSA)
        ], width = {"size":5, "offset":1}),
        dbc.Col([
            dcc.Graph(id='attitudes_USA', figure=figAttUSA)
        ], width = {"size":5})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='ages_USA', figure=figAgeUSA)
        ], width = {"size":5, "offset":1}),
        dbc.Col([
            dcc.Graph(id='income_USA', figure=figIncomeUSA)
        ], width = {"size":5})
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([html.P("Vaccination level per US Location:")],
                            className='custom-graph-title'),
            dcc.Dropdown(   id='US-location-dropwdown', multi=False,
                            options = [{"label": "US County Level", "value":"counties"},
                                      {"label": "US State Level", "value":"states"}],
                            value = "states"),
            dcc.Graph(id='counties_USA', figure={})
        ], width = {"size":5, "offset":1}),
    ]),

], fluid = True)

## INTERACTIEVE FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur states en counties US

@app.callback(
    Output('counties_USA', 'figure'),
    Input('US-location-dropwdown', 'value')
)
def update_graph(US_location_dropwdown):
    figLocationUSA = {}
    if US_location_dropwdown == "counties":
        figLocationUSA = px.choropleth( countiesUSAGeoData,
                                    geojson=countiesUSAGeoData.geometry,
                                    locations=countiesUSAGeoData.index,
                                    color="vaccinated",
                                    labels = {"vaccinated":"Vaccination Level (%)", "id":"County code"},
                                    color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                                    template = "seaborn")
        figLocationUSA.update_geos(fitbounds="locations", visible=False)
        figLocationUSA.update_geos(projection_type="orthographic")
    elif US_location_dropwdown == "states":
        figLocationUSA = px.choropleth( statesUSAGeoData,
                                    geojson=statesUSAGeoData.geometry,
                                    locations=statesUSAGeoData.index,
                                    color="vaccinated",
                                    labels = {"vaccinated":"Vaccination Level (%)", "name":"State"},
                                    color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                                    template = "seaborn")
        figLocationUSA.update_geos(fitbounds="locations", visible=False)
        figLocationUSA.update_geos(projection_type="orthographic")
    return figLocationUSA
