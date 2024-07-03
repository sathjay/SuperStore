import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dcc import Location, Link
from dash.dependencies import Input, Output, State


from index import app  # Import the app from index.py


from pages.home_page import home_page_layout
from pages.graph_page import graph_page_layout
from pages.table_page import table_page_layout

from Functions import load_and_preprocess_data


# File path to the Excel file
file_path = 'assets/Sample - Superstore.xlsx'

# Load and preprocess the data
original_sales_data, sales_data_with_return_and_profit_margin = load_and_preprocess_data(
    file_path)


app.layout = dbc.Container([
    dbc.Row([

        dbc.Col(

            html.H2("SuperStore Data and Analytics Dashboard"),
            width=6,
            className="text-center d-flex align-items-center justify-content-center"
        ),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.A([
                        # FontAwesome Home icon
                        html.I(
                            className="fa-solid fa-home  me-1 text-white icon-size "),
                        html.H4("Home Page", id="home-link",
                                className="card-title inactive-link")
                    ],
                        href="/",
                        className="stretched-link d-flex align-items-center no-underline")
                ]),
                className="text-center  justify-content-center align-items-center "
            )],
            width=2,
            className="no-padding "
        ),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.A([
                        # FontAwesome Table icon
                        html.I(
                            className="fa-solid fa-table   me-1 text-white icon-size "),
                        html.H4("Table Page", id="table-link",
                                className="card-title inactive-link")
                    ],
                        href="/table",
                        className="stretched-link d-flex align-items-center no-underline")
                ]),
                className="text-center justify-content-center align-items-center "
            )],
            width=2,
            className="no-padding"
        ),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.A([
                        # FontAwesome Chart icon
                        html.I(
                            className="fa-solid fa-chart-line  me-1 text-white icon-size"),
                        html.H4("Graph Page", id="graph-link",
                                className="card-title inactive-link")
                    ],
                        href="/graph",
                        className="stretched-link d-flex align-items-center no-underline")
                ]),
                className="text-center d-flex justify-content-center align-items-center"
            )],
            width=2,
            className="no-padding"
        )

    ], className="header-row no-gutters align-items-center justify-content-center"),

    html.Div(id='page-content'),

    dcc.Location(id='url', refresh=False)


], fluid=True, className="mainContainer")


@app.callback(
    [Output("home-link", "className"),
     Output("table-link", "className"),
     Output("graph-link", "className")],
    [Input("url", "pathname")]
)
def update_active_link(pathname):
    # Set all to inactive by default
    home_class = "card-title d-inline inactive-link"
    table_class = "card-title d-inline inactive-link"
    graph_class = "card-title d-inline inactive-link"

    # Set the active link based on the current pathname
    if pathname == "/":
        home_class = "card-title d-inline active-link"
    elif pathname == "/table":
        table_class = "card-title d-inline active-link"
    elif pathname == "/graph":
        graph_class = "card-title d-inline active-link"

    return home_class, table_class, graph_class


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    if pathname == "/":
        return home_page_layout
    elif pathname == "/table":
        return table_page_layout
    elif pathname == "/graph":
        return graph_page_layout

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ], style={"margin-left": "17%"},
        className="p-3 bg-light rounded-3",
    )


if __name__ == '__main__':
    app.run_server(debug=True)
