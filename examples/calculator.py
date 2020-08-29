import dash
import dash_core_components as dcc
import dash_html_components as html
import examples.caculator_cf as ccf

from dash.dependencies import Output, Input
from dash_transcrypt import module_to_clientside_functions, inject_js

# Create example app.
app = dash.Dash()
app.layout = html.Div([
    dcc.Input(id="a", value=2, type="number"), html.Div("+"),
    dcc.Input(id="b", value=2, type="number"), html.Div("="), html.Div(id="c"),
])
# Create clientside callback.
inject_js(app, module_to_clientside_functions(ccf))
app.clientside_callback(ccf.add, Output("c", "children"), [Input("a", "value"), Input("b", "value")])

if __name__ == '__main__':
    app.run_server()
