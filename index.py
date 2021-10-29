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

def stateRecUSA():
    c = USA.statesUSAData
    c = c.sort_values(by='vaccinated').iloc[0:10,0].to_string(index=False)
    c = c.replace("\n", ", ")
    c = re.sub('\s+',' ',c).strip()
    return c

def ageRecUSA():
    a = USA.ageUSA
    a = a[a["vaccinated"] == a["vaccinated"].min()]["age_group"]
    a = a.to_string(index=False)
    return a

def incomeRecUSA():
    i = USA.incomeUSA
    # Line below excludes "no income reported" class as this is no clear target group
    # LET OP: VERANDER LINE ONDER als deze klasse bij uiteindelijke dataset andere naam heeft
    i = i[i["income"] != "No Income Reported"]
    i = i[i["vaccinated"] == i["vaccinated"].min()]["income"]
    i = i.to_string(index=False)
    return i

def highestVacComp():
    v = comparison.vacComp
    v = v.loc[v["location"].isin(["Netherlands", "United Kingdom", "United States"])]
    v = v[v["people_fully_vaccinated_per_hundred"]==v["people_fully_vaccinated_per_hundred"].max()]["location"]
    v = v.to_string(index=False)
    return v

def highestUnwilComp():
    a = comparison.attComp
    a = a[a["unwilling"]==a["unwilling"].max()]["country"]
    a = a.to_string(index=False)
    return a



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
            html.Div([html.P("Municipalities: " + municRecNL() + " (top-ten targets).")],
                    className = "target-report-text"),
            html.Div([html.P("Age group: " + ageRecNL() + " (top target).")],
                    className = "target-report-text"),
        ],className='target-report-card target-report-card-NL'),
    ],width = {"size":4, "offset":0}, className="target-report-col"),

        dbc.Col([
            html.Div([
                html.Div([html.P("British target group estimation:")],
                        className = "target-report-title target-report-title-UK"),
                html.Div([html.P("Municipalities: " + ltlaRecUK() + " (top-ten targets).")],
                        className = "target-report-text"),
                html.Div([html.P("Deprivation group: " + incomeRecUK() + " (top target).")],
                        className = "target-report-text"),
            ],className='target-report-card target-report-card-UK'),
        ],width = {"size":4, "offset":0}, className="target-report-col"),

        ], justify = "center"),

dbc.Row([

        dbc.Col([
            html.Div([
                html.Div([html.P("American target group estimation:")],
                        className = "target-report-title target-report-title-USA"),
                html.Div([html.P("States: " + stateRecUSA() + " (top-ten targets).")],
                        className = "target-report-text"),
                html.Div([html.P("Age group: " + ageRecUSA() + " (top target).")],
                        className = "target-report-text"),
                html.Div([html.P("Income group: " + incomeRecUSA() + " (top target).")],
                        className = "target-report-text"),
            ],className='target-report-card target-report-card-USA'),
        ],width = {"size":4, "offset":0}, className="target-report-col"),

        dbc.Col([
            html.Div([
                html.Div([html.P("Country vaccination success:")],
                        className = "target-report-title target-report-title-comp"),
                html.Div([html.P("Country with the highest vaccination degree: " + highestVacComp() + " (of the three included in dashboard).")],
                        className = "target-report-text"),
                html.Div([html.P("Country with most citizens unwilling to take vaccine: " + highestUnwilComp() + " (of the three included in dashboard).")],
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
