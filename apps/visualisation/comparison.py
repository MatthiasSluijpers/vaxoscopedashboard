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



## DEFINE LAYOUT OF COMPARISON PAGE --------------------------------------------

# Create a grid with the comparison visualisations as defined below
# Also contains checkboxes to select countries to compare
# Also contains dropdown menu to choose between vaccination attitude
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

    ]),



], fluid = True)


## UPDATE COMPARISON VISUALISATIONS --------------------------------------------


# Return correct user requested line graph of vaccination coverage comparison
@app.callback(
    Output('vaccinations_Comp', 'figure'),
    Input('selected-countries', 'value')
)
def update_graph(selected_countries):

    # Create and return line graph that compares selected countries in terms of vaccination coverage
    figVacComp = px.line(   preparation.vaccCov.loc[preparation.vaccCov['country'].isin(selected_countries)],
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


# Return correct user requested line graph of vaccination attitude comparison
@app.callback(
    Output('attitudes_Comp', 'figure'),
    [Input('selected-countries', 'value'),
     Input('attitude-dropwdown', 'value')]
)
def update_graph(selected_countries, attitude_dropdown):

    # Create and return line graph that compares selected countries in terms of vaccination attitudes
    figAttComp = px.line(   preparation.vaccAttitudes.loc[preparation.vaccAttitudes['country'].isin(selected_countries)],
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
