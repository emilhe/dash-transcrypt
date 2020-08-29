import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import examples.scatter_rt_js as rjs

from dash.dependencies import Input, Output
from dash_transcrypt import inject_js, module_to_props

# Create geojson.
js = module_to_props(rjs)  # compiles the js
geojson = dl.GeoJSON(url="/assets/CA.json", options=dict(pointToLayer=rjs.point_to_layer), # pass function as prop
                     hideout=dict(scale=100, radius_property="population"), id="geojson")  # pass variables to function
# Create the app.
app = dash.Dash()
app.layout = html.Div([
    dl.Map([dl.TileLayer(), geojson], center=(36.77, -119.41), zoom=5, style={'height': '50vh'}),
    dcc.Slider(min=5, max=200, value=100, id="slider")
])
inject_js(app, js)  # adds the js to the app


@app.callback(Output("geojson", "hideout"), [Input("slider", "value")], prevent_initial_call=False)
def update_scale(value):
    return dict(scale=value, radius_property="population")


if __name__ == '__main__':
    app.run_server(port=8888)
