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

# Figuur vaccinatiegraad USA
figVacUSA = px.line(preparation.vaccCovUS,
                    x="date",
                    y="coverage_full_dose",
                    title='<b>Vaccination level in the United States:</b>',
                    labels = {"coverage_full_dose" : "Vaccination Level (%)",
                              "date" : "Date"},
                    range_y = [0,100],
                    template = "seaborn")

figVacPredUSA = px.line(     modelling.vaccCovPredUS,
                            x="date",
                            y="predicted",
                            labels = {"predicted" : "Predicted Vaccination Level (%)"})
figVacConfLowUSA = px.line(  modelling.vaccCovPredUS,
                            x="date",
                            y="lower_confint",
                            labels = {"lower_confint" : "Lower limit of confidence interval"})
figVacConfUpUSA = px.line(   modelling.vaccCovPredUS,
                            x="date",
                            y="upper_confint",
                            labels = {"upper_confint" : "Upper limit of confidence interval"})

figVacUSA.update_traces(connectgaps=True)
figVacUSA.update_traces(line_color="steelblue")
figVacPredUSA.update_traces(line_color="seagreen")
figVacConfLowUSA.update_traces(line_color="#b8d7c6")
figVacConfUpUSA.update_traces(line_color="#b8d7c6")
figVacUSA.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")
figVacUSA.add_trace(figVacPredUSA.data[0])
figVacUSA.add_trace(figVacConfLowUSA.data[0])
figVacUSA.add_trace(figVacConfUpUSA.data[0])

# Figuur attitudes USA
def custom_legend_name(figure, new_names):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


figAttUSA = px.line(preparation.vaccAttitudesUS,
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
figAgeUSA = px.bar( preparation.vaccAgeUS,
                    x='age_group',
                    y='coverage_full_dose',
                    title='<b>Vaccination level per age group the United States:</b>',
                    labels= {"age_group" : "Age Group",
                             "coverage_full_dose" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeUSA.update_traces(marker_color='steelblue')

# Figuur inkomensgroepen USA
figIncomeUSA = px.bar(  preparation.vaccIncomeUS,
                        x='income_group',
                        y='coverage_full_dose',
                        title='<b>Vaccination level per income group the United States:</b>',
                        labels= {"income_group" : "Income Group",
                                 "coverage_full_dose" : "Vaccination Level (%)"},
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
        figLocationUSA = px.choropleth( preparation.vaccLocMapCountyUS,
                                    geojson=preparation.vaccLocMapCountyUS.geometry,
                                    locations=preparation.vaccLocMapCountyUS.index,
                                    color="coverage_full_dose",
                                    labels = {"coverage_full_dose":"Vaccination Level (%)", "index":"County code"},
                                    color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                                    template = "seaborn")
        figLocationUSA.update_geos(fitbounds=False, visible=True)
        figLocationUSA.update_geos(projection_rotation_lon=-100)
        figLocationUSA.update_geos(projection_rotation_lat=40)
        figLocationUSA.update_geos(projection_scale=1.5)
        figLocationUSA.update_geos(projection_type="orthographic")
    elif US_location_dropwdown == "states":
        figLocationUSA = px.choropleth( preparation.vaccLocMapStateUS,
                                    geojson=preparation.vaccLocMapStateUS.geometry,
                                    locations=preparation.vaccLocMapStateUS.index,
                                    color="coverage_full_dose",
                                    labels = {"coverage_full_dose":"Vaccination Level (%)", "name":"State"},
                                    color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                                    template = "seaborn")
        figLocationUSA.update_geos(fitbounds=False, visible=True)
        figLocationUSA.update_geos(projection_rotation_lon=-100)
        figLocationUSA.update_geos(projection_rotation_lat=40)
        figLocationUSA.update_geos(projection_type="orthographic")
    return figLocationUSA
