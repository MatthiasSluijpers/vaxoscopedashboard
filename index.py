from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import re

# Connect to main app.py file
from app import app
from app import server

# Connect to seperate app screens
from apps.visualisation import NL, UK, USA, comparison
from apps.preparation import preparation
from apps.modelling import modelling

# DEFINE GLOBAL APP LAYOUT -----------------------------------------------------------------------

navbar = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink("VaxoScope:", href="/", active=False)),
        dbc.NavItem(dbc.NavLink("The Netherlands", href="/NL", active="partial")),
        dbc.NavItem(dbc.NavLink("United Kingdom", href="/UK", active="partial")),
        dbc.NavItem(dbc.NavLink("United States of America", href="/USA", active="partial")),
        dbc.NavItem(dbc.NavLink("Comparison", href="/Comparison", active="partial"))
    ],
    pills=True,
    horizontal="center",

)

content = html.Div(id="page-content")

app.layout = dbc.Container([dcc.Location(id="url"), navbar, content], fluid=True)

# DEFINE HOMESCREEN LAYOUT -----------------------------------------------------------------------

home_layout = dbc.Container([

dbc.Row([
    dbc.Col([html.H3("""Welcome! Please select a category above to start
                        or view the direct target group reports below.""",
                        className="introduction-message"),
    ],width = {"size":6, "offset":3})
    ]),

dbc.Row([

    dbc.Col([
        html.Div([
            html.Div([html.P("Dutch target group estimation:")],
                    className = "target-report-title target-report-title-NL"),
            html.Div([html.P("Municipalities: " + modelling.locTargetRecNL() + " (top-ten targets).")],
                    className = "target-report-text"),
            html.Div([html.P("Age group: " + modelling.ageTargetRecNL() + " (top target).")],
                    className = "target-report-text"),
        ],className='target-report-card target-report-card-NL'),
    ],width = {"size":4, "offset":0}, className="target-report-col"),

        dbc.Col([
            html.Div([
                html.Div([html.P("British target group estimation:")],
                        className = "target-report-title target-report-title-UK"),
                html.Div([html.P("Local authorities: " + modelling.locTargetRecUK() + " (top-ten targets).")],
                        className = "target-report-text"),
                html.Div([html.P("Age group: " + modelling.ageTargetRecUK() + " (top target).")],
                        className = "target-report-text"),
                html.Div([html.P("Deprivation group: " + modelling.incomeTargetRecUK() + " (top target).")],
                        className = "target-report-text"),
            ],className='target-report-card target-report-card-UK'),
        ],width = {"size":4, "offset":0}, className="target-report-col"),

        ], justify = "center"),

dbc.Row([

        dbc.Col([
            html.Div([
                html.Div([html.P("American target group estimation:")],
                        className = "target-report-title target-report-title-USA"),
                html.Div([html.P("States: " + modelling.locTargetRecUS() + " (top-ten targets).")],
                        className = "target-report-text"),
                html.Div([html.P("Age group: " + modelling.ageTargetRecUS() + " (top target).")],
                        className = "target-report-text"),
                html.Div([html.P("Income group: " + modelling.incomeTargetRecUS() + " (top target).")],
                        className = "target-report-text"),
            ],className='target-report-card target-report-card-USA'),
        ],width = {"size":4, "offset":0}, className="target-report-col"),

        dbc.Col([
            html.Div([
                html.Div([html.P("Country vaccination success:")],
                        className = "target-report-title target-report-title-comp"),
                html.Div([html.P("Country with the highest vaccination degree: " + modelling.highestCovComp() + " (of the three included in dashboard).")],
                        className = "target-report-text"),
                html.Div([html.P("Country with most citizens unwilling to take vaccine: " + modelling.highestUnwilComp() + " (of the three included in dashboard).")],
                        className = "target-report-text"),
            ],className='target-report-card target-report-card-comp'),
        ],width = {"size":4, "offset":0}, className="target-report-col"),

        ], justify = "center"),

dbc.Row([
        dbc.Col([
            html.Div([html.P("""Recommendations based on characteristics of groups with lowest vaccination degree in available data.
            Note that further medical considerations (e.g. high-risk groups) are not accounted for.
            Use the seperate country screens to identify additional target groups.""")],
                 className = "target-report-explanation"),],
         width = {"size":6, "offset":3}),
        ]),

])

# UPDATE APP LAYOUT -----------------------------------------------------------------------------


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        if(preparation.checkForRefresh()):
            preparation.refreshData()
            modelling.refreshFutureCoveragePrediction()
        return home_layout
    if pathname == '/NL':
        if(preparation.checkForRefresh()):
            preparation.refreshData()
            modelling.refreshFutureCoveragePrediction()
        return NL.layout
    if pathname == '/UK':
        if(preparation.checkForRefresh()):
            preparation.refreshData()
            modelling.refreshFutureCoveragePrediction()
        return UK.layout
    if pathname == '/USA':
        if(preparation.checkForRefresh()):
            preparation.refreshData()
            modelling.refreshFutureCoveragePrediction()
        return USA.layout
    if pathname == '/Comparison':
        if(preparation.checkForRefresh()):
            preparation.refreshData()
            modelling.refreshFutureCoveragePrediction()
        return comparison.layout
    if pathname == '/Refresh':
        preparation.refreshData()
        modelling.refreshFutureCoveragePrediction()
        return "The data was successfully refreshed."
    else:
        return "This page does not exist."


# RUN APP ON SERVER -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=5000)
