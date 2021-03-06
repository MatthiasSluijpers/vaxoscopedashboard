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



## CREATE VISUALISATIONS FOR US ------------------------------------------------

# Line graph for vaccination coverage in US
def createCovFigUS():
    """ Create line graph for vaccination coverage in US

        Requires:
        vaccCovUS (dataframe) to be made available by preparation code

        Returns:
        figVacUSA (plotly express graph): line graph for vaccination coverage in US
    """
    figVacUSA = px.line(preparation.vaccCovUS,
                        x="date",
                        y="coverage_full_dose",
                        title='<b>Vaccination level in the United States:</b>',
                        labels = {"coverage_full_dose" : "Vaccination Level (%)",
                                  "date" : "Date"},
                        range_y = [0,100],
                        template = "seaborn")

    # Line graph for predicted vaccination coverage in US
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

    # Combine line graphs from above and adjust appearance
    figVacUSA.update_traces(connectgaps=True)
    figVacUSA.update_traces(line_color="steelblue")
    figVacPredUSA.update_traces(line_color="seagreen")
    figVacConfLowUSA.update_traces(line_color="#b8d7c6")
    figVacConfUpUSA.update_traces(line_color="#b8d7c6")
    figVacUSA.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")
    figVacUSA.add_trace(figVacPredUSA.data[0])
    figVacUSA.add_trace(figVacConfLowUSA.data[0])
    figVacUSA.add_trace(figVacConfUpUSA.data[0])
    return figVacUSA

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

# Line graph for attitudes towards vaccination in US
def createAttitudeFigUS():
    """ Creates a line graph with vaccination attitudes in US

        Requires:
        vaccAttitudesUS (dataframe) to be made available by preparation code

        Returns:
        figAttUSA (plotly express graph): line graph with vaccination attitudes in US
    """
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
    return figAttUSA

# Bar chart for vaccination coverage per age in US
def createAgeBarChartUS():
    """ Creates a bar chart with vaccination coverage per age group in US

        Requires:
        vaccAgeUS (dataframe) to be made available by preparation code

        Returns:
        figAgeUSA (plotly express graph): bar chart with vaccination coverage per age group in US
    """
    figAgeUSA = px.bar( preparation.vaccAgeUS,
                        x='age_group',
                        y='coverage_full_dose',
                        title='<b>Vaccination level per age group the United States:</b>',
                        labels= {"age_group" : "Age Group",
                                 "coverage_full_dose" : "Vaccination Level (%)"},
                        range_y = [40,100],
                        template = "seaborn")

    figAgeUSA.update_traces(marker_color='steelblue')
    return figAgeUSA

# Bar chart for vaccination level per income group in US
def createIncomeBarChartUS():
    """ Creates a bar chart with vaccination coverage per income group in US

        Requires:
        vaccIncomeUS (dataframe) to be made available by preparation code

        Returns:
        figIncomeUSA (plotly express graph): bar chart with vaccination coverage per income group in US
    """
    figIncomeUSA = px.bar(  preparation.vaccIncomeUS,
                            x='income_group',
                            y='coverage_full_dose',
                            title='<b>Vaccination level per income group the United States:</b>',
                            labels= {"income_group" : "Income Group",
                                     "coverage_full_dose" : "Vaccination Level (%), adults"},
                            range_y = [40,100],
                            template = "seaborn")

    figIncomeUSA.update_traces(marker_color='steelblue')
    return figIncomeUSA


## DEFINE LAYOUT OF US PAGE ----------------------------------------------------

# Create a grid with the US visualisations as defined above and below
# Also contains dropdown menu to choose between state of country level choropleth
def createLayoutUS():
    """ Create updated layout for US screen

        Returns:
        layout (dash layout): layout for US screen
    """
    layout = dbc.Container([

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='vaccinations_USA', figure=createCovFigUS())
            ], width = {"size":5, "offset":1}),
            dbc.Col([
                dcc.Graph(id='attitudes_USA', figure=createAttitudeFigUS())
            ], width = {"size":5})
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ages_USA', figure=createAgeBarChartUS())
            ], width = {"size":5, "offset":1}),
            dbc.Col([
                dcc.Graph(id='income_USA', figure=createIncomeBarChartUS())
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
    return layout

## UPDATE US VISUALISATIONS ----------------------------------------------------


# Return correct user requested choropleth of US
@app.callback(
    Output('counties_USA', 'figure'),
    Input('US-location-dropwdown', 'value')
)
def update_graph(US_location_dropwdown):
    figLocationUSA = {}

    # If user selected counties, then create and return county level US choropleth
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

    # If user selected states, then create and return state level US choropleth
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
