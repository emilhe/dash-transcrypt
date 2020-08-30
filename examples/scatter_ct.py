import random
import dash
import dash_html_components as html
import dash_leaflet as dl
import examples.scatter_ct_js as cjs
import dash_leaflet.express as dlx

from dash_transcrypt import inject_js, module_to_props

# Create some markers.
points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]
data = dlx.dicts_to_geojson(points)
# Create geojson.
js = module_to_props(cjs, scale=20)  # compiles the js
geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=cjs.point_to_layer))  # pass function as prop
# Create the app.
app = dash.Dash()
app.layout = html.Div([dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'})])
inject_js(app, js)  # adds the js to the app

if __name__ == '__main__':
    app.run_server()
