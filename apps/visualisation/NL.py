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



## CREATE VISUALISATIONS FOR NL ------------------------------------------------

# Line graph for vaccination coverage in NL
def createCovFigNL():
    """ Create line graph for vaccination coverage in NL

        Requires:
        vaccCovNL (dataframe) to be made available by preparation code

        Returns:
        figVacNL (plotly express graph): line graph for vaccination coverage in NL
    """
    # Line graph for historical vaccination coverage in NL
    figVacNL = px.line( preparation.vaccCovNL,
                        x="date",
                        y="coverage_full_dose",
                        title='<b>Vaccination level in The Netherlands:</b>',
                        labels = {"coverage_full_dose" : "Vaccination Level (%)",
                                  "date" : "Date"},
                        range_y = [0,100],
                        template = "seaborn")

    # Line graph for predicted vaccination coverage in NL
    figVacPredNL = px.line(     modelling.vaccCovPredNL,
                                x="date",
                                y="predicted",
                                labels = {"predicted" : "Predicted Vaccination Level (%)"})
    figVacConfLowNL = px.line(  modelling.vaccCovPredNL,
                                x="date",
                                y="lower_confint",
                                labels = {"lower_confint" : "Lower limit of confidence interval"})
    figVacConfUpNL = px.line(   modelling.vaccCovPredNL,
                                x="date",
                                y="upper_confint",
                                labels = {"upper_confint" : "Upper limit of confidence interval"})

    figVacNL.update_traces(connectgaps=True)
    figVacNL.update_traces(line_color='#b67a0c')
    figVacPredNL.update_traces(line_color="seagreen")
    figVacConfLowNL.update_traces(line_color="#b8d7c6")
    figVacConfUpNL.update_traces(line_color="#b8d7c6")
    figVacNL.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")
    figVacNL.add_trace(figVacPredNL.data[0])
    figVacNL.add_trace(figVacConfLowNL.data[0])
    figVacNL.add_trace(figVacConfUpNL.data[0])
    return figVacNL


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

# Line graph for attitudes towards vaccination in NL
def createAttitudeFigNL():
    """ Creates a line graph with vaccination attitudes in NL

        Requires:
        vaccAttitudesNL (dataframe) to be made available by preparation code

        Returns:
        figAttNL (plotly express graph): line graph with vaccination attitudes in NL
    """
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
    return figAttNL

# Bar chart for vaccination coverage per age in NL
def createAgeBarChartNL():
    """ Creates a bar chart with vaccination coverage per age group in NL

        Requires:
        vaccAgeNL (dataframe) to be made available by preparation code

        Returns:
        figAgeNL (plotly express graph): bar chart with vaccination coverage per age group in NL
    """
    figAgeNL = px.bar(  preparation.vaccAgeNL,
                        x='age_group',
                        y='coverage_full_dose',
                        title='<b>Vaccination level per age group The Netherlands:</b>',
                        labels= {"age_group" : "Age Group",
                                 "coverage_full_dose" : "Vaccination Level (%)"},
                        range_y = [40,100],
                        template = "seaborn")

    figAgeNL.update_traces(marker_color='#b67a0c')
    return figAgeNL


# Choropleth for vaccination coverage per Dutch municipality
def createLocationMapNL():
    """ Creates a choropleth of vaccination coverage per Dutch municipality

        Requires:
        vaccLocMapNL (geodataframe) to be made available by preparation code

        Returns:
        figMunicNL (plotly express choropleth): map of vaccination coverage per Dutch municipality
    """
    figMunicNL = px.choropleth( preparation.vaccLocMapNL,
                                geojson=preparation.vaccLocMapNL.geometry,
                                locations=preparation.vaccLocMapNL.index,
                                color="coverage_full_dose",
                                title="<b>Vaccination level per Dutch municipality:</b>",
                                labels = {"coverage_full_dose":"Vaccination Level (%), 12+", "statnaam":"Municipality"},
                                color_continuous_scale = [[0,"red"], [0.6,"orange"], [1,"steelblue"]],
                                template = "seaborn")
    figMunicNL.update_geos(fitbounds="locations", visible=False)
    figMunicNL.update_geos(projection_type="orthographic")
    return figMunicNL



## DEFINE LAYOUT OF NL PAGE ----------------------------------------------------

# Create a grid with the NL visualisations as defined above
def createLayoutNL():
    """ Create updated layout for NL screen

        Returns:
        layout (dash layout): layout for NL screen
    """
    layout = dbc.Container([

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='vaccinations_NL', figure=createCovFigNL())
            ], width = {"size":5, "offset":1}),
            dbc.Col([
                dcc.Graph(id='attitudes_NL', figure=createAttitudeFigNL())
            ], width = {"size":5})
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ages_NL', figure=createAgeBarChartNL())
            ], width = {"size":5, "offset":1}),
            dbc.Col([
                dcc.Graph(id='munic_NL', figure=createLocationMapNL())
            ], width = {"size":5})
        ]),

    ], fluid = True)
    return layout
