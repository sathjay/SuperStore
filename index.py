import dash
import dash_bootstrap_components as dbc

# Define the external CSS

font_awesome1 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css'
font_awesome2 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/regular.min.css'
font_awesome3 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/solid.min.css'

external_stylesheets = [font_awesome1, font_awesome2,
                        font_awesome3, dbc.themes.BOOTSTRAP]

# create a Dash instance

app = dash.Dash(__name__, title='SuperStore Data & Analytics', external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)


server = app.server
