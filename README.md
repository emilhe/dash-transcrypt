The purpose of dash-transcrypt is making it easy to

* Write clientside callbacks in Python 
* Pass function handles as component properties 

Under the hood, it utilizes [transcrypt](https://www.transcrypt.org/) for the transpiling of Python to JavaScript.

## Getting started  
  
The recommended way to install dash-transcrypt is via pip,
  
	 pip install dash-transcrypt  

In addition, a working java installation is required (it's used in the minification process). To run the examples related to function properties, dash-leaflet and geobuf are also needed,
  
	 pip install geobuf dash-leaflet   
 
## Clientside callbacks 
  
The functions to be used as clientside callbacks must be placed in a separate module (file), say `calculator_cf.py`. In this example, we will consider a simple `add` function,  
  
	 def add(a, b): return a + b 

Before the `add` function can be used as a clientside callback, the `calculator_cf` module must be passed to the `to_clientside_functions` function. In addition to transpiling the module into JavaScript, it replaces the function attributes of the module with appropriate `ClientsideFunction` objects so that they can be used in clientside callbacks,  
  
	 import caculator_cf as ccf 
	 from dash_transcrypt import module_to_clientside_functions, inject_js 
	 ... 
	 inject_js(app, module_to_clientside_functions(ccf))
	 app.clientside_callback(ccf.add, ...)  
 
The `to_clientside_functions` returns the path to a JavaScript index file, which must be made available by the app (that's what `inject_js` does). For completeness, here is the full (apart from the `caculator_cf.py` file)  example app, 

	import dash  
	import dash_core_components as dcc  
	import dash_html_components as html  
	import caculator_cf as ccf  
	  
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
  
## Functions as properties  

As you might know already, it is not possible to pass function handles as component properties in Dash. Instead, dash-transcrypt passes the *full path to the function* as a string. And it's then up to the component to create the function.  

An example of a component that supports this flow is the `GeoJSON` component in [dash-leaflet]([https://pypi.org/project/dash-leaflet/](https://pypi.org/project/dash-leaflet/)). One of the function properties is `pointToLayer`, which must be a function (or rather a full path to a function) that matches the signature if the `pointToLayer` options of the underlying [Leaflet GeoJSON object](https://leafletjs.com/reference-0.7.7.html#geojson-pointtolayer). The relevant function(s) must be placed in a separate module (file), say `scatter_js.py`,  

	 def point_to_layer(feature, latlng, context): 
	 radius = feature.properties.population**0.5/100 return L.circleMarker(latlng, dict(radius=radius))  
 
Before the function(s) can be used as a property, the module must be passed through the `module_to_props` function. In addition to transpiling the module into JavaScript, it replaces the function attributes of the module with the appropriate strings,
  
	import scatter_js as sjs 
	import dash_leaflet as dl
	from dash_transcrypt import inject_js, module_to_props 
	... 
	js = module_to_props(sjs)
	geojson = dl.GeoJSON(url="/assets/CA.json", options=dict(pointToLayer=sjs.point_to_layer))
	...
	inject_js(app, js)  

The assets can be found in this repository in the examples folder. For completeness, here is the full example app  
  
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

## Passing arguments at compile time  
  
Variable assignments followed by `# <kwarg>` are overwritten at compile time. As an extension of the previous example, say one would like to be able to vary the `radius_property` and the `scale`. This could be achieved by modifying `scatter_js.py` to  
  
	scale = 100 # <kwarg>  
	radius_property = "population" # <kwarg>  
	  
	def point_to_layer(feature, latlng, context):  
	    radius = feature.properties[radius_property] ** 0.5 / scale  
	    return L.circleMarker(latlng, dict(radius=radius))
  
The default `radius_property`(`scale`) is population(100) as before, but the value(s) can now be modified by changing a single line in the application code,  
  
	js = module_to_props(cjs, radius_property="density", scale=5)  # compiles the js
 
## Passing arguments at runtime  
  
While not enforced by dash-transcrypt, it is recommended that a context (typically a reference to `this`) is passed to all functional properties. Furthermore, it is recommended that a `hideout` property is added which *does nothing*, but serves as a container for passing argument at runtime. 

The `GeoJSON` from the example(s) follows these guidelines. Hence by modifying `scatter_js.py` to  

	def point_to_layer(feature, latlng, context):  
	    scale = context.props.hideout.scale  
	    radius_property = context.props.hideout.radius_property  
	    radius = feature.properties[radius_property] ** 0.5 / scale  
	    return L.circleMarker(latlng, dict(radius=radius))
  
the `scale` and `radius_property` can now be changed on runtime. Hence the map visualization can now be *interactive*. Here is a small app, where a slider changes the `scale` and thus the size of the makers,

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
	    app.run_server()
  
  
## Notes  
  
* Browsers tend to cache javascript assets. When changes have been made to the python functions, it might therefore be necessary to force a reload of the page (ctrl+F5) to get the updated function definitions.