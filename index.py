from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import NL, UK, USA


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



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        welcome_layout = dbc.Container([
        dbc.Col([html.H3("Welcome! Please select a category above to start.")],
        width = {"size":6, "offset":3})
        ])
        return welcome_layout
    if pathname == '/NL':
        return NL.layout
    if pathname == '/UK':
        return UK.layout
    if pathname == '/USA':
        return USA.layout
    else:
        return "This page is not implemented yet."


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=5000)
