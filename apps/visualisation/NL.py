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
from apps.modelling import modelling



## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad NL
figVacNL = px.line( preparation.vaccCovNL,
                    x="date",
                    y="coverage_full_dose",
                    title='<b>Vaccination level in The Netherlands:</b>',
                    labels = {"coverage_full_dose" : "Vaccination Level (%)",
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


figAttNL = px.line( preparation.vaccAttitudesNL,
                    x="date",
                    y=["unwilling_percentage", "uncertain_percentage", "willing_percentage"],
                    title='<b>Attitudes towards vaccination in The Netherlands:</b>',
                    labels = {"date" : "Date",
                              "value" : "Share of Population (%)",
                              "variable" : "Attitude category:"},
                    range_y = [0,100],
                    template = "seaborn",
                    color_discrete_map = {"unwilling_percentage":"black", "uncertain_percentage":"purple", "willing_percentage":"seagreen"})

figAttNL.update_traces(connectgaps=True)
custom_legend_name(figAttNL, ['unwilling to get vaccinated','uncertain about vaccination', "willing but not yet vaccinated"])

# Figuur leeftijdsgroepen NL
figAgeNL = px.bar(  preparation.vaccAgeNL,
                    x='age_group',
                    y='coverage_full_dose',
                    title='<b>Vaccination level per age group The Netherlands:</b>',
                    labels= {"age_group" : "Age Group",
                             "coverage_full_dose" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeNL.update_traces(marker_color='#b67a0c')


# Figuur gemeentes NL
figMunicNL = px.choropleth( preparation.vaccLocMapNL,
                            geojson=preparation.vaccLocMapNL.geometry,
                            locations=preparation.vaccLocMapNL.index,
                            color="coverage_full_dose",
                            title="<b>Vaccination level per Dutch municipality:</b>",
                            labels = {"coverage_full_dose":"Vaccination Level (%)", "statnaam":"Municipality"},
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
