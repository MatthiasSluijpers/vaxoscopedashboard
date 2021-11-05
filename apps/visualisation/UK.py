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



## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad UK
figVacUK = px.line( preparation.vaccCovUK,
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


figAttUK = px.line( preparation.vaccAttitudesUK,
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
figIncomeUK = px.bar(   preparation.vaccIncomeUK,
                        x='income_group',
                        y='coverage_one_dose',
                        title='<b>Vaccination level per deprivation class in the United Kingdom:</b>',
                        labels= {"income_group" : "Index of Multiple Deprivation (IMD) Groups",
                                 "coverage_one_dose" : "Vaccination Level (%) adults, one-or-two doses"},
                        range_y = [75,100],
                        template = "seaborn")

figIncomeUK.update_traces(marker_color='crimson')

# Figure age groups UK
figAgeUK = px.bar(  preparation.vaccAgeUK,
                    x='age_group',
                    y='coverage_full_dose',
                    title='<b>Vaccination level per age group in the United Kingdom:</b>',
                    labels= {"age_group" : "Age Group",
                             "coverage_full_dose" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeUK.update_traces(marker_color='crimson')

# Figuur lower tier local authorities UK
figLtlaUK = px.choropleth( preparation.vaccLocMapUK,
                            geojson=preparation.vaccLocMapUK.geometry,
                            locations=preparation.vaccLocMapUK.index,
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
