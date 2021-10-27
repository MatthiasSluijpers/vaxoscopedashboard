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
vacComp = vacComp.loc[vacComp["location"].isin(["Netherlands", "United Kingdom", "United States"])][["location", "date","people_fully_vaccinated_per_hundred"]]
vacComp.dropna(inplace = True)

# Data attitudes COMP
attitudes = pd.read_csv("data/attitudes.csv")
attComp = attitudes.copy()
attComp.columns = ["country", "code", "date", "unwilling", "uncertain", "willing", "vaccinated"]
attComp = attComp.loc[attComp["country"].isin(["Netherlands", "United Kingdom", "United States"])]


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

    dbc.Row([

        dbc.Col([
            html.Div([html.P("Attitudes towards vaccination per Country:")],
                            className='custom-graph-title'),
            dcc.Dropdown(   id='attitude-dropwdown', multi=False,
                            options = [{"label": "Unwilling to get vaccinated", "value":"unwilling"},
                                      {"label": "Uncertain about vaccination", "value":"uncertain"},
                                      {"label": "Willing but not yet vaccinated", "value":"willing"}],
                            value = "unwilling"
                     ),
            dcc.Graph(id='attitudes_Comp', figure={})
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

# Figuur attitudes

@app.callback(
    Output('attitudes_Comp', 'figure'),
    [Input('selected-countries', 'value'),
     Input('attitude-dropwdown', 'value')]
)
def update_graph(selected_countries, attitude_dropdown):
    def custom_legend_name(figure, new_names):
        for i, new_name in enumerate(new_names):
            figure.data[i].name = new_name
    figAttComp = px.line(attComp.loc[attComp['country'].isin(selected_countries)],
                    x="date",
                    y= attitude_dropdown,
                    color="country",
                    labels = {"date" : "Date",
                              "value" : "Share of Population (%)"},
                    range_y = [0,100],
                    template = "seaborn",
                    color_discrete_map = {"unwilling":"black", "uncertain":"purple", "willing":"seagreen"})
    figAttComp.update_traces(connectgaps=True)
    #custom_legend_name(attComp, ['unwilling to get vaccinated','uncertain about vaccination', "willing but not yet vaccinated"])
    return figAttComp
