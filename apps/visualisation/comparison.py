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

# Data vaccinatiegraad COMP OUD
# vaccinations = pd.read_csv("data/backup/vaccinations.csv")
# vacComp = vaccinations.copy()
# vacComp = vacComp.loc[vacComp["location"].isin(["Netherlands", "United Kingdom", "United States"])][["location", "date","people_fully_vaccinated_per_hundred"]]
# vacComp.dropna(inplace = True)

# Data vaccination coverage for all three countries
vacComp = preparation.vaccCov
vacComp.dropna(inplace = True)


# # Data attitudes COMP OUD
# attitudes = pd.read_csv("data/backup/attitudes.csv")
# attComp = attitudes.copy()
# attComp.columns = ["country", "code", "date", "unwilling", "uncertain", "willing", "vaccinated"]
# attComp = attComp.loc[attComp["country"].isin(["Netherlands", "United Kingdom", "United States"])]

# Data vaccination attitudes for all three countries
attComp = preparation.vaccAttitudes



## LAYOUT VAN PAGINA ------------------------------------------------------------------------------------------------

layout = dbc.Container([


    dbc.Row([

        dbc.Col([
            html.P("Select countries to compare:",style={"fontStyle": "italic", "fontWeight":600})
        ], width = {"size":2, "offset":3}, className="country-selection-instruction"),

        dbc.Col([
            dcc.Checklist(id='selected-countries',
                          options= [{"label": "The Netherlands", "value":"NL"},
                                    {"label": "United Kingdom", "value":"UK"},
                                    {"label": "United States", "value":"US"}],
                          value=['NL', 'UK', 'US'],
                          labelClassName="checkbox-list")
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

    dbc.Row([

        dbc.Col([
            html.Div([html.P("Attitudes towards vaccination per Country:")],
                            className='custom-graph-title'),
            dcc.Dropdown(   id='attitude-dropwdown', multi=False,
                            options = [{"label": "Unwilling to get vaccinated", "value":"unwilling_percentage"},
                                      {"label": "Uncertain about vaccination", "value":"uncertain_percentage"},
                                      {"label": "Willing but not yet vaccinated", "value":"willing_percentage"}],
                            value = "unwilling_percentage"
                     ),
            dcc.Graph(id='attitudes_Comp', figure={})
        ], width = {"size":8, "offset":2}),

        dbc.Col([
            #dcc.Graph(id='graph_name', figure={})
        ], width = {"size":0})
    ]),



], fluid = True)


## INTERACTIEVE FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad

@app.callback(
    Output('vaccinations_Comp', 'figure'),
    Input('selected-countries', 'value')
)
def update_graph(selected_countries):
    figVacComp = px.line(  vacComp.loc[vacComp['country'].isin(selected_countries)],
                    x="date",
                    y="coverage_full_dose",
                    color="country",
                    title='<b>Vaccination level per Country:</b>',
                    labels = {"coverage_full_dose" : "Vaccination Level (%)",
                              "date" : "Date"},
                    range_y = [0,100],
                    template = "seaborn",
                    color_discrete_map = {"Netherlands":"#b67a0c", "United Kingdom":"crimson", "United States":"steelblue"})

    figVacComp.update_traces(connectgaps=True)
    figVacComp.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")
    return figVacComp

# Figuur attitudes

@app.callback(
    Output('attitudes_Comp', 'figure'),
    [Input('selected-countries', 'value'),
     Input('attitude-dropwdown', 'value')]
)
def update_graph(selected_countries, attitude_dropdown):
    figAttComp = px.line(attComp.loc[attComp['country'].isin(selected_countries)],
                    x="date",
                    y= attitude_dropdown,
                    color="country",
                    labels = {"date" : "Date",
                              "value" : "Share of Population (%)"},
                    range_y = [0,100],
                    template = "seaborn",
                    color_discrete_map = {"unwilling_percentage":"black", "uncertain_percentage":"purple", "willing_percentage":"seagreen"})
    figAttComp.update_traces(connectgaps=True)
    return figAttComp