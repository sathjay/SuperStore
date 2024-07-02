import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import dash  # (version 1.9.1) pip install dash==1.9.1
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State



home_page_layout = html.Div([
    
    html.H1("This is Home Page", className="text-center"),
    ])