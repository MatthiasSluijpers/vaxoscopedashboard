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

# Data vaccinatiegraad COMP
vaccinations = pd.read_csv("data/vaccinations.csv")
vacComp = vaccinations.copy()
vacComp = vacComp[(vacComp["location"] == "Netherlands") | (vacComp["location"] == "United Kingdom") | (vacComp["location"] == "United States")][["location", "date","people_fully_vaccinated_per_hundred"]]
vacComp.dropna(inplace = True)

# Data attitudes UK
attitudes = pd.read_csv("data/attitudes.csv")
attUK = attitudes.copy()
attUK = attUK[attUK["Entity"] == "United Kingdom"]
attUK.columns = ["country", "code", "date", "unwilling", "uncertain", "willing", "vaccinated"]

# Data inkomensgroepen UK
incomeUK = pd.read_csv("data/incomeUK.csv")



## LAYOUT VAN PAGINA ------------------------------------------------------------------------------------------------

layout = dbc.Container([


    dbc.Row([

        dbc.Col([
            html.P("Select countries to compare:",style={"fontStyle": "italic", "fontWeight":600})
        ], width = {"size":2, "offset":3}, className="country-selection-instruction"),

        dbc.Col([
            dcc.Checklist(id='selected-countries',
                          options= [{"label": "The Netherlands", "value":"Netherlands"},
                                    {"label": "United Kingdom", "value":"United Kingdom"},
                                    {"label": "United States", "value":"United States"}],
                          value=['Netherlands', 'United Kingdom', 'United States'],
                          labelClassName="radio-button")
        ], width = {"size":4, "offset":0}, className="country-selection-box"),
    ], className="country-selection-row"),

    dbc.Row([

        dbc.Col([
            dcc.Graph(id='vaccinations_Comp', figure={})
        ], width = {"size":8, "offset":2}),

        dbc.Col([
            #dcc.Graph(id='graph_name', figure={})
        ], width = {"size":0})
    ]),


], fluid = True)


## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad

@app.callback(
    Output('vaccinations_Comp', 'figure'),
    Input('selected-countries', 'value')
)
def update_graph(selected_countries):
    figVacComp = px.line(  vacComp.loc[vacComp['location'].isin(selected_countries)],
                    x="date",
                    y="people_fully_vaccinated_per_hundred",
                    color="location",
                    title='<b>Vaccination level per Country:</b>',
                    labels = {"people_fully_vaccinated_per_hundred" : "Vaccination Level (%)",
                              "date" : "Date"},
                    range_y = [0,100],
                    template = "seaborn",
                    color_discrete_map = {"Netherlands":"#b67a0c", "United Kingdom":"crimson", "United States":"steelblue"})

    figVacComp.update_traces(connectgaps=True)
    figVacComp.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")
    return figVacComp
