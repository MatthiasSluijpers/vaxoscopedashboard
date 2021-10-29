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



## DATA OPHALEN ------------------------------------------------------------------------------------------------

# Data vaccinatiegraad NL
vaccinations = pd.read_csv("data/backup/vaccinations.csv")
vacNL = vaccinations.copy()
vacNL = vacNL[vacNL["location"] == "Netherlands"][["location", "date","people_fully_vaccinated_per_hundred"]]
vacNL.dropna(inplace = True)

# Data attitudes NL
attitudes = pd.read_csv("data/backup/attitudes.csv")
attNL = attitudes.copy()
attNL = attNL[attNL["Entity"] == "Netherlands"]
attNL.columns = ["country", "code", "date", "unwilling", "uncertain", "willing", "vaccinated"]

# Data leeftijdsgroepen NL
ageNL = pd.read_csv("data/backup/agesNL.csv")

# Data gemeentes NL
municNLGeo = gpd.read_file("data/geometry/municipalitiesNL.json")
municNLGeo.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
municNLData = pd.read_csv("data/backup/municNL.csv")
municNLGeoData = municNLGeo.set_index('statnaam').join(municNLData.set_index('region'))




## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad NL
figVacNL = px.line(  vacNL,
                x="date",
                y="people_fully_vaccinated_per_hundred",
                title='<b>Vaccination level in The Netherlands:</b>',
                labels = {"people_fully_vaccinated_per_hundred" : "Vaccination Level (%)",
                          "date" : "Date"},
                range_y = [0,100],
                template = "seaborn")

figVacNL.update_traces(connectgaps=True)
figVacNL.update_traces(line_color='#b67a0c')
figVacNL.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")

# Figuur attitudes NL
def custom_legend_name(figure, new_names):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


figAttNL = px.line(  attNL,
                x="date",
                y=["unwilling", "uncertain", "willing"],
                title='<b>Attitudes towards vaccination in The Netherlands:</b>',
                labels = {"date" : "Date",
                          "value" : "Share of Population (%)",
                          "variable" : "Attitude category:"},
                range_y = [0,100],
                template = "seaborn",
                color_discrete_map = {"unwilling":"black", "uncertain":"purple", "willing":"seagreen"})

figAttNL.update_traces(connectgaps=True)
custom_legend_name(figAttNL, ['unwilling to get vaccinated','uncertain about vaccination', "willing but not yet vaccinated"])

# Figuur leeftijdsgroepen NL
figAgeNL = px.bar(  ageNL,
                    x='age_group',
                    y='vaccinated',
                    title='<b>Vaccination level per age group The Netherlands:</b>',
                    labels= {"age_group" : "Age Group",
                             "vaccinated" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeNL.update_traces(marker_color='#b67a0c')


# Figuur gemeentes NL
figMunicNL = px.choropleth( municNLGeoData,
                            geojson=municNLGeoData.geometry,
                            locations=municNLGeoData.index,
                            color="vaccinated",
                            title="<b>Vaccination level per Dutch municipality:</b>",
                            labels = {"vaccinated":"Vaccination Level (%)", "statnaam":"Municipality"},
                            color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                            template = "seaborn")
figMunicNL.update_geos(fitbounds="locations", visible=False)
figMunicNL.update_geos(projection_type="orthographic")



## LAYOUT VAN PAGINA ------------------------------------------------------------------------------------------------

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vaccinations_NL', figure=figVacNL)
        ], width = {"size":5, "offset":1}),
        dbc.Col([
            dcc.Graph(id='attitudes_NL', figure=figAttNL)
        ], width = {"size":5})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='ages_NL', figure=figAgeNL)
        ], width = {"size":5, "offset":1}),
        dbc.Col([
            dcc.Graph(id='munic_NL', figure=figMunicNL)
        ], width = {"size":5})
    ]),

], fluid = True)
