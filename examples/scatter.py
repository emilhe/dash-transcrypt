import dash
import dash_html_components as html
import dash_leaflet as dl
import examples.scatter_js as sjs

from dash_transcrypt import inject_js, module_to_props

# Create geojson.
js = module_to_props(sjs)  # compiles the js
geojson = dl.GeoJSON(url="/assets/CA.json", options=dict(pointToLayer=sjs.point_to_layer))  # pass function as prop
# Create the app.
app = dash.Dash()
app.layout = html.Div([dl.Map([dl.TileLayer(), geojson], center=(36.77, -119.41), zoom=5, style={'height': '50vh'})])
inject_js(app, js)  # adds the js to the app

if __name__ == '__main__':
    app.run_server()
