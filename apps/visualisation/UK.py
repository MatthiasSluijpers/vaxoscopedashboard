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



## CREATE VISUALISATIONS FOR UK ------------------------------------------------

# Line graph for vaccination coverage in UK
figVacUK = px.line( preparation.vaccCovUK,
                    x="date",
                    y="coverage_full_dose",
                    title='<b>Vaccination level in the United Kingdom:</b>',
                    labels = {"coverage_full_dose" : "Vaccination Level (%)",
                              "date" : "Date"},
                    range_y = [0,100],
                    template = "seaborn")

# Line graph for predicted vaccination coverage in UK
figVacPredUK = px.line(     modelling.vaccCovPredUK,
                            x="date",
                            y="predicted",
                            labels = {"predicted" : "Predicted Vaccination Level (%)"})
figVacConfLowUK = px.line(  modelling.vaccCovPredUK,
                            x="date",
                            y="lower_confint",
                            labels = {"lower_confint" : "Lower limit of confidence interval"})
figVacConfUpUK = px.line(   modelling.vaccCovPredUK,
                            x="date",
                            y="upper_confint",
                            labels = {"upper_confint" : "Upper limit of confidence interval"})

# Combine line graphs from above and adjust appearance
figVacUK.update_traces(connectgaps=True)
figVacUK.update_traces(line_color="crimson")
figVacPredUK.update_traces(line_color="seagreen")
figVacConfLowUK.update_traces(line_color="#b8d7c6")
figVacConfUpUK.update_traces(line_color="#b8d7c6")
figVacUK.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")
figVacUK.add_trace(figVacPredUK.data[0])
figVacUK.add_trace(figVacConfLowUK.data[0])
figVacUK.add_trace(figVacConfUpUK.data[0])

# Define function to recode category labels
def custom_legend_name(figure, new_names):
    """ Recode labels for variable categories in plotly express graph

        Parameters:
        figure (plotly express graph): graph containing category labels to recode
        new_names (list): list with new category names as strings

        Returns:
        Nothing, instead directly adjusts the ploty express graph
    """
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name

# Line graph for attitudes towards vaccination in UK
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

# Bar chart for vaccination level per income group in UK
figIncomeUK = px.bar(   preparation.vaccIncomeUK,
                        x='income_group',
                        y='coverage_one_dose',
                        title='<b>Vaccination level per deprivation class in the United Kingdom:</b>',
                        labels= {"income_group" : "Index of Multiple Deprivation (IMD) Groups",
                                 "coverage_one_dose" : "Vaccination Level (%) adults, one-or-two doses"},
                        range_y = [75,100],
                        template = "seaborn")

figIncomeUK.update_traces(marker_color='crimson')

# Bar chart for vaccination coverage per age in UK
figAgeUK = px.bar(  preparation.vaccAgeUK,
                    x='age_group',
                    y='coverage_full_dose',
                    title='<b>Vaccination level per age group in the United Kingdom:</b>',
                    labels= {"age_group" : "Age Group",
                             "coverage_full_dose" : "Vaccination Level (%)"},
                    range_y = [40,100],
                    template = "seaborn")

figAgeUK.update_traces(marker_color='crimson')

# Choropleth for vaccination coverage per UK lower tier local authority
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



## DEFINE LAYOUT OF UK PAGE ----------------------------------------------------

# Create a grid with the UK visualisations as defined above
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
