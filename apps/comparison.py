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



## FIGUREN MAKEN ------------------------------------------------------------------------------------------------

# Figuur vaccinatiegraad UK
figVacUK = px.line(  vacComp,
                x="date",
                y="people_fully_vaccinated_per_hundred",
                color="location",
                title='<b>Vaccination level per Country:</b>',
                labels = {"people_fully_vaccinated_per_hundred" : "Vaccination Level (%)",
                          "date" : "Date"},
                range_y = [0,100],
                template = "seaborn",
                color_discrete_map = {"Netherlands":"#b67a0c", "United Kingdom":"crimson", "United States":"steelblue"})

figVacUK.update_traces(connectgaps=True)
figVacUK.add_hline(y=90, line_width=2, line_dash="dash", opacity=0.2, annotation_text="<i>theoretical herd immunity</i>", annotation_position="top right")

# Figuur attitudes UK
def custom_legend_name(figure, new_names):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


figAttUK = px.line(  attUK,
                x="date",
                y=["unwilling", "uncertain", "willing"],
                title='<b>Attitudes towards vaccination in the United Kingdom:</b>',
                labels = {"date" : "Date",
                          "value" : "Share of Population (%)"},
                range_y = [0,100],
                template = "seaborn",
                color_discrete_map = {"unwilling":"black", "uncertain":"purple", "willing":"seagreen"})

figAttUK.update_traces(connectgaps=True)
custom_legend_name(figAttUK, ['unwilling to get vaccinated','uncertain about vaccination', "willing but not yet vaccinated"])

# Figuur inkomensgroepen UK
figIncomeUK = px.bar(  incomeUK,
                    x='deprivation',
                    y='vaccinated',
                    title='<b>Vaccination level per deprivation class the United Kingdom:</b>',
                    labels= {"deprivation" : "Index of Multiple Deprivation (IMD) Groups",
                             "vaccinated" : "Vaccination Level (%) one-or-two doses"},
                    range_y = [75,100],
                    template = "seaborn")

figIncomeUK.update_traces(marker_color='crimson')




## LAYOUT VAN PAGINA ------------------------------------------------------------------------------------------------

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vaccinations_UK', figure=figVacUK)
        ], width = {"size":9, "offset":2}),
        dbc.Col([
            #dcc.Graph(id='graph_name', figure={})
        ], width = {"size":0})
    ]),


], fluid = True)
