from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import re

# Connect to main app.py file
from app import app
from app import server

# Connect to seperate app screens
from apps import NL, UK, USA, comparison

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

# GENERATE REPORT STATS --------------------------------------------------------------------------------

def municRecNL():
    m = NL.municNLData
    m = m.sort_values(by='vaccinated').iloc[0:10,0].to_string(index=False)
    m = re.sub('\s+',' ',m).strip().replace(" ", ", ")
    return m

def ageRecNL():
    a = NL.ageNL
    a = a[a["vaccinated"] == a["vaccinated"].min()]["age_group"]
    a = a.to_string(index=False)
    return a

def ltlaRecUK():
    l = UK.ltlaUKData
    l = l.sort_values(by='vaccinated').iloc[0:10,1].to_string(index=False)
    l = l.replace('\n', ",")
    l = re.sub('\s+',' ',l).strip()
    return l

def incomeRecUK():
    i = UK.incomeUK
    i = i[i["vaccinated"] == i["vaccinated"].min()]["deprivation"]
    i = i.to_string(index=False)
    return i



# DEFINE HOMESCREEN LAYOUT -----------------------------------------------------------------------

home_layout = dbc.Container([

dbc.Row([
    dbc.Col([html.H3("Welcome! Please select a category above to start.")
    ],width = {"size":6, "offset":3})
    ]),

dbc.Row([

    dbc.Col([
        html.Div([
            html.Div([html.P("Dutch target group estimation:")],
                    className = "target-report-title target-report-title-NL"),
            html.Div([html.P("Municipalities: " + municRecNL() + " (top-ten targets).")],
                    className = "target-report-text"),
            html.Div([html.P("Age group: " + ageRecNL() + " (top target).")],
                    className = "target-report-text"),
            html.Div([html.P("Recommended based on characteristics of groups with lowest vaccination degree in available data.")],
                    className = "target-report-explanation"),
        ],className='target-report-card target-report-card-NL'),
    ],width = {"size":4, "offset":1}),

        dbc.Col([
            html.Div([
                html.Div([html.P("British target group estimation:")],
                        className = "target-report-title target-report-title-UK"),
                html.Div([html.P("Municipalities: " + ltlaRecUK() + " (top-ten targets).")],
                        className = "target-report-text"),
                html.Div([html.P("Deprivation group: " + incomeRecUK() + " (top target).")],
                        className = "target-report-text"),
                html.Div([html.P("Recommended based on characteristics of groups with lowest vaccination degree in available data.")],
                        className = "target-report-explanation"),
            ],className='target-report-card target-report-card-UK'),
        ],width = {"size":4, "offset":1}),
        ]),
])

# UPDATE APP LAYOUT -----------------------------------------------------------------------------


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        return home_layout
    if pathname == '/NL':
        return NL.layout
    if pathname == '/UK':
        return UK.layout
    if pathname == '/USA':
        return USA.layout
    if pathname == '/Comparison':
        return comparison.layout
    else:
        return "This page is not implemented yet."


# RUN APP ON SERVER -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=5000)
