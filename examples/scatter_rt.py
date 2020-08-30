import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import examples.scatter_rt_js as rjs
import dash_leaflet.express as dlx

from dash.dependencies import Input, Output
from dash_transcrypt import inject_js, module_to_props

# Create some markers.
points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]
data = dlx.dicts_to_geojson(points)
# Create geojson.
js = module_to_props(rjs)  # compiles the js
geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=rjs.point_to_layer),  # pass function as prop
                     hideout=dict(scale=10), id="geojson")  # pass variables to function
# Create the app.
app = dash.Dash()
app.layout = html.Div([
    dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'}),
    dcc.Slider(min=1, max=100, value=10, id="slider")
])
inject_js(app, js)  # adds the js to the app


@app.callback(Output("geojson", "hideout"), [Input("slider", "value")], prevent_initial_call=False)
def update_scale(value):
    return dict(scale=value)


if __name__ == '__main__':
    app.run_server()
